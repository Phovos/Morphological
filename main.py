from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Union, Generic, TypeVar, Mapping, Optional
import hashlib
import inspect
import ast
import logging
import json
import pathlib
import sys
from datetime import datetime
from enum import Enum
from functools import wraps
from types import SimpleNamespace

#------------------------------------------------------------------------------
# BaseModel (no-copy immutable dataclasses for data models)
#------------------------------------------------------------------------------
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
                raise TypeError(f"Expected {expected_type} for {name}, got {type(value)}")
            
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
            attrs = ', '.join(f"{name}={value!r}" for name, value in self.__dict__.items())
        return f"{self.__class__.__name__}({attrs})"
        
    def __str__(self):
        if hasattr(self.__class__, '__annotations__'):
            attrs = ', '.join(
                f"{name}={getattr(self, name, None)}" 
                for name in self.__class__.__annotations__
            )
        else:
            attrs = ', '.join(f"{name}={value}" for name, value in self.__dict__.items())
        return f"{self.__class__.__name__}({attrs})"
        
    def clone(self):
        return self.__class__(**self.dict())


def validate(validator: Callable[[Any], Any]):
    """
    Decorator for validation functions that allows returning the validated value.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, value):
            return validator(value)
        return wrapper
    return decorator

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
        instance = model_class.create(file_name=file_path.name, file_content=content)
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
                self.security_context.log_access(node.func.id, "execute", False)
                raise PermissionError(violation)
            self.security_context.log_access(node.func.id, "execute", True)
        self.generic_visit(node)
#------------------------------------------------------------------------------
# Runtime Namespace Management
#------------------------------------------------------------------------------
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
        self._children = {}
        self._content = SimpleNamespace()
        self._security_context = None
        self.available_modules = {}
    
    @property
    def full_path(self) -> str:
        """Get the full path of this namespace."""
        if self._parent:
            return f"{self._parent.full_path}.{self._name}"
        return self._name
    
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
            self._security_context.log_access(f"{self.full_path}.{name}", "read", can_access)
            if not can_access:
                raise PermissionError(f"Access denied to attribute: {name}")
        
        return getattr(self._content, name, default)
    
    def set_attribute(self, name: str, value: Any):
        """Set an attribute with security validation."""
        if self._security_context:
            can_access = self._security_context.access_policy.can_access(
                f"{self.full_path}.{name}", "write"
            )
            self._security_context.log_access(f"{self.full_path}.{name}", "write", can_access)
            if not can_access:
                raise PermissionError(f"Access denied to modify attribute: {name}")
        
        setattr(self._content, name, value)
#------------------------------------------------------------------------------
# Homoiconic-Atomic-logic
#------------------------------------------------------------------------------
"""
This module implements a runtime system inspired by homoiconic principles and S-expression logic,
where source code is treated as both data and executable instructions. The system dynamically
composes, evaluates, and reflects on code configurations at runtime, enabling non-deterministic
behavior akin to quantum mechanics' wave function collapse.

Key Features:
1. **Dynamic Composition**: Functions and values are nested and evaluated like S-expressions,
   allowing runtime code generation and modification.
2. **Reflection**: The runtime can analyze and modify its own structure, adapting to changing
   states and inputs.
3. **Non-Determinism**: The system transitions between configurations based on input and
   structural constraints, simulating multi-threaded or quantum-like behavior.
4. **State Preservation**: Maintains consistency across configurations, ensuring predictable
   execution paths.

The core abstraction is the `__Atom__` class, which encapsulates data, logic, and metadata.
Instances of `__Atom__` can be nested, manipulated, and executed dynamically, forming a
self-modifying runtime environment. This approach synthesizes static and dynamic paradigms,
drawing inspiration from lambda calculus, LISP, and modern programming techniques.

