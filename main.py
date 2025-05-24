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
# ------------------------------------------------------------------------------
# BaseModel (no-copy immutable dataclasses for data models)
# ------------------------------------------------------------------------------


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
            return input_data.get(key[1:])
        return input_data.get(key)

    def process_mapping(mapping_desc):
        result = {}
        for key, xform in mapping_desc.items():
            if isinstance(xform, str):
                result[key] = get_value(xform)
            elif isinstance(xform, Mapping):
                if "key" in xform:
                    value = get_value(xform["key"])
                    if value is not None:
                        if "xform" in xform:
                            result[key] = transform(xform["xform"], value)
                        elif "xf" in xform:
                            if isinstance(value, list):
                                transformed = [xform["xf"](v) for v in value]
                                if "f" in xform:
                                    result[key] = xform["f"](transformed)
                                else:
                                    result[key] = transformed
                            else:
                                result[key] = xform["xf"](value)
                        else:
                            result[key] = value
                else:
                    result[key] = process_mapping(xform)
            else:
                result[key] = xform
        return result
    return process_mapping(mapping_description)


def jsonload_file(file_path: pathlib.Path, mapping_description: dict):
    """Load a JSON file and transform it according to a mapping description."""
    with file_path.open('r') as file:
        data = json.load(file)
    return mapper(mapping_description, data)


class PyObject(ABC):
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
    __slots__ = ('__dict__', '__weakref__')

    def __init__(self, **data):
        for name, value in data.items():
            setattr(self, name, value)

    def __setattr__(self, name, value):
        if hasattr(self.__class__, '__annotations__') and name in self.__class__.__annotations__:
            expected_type = self.__class__.__annotations__[name]
            if not isinstance(value, expected_type):
                raise TypeError(
                    f"Expected {expected_type} for {name}, got {type(value)}")
            validator = getattr(self.__class__, f'validate_{name}', None)
            if validator:
                value = validator(self, value)  # Store the validated value
        super().__setattr__(name, value)

    @classmethod
    def create(cls, **kwargs):
        return cls(**kwargs)

    def dict(self):
        if hasattr(self.__class__, '__annotations__'):
            return {name: getattr(self, name, None) for name in self.__class__.__annotations__}
        return self.__dict__.copy()

    def __repr__(self):
        if hasattr(self.__class__, '__annotations__'):
            attrs = ', '.join(
                f"{name}={getattr(self, name, None)!r}"
                for name in self.__class__.__annotations__
            )
        else:
            attrs = ', '.join(f"{name}={value!r}" for name,
                              value in self.__dict__.items())
        return f"{self.__class__.__name__}({attrs})"

    def __str__(self):
        if hasattr(self.__class__, '__annotations__'):
            attrs = ', '.join(
                f"{name}={getattr(self, name, None)}"
                for name in self.__class__.__annotations__
            )
        else:
            attrs = ', '.join(f"{name}={value}" for name,
                              value in self.__dict__.items())
        return f"{self.__class__.__name__}({attrs})"

    def clone(self):
        return self.__class__(**self.dict())


class FileModel(BaseModel):
    file_name: str
    file_content: str

    def save(self, directory: pathlib.Path):
        """Save the file content to the specified directory."""
        target_path = directory / self.file_name
        with target_path.open('w') as file:
            file.write(self.file_content)
        return target_path


def create_model_from_file(file_path: pathlib.Path):
    """Create a FileModel instance from a file path."""
    try:
        with file_path.open('r', encoding='utf-8', errors='ignore') as file:
            content = file.read()
        model_name = file_path.stem.capitalize() + 'Model'
        model_class = type(model_name, (FileModel,), {})
        instance = model_class.create(
            file_name=file_path.name, file_content=content)
        logging.info(f"Created {model_name} from {file_path}")
        return model_name, instance
    except Exception as e:
        logging.error(f"Failed to create model from {file_path}: {e}")
        return None, None


def load_files_as_models(root_dir: pathlib.Path, file_extensions: List[str]) -> Dict[str, BaseModel]:
    """Load all files with specified extensions as models."""
    models = {}
    for ext in file_extensions:
        for file_path in root_dir.rglob(f'*{ext}'):
            if file_path.is_file():  # Double-check it's a file
                model_name, instance = create_model_from_file(file_path)
                if model_name and instance:
                    models[model_name] = instance
                    sys.modules[model_name] = instance
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
        return any(pattern in namespace for pattern in self.namespace_patterns) and \
            operation in self.allowed_operations


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
        if not self.security_context.access_policy.can_access(node.id, "read"):
            violation = f"Access denied to name: {node.id}"
            self.violations.append(violation)
            self.security_context.log_access(node.id, "read", False)
            raise PermissionError(violation)
        self.security_context.log_access(node.id, "read", True)
        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            if not self.security_context.access_policy.can_access(node.func.id, "execute"):
                violation = f"Access denied to function: {node.func.id}"
                self.violations.append(violation)
                self.security_context.log_access(
                    node.func.id, "execute", False)
                raise PermissionError(violation)
            self.security_context.log_access(node.func.id, "execute", True)
        self.generic_visit(node)


