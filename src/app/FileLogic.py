from __future__ import annotations
import sys
import os
import pathlib
import importlib.util
import hashlib
import mimetypes
import json
from typing import Dict, Any, Optional, List, Set, Union
from dataclasses import dataclass, field
import threading
from concurrent.futures import ThreadPoolExecutor
from enum import Enum, auto
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ContentType(Enum):
    TEXT = auto()
    IMAGE = auto()
    AUDIO = auto()
    VIDEO = auto()
    BINARY = auto()
    PYTHON = auto()
    OTHER = auto()

@dataclass
class ContentMetadata:
    """Metadata for any file in the system"""
    path: pathlib.Path
    relative_path: pathlib.Path  # Path relative to root
    file_size: int
    last_modified: float
    content_hash: str
    mime_type: str
    content_type: ContentType
    extension: str
    is_loadable: bool = False  # Can be loaded as a Python module

@dataclass
class FileSystem:
    """Manager for the real filesystem content"""
    root_dir: pathlib.Path
    exclude_dirs: Set[str] = field(default_factory=lambda: {'.git', '__pycache__', '.venv', 'node_modules'})
    exclude_files: Set[str] = field(default_factory=lambda: {'.DS_Store', 'thumbs.db'})
    max_workers: int = 8
    chunk_size: int = 1024 * 1024  # 1MB for reading large files
    metadata_cache: Dict[str, ContentMetadata] = field(default_factory=dict)
    content_cache: Dict[str, Any] = field(default_factory=dict)
    loaded_modules: Dict[str, Any] = field(default_factory=dict)
    _lock: threading.RLock = field(default_factory=threading.RLock)
    _executor: ThreadPoolExecutor = None

    def __post_init__(self):
        """Initialize the ThreadPoolExecutor"""
        self._executor = ThreadPoolExecutor(max_workers=self.max_workers)
        # Ensure root directory exists
        self.root_dir = pathlib.Path(self.root_dir).resolve()
        if not self.root_dir.exists():
            raise FileNotFoundError(f"Root directory {self.root_dir} does not exist")
        # Initialize mimetypes
        mimetypes.init()

    def scan_directory(self, refresh: bool = False) -> None:
        """Scan the directory tree and build metadata cache"""
        if self.metadata_cache and not refresh:
            logger.info(f"Using cached metadata for {len(self.metadata_cache)} files")
            return

        logger.info(f"Scanning directory: {self.root_dir}")
        scanned_paths = []
        
        for file_path in self.root_dir.rglob('*'):
            # Skip excluded directories and files
            if any(part in self.exclude_dirs for part in file_path.parts):
                continue
            if file_path.name in self.exclude_files:
                continue
            
            if file_path.is_file():
                scanned_paths.append(file_path)
        
        # Process files in parallel
        futures = [self._executor.submit(self._process_file, path) for path in scanned_paths]
        for future in futures:
            metadata = future.result()
            if metadata:
                rel_path_str = str(metadata.relative_path)
                with self._lock:
                    self.metadata_cache[rel_path_str] = metadata
        
        logger.info(f"Indexed {len(self.metadata_cache)} files")

    def _process_file(self, file_path: pathlib.Path) -> Optional[ContentMetadata]:
        """Process a single file and create metadata"""
        try:
            stat = file_path.stat()
            rel_path = file_path.relative_to(self.root_dir)
            
            # Determine content type
            mime_type, _ = mimetypes.guess_type(file_path)
            mime_type = mime_type or 'application/octet-stream'
            
            # Determine content classification
            content_type = self._classify_content(file_path, mime_type)
            
            # Compute hash for smaller files, use size+mtime for larger ones
            content_hash = ""
            if stat.st_size < 10 * 1024 * 1024:  # 10MB
                content_hash = self._compute_file_hash(file_path)
            else:
                content_hash = f"size:{stat.st_size}-mtime:{stat.st_mtime}"
            
            # Check if file can be loaded as Python module
            is_loadable = self._is_loadable(file_path)
            
            return ContentMetadata(
                path=file_path,
                relative_path=rel_path,
                file_size=stat.st_size,
                last_modified=stat.st_mtime,
                content_hash=content_hash,
                mime_type=mime_type,
                content_type=content_type,
                extension=file_path.suffix.lower(),
                is_loadable=is_loadable
            )
        except Exception as e:
            logger.error(f"Error processing {file_path}: {e}")
            return None

    def _classify_content(self, file_path: pathlib.Path, mime_type: str) -> ContentType:
        """Classify file content type"""
        if file_path.suffix.lower() == '.py':
            return ContentType.PYTHON
        
        if mime_type:
            if mime_type.startswith('text/'):
                return ContentType.TEXT
            if mime_type.startswith('image/'):
                return ContentType.IMAGE
            if mime_type.startswith('audio/'):
                return ContentType.AUDIO
            if mime_type.startswith('video/'):
                return ContentType.VIDEO
        
        # Check if it might be text based on content
        if file_path.stat().st_size < 1024 * 1024:  # 1MB max for text detection
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    f.read(1024)  # Try to read first 1KB as text
                return ContentType.TEXT
            except UnicodeDecodeError:
                pass
        
        return ContentType.BINARY

    def _compute_file_hash(self, file_path: pathlib.Path) -> str:
        """Compute SHA-256 hash of file contents"""
        hasher = hashlib.sha256()
        try:
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(self.chunk_size), b''):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except Exception as e:
            logger.error(f"Error computing hash for {file_path}: {e}")
            return f"error:{str(e)}"

    def _is_loadable(self, file_path: pathlib.Path) -> bool:
        """Check if file can be loaded as a Python module"""
        if file_path.suffix.lower() == '.py':
            return True
        # Additional checks could be added here for other loadable formats
        return False

    def load_content(self, rel_path: Union[str, pathlib.Path], force_reload: bool = False) -> Optional[Any]:
        """Load file content, with caching"""
        rel_path_str = str(rel_path) if isinstance(rel_path, pathlib.Path) else rel_path
        
        # Return from cache if available and not force_reload
        if rel_path_str in self.content_cache and not force_reload:
            return self.content_cache[rel_path_str]
        
        metadata = self.metadata_cache.get(rel_path_str)
        if not metadata:
            logger.warning(f"No metadata found for {rel_path_str}")
            return None
        
        content = None
        try:
            if metadata.content_type == ContentType.TEXT:
                with open(metadata.path, 'r', encoding='utf-8', errors='replace') as f:
                    content = f.read()
            elif metadata.content_type == ContentType.PYTHON:
                # For Python files, load as text but don't execute
                with open(metadata.path, 'r', encoding='utf-8', errors='replace') as f:
                    content = f.read()
            else:
                # Binary data loaded but not stored in cache
                with open(metadata.path, 'rb') as f:
                    content = f.read()
                return content  # Return directly, don't cache
                
            # Cache text content
            with self._lock:
                self.content_cache[rel_path_str] = content
                
            return content
        except Exception as e:
            logger.error(f"Error loading content for {rel_path_str}: {e}")
            return None

    def load_module(self, rel_path: Union[str, pathlib.Path], force_reload: bool = False) -> Optional[Any]:
        """Load a Python module from a file"""
        rel_path_str = str(rel_path) if isinstance(rel_path, pathlib.Path) else rel_path
        
        # Return from cache if available and not force_reload
        if rel_path_str in self.loaded_modules and not force_reload:
            return self.loaded_modules[rel_path_str]
        
        metadata = self.metadata_cache.get(rel_path_str)
        if not metadata or not metadata.is_loadable:
            logger.warning(f"File {rel_path_str} cannot be loaded as a module")
            return None
        
        try:
            # Create a valid module name from the relative path
            module_name = f"fs_module_{metadata.relative_path.stem}"
            
            # Remove invalid characters
            module_name = ''.join(c if c.isalnum() or c == '_' else '_' for c in module_name)
            
            # Try to load the module
            spec = importlib.util.spec_from_file_location(module_name, str(metadata.path))
            if spec is None or spec.loader is None:
                logger.error(f"Could not create module spec for {rel_path_str}")
                return None
                
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module  # Add to sys.modules
            
            # Inject metadata into module
            module.__file_metadata__ = metadata
            
            # Execute the module
            spec.loader.exec_module(module)
            
            # Cache the module
            with self._lock:
                self.loaded_modules[rel_path_str] = module
                
            return module
        except Exception as e:
            logger.error(f"Error loading module {rel_path_str}: {e}")
            return None

    def generate_content_module(self, rel_path: Union[str, pathlib.Path]) -> Optional[str]:
        """Generate a Python module string for non-Python content"""
        rel_path_str = str(rel_path) if isinstance(rel_path, pathlib.Path) else rel_path
        metadata = self.metadata_cache.get(rel_path_str)
        
        if not metadata:
            logger.warning(f"No metadata found for {rel_path_str}")
            return None
        
        if metadata.content_type == ContentType.PYTHON:
            # Just return the original content for Python files
            return self.load_content(rel_path_str)
        
        # For text files
        if metadata.content_type == ContentType.TEXT:
            content = self.load_content(rel_path_str)
            if content is None:
                return None
                
            # Escape triple quotes in content
            content = content.replace('"""', '\\"\\"\\"')
            
            return f'''"""
Auto-generated content module for: {metadata.relative_path}
Content type: {metadata.content_type.name}
MIME type: {metadata.mime_type}
File size: {metadata.file_size} bytes
Last modified: {metadata.last_modified}
"""

# File metadata
FILE_PATH = "{metadata.path}"
RELATIVE_PATH = "{metadata.relative_path}"
CONTENT_TYPE = "{metadata.content_type.name}"
MIME_TYPE = "{metadata.mime_type}"

# Original content as string
CONTENT = """
{content}
"""

# Quantum state marker
__quantum_state__ = "SUPERPOSITION"

def get_content() -> str:
    """Returns the original content."""
    return CONTENT

def get_metadata() -> dict:
    """Returns metadata about the file."""
    return {{
        "path": "{metadata.path}",
        "relative_path": "{metadata.relative_path}",
        "file_size": {metadata.file_size},
        "last_modified": {metadata.last_modified},
        "content_type": "{metadata.content_type.name}",
        "mime_type": "{metadata.mime_type}"
    }}

# Immediate execution upon loading
@lambda _: _()
def __quantum_collapse__():
    global __quantum_state__
    __quantum_state__ = "COLLAPSED"
    return True
'''
        
        # For binary files, just include metadata, not content
        return f'''"""
Auto-generated content module for: {metadata.relative_path}
Content type: {metadata.content_type.name}
MIME type: {metadata.mime_type}
File size: {metadata.file_size} bytes
Last modified: {metadata.last_modified}
"""

# File metadata
FILE_PATH = "{metadata.path}"
RELATIVE_PATH = "{metadata.relative_path}"
CONTENT_TYPE = "{metadata.content_type.name}"
MIME_TYPE = "{metadata.mime_type}"

# Binary content not included in module
def get_content_bytes() -> bytes:
    """Load and return binary content."""
    with open("{metadata.path}", "rb") as f:
        return f.read()
        
def get_metadata() -> dict:
    """Returns metadata about the file."""
    return {{
        "path": "{metadata.path}",
        "relative_path": "{metadata.relative_path}",
        "file_size": {metadata.file_size},
        "last_modified": {metadata.last_modified},
        "content_type": "{metadata.content_type.name}",
        "mime_type": "{metadata.mime_type}"
    }}

# Immediate execution upon loading
@lambda _: _()
def __quantum_collapse__():
    global __quantum_state__
    __quantum_state__ = "COLLAPSED"
    return True
'''

    def create_dynamic_module(self, rel_path: Union[str, pathlib.Path]) -> Optional[Any]:
        """Create a dynamic module for any file, even non-Python files"""
        rel_path_str = str(rel_path) if isinstance(rel_path, pathlib.Path) else rel_path
        
        # Check if we already have this module
        if rel_path_str in self.loaded_modules:
            return self.loaded_modules[rel_path_str]
            
        metadata = self.metadata_cache.get(rel_path_str)
        if not metadata:
            logger.warning(f"No metadata found for {rel_path_str}")
            return None
            
        # For Python files, load normally
        if metadata.is_loadable:
            return self.load_module(rel_path_str)
            
        # Generate module content for non-Python files
        module_code = self.generate_content_module(rel_path_str)
        if not module_code:
            return None
            
        # Create module name
        module_name = f"fs_content_{metadata.relative_path.stem}"
        module_name = ''.join(c if c.isalnum() or c == '_' else '_' for c in module_name)
        
        # Create module
        module = type(sys)(module_name)
        module.__file__ = str(metadata.path)
        module.__file_metadata__