Ultimately, this model enables the creation of a "runtime of runtimes," where source code is
rewritten dynamically, limited only by hardware and operating system constraints.
"""

@dataclass
class GrammarRule:
    """
    Represents a single grammar rule in a context-free grammar.
    """
    lhs: str
    rhs: List[Union[str, 'GrammarRule']]

    def __repr__(self) -> str:
        rhs_str = " ".join(str(elem) for elem in self.rhs)
        return f"{self.lhs} -> {rhs_str}"


class CustomEncoder(json.JSONEncoder):
    """
    Custom JSON encoder to handle non-serializable types.
    """
    def default(self, obj: Any) -> Any:
        if isinstance(obj, set):
            return list(obj)  # Convert sets to lists
        elif hasattr(obj, '__dict__'):
            return obj.__dict__  # Serialize objects with __dict__
        elif callable(obj):
            return f"<function {obj.__name__}>"  # Represent functions as strings
        return super().default(obj)


@dataclass
class __Atom__(Generic[T, V, C]):
    """
    Abstract Base Class for all __Atom__ types.
    
    __Atom__ is the smallest unit of data or executable code, and this interface
    defines common operations such as encoding, decoding, execution, and conversion
    to data classes.
    """
    value: Union[T, V, C] = field(default=None)
    type: Union[str, type] = field(default=None)
    grammar_rules: List[GrammarRule] = field(default_factory=list)
    id: str = field(init=False)
    metadata: Dict[str, Any] = field(default_factory=dict)
    children: List[__Atom__] = field(default_factory=list)
    hash: str = field(init=False)
    tag: str = field(default="")

    def __post_init__(self):
        # Generate a unique ID and hash based on the value
        self.id = f"__Atom__-{id(self)}"
        self.hash = hashlib.sha256(repr(self.value).encode()).hexdigest()

        # Define logical operators as part of the case base
        self.case_base = {
            "⊤": lambda x, _: x,
            "⊥": lambda _, y: y,
            "¬": lambda a: not a,
            "∧": lambda a, b: a and b,
            "∨": lambda a, b: a or b,
            "→": lambda a, b: (not a) or b,
            "↔": lambda a, b: (a and b) or (not a and not b),
        }

    def process_attributes(self, mapping_description: Dict[str, Any], input_data: Dict[str, Any]) -> None:
        """
        Use the `mapper` function to process input data and map it to attributes.
        """
        mapped_data = mapper(mapping_description, input_data)
        for key, value in mapped_data.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def encode(self) -> bytes:
        """
        Encode the __Atom__ instance into a JSON-serialized byte string using a custom encoder.
        """
        return json.dumps({"id": self.id, "attributes": self.__dict__}, cls=CustomEncoder).encode()

    @classmethod
    def decode(cls, data: bytes) -> __Atom__:
        """
        Decode a JSON-serialized byte string back into an __Atom__ instance.
        """
        decoded_data = json.loads(data.decode())
        return cls(**decoded_data["attributes"])

    def introspect(self) -> str:
        """
        Reflect on its own code structure via AST.
        If the class is dynamically generated, fallback to a predefined template.
        """
        try:
            # Attempt to retrieve the source code of the class
            source = inspect.getsource(self.__class__)
            return ast.dump(ast.parse(source))
        except (OSError, IndentationError):
            # Fallback to a predefined template if source retrieval fails
            fallback_source = f"""
class {self.__class__.__name__}(__Atom__):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
"""
            return ast.dump(ast.parse(fallback_source))

    def __repr__(self) -> str:
        return f"{self.value} : {self.type}"

    def __str__(self) -> str:
        return str(self.value)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, __Atom__) and self.hash == other.hash

    def __hash__(self) -> int:
        return int(self.hash, 16)

    def __getitem__(self, key):
        return self.value[key]

    def __setitem__(self, key, value):
        self.value[key] = value

    def __delitem__(self, key):
        del self.value[key]

    def __len__(self):
        return len(self.value)

    def __iter__(self):
        return iter(self.value)

    def __contains__(self, item):
        return item in self.value

    def __call__(self, *args, **kwargs):
        return self.value(*args, **kwargs)

    def __bytes__(self) -> bytes:
        return bytes(self.value)

    @property
    def memory_view(self) -> memoryview:
        if isinstance(self.value, (bytes, bytearray)):
            return memoryview(self.value)
        raise TypeError("Unsupported type for memoryview")

    def __buffer__(self, flags: int) -> memoryview:
        return memoryview(self.value)

    async def send_message(self, message: Any, ttl: int = 3) -> None:
        """
        Send a message to subscribers with a time-to-live (TTL).
        """
        if ttl <= 0:
            logging.warning(f"Message TTL expired for Atom {self.id}")
            return
        logging.info(f"__Atom__ {self.id} processing received message: {message} with TTL {ttl}")
        await self.send_message(message, ttl - 1)

    def subscribe(self, atom: __Atom__) -> None:
        """
        Subscribe another __Atom__ to this one.
        """
        self.children.append(atom)
        logging.info(f"__Atom__ {self.id} subscribed to {atom.id}")

    def unsubscribe(self, atom: __Atom__) -> None:
        """
        Unsubscribe another __Atom__ from this one.
        """
        self.children.remove(atom)
        logging.info(f"__Atom__ {self.id} unsubscribed from {atom.id}")

def frozen(cls):
    """
    Decorator to make a class immutable after initialization.
    """
    original_init = cls.__init__
    original_setattr = cls.__setattr__
    
    @wraps(original_init)
    def __init__(self, *args, **kwargs):
        self._initialized = False
        original_init(self, *args, **kwargs)
        self._initialized = True
    
    def __setattr__(self, name, value):
        if getattr(self, '_initialized', False) and name != '_initialized':
            raise AttributeError(f"Cannot modify frozen attribute '{name}'")
        original_setattr(self, name, value)
        
    cls.__init__ = __init__
    cls.__setattr__ = __setattr__
    return cls

@frozen
class Module(BaseModel):
    file_path: pathlib.Path
    module_name: str
    
    @validate(lambda x: x if x.endswith('.py') else None)
    def validate_file_path(self, value):
        return value
    
    @validate(lambda x: x if x.isidentifier() else None)
    def validate_module_name(self, value):
        return value


def __Decorator__(cls):
    """
    Decorator to enhance a class with __Atom__ behavior.
    """
    class EnhancedAtom(__Atom__, cls):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

    return EnhancedAtom
def main():
    """Access enhanced __Atom__ features"""
    @__Decorator__
    class MyCustomClass:
        def __init__(self, value: int):
            self.value = value
    custom_atom = MyCustomClass(value=69)
    print(custom_atom.introspect())
    print(custom_atom.encode())
    # print(custom_atom.memory_view)
    custom_atom.subscribe(custom_atom)
    custom_atom.send_message("Ayylmao")
    custom_atom.unsubscribe(custom_atom)
    # print(custom_atom.decode(custom_atom.encode()))

if __name__ == "__main__":
    main()