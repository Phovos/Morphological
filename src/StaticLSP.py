#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unified Morphological Analysis Engine
======================================
Combines AtomicLogic architecture with static analysis, RPC, and LSP capabilities.
Single-file, stdlib-only, polymorphic-first design.

© 2025 Phovos | BSD-3 & CC ND

Morphological Analysis Engine
├── Logging Layer (JSON, contextual, rotating)
├── Exception Hierarchy (typed errors with HTTP codes)
├── BaseModel System (validation, serialization)
├── Configuration Models (immutable, validated)
├── DTOs (frozen dataclasses)
├── Dynamic Module System (homoiconic behavior)
├── Static Analysis Engine
│   ├── Security validation
│   ├── AST parsing
│   ├── Semantic visitor
│   └── Graph building
├── RPC Server (HTTP/JSON, threaded)
└── CLI Interface (serve, analyze, demo)
"""

"""(MSC) Morphological Source Code Framework – V0.0.16
================================================================================
<https://github.com/MOONLAPSED/Morphological> • Morphological Source Code © 2023 by MOONLAPSED
<https://github.com/Phovos/Morphological> • QSD © 2024 by Phovos/MOONLAPSED
<https://github.com/orgs/Morphological-Source-Code> •
QSD: Quineic Statistical Dyamics • MSC: Morphological Source Code © 2025 by Phovos"""
import os
import sys
import ast
import time
import json
import uuid
import base64
import hashlib
import logging
import logging.config
import inspect
import threading
from pathlib import Path
from enum import Enum, auto
from dataclasses import dataclass, field, fields, asdict
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Union,
    Callable,
    TypeVar,
    Tuple,
    Type,
    get_type_hints,
    get_origin,
    get_args,
    final,
)
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer, HTTPServer
from types import ModuleType
from importlib.metadata import distributions

# Try to import sub-interpreters (Python 3.12+)
try:
    from concurrent import interpreters

    HAS_INTERPRETERS = True
except ImportError:
    HAS_INTERPRETERS = False
    interpreters = None

# ============================================================================
# LOGGING INFRASTRUCTURE: JSON-formatted, contextual logging
# ============================================================================


class JsonLogFormatter(logging.Formatter):
    """Formats log records as JSON for machine parsing"""

    def format(self, record: logging.LogRecord) -> str:
        log_object = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
            "source": record.name,
            "context": getattr(record, 'context', {}),
            "correlation_id": getattr(record, 'correlation_id', 'SYSTEM'),
        }
        if record.exc_info:
            log_object["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_object)


class ContextualLogger(logging.LoggerAdapter):
    """Logger adapter that injects correlation_id into all log messages"""

    def process(self, msg, kwargs):
        if 'correlation_id' not in self.extra:
            self.extra['correlation_id'] = 'SYSTEM'
        # Inject context into the record
        if 'extra' not in kwargs:
            kwargs['extra'] = {}
        kwargs['extra']['correlation_id'] = self.extra['correlation_id']
        kwargs['extra']['context'] = kwargs.get('extra', {}).get('context', {})
        return f"[{self.extra['correlation_id']}] {msg}", kwargs


def setup_logging(
    log_dir: str = "logs",
    log_file: str = "morphological.log",
    level: int = logging.INFO,
    json_format: bool = True,
) -> logging.Logger:
    """Configure comprehensive logging system"""
    logs_path = Path(log_dir)
    logs_path.mkdir(parents=True, exist_ok=True)
    log_filepath = logs_path / log_file

    formatter_class = JsonLogFormatter if json_format else logging.Formatter
    format_str = (
        '%(message)s'
        if json_format
        else '[%(levelname)s]%(asctime)s||%(name)s: %(message)s'
    )

    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                '()': formatter_class,
                'format': format_str,
                'datefmt': '%Y-%m-%d~%H:%M:%S%z',
            }
        },
        'handlers': {
            'console': {
                'level': level,
                'class': 'logging.StreamHandler',
                'formatter': 'default',
                'stream': 'ext://sys.stdout',
            },
            'file': {
                'level': level,
                'formatter': 'default',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': str(log_filepath),
                'maxBytes': 10485760,  # 10MB
                'backupCount': 10,
            },
        },
        'root': {'level': level, 'handlers': ['console', 'file']},
    }

    logging.config.dictConfig(logging_config)
    return logging.getLogger("MorphologicalEngine")


def get_logger(name: str = None, correlation_id: str = 'SYSTEM') -> ContextualLogger:
    """Get a contextual logger for a specific component"""
    if name is None:
        # Auto-detect calling module
        frame = inspect.currentframe().f_back
        name = frame.f_globals.get('__name__', 'unknown')

    logger = logging.getLogger(name)
    return ContextualLogger(logger, {'correlation_id': correlation_id})


# Initialize root logger
logger = setup_logging()

# ============================================================================
# EXCEPTION HIERARCHY: Typed error handling
# ============================================================================


class MorphologicalError(Exception):
    """Base exception for all morphological engine errors"""

    def __init__(self, message: str, status_code: int = 500):
        self.status_code = status_code
        super().__init__(message)


class AnalyzerError(MorphologicalError):
    """Base for analysis-specific errors"""

    pass


class ConfigurationError(AnalyzerError):
    """Invalid or insecure configuration"""

    def __init__(self, message: str):
        super().__init__(message, status_code=500)


class SourceError(AnalyzerError):
    """Issues with source files"""

    pass


class SourceNotFoundError(SourceError):
    """Source file does not exist"""

    def __init__(self, message: str):
        super().__init__(message, status_code=404)


class SourcePermissionError(SourceError):
    """Source file access denied"""

    def __init__(self, message: str):
        super().__init__(message, status_code=403)


class SourceSizeExceededError(SourceError):
    """Source file too large"""

    def __init__(self, message: str):
        super().__init__(message, status_code=413)


class ParsingError(AnalyzerError):
    """Invalid Python syntax"""

    def __init__(self, message: str):
        super().__init__(message, status_code=400)


class InputValidationError(MorphologicalError):
    """Hostile or malformed input"""

    def __init__(self, message: str):
        super().__init__(message, status_code=400)


class SecurityViolationError(MorphologicalError):
    """Security policy violation"""

    def __init__(self, message: str):
        super().__init__(message, status_code=403)


class ResourceLimitExceededError(MorphologicalError):
    """Resource limits exceeded"""

    def __init__(self, message: str):
        super().__init__(message, status_code=413)


class LspError(AnalyzerError):
    """LSP-specific errors"""

    pass


# ============================================================================
# ENUMS: State and mode definitions
# ============================================================================
T = TypeVar('T')
V = TypeVar('V')
C = TypeVar('C', bound=Callable)


class QuantumState(Enum):
    """Quantum-inspired state representation"""

    SUPERPOSITION = auto()
    ENTANGLED = auto()
    COLLAPSED = auto()
    DECOHERENT = auto()


class RuntimeMode(Enum):
    """Runtime execution mode"""

    SUBINTERPRETER = auto()
    THREADED = auto()
    SEQUENTIAL = auto()


class Mutability(Enum):
    """Data mutability mode"""

    IMMUTABLE = auto()
    MUTABLE = auto()
    QUEINIC = auto()  # Quantum + homoiconic


class SerializationFormat(Enum):
    """Supported serialization formats"""

    JSON = "json"
    PICKLE = "pickle"
    REPR = "repr"
    MSGPACK = "msgpack"


# ============================================================================
# BASEMODEL: Validation and serialization foundation
# ============================================================================


def _matches_type(value: Any, tp: Any) -> bool:
    """Check if value conforms to type"""
    if tp is Any:
        return True

    origin = get_origin(tp)
    if origin is Union:
        return any(_matches_type(value, arg) for arg in get_args(tp))

    if origin:
        if not isinstance(value, origin):
            return False
        args = get_args(tp)
        if origin is list and args:
            return all(_matches_type(v, args[0]) for v in value)
        if origin is dict and len(args) == 2:
            kt, vt = args
            return all(
                _matches_type(k, kt) and _matches_type(v, vt) for k, v in value.items()
            )
        return True

    return isinstance(value, tp)


def _coerce(raw: Any, tp: Any) -> Any:
    """Coerce value to target type"""
    if tp is Any:
        return raw

    origin = get_origin(tp)

    if origin is Union:
        for arg_type in get_args(tp):
            if arg_type is type(None) and raw is None:
                return None
            try:
                return _coerce(raw, arg_type)
            except (TypeError, ValueError):
                continue
        raise TypeError(f"Cannot coerce {raw!r} to {tp}")

    if origin is list:
        if not isinstance(raw, list):
            raise TypeError(f"Expected list, got {type(raw).__name__}")
        elem_tp = get_args(tp)[0] if get_args(tp) else Any
        return [_coerce(item, elem_tp) for item in raw]

    if origin is dict:
        if not isinstance(raw, dict):
            raise TypeError(f"Expected dict, got {type(raw).__name__}")
        args = get_args(tp)
        if len(args) >= 2:
            kt, vt = args[0], args[1]
            return {_coerce(k, kt): _coerce(v, vt) for k, v in raw.items()}
        return raw

    if inspect.isclass(tp) and issubclass(tp, BaseModel):
        if isinstance(raw, dict):
            return tp.from_dict(raw)
        elif isinstance(raw, tp):
            return raw

    return raw


def _uncoerce(value: Any) -> Any:
    """Convert to JSON-serializable format"""
    if isinstance(value, BaseModel):
        return value.to_dict()
    if isinstance(value, list):
        return [_uncoerce(v) for v in value]
    if isinstance(value, dict):
        return {k: _uncoerce(v) for k, v in value.items()}
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, uuid.UUID):
        return str(value)
    return value


@dataclass(frozen=True)
class BaseModel:
    """
    Foundation for all data models with validation and serialization.
    Provides Pydantic-like semantics with stdlib-only implementation.
    """

    __slots__ = ('__weakref__',)

    def __post_init__(self):
        """Validate all fields after initialization"""
        annotations = self.__annotate_func__

        for field_name, expected_type in annotations.items():
            value = getattr(self, field_name)

            if not _matches_type(value, expected_type):
                raise TypeError(
                    f"{self.__class__.__name__}.{field_name}: expected {expected_type}, "
                    f"got {type(value).__name__}"
                )

        if hasattr(self, '_validate_model'):
            self._validate_model()

    def _validate_model(self):
        """Override for model-level validation"""
        pass

    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        """Deserialize from dictionary"""
        if not isinstance(data, dict):
            raise ValueError(f"Expected dict, got {type(data).__name__}")

        field_names = {f.name for f in fields(cls)}
        init_data = {k: v for k, v in data.items() if k in field_names}

        field_types = get_type_hints(cls)

        for field_name, field_type in field_types.items():
            if field_name in init_data:
                try:
                    init_data[field_name] = _coerce(init_data[field_name], field_type)
                except (TypeError, ValueError) as e:
                    raise ValueError(f"Failed to coerce {field_name}: {e}")

        try:
            return cls(**init_data)
        except TypeError as e:
            raise ValueError(f"Failed to create {cls.__name__}: {e}")

    def to_dict(self, exclude_none: bool = False) -> Dict[str, Any]:
        """Serialize to dictionary"""
        result = {}
        for f in fields(self):
            value = getattr(self, f.name)
            if exclude_none and value is None:
                continue
            result[f.name] = _uncoerce(value)
        return result

    def to_json(self, *, indent: int | None = None, sort_keys: bool = False) -> str:
        """Return JSON string. Fully deterministic if sort_keys=True."""
        return json.dumps(
            self.to_dict(),
            indent=indent,
            sort_keys=sort_keys,
            separators=(",", ":") if indent is None else None,
            ensure_ascii=False,
        )

    @classmethod
    def from_json(cls, data: str | bytes) -> "BaseModel":
        """Parse JSON string/bytes → instance. Fully reversible."""
        if isinstance(data, (bytes, bytearray)):
            data = data.decode("utf-8")
        return cls.from_dict(json.loads(data))

    def fingerprint(self) -> str:
        """Content-based fingerprint for caching"""
        content = json.dumps(self.to_dict(), sort_keys=True, separators=(',', ':'))
        return hashlib.sha256(content.encode()).hexdigest()[:16]


# CONFIGURATION MODELS


@final
@dataclass(frozen=True)
class AnalyzerConfig(BaseModel):
    """
    Immutable configuration for static analysis engine.
    Enforces security boundaries and resource limits.
    """

    # Allowed source directories (security boundary)
    allowed_source_roots: Tuple[Path, ...]

    # Resource limits
    max_file_size_bytes: int = 1 * 1024 * 1024  # 1 MiB
    max_request_body_size: int = 10 * 1024 * 1024  # 10 MiB

    # File handling
    source_encoding: str = 'utf-8'
    allowed_extensions: Tuple[str, ...] = ('.py', '.md', '.txt')

    # Security
    hmac_secret_key: bytes = field(default_factory=lambda: os.urandom(32))

    def _validate_model(self):
        """Post-initialization validation"""
        if not self.allowed_source_roots:
            raise ConfigurationError("allowed_source_roots cannot be empty")

        for p in self.allowed_source_roots:
            if not p.is_absolute():
                raise ConfigurationError(f"Path not absolute: {p}")
            if not p.exists() or not p.is_dir():
                raise ConfigurationError(f"Path does not exist or not a directory: {p}")

        if self.max_file_size_bytes <= 0:
            raise ConfigurationError("max_file_size_bytes must be positive")


@dataclass
class RuntimeConfig:
    """Configuration for runtime execution"""

    mode: RuntimeMode = RuntimeMode.THREADED
    max_workers: int = 4
    shared_memory_size: int = 8192

    def __post_init__(self):
        if self.mode == RuntimeMode.SUBINTERPRETER and not HAS_INTERPRETERS:
            logger.warning(
                "Sub-interpreters not available, falling back to THREADED mode"
            )
            object.__setattr__(self, 'mode', RuntimeMode.THREADED)


# ============================================================================
# DATA TRANSFER OBJECTS (DTOs)
# ============================================================================


@final
@dataclass(frozen=True)
class SourceRequest(BaseModel):
    """Immutable analysis request"""

    source_path: Path
    request_id: uuid.UUID = field(default_factory=uuid.uuid4)

    def __post_init__(self):
        super().__post_init__()
        # Convert string paths to Path objects
        if isinstance(self.source_path, str):
            object.__setattr__(self, 'source_path', Path(self.source_path))


@final
@dataclass(frozen=True)
class AnalysisMetadata(BaseModel):
    """Metadata for analysis results"""

    request_id: uuid.UUID
    source_path: Path
    source_hash_sha256: str
    analysis_timestamp_utc: float
    engine_version: str = "1.0.0"

    def __post_init__(self):
        super().__post_init__()
        if isinstance(self.source_path, str):
            object.__setattr__(self, 'source_path', Path(self.source_path))


@final
@dataclass(frozen=True)
class SemanticGraph(BaseModel):
    """Analysis result with semantic information"""

    source_artifact_hash: str
    processed_at_unix_ts: float
    engine_version: str
    graph_data: Dict[str, Any]
    signature_hmac_sha256: str


@final
@dataclass(frozen=True)
class AnalysisResult(BaseModel):
    """Complete analysis result with metadata"""

    metadata: AnalysisMetadata
    semantic_graph: Dict[str, Any]

    def to_markdown(self) -> str:
        lines = []
        meta = self.metadata
        sg = self.semantic_graph

        lines.append(f"# Python Module: `{meta.source_path.name}`")
        lines.append(f"- **Hash**: `{meta.source_hash_sha256[:16]}`")
        lines.append(f"- **Analyzed**: `{time.ctime(meta.analysis_timestamp_utc)}`")
        lines.append("")

        lines.append("## Functions")
        for f in sg.get("functions", []):
            args = ", ".join(f["args"])
            decs = " ⟶ " + ", ".join(f["decorators"]) if f["decorators"] else ""
            line = f"- `{f['name']}({args})` (line {f['lineno']}){decs}"
            lines.append(line)

        lines.append("\n## Classes")
        for c in sg.get("classes", []):
            bases = " → " + ", ".join(c["bases"]) if c["bases"] else ""
            line = f"- `{c['name']}`{bases} (line {c['lineno']})"
            lines.append(line)

        lines.append("\n## Imports")
        for imp in sg.get("imports", []):
            if "name" in imp:
                lines.append(f"- `from {imp['module']} import {imp['name']}`")
            else:
                lines.append(f"- `import {imp['module']}`")

        lines.append(f"\n## Complexity Score: `{sg.get('complexity', 0)}`")
        return "\n".join(lines)


# IWE LSP DTO


@dataclass(frozen=True)
class MarkdownSection(BaseModel):
    title: str
    level: int
    start_line: int
    end_line: int
    parent_section: Optional[str] = None


@dataclass(frozen=True)
class MarkdownGraph(BaseModel):
    sections: List[MarkdownSection]
    links: List[Dict[str, Any]]
    backlinks: List[str]
    path_hierarchy: List[str]


@dataclass(frozen=True)
class LspMessage(BaseModel):
    jsonrpc: str = "2.0"
    id: Optional[int] = None
    method: Optional[str] = None
    params: Optional[Dict[str, Any]] = None
    result: Optional[Any] = None
    error: Optional[Dict[str, Any]] = None


# DYNAMIC MODULE CREATION: Morphological self-modification


def create_module(
    module_name: str, module_code: str, main_module_path: str = None
) -> Optional[ModuleType]:
    """
    Dynamically create a module with injected code.
    Enables homoiconic behavior and runtime code generation.

    Args:
        module_name: Name for the new module
        module_code: Python code to execute in module
        main_module_path: Optional path for __file__ attribute

    Returns:
        The created module or None on error
    """
    dynamic_module = ModuleType(module_name)
    dynamic_module.__file__ = main_module_path or "runtime_generated"
    dynamic_module.__package__ = module_name
    dynamic_module.__path__ = None
    dynamic_module.__doc__ = f"Dynamically generated module: {module_name}"

    try:
        exec(module_code, dynamic_module.__dict__)
        sys.modules[module_name] = dynamic_module
        logger.info(f"Created dynamic module: {module_name}")
        return dynamic_module
    except Exception as e:
        logger.error(f"Failed to create module {module_name}: {e}", exc_info=True)
        return None


# ============================================================================
# STATIC ANALYSIS ENGINE: Core analysis logic
# ============================================================================


class StaticAnalysisEngine:
    """
    Core static analysis engine for Python source code.
    Performs security validation, parsing, and semantic analysis.
    """

    def __init__(self, config: AnalyzerConfig):
        self._config = config
        self._logger = get_logger(self.__class__.__name__)
        self._logger.info(
            "Engine initialized", extra={'context': {'config': str(config)}}
        )

    def analyze(self, request: SourceRequest) -> AnalysisResult:
        """
        Main entry point for analysis pipeline.

        Args:
            request: Formal source request

        Returns:
            Complete analysis result

        Raises:
            AnalyzerError: For any predictable failure
        """
        logger = get_logger(self.__class__.__name__, str(request.request_id))
        logger.info(
            "Analysis started", extra={'context': {'source': str(request.source_path)}}
        )
        start_time = time.time()
        if request.source_path.suffix == '.md':
            # Proxy to IWE LSP for markdown
            if not hasattr(self, '_lsp_client'):
                self._lsp_client = LspClient()  # Lazy init
            # Example: Get document symbols (outline)
            params = {
                "textDocument": {"uri": f"file://{request.source_path.absolute()}"}
            }
            symbols = self._lsp_client.request("textDocument/documentSymbol", params)
            return AnalysisResult(  # Adapt to your model
                metadata=AnalysisMetadata(...),
                semantic_graph={"symbols": symbols},  # Or process further
            )
        try:
            # Stage 1: Security validation
            self._validate_source_path(request.source_path, logger)

            # Stage 2: Read content securely
            content, file_hash = self._read_source_content(request.source_path, logger)

            # Stage 3: Parse to AST
            tree = self._parse_to_ast(content, request.source_path, logger)

            # Stage 4: Build semantic graph
            graph = self._build_semantic_graph(tree, logger)

            # Stage 5: Create metadata
            metadata = AnalysisMetadata(
                request_id=request.request_id,
                source_path=request.source_path,
                source_hash_sha256=file_hash,
                analysis_timestamp_utc=time.time(),
            )

            result = AnalysisResult(metadata=metadata, semantic_graph=graph)

            duration = time.time() - start_time
            logger.info(
                "Analysis completed",
                extra={'context': {'duration': f"{duration:.4f}s"}},
            )
            return result

        except AnalyzerError:
            logger.error("Analysis failed", exc_info=True)
            raise
        except Exception as e:
            logger.critical("Unexpected error", exc_info=True)
            raise AnalyzerError(f"Unexpected internal error: {e}") from e

    def _validate_source_path(self, source_path: Path, logger: ContextualLogger):
        """Security validation of file path"""
        logger.info("Validating source path")

        try:
            real_path = source_path.resolve(strict=True)
        except FileNotFoundError:
            raise SourceNotFoundError(f"Source file does not exist: {source_path}")

        # Check against allowed roots
        if not any(
            real_path.is_relative_to(root) for root in self._config.allowed_source_roots
        ):
            raise SourcePermissionError(f"Path outside allowed roots: {real_path}")

        logger.info("Path validation passed")

    def _read_source_content(
        self, source_path: Path, logger: ContextualLogger
    ) -> Tuple[str, str]:
        """Securely read file content"""
        logger.info("Reading source content")

        if not os.access(source_path, os.R_OK):
            raise SourcePermissionError(f"Read permission denied: {source_path}")

        file_size = source_path.stat().st_size
        if file_size > self._config.max_file_size_bytes:
            raise SourceSizeExceededError(
                f"File size {file_size} exceeds limit of {self._config.max_file_size_bytes}"
            )

        try:
            with open(source_path, 'r', encoding=self._config.source_encoding) as f:
                content = f.read()

            content_bytes = content.encode(self._config.source_encoding)
            file_hash = hashlib.sha256(content_bytes).hexdigest()
            logger.info(
                f"Read {len(content_bytes)} bytes",
                extra={'context': {'hash': file_hash[:12]}},
            )
            return content, file_hash
        except (IOError, UnicodeDecodeError) as e:
            raise SourceError(f"Failed to read source: {e}") from e

    def _parse_to_ast(
        self, content: str, source_path: Path, logger: ContextualLogger
    ) -> ast.AST:
        """Parse Python source to AST"""
        logger.info("Parsing to AST")
        try:
            return ast.parse(content, filename=str(source_path))
        except SyntaxError as e:
            raise ParsingError(f"Invalid Python syntax: {e}") from e

    def _build_semantic_graph(
        self, tree: ast.AST, logger: ContextualLogger
    ) -> Dict[str, Any]:
        """Build semantic graph from AST"""
        logger.info("Building semantic graph")
        if source_path.suffix == ['.md', '.txt']:
            return self._build_markdown_graph(content, logger)
        else:
            return self._build_python_graph(tree, logger)
        # Extract basic semantic information
        visitor = SemanticVisitor()
        visitor.visit(tree)

        return {
            "ast_dump": ast.dump(tree, indent=2),
            "functions": visitor.functions,
            "classes": visitor.classes,
            "imports": visitor.imports,
            "variables": visitor.variables,
            "complexity": visitor.complexity_score,
        }


class SemanticVisitor(ast.NodeVisitor):
    """AST visitor for semantic analysis"""

    def __init__(self):
        self.functions = []
        self.classes = []
        self.imports = []
        self.variables = []
        self.complexity_score = 0

    def visit_FunctionDef(self, node):
        self.functions.append(
            {
                'name': node.name,
                'lineno': node.lineno,
                'args': [arg.arg for arg in node.args.args],
                'decorators': [ast.unparse(d) for d in node.decorator_list],
            }
        )
        self.complexity_score += 1
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        self.classes.append(
            {
                'name': node.name,
                'lineno': node.lineno,
                'bases': [ast.unparse(b) for b in node.bases],
                'decorators': [ast.unparse(d) for d in node.decorator_list],
            }
        )
        self.complexity_score += 2
        self.generic_visit(node)

    def visit_Import(self, node):
        for alias in node.names:
            self.imports.append(
                {'module': alias.name, 'alias': alias.asname, 'lineno': node.lineno}
            )
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            self.imports.append(
                {
                    'module': node.module,
                    'name': alias.name,
                    'alias': alias.asname,
                    'lineno': node.lineno,
                }
            )
        self.generic_visit(node)

    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.variables.append({'name': target.id, 'lineno': node.lineno})
        self.generic_visit(node)


# HTTP RPC SERVER: Network interface for analysis


class AnalysisRequestHandler(BaseHTTPRequestHandler):
    """
    HTTP request handler for analysis RPC endpoints.
    Enforces security and provides clean error handling.
    """

    # Class-level dependency injection
    engine: StaticAnalysisEngine
    config: AnalyzerConfig
    logger: ContextualLogger

    def _send_response(self, status_code: int, content_type: str, body: bytes):
        """Send HTTP response with proper headers"""
        self.send_response(status_code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Correlation-ID", self.correlation_id)
        self.end_headers()
        self.wfile.write(body)

    def _handle_error(self, e: Exception):
        """Handle errors with appropriate HTTP responses"""
        if isinstance(e, MorphologicalError):
            status_code = e.status_code
            message = str(e)
        else:
            status_code = 500
            message = "Internal server error"
            self.logger.error("Unhandled exception", exc_info=True)

        error_body = json.dumps(
            {"error": message, "correlation_id": self.correlation_id}
        ).encode('utf-8')
        self._send_response(status_code, "application/json", error_body)

    def do_POST(self):
        """Handle POST requests"""
        self.correlation_id = self.headers.get("X-Correlation-ID", str(uuid.uuid4()))
        logger = get_logger(self.__class__.__name__, self.correlation_id)
        self.logger = logger

        logger.info(
            "Request received", extra={'context': {'method': 'POST', 'path': self.path}}
        )

        try:
            if self.path != "/analyze":
                raise InputValidationError("Endpoint not found. Use POST /analyze")

            content_len = int(self.headers.get('Content-Length', 0))
            if content_len > self.config.max_request_body_size:
                raise ResourceLimitExceededError("Request body too large")

            body = self.rfile.read(content_len)
            data = json.loads(body)

            path = data.get("path")
            content_b64 = data.get("content_b64")

            if not path or not content_b64:
                raise InputValidationError(
                    "Request must contain 'path' and 'content_b64'"
                )

            content_bytes = base64.b64decode(content_b64)

            # Create source request
            request = SourceRequest(
                request_id=uuid.UUID(self.correlation_id), source_path=Path(path)
            )

            # Analyze
            result = self.engine.analyze(request)

            # Send response
            response_body = result.to_json(indent=2).encode('utf-8')
            self._send_response(200, "application/json", response_body)
            logger.info("Request completed successfully")

        except Exception as e:
            self._handle_error(e)

    def do_GET(self):
        """Handle GET requests"""
        self.correlation_id = self.headers.get("X-Correlation-ID", str(uuid.uuid4()))

        if self.path == "/health":
            body = json.dumps(
                {
                    "status": "healthy",
                    "timestamp": time.time(),
                    "correlation_id": self.correlation_id,
                }
            ).encode('utf-8')
            self._send_response(200, "application/json", body)
        else:
            self._handle_error(InputValidationError("Endpoint not found"))

    def log_message(self, format, *args):
        """Override to use our logger"""
        pass  # We handle logging explicitly


class ThreadedAnalysisServer(ThreadingHTTPServer):
    """Threaded HTTP server with dependency injection"""

    daemon_threads = True

    def __init__(
        self,
        server_address,
        RequestHandlerClass,
        engine: StaticAnalysisEngine,
        config: AnalyzerConfig,
    ):
        RequestHandlerClass.engine = engine
        RequestHandlerClass.config = config
        super().__init__(server_address, RequestHandlerClass)


class SubinterpreterMixIn:
    from concurrent.futures import InterpreterPoolExecutor
    from concurrent import interpreters
    from socketserver import BaseServer

    """Mixin to process requests in subinterpreters"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._executor = InterpreterPoolExecutor(
            max_workers=4
        )  # Pool of subinterpreters
        self._channel = interpreters.create_channel()  # For sending/receiving data

    def process_request(self, request, client_address):
        # Submit to executor: Run in subinterpreter
        future = self._executor.submit(
            self._handle_in_subinterpreter, request, client_address
        )
        # Wait or async handle (for non-blocking, use as_completed)
        try:
            response = future.result()  # Get result from subinterpreter
            # Send response back via socket (assuming you reconstruct it)
        except Exception as e:
            self.handle_error(request, client_address, e)

    def _handle_in_subinterpreter(self, request_fd, client_address):
        # This runs in subinterpreter: Reconstruct socket from FD
        import socket

        sock = socket.fromfd(request_fd, socket.AF_INET, socket.SOCK_STREAM)
        # Run your handler logic here (e.g., AnalysisRequestHandler)
        handler = self.RequestHandlerClass(sock, client_address, self)
        handler.handle()
        # Return response data via channel or directly (since future.result() can return picklable data)
        return "Response data"  # Serialize as needed

    def shutdown(self):
        self._executor.shutdown(wait=True)
        super().shutdown()