# Set metadata attribute
        module.__file_metadata__ = metadata
        
        # Execute the generated code in the module's namespace
        try:
            exec(module_code, module.__dict__)
            
            # Store in the loaded modules cache
            with self._lock:
                self.loaded_modules[rel_path_str] = module
                
            return module
        except Exception as e:
            logger.error(f"Error creating dynamic module for {rel_path_str}: {e}")
            return None

    def get_file_listing(self, directory: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get a listing of files with metadata"""
        dir_path = directory or ""
        result = []
        
        prefix = pathlib.Path(dir_path) if dir_path else pathlib.Path("")
        
        for rel_path, metadata in self.metadata_cache.items():
            path = pathlib.Path(rel_path)
            # Check if this path is under the requested directory
            if str(prefix) == "." or str(path).startswith(str(prefix)):
                if prefix == path.parent or (not directory and path.parent == pathlib.Path("")):
                    result.append({
                        "name": path.name,
                        "path": str(path),
                        "size": metadata.file_size,
                        "type": metadata.content_type.name,
                        "mime_type": metadata.mime_type,
                        "last_modified": metadata.last_modified,
                        "is_loadable": metadata.is_loadable
                    })
                    
        # Sort by name
        result.sort(key=lambda x: x["name"])
        return result
    
    def get_directory_tree(self) -> Dict[str, Any]:
        """Generate a nested tree representation of the filesystem"""
        root = {"name": self.root_dir.name, "type": "directory", "children": {}}
        
        for rel_path, metadata in self.metadata_cache.items():
            current = root
            parts = pathlib.Path(rel_path).parts
            
            # Build the directory structure
            for i, part in enumerate(parts[:-1]):
                if part not in current["children"]:
                    current["children"][part] = {"name": part, "type": "directory", "children": {}}
                current = current["children"][part]
            
            # Add the file
            filename = parts[-1]
            current["children"][filename] = {
                "name": filename,
                "type": "file",
                "content_type": metadata.content_type.name,
                "size": metadata.file_size,
                "is_loadable": metadata.is_loadable
            }
            
        return root
    
    def search_files(self, query: str, content_search: bool = False) -> List[Dict[str, Any]]:
        """Search for files by name or content"""
        results = []
        query = query.lower()
        
        for rel_path, metadata in self.metadata_cache.items():
            # Search in filename
            if query in str(metadata.relative_path).lower():
                results.append({
                    "path": str(metadata.relative_path),
                    "match_type": "filename",
                    "metadata": {
                        "size": metadata.file_size,
                        "type": metadata.content_type.name,
                        "mime_type": metadata.mime_type
                    }
                })
                continue  # Skip content search if filename matches
                
            # Optionally search in content for text files
            if content_search and metadata.content_type in [ContentType.TEXT, ContentType.PYTHON]:
                content = self.load_content(rel_path)
                if content and query in content.lower():
                    results.append({
                        "path": str(metadata.relative_path),
                        "match_type": "content",
                        "metadata": {
                            "size": metadata.file_size,
                            "type": metadata.content_type.name,
                            "mime_type": metadata.mime_type
                        }
                    })
                    
        return results
    
    def close(self):
        """Clean up resources"""
        if self._executor:
            self._executor.shutdown()
        self.content_cache.clear()
        self.loaded_modules.clear()
        self.metadata_cache.clear()

    def __enter__(self):
        """Context manager support"""
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean up on exit"""
        self.close()

# Utility functions
def create_filesystem(root_dir: Union[str, pathlib.Path], scan: bool = True) -> FileSystem:
    """Create and initialize a FileSystem"""
    fs = FileSystem(root_dir=pathlib.Path(root_dir))
    if scan:
        fs.scan_directory()
    return fs

def get_import_hook(fs: FileSystem):
    """Create an import hook to use the filesystem for imports"""
    class FSImportFinder:
        def __init__(self, fs):
            self.fs = fs
            
        def find_spec(self, fullname, path, target=None):
            # Check if this is a module we might handle
            if fullname.startswith('fs_'):
                # Extract the relative path from the module name
                parts = fullname.split('_', 2)
                if len(parts) >= 3:
                    rel_path = parts[2].replace('_', '/')
                    if rel_path in self.fs.metadata_cache:
                        return self.fs.create_dynamic_module(rel_path)
            return None
    
    return FSImportFinder(fs)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="FileSystem Manager")
    parser.add_argument("--root", type=str, default=".", help="Root directory to scan")
    parser.add_argument("--list", action="store_true", help="List files")
    parser.add_argument("--dir", type=str, help="Specific directory to list")
    parser.add_argument("--search", type=str, help="Search query")
    parser.add_argument("--content", action="store_true", help="Search in content")
    
    args = parser.parse_args()
    
    fs = create_filesystem(args.root)
    
    if args.list:
        files = fs.get_file_listing(args.dir)
        print(json.dumps(files, indent=2))
    
    if args.search:
        results = fs.search_files(args.search, args.content)
        print(json.dumps(results, indent=2))