class FrameModel(Generic[T, V, C], ABC):
    def init(self, start_delimiter: str = "<<CONTENT>>", end_delimiter: str = "<<END_CONTENT>>") -> None:
        self.start_delimiter = start_delimiter
        self.end_delimiter = end_delimiter

    @abstractmethod
    def to_bytes(self) -> bytes:
        pass

    @abstractmethod
    def parse_content(self, raw_content: str) -> str:
        pass

    def validate_content(self, content: str) -> bool:
        return content.startswith(self.start_delimiter) and content.endswith(self.end_delimiter)


@dataclass
class CustomDelimiterFrame(FrameModel):
    content: str

    def __post_init__(self):
        self.init()

    def to_bytes(self) -> bytes:
        return self.content.encode()

    def parse_content(self, raw_content: str) -> str:
        start_index = raw_content.find(self.start_delimiter)
        end_index = raw_content.rfind(self.end_delimiter)
        if start_index == -1 or end_index == -1 or start_index >= end_index:
            raise ValueError(
                "Invalid content format: Missing or mismatched delimiters.")
        return raw_content[start_index + len(self.start_delimiter):end_index]


def register_models(models: Dict[str, BaseModel], target_globals=None):
    """Register models in the specified globals dictionary or the caller's globals."""
    if target_globals is None:
        import inspect
        frame = inspect.currentframe().f_back
        target_globals = frame.f_globals
    for model_name, instance in models.items():
        target_globals[model_name] = instance
        logging.info(f"Registered {model_name} in the global namespace")


def runtime(root_dir: pathlib.Path, extensions=None):
    """Initialize the runtime with models from the specified directory."""
    if extensions is None:
        extensions = ['.md', '.txt']
    file_models = load_files_as_models(root_dir, extensions)
    register_models(file_models)
    return file_models


class RuntimeNamespace:
    """Manages hierarchical runtime namespaces with security controls."""

    def __init__(self, name: str = "root", parent: Optional['RuntimeNamespace'] = None):
        self._name = name
        self._parent = parent
        self._children: Dict[str, 'RuntimeNamespace'] = {}
        self._content = SimpleNamespace()
        self._security_context = None
        self.available_modules = {}
        self.frame_model: Optional[FrameModel] = None

    @property
    def full_path(self) -> str:
        return f"{self._parent.full_path}.{self._name}" if self._parent else self._name

    def add_child(self, name: str) -> 'RuntimeNamespace':
        """Add a child namespace."""
        if not isinstance(name, str) or not name.isidentifier():
            raise ValueError(f"Invalid namespace name: {name}")
        child = RuntimeNamespace(name, self)
        self._children[name] = child
        return child

    def get_child(self, path: str) -> Optional['RuntimeNamespace']:
        """Get a child namespace by path."""
        if not path:
            return self
        parts = path.split(".", 1)
        first_part = parts[0]
        if first_part not in self._children:
            return None
        child = self._children[first_part]
        if len(parts) == 1:
            return child
        return child.get_child(parts[1])

    def set_security_context(self, context: SecurityContext):
        """Set the security context for this namespace."""
        self._security_context = context

    def get_attribute(self, name: str, default=None):
        """Get an attribute with security validation."""
        if self._security_context:
            can_access = self._security_context.access_policy.can_access(
                f"{self.full_path}.{name}", "read"
            )
            self._security_context.log_access(
                f"{self.full_path}.{name}", "read", can_access)
            if not can_access:
                raise PermissionError(f"Access denied to attribute: {name}")
        return getattr(self._content, name, default)

    def set_attribute(self, name: str, value: Any):
        """Set an attribute with security validation."""
        if self._security_context:
            can_access = self._security_context.access_policy.can_access(
                f"{self.full_path}.{name}", "write"
            )
            self._security_context.log_access(
                f"{self.full_path}.{name}", "write", can_access)
            if not can_access:
                raise PermissionError(
                    f"Access denied to modify attribute: {name}")
        setattr(self._content, name, value)

    def set_frame_model(self, frame_model: Generic(FrameModel)) -> None:
        self.frame_model = frame_model

    def embed_content(self, raw_content: str) -> None:
        if not self.frame_model:
            raise ValueError("No FrameModel configured for this namespace.")
        if not self.frame_model.validate_content(raw_content):
            raise ValueError(
                "Content validation failed. Invalid delimiters or format.")
        self._content.embedded_data = self.frame_model.parse_content(
            raw_content)

    def retrieve_content(self) -> str:
        if hasattr(self._content, "embedded_data"):
            return self.frame_model.start_delimiter + self._content.embedded_data + self.frame_model.end_delimiter
        raise ValueError("No content embedded in this namespace.")
