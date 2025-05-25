from __future__ import annotations
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Union, Generic, TypeVar, Mapping, Optional
import hashlib
import inspect
import ast
import time
import logging
import json
import pathlib
import sys
from datetime import datetime
from enum import Enum
from functools import wraps
from types import SimpleNamespace
# Assuming sandbox_generator.py is located at ./platform/sandbox_generator.py
try:
    import platform.sandbox_generator as sg
except ImportError:
    print("Error: Could not import platform.sandbox_generator.")
    print("Please ensure sandbox_generator.py is in a 'platform' directory")
    print("relative to your main.py and that 'platform' is a valid Python package (e.g., has an __init__.py).")
    sys.exit(1)


def mapper(mapping_description, input_data):
    """Transform input data according to a mapping description."""
    def transform(xform, value):
        if callable(xform):
            return xform(value)
        elif isinstance(xform, Mapping):
            return {k: transform(v, value) for k, v in xform.items()}
        else:
            raise ValueError(f"Invalid transformation: {xform}")

    def get_value(key):
        if isinstance(key, str) and key.startswith(":"):
            # Access directly by key name without the colon prefix
            return input_data.get(key[1:])
        # Standard dictionary access
        return input_data.get(key)

    def process_mapping(mapping_desc):
        result = {}
        for key, xform in mapping_desc.items():
            if isinstance(xform, str):
                # Direct mapping from input key (string value)
                result[key] = get_value(xform)
            elif isinstance(xform, Mapping):
                # Complex mapping (dictionary value)
                if "key" in xform:
                    # Map from a specific input key
                    value = get_value(xform["key"])
                    if value is not None:
                        if "xform" in xform:
                            # Apply a single transformation function
                            result[key] = transform(xform["xform"], value)
                        elif "xf" in xform:
                            # Apply transformation to each item if list, or the item itself
                            if isinstance(value, list):
                                transformed = [xform["xf"](v) for v in value]
                                if "f" in xform:
                                    # Apply a final function to the list of transformed items
                                    result[key] = xform["f"](transformed)
                                else:
                                    # Keep the list of transformed items
                                    result[key] = transformed
                            else:
                                # Apply transformation to the single item
                                result[key] = xform["xf"](value)
                        else:
                            # No transformation specified, just use the value
                            result[key] = value
                else:
                    # Nested mapping (no "key" specified, process the sub-mapping)
                    result[key] = process_mapping(xform)
            else:
                # Static value (not a string or mapping)
                result[key] = xform
        return result
    return process_mapping(mapping_description)


def jsonload_file(file_path: pathlib.Path, mapping_description: dict):
    """Load a JSON file and transform it according to a mapping description."""
    try:
        with file_path.open('r', encoding='utf-8') as file:
            data = json.load(file)
        return mapper(mapping_description, data)
    except FileNotFoundError:
        logging.error(f"JSON file not found: {file_path}")
        return None
    except json.JSONDecodeError:
        logging.error(f"Error decoding JSON from file: {file_path}")
        return None
    except Exception as e:
        logging.error(f"Error loading or mapping JSON file {file_path}: {e}")
        return None