class SubinterpreterAnalysisServer(SubinterpreterMixIn, HTTPServer):
    daemon_threads = True  # Still useful for any threads
    ...


class LspClient:
    """Stdlib-only LSP client for iwes"""

    def __init__(
        self,
        iwes_path: str = 'iwes',
        project_root: Path = Path.cwd(),
        logger: ContextualLogger = None,
    ):
        self.logger = logger or get_logger(self.__class__.__name__)
        self.process = subprocess.Popen(
            [iwes_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=str(project_root),
            bufsize=0,  # Unbuffered
        )
        self._thread = threading.Thread(target=self._read_stderr, daemon=True)
        self._thread.start()
        self.initialize()  # Send LSP initialize

    def _read_stderr(self):
        """Log stderr in background"""
        while True:
            line = self.process.stderr.readline()
            if not line:
                break
            self.logger.info(line.decode().strip())

    def _send_message(self, message: LspMessage):
        content = json.dumps(asdict(message)).encode('utf-8')
        header = f"Content-Length: {len(content)}\r\n\r\n".encode('utf-8')
        self.process.stdin.write(header + content)
        self.process.stdin.flush()

    def _read_message(self) -> LspMessage:
        headers = {}
        while True:
            line = self.process.stdout.readline().decode('utf-8').strip()
            if not line:
                break
            if ':' in line:
                key, value = line.split(':', 1)
                headers[key.strip()] = value.strip()
        content_length = int(headers.get('Content-Length', 0))
        content = self.process.stdout.read(content_length).decode('utf-8')
        return LspMessage.from_dict(json.loads(content))

    def initialize(self):
        """Initialize LSP session"""
        init_id = uuid.uuid4().int & (1 << 32) - 1  # Simple ID
        params = {
            "processId": os.getpid(),
            "rootUri": f"file://{Path.cwd().absolute()}",
            "capabilities": {},  # Add client caps as needed
        }
        self._send_message(LspMessage(id=init_id, method="initialize", params=params))
        response = self._read_message()
        if response.error:
            raise LspError(f"Initialize failed: {response.error}")
        self.logger.info("LSP initialized")

    def request(self, method: str, params: Dict[str, Any]) -> Any:
        req_id = uuid.uuid4().int & (1 << 32) - 1
        self._send_message(LspMessage(id=req_id, method=method, params=params))
        while True:  # Handle notifications if any
            response = self._read_message()
            if response.id == req_id:
                if response.error:
                    raise LspError(f"Request failed: {response.error}")
                return response.result

    def close(self):
        self._send_message(LspMessage(method="shutdown"))
        self._read_message()  # Wait for response
        self.process.terminate()
        self.process.wait()


def main():
    """Main entry point for the morphological analysis engine"""
    logger.info("=" * 70)
    logger.info("Morphological Analysis Engine Starting")
    logger.info("=" * 70)

    # Display installed packages (for debugging)
    logger.info("Installed packages:")
    for dist in distributions():
        logger.info(f"  {dist.metadata['Name']}: {dist.metadata['Version']}")

    # Configuration
    allowed_roots = [Path.cwd()]  # Allow current directory

    analyzer_config = AnalyzerConfig(
        allowed_source_roots=tuple(allowed_roots),
        max_file_size_bytes=1 * 1024 * 1024,  # 1 MiB
        max_request_body_size=10 * 1024 * 1024,  # 10 MiB
        source_encoding='utf-8',
        allowed_extensions=('.py',),
    )

    logger.info(f"Configuration: {analyzer_config.to_dict()}")

    # Initialize analysis engine
    engine = StaticAnalysisEngine(analyzer_config)

    # Start HTTP server
    host = os.environ.get('HOST', '127.0.0.1')
    port = int(os.environ.get('PORT', '8698'))

    server = ThreadedAnalysisServer(
        (host, port), AnalysisRequestHandler, engine, analyzer_config
    )

    logger.info(f"Server listening on http://{host}:{port}")
    logger.info("Endpoints:")
    logger.info("  POST /analyze - Analyze Python source code")
    logger.info("  GET /health - Health check")
    logger.info("=" * 70)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("Shutting down server...")
        server.shutdown()
        logger.info("Server stopped")


# ============================================================================
# DEMONSTRATION AND TESTING
# ============================================================================


def demo_analysis():
    """Demonstrate static analysis capabilities"""
    logger.info("\n" + "=" * 70)
    logger.info("DEMO: Static Analysis Engine")
    logger.info("=" * 70)

    # Setup
    allowed_roots = [Path.cwd()]
    config = AnalyzerConfig(
        allowed_source_roots=tuple(allowed_roots), max_file_size_bytes=10 * 1024 * 1024
    )

    engine = StaticAnalysisEngine(config)

    # Create test file
    test_code = '''
"""Test module for analysis"""
import os
import sys
from pathlib import Path

class TestClass:
    """A test class"""
    def __init__(self, name: str):
        self.name = name
    
    def greet(self) -> str:
        return f"Hello, {self.name}!"

def test_function(x: int, y: int) -> int:
    """Add two numbers"""
    return x + y

# Global variable
CONSTANT = 42

if __name__ == "__main__":
    obj = TestClass("World")
    print(obj.greet())
    print(test_function(1, 2))
'''

    test_file = Path.cwd() / "test_analysis.py"
    test_file.write_text(test_code)

    try:
        # Analyze
        request = SourceRequest(source_path=test_file)
        result = engine.analyze(request)

        logger.info("✓ Analysis completed successfully")
        logger.info(f"  Request ID: {result.metadata.request_id}")
        logger.info(f"  Source hash: {result.metadata.source_hash_sha256[:16]}...")
        logger.info(f"  Functions found: {len(result.semantic_graph['functions'])}")
        logger.info(f"  Classes found: {len(result.semantic_graph['classes'])}")
        logger.info(f"  Imports found: {len(result.semantic_graph['imports'])}")
        logger.info(f"  Complexity score: {result.semantic_graph['complexity']}")

        # Display details
        logger.info("\n  Functions:")
        for func in result.semantic_graph['functions']:
            logger.info(f"    - {func['name']} (line {func['lineno']})")

        logger.info("\n  Classes:")
        for cls in result.semantic_graph['classes']:
            logger.info(f"    - {cls['name']} (line {cls['lineno']})")

        logger.info("\n  Imports:")
        for imp in result.semantic_graph['imports']:
            if 'name' in imp:
                logger.info(f"    - from {imp['module']} import {imp['name']}")
            else:
                logger.info(f"    - import {imp['module']}")

    finally:
        # Cleanup
        if test_file.exists():
            test_file.unlink()


def demo_dynamic_module():
    """Demonstrate dynamic module creation (morphological behavior)"""
    logger.info("\n" + "=" * 70)
    logger.info("DEMO: Dynamic Module Creation")
    logger.info("=" * 70)

    # Create a quine-like module that can introspect itself
    module_code = '''
import inspect
import ast
import hashlib

def introspect():
    """Examine own source code"""
    source = inspect.getsource(introspect)
    tree = ast.parse(source)
    
    print(f"Function: introspect")
    print(f"Lines: {len(source.splitlines())}")
    print(f"AST nodes: {len(list(ast.walk(tree)))}")
    print(f"Hash: {hashlib.sha256(source.encode()).hexdigest()[:16]}...")
    
    return source

def replicate():
    """Quine-like behavior: return own source"""
    return inspect.getsource(replicate)

def greet():
    """Simple greeting"""
    return "Hello from dynamically created module!"
'''

    # Create module
    module_name = "morphological_quine"
    module = create_module(module_name, module_code, __file__)

    if module:
        logger.info(f"✓ Created module: {module_name}")
        logger.info(f"  Module file: {module.__file__}")
        logger.info(f"  Module package: {module.__package__}")

        # Test functions
        logger.info(f"\n  Greeting: {module.greet()}")

        logger.info("\n  Introspection:")
        module.introspect()

        logger.info("\n  Replication (first 100 chars):")
        replica = module.replicate()
        logger.info(f"  {replica[:100]}...")

        # Verify it's in sys.modules
        logger.info(
            f"\n✓ Module registered in sys.modules: {module_name in sys.modules}"
        )
    else:
        logger.error("✗ Failed to create dynamic module")


def demo_rpc_client():
    """Demonstrate RPC client interaction"""
    logger.info("\n" + "=" * 70)
    logger.info("DEMO: RPC Client")
    logger.info("=" * 70)

    # Create test code
    test_code = '''
def fibonacci(n: int) -> int:
    """Calculate fibonacci number"""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

class Calculator:
    """Simple calculator"""
    def add(self, a, b):
        return a + b
    
    def multiply(self, a, b):
        return a * b
'''

    # Encode as base64
    import base64

    content_b64 = base64.b64encode(test_code.encode('utf-8')).decode('ascii')

    # Create request payload
    payload = {"path": "test_client.py", "content_b64": content_b64}

    logger.info("RPC Request Payload:")
    logger.info(json.dumps(payload, indent=2))

    logger.info("\nTo test with actual server, run:")
    logger.info("  1. Start server: python this_file.py")
    logger.info("  2. In another terminal:")
    logger.info(f'''
    curl -X POST http://127.0.0.1:8698/analyze \\
      -H "Content-Type: application/json" \\
      -H "X-Correlation-ID: test-{uuid.uuid4().hex[:8]}" \\
      -d '{json.dumps(payload)}'
    ''')


def demo_integration():
    """Full integration demo combining all components"""
    logger.info("\n" + "=" * 70)
    logger.info("DEMO: Full Integration")
    logger.info("=" * 70)

    try:
        # 1. Create dynamic module
        logger.info("\n1. Creating dynamic analysis module...")
        analysis_code = '''
import ast

def analyze_complexity(code: str) -> dict:
    """Analyze code complexity"""
    tree = ast.parse(code)
    
    nodes = list(ast.walk(tree))
    functions = [n for n in nodes if isinstance(n, ast.FunctionDef)]
    classes = [n for n in nodes if isinstance(n, ast.ClassDef)]
    loops = [n for n in nodes if isinstance(n, (ast.For, ast.While))]
    conditionals = [n for n in nodes if isinstance(n, ast.If)]
    
    return {
        'total_nodes': len(nodes),
        'functions': len(functions),
        'classes': len(classes),
        'loops': len(loops),
        'conditionals': len(conditionals),
        'complexity_score': len(loops) + len(conditionals) + len(functions) * 2
    }
'''

        analysis_module = create_module("dynamic_analysis", analysis_code)
        if not analysis_module:
            raise RuntimeError("Failed to create analysis module")

        logger.info("✓ Dynamic module created")

        # 2. Setup analysis engine
        logger.info("\n2. Initializing static analysis engine...")
        config = AnalyzerConfig(
            allowed_source_roots=(Path.cwd(),), max_file_size_bytes=1024 * 1024
        )
        engine = StaticAnalysisEngine(config)
        logger.info("✓ Engine initialized")

        # 3. Create test file
        logger.info("\n3. Creating test source file...")
        test_code = '''
class DataProcessor:
    """Process data with various methods"""
    
    def __init__(self, data):
        self.data = data
    
    def process(self):
        results = []
        for item in self.data:
            if item > 0:
                results.append(item * 2)
            else:
                results.append(0)
        return results
    
    def filter_positive(self):
        return [x for x in self.data if x > 0]

def main():
    processor = DataProcessor([1, -2, 3, -4, 5])
    print(processor.process())
    print(processor.filter_positive())
'''

        test_file = Path.cwd() / "integration_test.py"
        test_file.write_text(test_code)
        logger.info(f"✓ Test file created: {test_file}")

        # 4. Analyze with engine
        logger.info("\n4. Running static analysis...")
        request = SourceRequest(source_path=test_file)
        result = engine.analyze(request)
        logger.info("✓ Analysis completed")

        # 5. Run dynamic analysis
        logger.info("\n5. Running dynamic complexity analysis...")
        dynamic_result = analysis_module.analyze_complexity(test_code)
        logger.info("✓ Dynamic analysis completed")

        # 6. Compare results
        logger.info("\n6. Results comparison:")
        logger.info("  Static analysis:")
        logger.info(f"    Functions: {len(result.semantic_graph['functions'])}")
        logger.info(f"    Classes: {len(result.semantic_graph['classes'])}")
        logger.info(f"    Complexity: {result.semantic_graph['complexity']}")

        logger.info("\n  Dynamic analysis:")
        logger.info(f"    Functions: {dynamic_result['functions']}")
        logger.info(f"    Classes: {dynamic_result['classes']}")
        logger.info(f"    Loops: {dynamic_result['loops']}")
        logger.info(f"    Conditionals: {dynamic_result['conditionals']}")
        logger.info(f"    Complexity: {dynamic_result['complexity_score']}")

        # 7. Serialize result
        logger.info("\n7. Serializing results...")
        json_result = result.to_json(indent=2)
        logger.info(f"✓ JSON output ({len(json_result)} bytes)")
        logger.info(f"  Fingerprint: {result.fingerprint()}")

        logger.info("\n✓ Integration test completed successfully!")

    except Exception as e:
        logger.error(f"✗ Integration test failed: {e}", exc_info=True)

    finally:
        # Cleanup
        if test_file.exists():
            test_file.unlink()
            logger.info("✓ Cleanup completed")


# ============================================================================
# CLI INTERFACE
# ============================================================================


def cli():
    """Command-line interface for the engine"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Morphological Analysis Engine - Static code analysis with RPC interface"
    )

    parser.add_argument(
        'command', choices=['serve', 'analyze', 'demo'], help='Command to execute'
    )

    parser.add_argument(
        '--file', type=Path, help='File to analyze (for analyze command)'
    )

    parser.add_argument(
        '--host', default='127.0.0.1', help='Server host (for serve command)'
    )

    parser.add_argument(
        '--port', type=int, default=8698, help='Server port (for serve command)'
    )

    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        default='INFO',
        help='Logging level',
    )

    parser.add_argument(
        '--json-logs', action='store_true', help='Output logs in JSON format'
    )

    args = parser.parse_args()

    # Setup logging
    global logger
    log_level = getattr(logging, args.log_level)
    logger = setup_logging(level=log_level, json_format=args.json_logs)

    # Execute command
    if args.command == 'serve':
        os.environ['HOST'] = args.host
        os.environ['PORT'] = str(args.port)
        main()

    elif args.command == 'analyze':
        if not args.file:
            parser.error("--file required for analyze command")

        config = AnalyzerConfig(
            allowed_source_roots=(args.file.parent.resolve(),),
            max_file_size_bytes=10 * 1024 * 1024,
        )

        engine = StaticAnalysisEngine(config)
        request = SourceRequest(source_path=args.file)

        try:
            result = engine.analyze(request)
            print(result.to_json(indent=2))
        except Exception as e:
            logger.error(f"Analysis failed: {e}", exc_info=True)
            sys.exit(1)

    elif args.command == 'demo':
        demo_analysis()
        demo_dynamic_module()
        demo_rpc_client()
        demo_integration()


# ============================================================================
# EXPORT PUBLIC API
# ============================================================================


__all__ = [
    # Core classes
    'StaticAnalysisEngine',
    'SemanticVisitor',
    # Data models
    'SourceRequest',
    'AnalysisMetadata',
    'AnalysisResult',
    'SemanticGraph',
    # Configuration
    'AnalyzerConfig',
    'RuntimeConfig',
    # Enums
    'QuantumState',
    'RuntimeMode',
    'Mutability',
    'SerializationFormat',
    # Exceptions
    'MorphologicalError',
    'AnalyzerError',
    'ConfigurationError',
    'SourceError',
    'SourceNotFoundError',
    'SourcePermissionError',
    'SourceSizeExceededError',
    'ParsingError',
    'InputValidationError',
    'SecurityViolationError',
    'ResourceLimitExceededError',
    # Utilities
    'create_module',
    'setup_logging',
    'get_logger',
    # Server
    'ThreadedAnalysisServer',
    'AnalysisRequestHandler',
    # Base
    'BaseModel',
    'ContextualLogger',
]

__version__ = "1.0.0"
__author__ = "MOONLAPSED"
__license__ = "BSD-3 & CC BY"
__description__ = (
    "Morphological Analysis Engine: Static analysis with RPC/LSP capabilities"
)

# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    # Check if running as CLI
    if len(sys.argv) > 1:
        cli()
    else:
        # Default: run server
        main()

# ============================================================================
# USAGE EXAMPLES
# ============================================================================
"""
COMMAND LINE USAGE:

1. Start RPC server:
   python morphological_engine.py serve --host 0.0.0.0 --port 8698

2. Analyze a file directly:
   python morphological_engine.py analyze --file mycode.py

3. Run demonstrations:
   python morphological_engine.py demo

4. With custom logging:
   python morphological_engine.py serve --log-level DEBUG --json-logs


PROGRAMMATIC USAGE:

from morphological_engine import (
    StaticAnalysisEngine,
    AnalyzerConfig,
    SourceRequest
)
from pathlib import Path

# Configure
config = AnalyzerConfig(
    allowed_source_roots=(Path.cwd(),),
    max_file_size_bytes=1024 * 1024
)

# Create engine
engine = StaticAnalysisEngine(config)

# Analyze
request = SourceRequest(source_path=Path("mycode.py"))
result = engine.analyze(request)

# Access results
print(f"Functions: {len(result.semantic_graph['functions'])}")
print(f"Classes: {len(result.semantic_graph['classes'])}")
print(f"Complexity: {result.semantic_graph['complexity']}")


RPC CLIENT USAGE:

import requests
import base64

# Prepare code
with open("mycode.py", "rb") as f:
    code_bytes = f.read()

payload = {
    "path": "mycode.py",
    "content_b64": base64.b64encode(code_bytes).decode('ascii')
}

# Send request
response = requests.post(
    "http://127.0.0.1:8698/analyze",
    json=payload,
    headers={"X-Correlation-ID": "my-request-123"}
)

# Process result
if response.status_code == 200:
    result = response.json()
    print(result['semantic_graph'])
else:
    print(f"Error: {response.json()['error']}")


DYNAMIC MODULE CREATION:

from morphological_engine import create_module

code = '''
def my_function():
    return "Hello from dynamic module!"
'''

module = create_module("my_dynamic_module", code)
if module:
    print(module.my_function())


LSP INTEGRATION (Future):

The engine provides the foundation for LSP server implementation:
- Semantic analysis → Hover information
- Function/class detection → Document symbols
- Complexity scoring → Code metrics
- AST walking → Go to definition

Next steps for full LSP:
1. Implement LSP protocol message handling
2. Add incremental parsing for document changes
3. Implement diagnostics generation
4. Add code completion using semantic graph
---

**Goal**: Make your LSP **speak IWE’s dialect**—not just static analysis, but full **Markdown-as-a-graph**, **section-aware transformations**, **block references**, **header normalization**, **inlay hints**, etc. IWE is not a general-purpose Python analyzer—it’s a **Markdown-native LSP**. So your current LSP focuses on **Python AST**, while IWE focuses on **Markdown graph semantics**.

You don’t need to *replace* IWE. You need to **complement** or **bridge** it. Make your LSP IWE-aware**:

> → Use IWE as a **subprocess** or **sidecar**, and have your Python LSP **delegate Markdown tasks** to IWE’s `iwes` binary (via JSON-RPC over stdio or HTTP)

---

### 🛠 Security note: Sanitize paths and content before passing to `iwes`. Treat it like any external service.

#### **Support IWE’s “Block References” and “Path Hierarchy”**
| LSP Method                | IWE Feature                   | Your Action |
|--------------------------|-------------------------------|-------------|
| `textDocument/definition`| Go to definition (link nav)   | Parse `[text](file.md#header)` and resolve |
| `textDocument/references`| Backlinks                     | Build reverse index of all links |
| `textDocument/documentSymbol` | TOC / Outline         | Parse `# Header` hierarchy |
| `textDocument/codeAction` | Extract/Inline/Rename/AI     | Implement transformers on header ranges |
| `textDocument/completion` | Link auto-complete           | Fuzzy-search `.md` files & headers |
| `textDocument/formatting` | Normalize headers/links      | Rebuild header levels, sync link titles |

We have a **semantic visitor pattern**—just make a `MarkdownVisitor` using regex or stdlib `re`.

```python
# In MarkdownVisitor
def visit_header(self, line: str, lineno: int):
    level = count_leading_hashes(line)
    title = extract_title(line)
    self.sections.append(MarkdownSection(title, level, lineno, ...))
```
We need to:
- Parse header hierarchy
- Build parent-child relationships
- Expose this as `documentSymbol` hierarchy

> _“IWE will generate full paths… Journal, 2025 ⇒ Week 3 ⇒ Jan 26”_

We need to:
- Parse header hierarchy
- Build parent-child relationships
- Expose this as `documentSymbol` hierarchy

Example:
```python
# In MarkdownVisitor
def visit_header(self, line: str, lineno: int):
    level = count_leading_hashes(line)
    title = extract_title(line)
    self.sections.append(MarkdownSection(title, level, lineno, ...))
```
Then reconstruct tree via stack.
---
"""