class PyObject(ABC):
    # Note: __getattribute__, __setattr__, __call__, __repr__, __str__
    # are fundamental object methods. Making them abstract here means
    # any concrete subclass *must* implement them, which might be
    # overly restrictive depending on the intent. Python provides
    # default implementations for these. This is morphological or
    # intentional in nature.
    @abstractmethod
    def __getattribute__(self, name: str) -> Any:
        return object.__getattribute__(self, name)

    @abstractmethod
    def __setattr__(self, name: str, value: Any) -> None:
        object.__setattr__(self, name, value)

    @abstractmethod
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError

    @abstractmethod
    def __repr__(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def ob_refcnt(self) -> int:
        raise NotImplementedError

    @ob_refcnt.setter
    @abstractmethod
    def ob_refcnt(self, value: int) -> None:
        raise NotImplementedError

    @property
    @abstractmethod
    def ob_ttl(self) -> Optional[int]:
        raise NotImplementedError

    @ob_ttl.setter
    @abstractmethod
    def ob_ttl(self, value: Optional[int]) -> None:
        raise NotImplementedError


# Type variables for generic usage
T = TypeVar("T")
V = TypeVar("V")
C = TypeVar("C")


class BaseModel:
    def __init__(self, **data):
        # Use setattr to trigger the custom __setattr__ logic
        for name, value in data.items():
            setattr(self, name, value)

    def __setattr__(self, name, value):
        # Check if the attribute is defined in annotations for type checking/validation
        if hasattr(self.__class__, '__annotations__') and name in self.__class__.__annotations__:
            expected_type = self.__class__.__annotations__[name]
            # Basic type checking
            # Note: isinstance check might be too strict for Union, Optional, etc.
            # For simple types, this is okay.
            if not isinstance(value, expected_type):
                # Handle Optional types specifically
                if not (getattr(expected_type, '__origin__', None) is Union and
                        type(None) in getattr(expected_type, '__args__', ()) and
                        isinstance(value, tuple(t for t in getattr(expected_type, '__args__', ()) if t is not type(None)))):
                    raise TypeError(
                        f"Expected {expected_type} for {name}, got {type(value)}")

            # Call custom validator method if it exists
            validator = getattr(self.__class__, f'validate_{name}', None)
            if validator:
                # Pass self and value to the validator
                value = validator(self, value)

        # Use the superclass's setattr to actually set the attribute
        super().__setattr__(name, value)

    @classmethod
    def create(cls, **kwargs):
        """Factory method to create an instance."""
        return cls(**kwargs)

    def dict(self):
        """Return a dictionary representation of the model."""
        # Iterate over annotations to get defined fields, fallback to __dict__
        if hasattr(self.__class__, '__annotations__'):
            # Get attributes defined in annotations, handling potential missing attributes
            return {name: getattr(self, name, None) for name in self.__class__.__annotations__}
        # If no annotations, return a copy of the instance dictionary
        return self.__dict__.copy()

    def __repr__(self):
        """Return a developer-friendly string representation."""
        # Use annotations for repr if available, otherwise use __dict__
        if hasattr(self.__class__, '__annotations__'):
            attrs = ', '.join(
                # Use !r for repr() of attribute value
                f"{name}={getattr(self, name, None)!r}"
                for name in self.__class__.__annotations__
            )
        else:
            attrs = ', '.join(f"{name}={value!r}" for name,
                              value in self.__dict__.items())
        return f"{self.__class__.__name__}({attrs})"

    def __str__(self):
        """Return a user-friendly string representation."""
        # Use annotations for str if available, otherwise use __dict__
        if hasattr(self.__class__, '__annotations__'):
            attrs = ', '.join(
                # Use default str() of attribute value
                f"{name}={getattr(self, name, None)}"
                for name in self.__class__.__annotations__
            )
        else:
            attrs = ', '.join(f"{name}={value}" for name,
                              value in self.__dict__.items())
        return f"{self.__class__.__name__}({attrs})"

    def clone(self):
        """Create a shallow copy of the model instance."""
        # Create a new instance using the dictionary representation
        return self.__class__(**self.dict())


class FileModel(BaseModel):
    file_name: str
    file_content: str

    def save(self, directory: pathlib.Path):
        """Save the file content to the specified directory."""
        try:
            # Ensure directory exists
            directory.mkdir(parents=True, exist_ok=True)
            target_path = directory / self.file_name
            with target_path.open('w', encoding='utf-8') as file:  # Specify encoding
                file.write(self.file_content)
            logging.info(f"Saved {self.file_name} to {target_path}")
            return target_path
        except Exception as e:
            logging.error(
                f"Failed to save {self.file_name} to {directory}: {e}")
            return None


def create_model_from_file(file_path: pathlib.Path):
    """Create a FileModel instance from a file path."""
    try:
        with file_path.open('r', encoding='utf-8', errors='ignore') as file:
            content = file.read()
        # Dynamically create a class name based on the file stem
        model_name = file_path.stem.replace(
            '-', '_').replace(' ', '_').capitalize() + 'Model'
        # Create a new class inheriting from FileModel
        model_class = type(model_name, (FileModel,), {})
        # Create an instance of the new class
        instance = model_class.create(
            file_name=file_path.name, file_content=content)

        # --- POTENTIAL ISSUE ---
        # sys.modules is intended for storing *module* objects, not instances.
        # If other code tries to 'import ModelNameModel', it won't get this instance.
        # Consider removing this line and managing instances in a dedicated registry
        # or the models dictionary returned by load_files_as_models.
        # sys.modules[model_name] = instance
        # --- END POTENTIAL ISSUE ---

        logging.info(f"Created {model_name} instance from {file_path}")
        return model_name, instance
    except Exception as e:
        logging.error(f"Failed to create model from {file_path}: {e}")
        return None, None


def load_files_as_models(root_dir: pathlib.Path, file_extensions: List[str]) -> Dict[str, BaseModel]:
    """Load all files with specified extensions as models."""
    models = {}
    if not root_dir.is_dir():
        logging.warning(
            f"Root directory not found or is not a directory: {root_dir}")
        return models  # Return empty dict if root_dir is invalid

    for ext in file_extensions:
        # Ensure extension starts with a dot
        search_pattern = f'*{ext}' if ext.startswith('.') else f'*.{ext}'
        for file_path in root_dir.rglob(search_pattern):
            if file_path.is_file():
                model_name, instance = create_model_from_file(file_path)
                if model_name and instance:
                    # Store the instance in the models dictionary
                    models[model_name] = instance
    logging.info(f"Loaded {len(models)} models from {root_dir}")
    return models


AccessLevel = Enum('AccessLevel', 'READ WRITE EXECUTE ADMIN USER')


@dataclass
class AccessPolicy:
    """Defines access control policies for runtime operations."""
    level: AccessLevel
    namespace_patterns: list[str] = field(default_factory=list)
    allowed_operations: list[str] = field(default_factory=list)

    def can_access(self, namespace: str, operation: str) -> bool:
        """Check if access is allowed for the given namespace and operation."""
        # Check if the operation is allowed at all by the policy's allowed_operations list
        if operation not in self.allowed_operations:
            return False

        # Check if the namespace matches any of the allowed patterns
        # Using 'in' for substring check might be too broad. Consider regex or glob matching for more precision.
        return any(pattern in namespace for pattern in self.namespace_patterns)


class SecurityContext:
    """Manages security context and audit logging for runtime operations."""

    def __init__(self, user_id: str, access_policy: AccessPolicy):
        self.user_id = user_id
        self.access_policy = access_policy
        self._audit_log = []

    def log_access(self, namespace: str, operation: str, success: bool):
        """Log an access attempt."""
        self._audit_log.append({
            "user_id": self.user_id,
            "namespace": namespace,
            "operation": operation,
            "success": success,
            "timestamp": datetime.now().timestamp()
        })

    @property
    def audit_log(self):
        """Return a copy of the audit log."""
        return self._audit_log.copy()


class SecurityValidator(ast.NodeVisitor):
    """Validates AST nodes against security policies."""

    def __init__(self, security_context: SecurityContext):
        self.security_context = security_context
        self.violations = []

    def visit_Name(self, node):
        # Check read access for variable/name usage
        namespace = node.id  # Using the name itself as the namespace part
        operation = "read"
        can_access = self.security_context.access_policy.can_access(
            namespace, operation)
        self.security_context.log_access(namespace, operation, can_access)
        if not can_access:
            violation = f"Access denied to name: {node.id}"
            self.violations.append(violation)
            raise PermissionError(violation)
        self.generic_visit(node)  # Continue visiting child nodes

    def visit_Call(self, node):
        # Check execute access for function calls
        if isinstance(node.func, ast.Name):
            namespace = node.func.id  # Using the function name as the namespace part
            operation = "execute"
            can_access = self.security_context.access_policy.can_access(
                namespace, operation)
            self.security_context.log_access(namespace, operation, can_access)
            if not can_access:
                violation = f"Access denied to function: {node.func.id}"
                self.violations.append(violation)
                raise PermissionError(violation)
        # Note: This only checks calls where the function is a simple name (e.g., `print()`).
        # It won't check method calls (e.g., `obj.method()`) or calls via attributes (e.g., `module.func()`).
        # A more robust validator would need to handle ast.Attribute nodes as well.
        self.generic_visit(node)  # Continue visiting child nodes


class FrameModel(Generic[T, V, C], ABC):
    # Removed init method, moved delimiter setting to class attributes
    start_delimiter: str = "<<CONTENT>>"
    end_delimiter: str = "<<END_CONTENT>>"

    @abstractmethod
    def to_bytes(self) -> bytes:
        pass

    @abstractmethod
    def parse_content(self, raw_content: str) -> str:
        pass

    def validate_content(self, content: str) -> bool:
        """Validate content format based on delimiters."""
        # Check if content starts and ends with the defined delimiters
        return content.startswith(self.start_delimiter) and content.endswith(self.end_delimiter)


@dataclass
class CustomDelimiterFrame(FrameModel):
    content: str
    # Delimiters are inherited from FrameModel or can be overridden here
    # start_delimiter: str = "<<CUSTOM_START>>"
    # end_delimiter: str = "<<CUSTOM_END>>"

    # Removed __post_init__ calling init() as delimiters are now class/instance attributes

    def to_bytes(self) -> bytes:
        """Encode the framed content to bytes."""
        # Include delimiters when converting to bytes
        framed_content = self.start_delimiter + self.content + self.end_delimiter
        return framed_content.encode('utf-8')  # Specify encoding

    def parse_content(self, raw_content: str) -> str:
        """Extract content between delimiters."""
        start_index = raw_content.find(self.start_delimiter)
        end_index = raw_content.rfind(self.end_delimiter)
        # Validate indices to ensure delimiters are present and in correct order
        if start_index == -1 or end_index == -1 or start_index >= end_index:
            raise ValueError(
                "Invalid content format: Missing or mismatched delimiters.")
        # Extract content between the delimiters
        return raw_content[start_index + len(self.start_delimiter):end_index]

    # Added a method to create from raw framed content
    @classmethod
    def from_raw_content(cls, raw_content: str) -> 'CustomDelimiterFrame':
        """Create an instance by parsing raw framed content."""
        # Create a dummy instance to access class attributes (delimiters)
        dummy_instance = cls(content="")
        if not dummy_instance.validate_content(raw_content):
            raise ValueError(
                "Invalid content format: Content does not match expected delimiters.")
        parsed_content = dummy_instance.parse_content(raw_content)
        return cls(content=parsed_content)


def register_models(models: Dict[str, BaseModel], target_globals=None):
    """Register models in the specified globals dictionary or the caller's globals."""
    if target_globals is None:
        # Get the globals of the frame that called this function
        frame = inspect.currentframe()
        if frame is None:
            logging.error("Could not get current frame to register models.")
            return
        target_globals = frame.f_back.f_globals if frame.f_back else None
        if target_globals is None:
            logging.error("Could not get caller's globals to register models.")
            return

    for model_name, instance in models.items():
        target_globals[model_name] = instance
        logging.info(
            f"Registered {model_name} instance in the global namespace")


def runtime(root_dir: pathlib.Path, extensions=None):
    """Initialize the runtime with models from the specified directory."""
    if extensions is None:
        extensions = ['.md', '.txt']
    logging.info(
        f"Loading models from {root_dir} with extensions {extensions}")
    file_models = load_files_as_models(root_dir, extensions)
    # Register the loaded models (currently adds them to globals)
    register_models(file_models)
    logging.info("Runtime initialization complete.")
    return file_models


class RuntimeNamespace:
    """Manages hierarchical runtime namespaces with security controls."""

    def __init__(self, name: str = "root", parent: Optional['RuntimeNamespace'] = None):
        if not isinstance(name, str) or not name.isidentifier() and name != "root":
            raise ValueError(f"Invalid namespace name: {name}")
        self._name = name
        self._parent = parent
        self._children: Dict[str, 'RuntimeNamespace'] = {}
        # Use a dictionary for content for more explicit access than SimpleNamespace
        self._content: Dict[str, Any] = {}
        self._security_context: Optional[SecurityContext] = None
        # available_modules seems unused? Or intended for something else?
        self.available_modules = {}
        self.frame_model: Optional[FrameModel] = None

    @property
    def full_path(self) -> str:
        """Return the full dot-separated path of the namespace."""
        return f"{self._parent.full_path}.{self._name}" if self._parent else self._name

    def add_child(self, name: str) -> 'RuntimeNamespace':
        """Add a child namespace."""
        if not isinstance(name, str) or not name.isidentifier():
            raise ValueError(f"Invalid child namespace name: {name}")
        if name in self._children:
            logging.warning(
                f"Child namespace '{name}' already exists in '{self.full_path}'. Returning existing child.")
            return self._children[name]
        child = RuntimeNamespace(name, self)
        self._children[name] = child
        logging.info(f"Added child namespace '{name}' to '{self.full_path}'")
        return child

    def get_child(self, path: str) -> Optional['RuntimeNamespace']:
        """Get a child namespace by path (e.g., 'child1.grandchild')."""
        if not path:
            return self  # Return self if path is empty

        parts = path.split(".", 1)
        first_part = parts[0]

        if first_part not in self._children:
            logging.debug(
                f"Child '{first_part}' not found in '{self.full_path}'")
            return None

        child = self._children[first_part]

        if len(parts) == 1:
            # Reached the end of the path
            return child
        else:
            # Recurse into the rest of the path
            return child.get_child(parts[1])

    def set_security_context(self, context: SecurityContext):
        """Set the security context for this namespace."""
        if not isinstance(context, SecurityContext):
            raise TypeError("Context must be a SecurityContext instance.")
        self._security_context = context
        logging.info(f"Security context set for namespace '{self.full_path}'")

    def get_attribute(self, name: str, default=None):
        """Get an attribute from content with security validation."""
        full_attr_path = f"{self.full_path}.{name}"
        operation = "read"

        if self._security_context:
            can_access = self._security_context.access_policy.can_access(
                full_attr_path, operation
            )
            self._security_context.log_access(
                full_attr_path, operation, can_access)
            if not can_access:
                raise PermissionError(
                    f"Access denied to attribute: {full_attr_path}")

        # Access from the internal content dictionary
        return self._content.get(name, default)

    def set_attribute(self, name: str, value: Any):
        """Set an attribute in content with security validation."""
        full_attr_path = f"{self.full_path}.{name}"
        operation = "write"

        if self._security_context:
            can_access = self._security_context.access_policy.can_access(
                full_attr_path, operation
            )
            self._security_context.log_access(
                full_attr_path, operation, can_access)
            if not can_access:
                raise PermissionError(
                    f"Access denied to modify attribute: {full_attr_path}")

        # Set in the internal content dictionary
        self._content[name] = value
        logging.debug(
            f"Attribute '{name}' set in namespace '{self.full_path}'")

    def set_frame_model(self, frame_model: FrameModel) -> None:
        """Set the FrameModel for embedding/retrieving content."""
        if not isinstance(frame_model, FrameModel):
            raise TypeError(
                "frame_model must be an instance of FrameModel or its subclass.")
        self.frame_model = frame_model
        logging.info(f"FrameModel set for namespace '{self.full_path}'")

    def embed_content(self, raw_content: str) -> None:
        """Embed raw content using the configured FrameModel."""
        if not self.frame_model:
            raise ValueError("No FrameModel configured for this namespace.")

        # Validate and parse the content using the frame model
        # The frame model's parse_content should handle validation internally
        # or validate_content should be called first. Let's call validate first.
        if not self.frame_model.validate_content(raw_content):
            raise ValueError(
                "Content validation failed. Invalid delimiters or format.")

        try:
            parsed_content = self.frame_model.parse_content(raw_content)
            # Store the *parsed* content (without delimiters) in the namespace content
            self._content["embedded_data"] = parsed_content
            logging.info(f"Content embedded in namespace '{self.full_path}'")
        except ValueError as e:
            logging.error(
                f"Error parsing content for namespace '{self.full_path}': {e}")
            raise  # Re-raise the error after logging

    def retrieve_content(self) -> str:
        """Retrieve embedded content, framed by the FrameModel."""
        if "embedded_data" not in self._content:
            raise ValueError("No content embedded in this namespace.")
        if not self.frame_model:
            raise ValueError(
                "No FrameModel configured for this namespace to retrieve content.")

        # Reconstruct the framed content using the stored parsed data and delimiters
        parsed_content = self._content["embedded_data"]
        return self.frame_model.start_delimiter + parsed_content + self.frame_model.end_delimiter

    def __repr__(self) -> str:
        return f"RuntimeNamespace(name='{self._name}', full_path='{self.full_path}', children={list(self._children.keys())}, content_keys={list(self._content.keys())})"

    def __str__(self) -> str:
        return self.full_path


# ------------------------------------------------------------------------------
# Main Execution Block
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    # Configure basic logging
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    print("🚀 Starting Main Application Setup")
    print("=" * 50)

    # --- Step 1: Initialize Runtime (Load Models) ---
    # Define the root directory where your source code/files are located
    # This is where the 'runtime' function will look for files to load as models.
    # You might want to make this configurable (e.g., via command line args)
    # Example: Use the directory where main.py is located
    source_root_dir = pathlib.Path(__file__).parent

    # Ensure the 'platform' directory exists for the sandbox generator import check
    platform_dir = source_root_dir / "platform"
    if not platform_dir.is_dir():
        logging.warning(
            f"'{platform_dir}' directory not found. Sandbox generator import might fail.")
        # You might want to create it or exit here if it's essential

    # Example: Load .md and .txt files as models
    loaded_models = runtime(source_root_dir, extensions=['.md', '.txt'])
    print(f"\nLoaded {len(loaded_models)} models.")
    # print("Available models in global namespace:", [name for name in globals() if name.endswith('Model')]) # Use with caution due to global registration

    # --- Step 2: Generate Windows Sandbox Configuration ---
    # This calls the main function from the imported sandbox_generator module.
    # It will handle user interaction for the path and generate the .wsb file.
    print("\n🔧 Generating Windows Sandbox Configuration...")
    sg.main()  # This runs the interactive part of the sandbox generator

    # --- Step 3: Further Application Logic (Placeholders) ---
    # After generating the sandbox config, you might continue with other setup
    # or application logic here.

    print("\nContinuing with main application logic...")

    # Example: Create a root namespace
    root_ns = RuntimeNamespace("root")
    print(f"Created root namespace: {root_ns}")

    # Example: Add a child namespace
    platform_ns = root_ns.add_child("platform")
    print(f"Created child namespace: {platform_ns}")

    # Example: Set a security context (replace with actual policy)
    # admin_policy = AccessPolicy(AccessLevel.ADMIN, namespace_patterns=["root", "root.platform"], allowed_operations=["read", "write", "execute"])
    # admin_context = SecurityContext("admin_user", admin_policy)
    # root_ns.set_security_context(admin_context)
    # platform_ns.set_security_context(admin_context) # Apply same context or a different one

    # Example: Set a frame model
    # root_ns.set_frame_model(CustomDelimiterFrame(content="")) # Content is set when embedding

    # Example: Embed content (requires a frame model and content)
    # try:
    #     raw_data = "<<CONTENT>>Some important data<<END_CONTENT>>"
    #     root_ns.embed_content(raw_data)
    #     retrieved = root_ns.retrieve_content()
    #     print(f"Embedded and retrieved content: {retrieved}")
    # except ValueError as e:
    #     print(f"Could not embed/retrieve content: {e}")

    print("\n✅ Main Application Setup Complete.")
