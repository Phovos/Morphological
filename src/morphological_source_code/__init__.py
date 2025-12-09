# > © 2024-2025 Phovos https://github.com/Phovos/Morphologic BSD-3 & CC ND
# > © 2023-2025 Moonlapsed https://github.com/MOONLAPSED/Cognosis
"""
Quinic Statistical Dynamics (QSD) centers around three fundamental pillars:

**Probabilistic Runtimes:**

> Each runtime is a self-contained probabilistic entity capable of observing, acting, and quining itself into source code. This allows for recursive instantiation and coherent state resolution through statistical dynamics.

**Temporal Entanglement:**

> Information is entangled across runtime abstractions, creating a "network" of states that evolve and resolve over time. This entanglement captures the essence of quantum-like behavior in a deterministic computational framework.

**Distributed Statistical Coherence:**

> The resolution of states emerges through distributed interactions between runtimes. Statistical coherence is achieved as each runtime contributes to a shared, probabilistic resolution mechanism.

**Architectural Summary; Runtimes as Quanta:**

> Runtimes operate as quantum-like entities within the system. They observe events probabilistically, record outcomes, and quine themselves into new instances. This recursive behavior forms the foundation of QSD.

> Quined source code maintains entanglement metadata, ensuring that all instances share a common probabilistic lineage. This enables coherent interactions and state resolution across distributed runtimes.

> The distributed system functions as a field of interacting runtimes, where statistical coherence arises naturally from the aggregation of individual outcomes. This mimics the behavior of quantum fields in physical systems.

**Lazy/Eventual Consistency (CAP Thoerem):**

Inter-runtime communication adheres to an "AP" model internally (intensive/unitary) and an eventual consistency model externally (extensive, radiative). This allows the system to balance synchronicity with scalability.

The idea of "runtime as quanta" transcends the diminutive associations one might instinctively draw when imagining quantum-scale simulations in software. Unlike subatomic particles, which are bound by strict physical laws and limited degrees of freedom, a runtime in the context of our speculative architecture is hierarchical and associative. This allows us to exploit the 'structure' of informatics and emergent-reality and the ontology of being --- that representing intensive and extensive thermodynamic character: |Φ| --- by hacking-into this ontology using quinic behavior and focusing on the computation as the core object,  not the datastructure,  the data,  or the state/logic,  instead focusing on the holistic state/logic duality of 'collapsed' runtimes creating 'entangled' (quinic) source code; for purposes of multi-instantiation in a distributed systematic probabilistic architecture.

This hierarchical richness inherently provides a scaffold for representing intricate realities, from probabilistic field theories to distributed decision-making systems. However, this framework does not merely simulate quantum phenomena but reinterprets them within a meta-reality that operates above and beyond their foundational constraints. It is this capacity for layered abstraction and emergent behavior that makes "runtime as quanta" a viable and transformative concept for the simulation of any conceivable reality. "Quinic-behavior" and probabilistic action, this architecture aims to quantize classical hardware for agentic 'AGI' on any/all plaforms/scales.

____
### CAP Theorem Overview
Consistency (C): Every read receives the most recent write or an error.
Availability (A): Every request receives a (non-error) response, without the
guarantee that it contains the most recent write.
Partition Tolerance (P): The system continues to operate despite an
arbitrary number of messages being dropped or delayed by the network.
___
Decorator State Space
Let Δ = (T, Φ, O) where:
- T: Temporal lattice of computational states
- Φ: Method Resolution Order functor
- O: Observable operations
class TemporalMRO:
    # This maps to quantum space Ω = (H, ρ, U) via:- T → H (Hilbert space)
    - Φ → ρ (density operator)
    - O → U (unitary evolution)

    def __init__(self, T, Φ, O):
        # T maps to H (Hilbert space)
        # Φ maps to ρ (density operator)
        # O maps to U (unitary evolution)
        self.T = T
        self.Φ = Φ
        self.O = O
___
1. **Linearization**:

    - In Python, MRO is determined by **C3 linearization** (also called C3 superclass linearization), which creates a linear order of classes in a multiple inheritance tree while preserving the hierarchy. This is much like a **partially ordered set**, where Python resolves methods by following a predictable, deterministic path through the hierarchy.
    - The MRO in Python respects class precedence, preserving the relationship between the superclass and subclass methods.
2. **Poset Structure**:

    - If you think of each class as a node, inheritance as directed edges, and the MRO as a linear path through the directed acyclic graph (DAG) of classes, Python’s MRO creates a directed path. This ensures that each class’s methods are called only once and in the correct sequence, even in complex hierarchies.

### `super()` as a Traversal Mechanism in the MRO Graph

When you use `super()`, you’re not just calling the “parent” class; instead, you're invoking the **next class in the MRO**, following the hierarchy Python calculated. This makes `super()` incredibly flexible and avoids hardcoding which superclass to call. It operates in a **context-aware way**, adapting based on the MRO, which is why it’s sometimes described as a “contextual `super()`.”
____
"""
# (Windows) Platform and app (threading, tracing)
try:
    IS_WINDOWS: bool = os.name == "nt"
    if IS_WINDOWS:
        from ctypes import windll, wintypes
        from ctypes.wintypes import HANDLE, DWORD, LPWSTR, LPVOID, BOOL
        from pathlib import PureWindowsPath
        global localSite
        localSite = pathlib.PureWindowsPath(site.getusersitepackages())
except:
    sys.exit('Windows platform-only.')
#------------------------------------------------------------------------------
# Security
#------------------------------------------------------------------------------
AccessLevel = Enum('AccessLevel', 'READ WRITE EXECUTE ADMIN USER')
@dataclass
class AccessPolicy:
    """Defines access control policies for runtime operations."""
    level: AccessLevel
    namespace_patterns: list[str] = field(default_factory=list)
    allowed_operations: list[str] = field(default_factory=list)
    def can_access(self, namespace: str, operation: str) -> bool:
        return any(pattern in namespace for pattern in self.namespace_patterns) and \
               operation in self.allowed_operations

class SecurityContext:
    """Manages security context and audit logging for runtime operations."""
    def __init__(self, user_id: str, access_policy: AccessPolicy):
        self.user_id = user_id
        self.access_policy = access_policy
        self._audit_log = []
    def log_access(self, namespace: str, operation: str, success: bool):
        self._audit_log.append({
            "user_id": self.user_id,
            "namespace": namespace,
            "operation": operation,
            "success": success,
            "timestamp": datetime.now().timestamp()
        })

class SecurityValidator(ast.NodeVisitor):
    """Validates AST nodes against security policies."""
    def __init__(self, security_context: SecurityContext):
        self.security_context = security_context
    def visit_Name(self, node):
        if not self.security_context.access_policy.can_access(node.id, "read"):
            raise PermissionError(f"Access denied to name: {node.id}")
        self.generic_visit(node)
    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            if not self.security_context.access_policy.can_access(node.func.id, "execute"):
                raise PermissionError(f"Access denied to function: {node.func.id}")
        self.generic_visit(node)

#------------------------------------------------------------------------------
# Runtime State Management
#------------------------------------------------------------------------------
def register_models(models: Dict[str, BaseModel]):
    for model_name, instance in models.items():
        globals()[model_name] = instance
        logging.info(f"Registered {model_name} in the global namespace")

def runtime(root_dir: pathlib.Path):
    file_models = load_files_as_models(root_dir, ['.md', '.txt'])
    register_models(file_models)

class MemoryTraceLevel(Enum):
    """Granularity levels for memory tracing."""
    BASIC = auto()
    DETAILED = auto()   # Include stack traces
    FULL = auto()       # Include object references

class _ColorFormatter(logging.Formatter):
    """Colour console output for Windows terminal."""
    _COLOURS = {
        logging.DEBUG: "\033[34m",    # blue
        logging.INFO: "\033[32m",     # green
        logging.WARNING: "\033[33m",  # yellow
        logging.ERROR: "\033[31m",    # red
        logging.CRITICAL: "\033[41m", # red background
    }
    _RESET = "\033[0m"
    def format(self, record: logging.LogRecord) -> str:
        ts = datetime.datetime.fromtimestamp(record.created).strftime("%Y-%m-%d %H:%M:%S")
        colour = self._COLOURS.get(record.levelno, "")
        level = f"{record.levelname:<8}"
        where = f"({record.filename}:{record.lineno})"
        msg = record.getMessage()
        return f"{colour}{ts} - {level} - {msg} {where}{self._RESET}"

class _CorrelationAdapter(logging.LoggerAdapter):
    """Adds a correlation id to every message."""
    def process(self, msg: str, kwargs: Any) -> tuple[str, Any]:
        cid = self.extra.get("cid", "SYSTEM")
        return f"[{cid}] {msg}", kwargs

class CustomFormatter(logging.Formatter):
    """Custom formatter for colored console output."""
    
    COLORS = {
        'grey': "\x1b[38;20m",
        'yellow': "\x1b[33;20m",
        'red': "\x1b[31;20m",
        'bold_red': "\x1b[31;1m",
        'green': "\x1b[32;20m",
        'reset': "\x1b[0m"
    }
    FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    FORMATS = {
        logging.DEBUG: COLORS['grey'] + FORMAT + COLORS['reset'],
        logging.INFO: COLORS['green'] + FORMAT + COLORS['reset'],
        logging.WARNING: COLORS['yellow'] + FORMAT + COLORS['reset'],
        logging.ERROR: COLORS['red'] + FORMAT + COLORS['reset'],
        logging.CRITICAL: COLORS['bold_red'] + FORMAT + COLORS['reset']
    }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.log_queue = Queue()
        self.log_thread = threading.Thread(target=self._log_thread_func, daemon=True)
        self.log_thread.start()
    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno, self.FORMAT)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
    def _log_thread_func(self):
        while True:
            try:
                record = self.log_queue.get()
                if record is None:
                    break
                super().handle(record)
            except Exception:
                import traceback
                print("Error in log thread:", file=sys.stderr)
                traceback.print_exc()
    def emit(self, record):
        self.log_queue.put(record)
    def close(self):
        self.log_queue.put(None)
        self.log_thread.join()

class AdminLogger(logging.LoggerAdapter):
    """Logger adapter for administrative logging."""
    def __init__(self, logger, extra=None):
        super().__init__(logger, extra or {})
    def process(self, msg, kwargs):
        return f"{self.extra.get('name', 'Admin')}: {msg}", kwargs

logger = AdminLogger(logging.getLogger(__name__))

def setup_logger(
    name: str = __name__,
    *,
    level: int = logging.INFO,
    console: bool = True,
    file_log: str | None = None,
) -> logging.Logger:
    """
    Configure and return a logger.
    :param name: logger name.
    :param level: logging level.
    :param console: add coloured console handler.
    :param file_log: path for a rotating file handler (10 MB × 5 kept).
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.handlers.clear()  # idempotent setup
    if console:
        ch = logging.StreamHandler()
        ch.setFormatter(_ColorFormatter())
        logger.addHandler(ch)
    if file_log:
        fh = logging.handlers.RotatingFileHandler(
            file_log, maxBytes=10 * 1024 * 1024, backupCount=5, encoding="utf-8"
        )
        fh.setFormatter(
            logging.Formatter(
                "%(asctime)s [%(levelname)s] (%(filename)s:%(lineno)d) %(message)s"
            )
        )
        logger.addHandler(fh)
    return logger

class RuntimeNamespace:
    """Manages hierarchical runtime namespaces with security controls."""
    def __init__(self, name: str = "root", parent: Optional['RuntimeNamespace'] = None):
        self._name = name
        self._parent = parent
        self._children: Dict[str, 'RuntimeNamespace'] = {}
        self._content = SimpleNamespace()
        self._security_context: Optional[SecurityContext] = None
        self.available_modules: Dict[str, Any] = {}
    @property
    def full_path(self) -> str:
        if self._parent:
            return f"{self._parent.full_path}.{self._name}"
        return self._name
    def add_child(self, name: str) -> 'RuntimeNamespace':
        child = RuntimeNamespace(name, self)
        self._children[name] = child
        return child
    def get_child(self, path: str) -> Optional['RuntimeNamespace']:
        parts = path.split(".", 1)
        if len(parts) == 1:
            return self._children.get(parts[0])
        child = self._children.get(parts[0])
        return child.get_child(parts[1]) if child and len(parts) > 1 else None

def get_logger(name: str = __name__, cid: str = "SYSTEM") -> _CorrelationAdapter:
    """Return a correlation-id-aware logger."""
    return _CorrelationAdapter(logging.getLogger(name), {"cid": cid})

def log(level=logging.INFO):
    """
    Decorator that logs function calls, works with both sync and async functions.
    """
    def decorator(func):
        if asyncio.iscoroutinefunction(func):
            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs):
                logger.log(level, f"Executing {func.__name__} with args: {args}, kwargs: {kwargs}")
                try:
                    result = await func(*args, **kwargs)
                    logger.log(level, f"Completed {func.__name__} with result: {result}")
                    return result
                except Exception as e:
                    logger.exception(f"Error in {func.__name__}: {e}")
                    raise
            return async_wrapper
        else:
            @functools.wraps(func)
            def sync_wrapper(*args, **kwargs):
                logger.log(level, f"Executing {func.__name__} with args: {args}, kwargs: {kwargs}")
                try:
                    result = func(*args, **kwargs)
                    logger.log(level, f"Completed {func.__name__} with result: {result}")
                    return result
                except Exception as e:
                    logger.exception(f"Error in {func.__name__}: {e}")
                    raise
            return sync_wrapper
    return decorator


def measure_time(func):
    """
    Decorator that measures execution time, works with both sync and async functions.
    Uses time.perf_counter() for high-resolution timing.
    """
    if asyncio.iscoroutinefunction(func):
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            start = time.perf_counter()
            try:
                result = await func(*args, **kwargs)
            finally:
                end = time.perf_counter()
                logger.info(f"{func.__name__} executed in {end - start:.4f} seconds")
            return result
        return async_wrapper
    else:
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            start = time.perf_counter()
            try:
                result = func(*args, **kwargs)
            finally:
                end = time.perf_counter()
                logger.info(f"{func.__name__} executed in {end - start:.4f} seconds")
            return result
        return sync_wrapper

# MSC Framework Constants and Definitions
MSC_REGISTRY: Dict[str, Set[str]] = {'classes': set(), 'functions': set()}

class MorphodynamicCollapse(Exception):
    """Raised when a morph object destabilizes under thermal pressure."""
    pass

@dataclass
class MorphSpec:
    """Blueprint for morphological classes."""
    entropy: float
    trigger_threshold: float
    memory: dict
    signature: str

def hash_state(value: Any) -> int:
    """Hash a state value in a deterministic way"""
    if isinstance(value, int):
        return value * 2654435761 % 2**32  # Knuth's multiplicative hash
    elif isinstance(value, str):
        return sum(ord(c) * (31**i) for i, c in enumerate(value)) % 2**32
    else:
        return hash(str(value)) % 2**32

def morphology(source_model: Type) -> Callable[[Type], Type]:
    """Decorator: register & validate a class against a MorphSpec."""
    def decorator(target: Type) -> Type:
        target.__msc_source__ = source_model
        # Ensure target has all annotated fields from source_model
        for field_name in getattr(source_model, '__annotations__', {}):
            if field_name not in getattr(target, '__annotations__', {}):
                raise TypeError(f"{target.__name__} missing field '{field_name}'")
        MSC_REGISTRY['classes'].add(target.__name__)
        return target
    return decorator

# Functional Programming Patterns - Transducers
def mapper(mapping_description: Mapping[str, Any], input_data: Dict[str, Any]):
    def transform(xform, value):
        if callable(xform):
            return xform(value)
        elif isinstance(xform, Mapping):
            return {k: transform(v, value) for k, v in xform.items()}
        else:
            raise ValueError(f"Invalid transformation type: {type(xform)}. Expected callable or Mapping.")
    
    def get_value(key):
        if isinstance(key, str) and key.startswith(":"):
            return input_data.get(key[1:])
        return input_data.get(key)
    
    def process_mapping(mapping_description):
        result = {}
        for key, xform in mapping_description.items():
            if isinstance(xform, str):
                value = get_value(xform)
                result[key] = value
            elif isinstance(xform, Mapping):
                if "key" in xform:
                    value = get_value(xform["key"])
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

class Missing:
    """Marker class to indicate a missing value."""
    pass

class Reduced:
    """Sentinel class to signal early termination during reduction."""
    def __init__(self, val: Any):
        self.val = val

def ensure_reduced(x: Any) -> Union[Any, Reduced]:
    """Ensure the value is wrapped in a Reduced sentinel."""
    return x if isinstance(x, Reduced) else Reduced(x)

def unreduced(x: Any) -> Any:
    """Unwrap a Reduced value or return the value itself."""
    return x.val if isinstance(x, Reduced) else x

def reduce(function: Callable[[Any, T], Any], iterable: Iterable[T], initializer: Any = Missing) -> Any:
    """A custom reduce implementation that supports early termination with Reduced."""
    if initializer is Missing:
        if callable(function):
            accum_value = function()
        else:
            raise TypeError("No initializer provided and function is not callable.")
    else:
        accum_value = initializer
    
    for x in iterable:
        accum_value = function(accum_value, x)
        if isinstance(accum_value, Reduced):
            return accum_value.val
    return accum_value

class Transducer(ABC):
    """Base class for defining transducers."""
    @abstractmethod
    def step(self, step_fn: Callable[[Any, T], Any]) -> Callable[[Any, T], Any]:
        pass

    def __call__(self, step: Callable[[Any, T], Any]) -> Callable[[Any, T], Any]:
        """The transducer's __call__ method allows it to be used as a decorator."""
        return self.step(step)

class Map(Transducer):
    """Transducer for mapping elements with a function."""
    def __init__(self, f: Callable[[T], V]):
        self.f = f

    def step(self, step_fn: Callable[[Any, T], Any]) -> Callable[[Any, T], Any]:
        def new_step(r: Any, x: T):
            return step_fn(r, self.f(x))
        return new_step

class Filter(Transducer):
    """Transducer for filtering elements based on a predicate."""
    def __init__(self, pred: Callable[[T], bool]):
        self.pred = pred

    def step(self, step_fn: Callable[[Any, T], Any]) -> Callable[[Any, T], Any]:
        def new_step(r: Any, x: T):
            return step_fn(r, x) if self.pred(x) else r
        return new_step

class Cat(Transducer):
    """Transducer for flattening nested collections."""
    def step(self, step_fn: Callable[[Any, T], Any]) -> Callable[[Any, T], Any]:
        def new_step(r: Any, x: Any):
            if not hasattr(x, '__iter__'):
                raise TypeError(f"Expected iterable, got {type(x)} with value {x}")
            result = r
            for item in x:
                result = step_fn(result, item)
                if isinstance(result, Reduced):
                    return result
            return result
        return new_step

def compose(*fns: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """Compose functions such that the rightmost function is applied first."""
    return functools.reduce(lambda f, g: lambda x: f(g(x)), fns)

def transduce(xform: Transducer, f: Callable[[Any, T], Any], start: Any, coll: Iterable[T]) -> Any:
    """Apply a transducer to a collection with an initial value."""
    if not isinstance(coll, Iterable):
        raise TypeError("Expected an iterable collection.")
    reducer = xform(f)
    return reduce(reducer, coll, start)

def mapcat(f: Callable[[T], Iterable[V]]) -> Transducer:
    """Map then flatten results into one collection."""
    return compose(Map(f), Cat())

def into(target: Union[list, set], xducer: Transducer, coll: Iterable[T]) -> Any:
    """Apply transducer and collect results into a target container."""
    def append(r: Any, x: Any):
        if hasattr(r, 'append'):
            r.append(x)
        elif hasattr(r, 'add'):
            r.add(x)
        return r
    return transduce(xducer, append, target, coll)

@dataclass
class MorphicComplex:
    real: float
    imag: float

    def conjugate(self) -> 'MorphicComplex':
        return MorphicComplex(self.real, -self.imag)

    def __add__(self, other: 'MorphicComplex') -> 'MorphicComplex':
        if not isinstance(other, MorphicComplex):
            raise TypeError(f"Unsupported operand type(s) for +: 'MorphicComplex' and '{type(other)}'")
        return MorphicComplex(self.real + other.real, self.imag + other.imag)

    def __mul__(self, other: 'MorphicComplex') -> 'MorphicComplex':
        if not isinstance(other, MorphicComplex):
            raise TypeError(f"Unsupported operand type(s) for *: 'MorphicComplex' and '{type(other)}'")
        return MorphicComplex(
            self.real * other.real - self.imag * other.imag,
            self.real * other.imag + self.imag * other.real
        )

    def __eq__(self, other: 'MorphicComplex') -> bool:
        return isinstance(other, MorphicComplex) and self.real == other.real and self.imag == other.imag

    def __repr__(self) -> str:
        if self.imag == 0:
            return f"{self.real}"
        sign = "+" if self.imag >= 0 else ""
        return f"{self.real}{sign}{self.imag}j"

def format_complex_matrix(matrix: List[List[complex]], precision: int = 3) -> str:
    """Helper function to format complex matrices for printing."""
    result = []
    for row in matrix:
        formatted_row = []
        for elem in row:
            if not isinstance(elem, complex):
                raise ValueError(f"Expected complex number, got {type(elem)}.")
            real = round(elem.real, precision)
            imag = round(elem.imag, precision)
            if abs(imag) < 1e-10:
                formatted_row.append(f"{real:6.3f}")
            else:
                formatted_row.append(f"{real:6.3f}{'+' if imag >= 0 else ''}{imag:6.3f}j")
        result.append("[" + ", ".join(formatted_row) + "]")
    return "[\n " + "\n ".join(result) + "\n]"

def _matches_type(value: Any, tp: Any) -> bool:
    """True if `value` conforms to the (possibly generic) type `tp`."""
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
        if origin is dict and len(args) >= 2:
            kt, vt = args[0], args[1]
            return all(_matches_type(k, kt) and _matches_type(v, vt) for k, v in value.items())
        return True
    return isinstance(value, tp)

def _coerce(raw: Any, tp: Any) -> Any:
    """Turn raw JSON into the correct nested structure."""
    if tp is Any:
        return raw
    origin = get_origin(tp)
    # Handle Union types (including Optional)
    if origin is Union:
        args = get_args(tp)
        # Try each type in the union
        for arg_type in args:
            if arg_type is type(None) and raw is None:
                return None
            try:
                return _coerce(raw, arg_type)
            except (TypeError, ValueError):
                continue
        raise TypeError(f"Cannot coerce {raw!r} to any type in {tp}")
    # Handle generic types
    if origin is list:
        if not isinstance(raw, list):
            raise TypeError(f"Expected list, got {type(raw).__name__}")
        elem_tp = get_args(tp)[0]
        return [_coerce(item, elem_tp) for item in raw]
    if origin is dict:
        if not isinstance(raw, dict):
            raise TypeError(f"Expected dict, got {type(raw).__name__}")
        args = get_args(tp)
        if len(args) >= 2:
            kt, vt = args[0], args[1]
            return {_coerce(k, kt): _coerce(v, vt) for k, v in raw.items()}
        return raw
    # Handle BaseModel subclasses
    if inspect.isclass(tp) and issubclass(tp, BaseModel):
        if isinstance(raw, dict):
            return tp.from_dict(raw)
        elif isinstance(raw, tp):
            return raw
        raise TypeError(f"Expected dict or {tp.__name__} instance for nested model")
    # Handle common serializable types
    if tp is datetime and isinstance(raw, str):
        return datetime.fromisoformat(raw.replace('Z', '+00:00'))
    if tp is date and isinstance(raw, str):
        return date.fromisoformat(raw)
    if tp is UUID and isinstance(raw, str):
        return UUID(raw)
    if inspect.isclass(tp) and issubclass(tp, Enum) and isinstance(raw, (str, int)):
        return tp(raw)
    if tp is bytes and isinstance(raw, str):
        return base64.b64decode(raw)
    if tp is pathlib.Path and isinstance(raw, str):
        return pathlib.Path(raw)
    # Primitive types with coercion
    if tp in (int, float, str, bool):
        if isinstance(raw, tp):
            return raw
        if tp is bool and isinstance(raw, (int, str)):
            return bool(raw) if isinstance(raw, int) else raw.lower() in ('true', '1', 'yes', 'on')
        if tp in (int, float) and isinstance(raw, (int, float, str)):
            return tp(raw)
        if tp is str:
            return str(raw)
    return raw  # No conversion needed or possible

def _uncoerce(value: Any) -> Any:
    """Inverse of _coerce for serialization."""
    if isinstance(value, BaseModel):
        return value.to_dict()
    if isinstance(value, list):
        return [_uncoerce(v) for v in value]
    if isinstance(value, dict):
        return {k: _uncoerce(v) for k, v in value.items()}
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, UUID):
        return str(value)
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, bytes):
        return base64.b64encode(value).decode('ascii')
    if isinstance(value, pathlib.Path):
        return str(value)
    return value

class SerializationFormat(Enum):
    """Supported serialization formats for IPC."""
    JSON = "json"
    PICKLE = "pickle" 
    REPR = "repr"
    PYTHONC = "pythonc"  # C-Python, Python(i)C; don't name mangle

class MessageType(Enum):
    """Standard message types for RPC/networking."""
    REQUEST = "request"
    RESPONSE = "response"
    ERROR = "error"
    EVENT = "event"
    HEARTBEAT = "heartbeat"

class GlobalWindingMode(Enum):
    BINARY = "binary"
    TERNARY = "ternary"

GLOBAL_WINDING_MODE = GlobalWindingMode.TERNARY

def elevate(data: Any, cls: Type) -> object:
    """Raise a dict or object to a registered morphological class."""
    if not hasattr(cls, '__msc_source__'):
        raise TypeError(f"{cls.__name__} is not a morphological class.")
    source = cls.__msc_source__
    kwargs = {k: getattr(data, k, data.get(k)) for k in source.__annotations__}
    return cls(**kwargs)

@dataclass(frozen=True)
class WindingPair:
    w1: int
    w2: int
    mode: WindingMode = WindingMode.TERNARY
    def __post_init__(self):
        if self.mode == WindingMode.BINARY:
            if self.w1 not in (0, 1) or self.w2 not in (0, 1):
                raise ValueError("Binary winding must be 0 or 1")
        else:
            if self.w1 not in (-1, 0, 1) or self.w2 not in (-1, 0, 1):
                raise ValueError("Ternary winding must be -1,0,1")
    def tx(self, a: int, b: int) -> int:
        if a == b:
            return 0
        if a == 0:
            return b
        if b == 0:
            return a
        return 0
    def xor(self, other: "WindingPair") -> "WindingPair":
        if self.mode != other.mode:
            raise ValueError("Mode mismatch")
        if self.mode == WindingMode.BINARY:
            return WindingPair(self.w1 ^ other.w1, self.w2 ^ other.w2, mode=self.mode)
        return WindingPair(
            self.tx(self.w1, other.w1), self.tx(self.w2, other.w2), mode=self.mode
        )
    def apply_val(self, mask: "WindingPair") -> "WindingPair":
        if self.mode != mask.mode:
            raise ValueError("Mode mismatch")
        if self.mode == WindingMode.BINARY:
            return WindingPair(self.w1 ^ mask.w1, self.w2 ^ mask.w2, mode=self.mode)
        return WindingPair(
            self.w1 if mask.w1 == -1 else self.tx(self.w1, mask.w1),
            self.w2 if mask.w2 == -1 else self.tx(self.w2, mask.w2),
            mode=self.mode,
        )
    def to_state_index(self) -> int:
        if self.mode == WindingMode.BINARY:
            return (self.w1 << 1) | self.w2
        idx_map = {-1: 0, 0: 1, 1: 2}
        return (idx_map[self.w1] * 3) + idx_map[self.w2]
    def __repr__(self):
        tag = "B" if self.mode == WindingMode.BINARY else "T"
        return f"WindingPair({self.w1},{self.w2})[{tag}]"

@dataclass(frozen=True)
class Datagram:
    """Universal message format for multi-layer IPC communication."""
    msg_id: str
    msg_type: MessageType
    timestamp: float
    sender: str
    recipient: Optional[str]
    payload: Dict[str, Any]
    checksum: Optional[str] = None
    def __post_init__(self):
        # Calculate checksum if not provided
        if self.checksum is None:
            payload_str = json.dumps(self.payload, sort_keys=True, separators=(',', ':'))
            checksum = hashlib.md5(f"{self.msg_id}{self.msg_type.value}{payload_str}".encode()).hexdigest()
            object.__setattr__(self, 'checksum', checksum)
    @classmethod
    def create_request(cls, sender: str, recipient: str, method: str, params: Dict[str, Any]) -> 'Datagram':
        """Create an RPC request datagram."""
        return cls(
            msg_id=str(uuid.uuid4()),
            msg_type=MessageType.REQUEST,
            timestamp=datetime.now().timestamp(),
            sender=sender,
            recipient=recipient,
            payload={"method": method, "params": params}
        )
    @classmethod
    def create_response(cls, request_msg: 'Datagram', sender: str, result: Any) -> 'Datagram':
        """Create an RPC response datagram."""
        return cls(
            msg_id=request_msg.msg_id,  # Same ID as request
            msg_type=MessageType.RESPONSE,
            timestamp=datetime.now().timestamp(),
            sender=sender,
            recipient=request_msg.sender,
            payload={"result": _uncoerce(result)}
        )
    def to_bytes(self, format: SerializationFormat = SerializationFormat.JSON) -> bytes:
        """Serialize datagram to bytes for network transmission."""
        data = _uncoerce(self)
        if format == SerializationFormat.JSON:
            return json.dumps(data, separators=(',', ':')).encode('utf-8')
        elif format == SerializationFormat.PICKLE:
            return pickle.dumps(data)
        elif format == SerializationFormat.REPR:
            return repr(data).encode('utf-8')
        else:
            raise ValueError(f"Unsupported format: {format}")
    @classmethod
    def from_bytes(cls, data: bytes, format: SerializationFormat = SerializationFormat.JSON) -> 'Datagram':
        """Deserialize datagram from bytes."""
        if format == SerializationFormat.JSON:
            parsed = json.loads(data.decode('utf-8'))
        elif format == SerializationFormat.PICKLE:
            parsed = pickle.loads(data)
        elif format == SerializationFormat.REPR:
            parsed = eval(data.decode('utf-8'))  # Note: eval is dangerous in production
        else:
            raise ValueError(f"Unsupported format: {format}")
        # Convert msg_type back to enum
        parsed['msg_type'] = MessageType(parsed['msg_type'])
        return cls(**parsed)

#  十十十十十 DOMAIN LAYER: BaseModel + Validation Framework 十十十十十 
Validator = Callable[[Any], None]
ValidatorSet = Union[Validator, Tuple[Validator, ...]]
# === Decorator for method-based validation ===
def validate(validator: Validator):
    def decorator(fn: Callable[[Any, Any], None]):
        def wrapper(self, value):
            validator(value)
            return fn(self, value)
        return wrapper
    return decorator

@dataclass(frozen=True)
class BaseModel:
    """
    Provides Pydantic-style semantics with stdlib-only implementation.
    """
    __slots__ = ('__weakref__',)
    def _validate_model(self):
        """Override for model-level validation logic."""
        pass
    def __post_init__(self):
        """Validate all fields after initialization."""
        annotations = self.__annotations__
        for field_name, expected_type in annotations.items():
            value = getattr(self, field_name)
            # === Type validation ===
            if not self._validate_type(value, expected_type):
                raise TypeError(
                    f"{self.__class__.__name__}.{field_name}: expected {expected_type}, got {type(value).__name__}"
                )
            # === Metadata-based validation ===
            field_obj = next((f for f in fields(self) if f.name == field_name), None)
            if field_obj:
                validators = field_obj.metadata.get("validate")
                if validators:
                    for validator in (validators if isinstance(validators, (list, tuple)) else (validators,)):
                        validator(value)
            # === Decorator-based validation ===
            validator_method = getattr(self.__class__, f'validate_{field_name}', None)
            if validator_method and callable(validator_method):
                for validator in getattr(validator_method, '_validators', []):
                    validator(value)
        # === Model-level validation ===
        if hasattr(self, '_validate_model'):
            self._validate_model()
        self._validate_model()
    # === Shared Validators ===
    @staticmethod
    def must_be_str(x: Any) -> None:
        if not isinstance(x, str):
            raise ValueError(f"Expected a string, got {type(x).__name__}")
    @staticmethod
    def non_negative(x: Any) -> None:
        if not isinstance(x, int) or x < 0:
            raise ValueError(f"Expected a non-negative int, got {x!r}")
    # === Validation Helpers ===
    def is_valid(self) -> bool:
        """Check if model passes all validations without raising."""
        try:
            # Re-run post_init validation
            self.__post_init__()
            return True
        except (TypeError, ValueError):
            return False
    def validate(self) -> List[str]:
        """Return list of validation errors (empty if valid)."""
        errors = []
        annotations = self.__annotations__
        for field_name, expected_type in annotations.items():
            value = getattr(self, field_name)
            # Type validation
            if not _matches_type(value, expected_type):
                errors.append(f"{field_name}: expected {expected_type}, got {type(value).__name__}")
            # Custom validation
            try:
                validator_method = getattr(self, f'validate_{field_name}', None)
                if validator_method and callable(validator_method):
                    if hasattr(validator_method, '_validators'):
                        for validator in validator_method._validators:
                            validator(value)
                    else:
                        validator_method(value)
            except (TypeError, ValueError) as e:
                errors.append(f"{field_name}: {str(e)}")
        
        # Model-level validation
        try:
            if hasattr(self, '_validate_model'):
                self._validate_model()
        except (TypeError, ValueError) as e:
            errors.append(f"model: {str(e)}")
        return errors
    def _validate_type(self, value: Any, expected_type: Any) -> bool:
        if expected_type is Any:
            return True
        # Handle Optional[T] (Union[T, None])
        origin = get_origin(expected_type)
        if origin is Union:
            return any(self._validate_type(value, arg) for arg in get_args(expected_type))
        # Handle List[T], Dict[K, V], etc.
        if origin and not isinstance(value, origin):
            return False
        if origin is list:
            (elem_type,) = get_args(expected_type)
            return all(self._validate_type(v, elem_type) for v in value)
        if origin is dict:
            key_type, val_type = get_args(expected_type)
            return all(self._validate_type(k, key_type) for k in value) and all(self._validate_type(v, val_type) for v in value.values())
        if hasattr(expected_type, '__origin__'):
            return isinstance(value, expected_type.__origin__)
        return isinstance(value, expected_type)
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BaseModel':
        if not isinstance(data, dict):
            raise ValueError(f"Expected dict, got {type(data).__name__}")
        field_names = {f.name for f in fields(cls)}
        filtered_data = {k: v for k, v in data.items() if k in field_names}
        annotations = get_type_hints(cls)
        for field_name, field_type in annotations.items():
            if field_name in filtered_data:
                value = filtered_data[field_name]
                if (inspect.isclass(field_type) and issubclass(field_type, BaseModel) and isinstance(value, dict)):
                    filtered_data[field_name] = field_type.from_dict(value)
                elif get_origin(field_type) is list and get_args(field_type) and issubclass(get_args(field_type)[0], BaseModel):
                    model_class = get_args(field_type)[0]
                    filtered_data[field_name] = [model_class.from_dict(item) if isinstance(item, dict) else item for item in value]
        try:
            return cls(**filtered_data)
        except TypeError as e:
            raise ValueError(f"Failed to create {cls.__name__}: {e}")
    def to_dict(self, exclude_none: bool = False) -> Dict[str, Any]:
        result = {}
        for f in fields(self):
            value = getattr(self, f.name)
            if exclude_none and value is None:
                continue
            if isinstance(value, BaseModel):
                result[f.name] = value.to_dict(exclude_none=exclude_none)
            elif isinstance(value, list) and value and isinstance(value[0], BaseModel):
                result[f.name] = [v.to_dict(exclude_none=exclude_none) for v in value]
            elif isinstance(value, dict):
                result[f.name] = {k: v.to_dict(exclude_none=exclude_none) if isinstance(v, BaseModel) else v for k, v in value.items()}
            else:
                result[f.name] = value
        return result
    def clone(self, **overrides) -> 'BaseModel':
        data = self.to_dict()
        data.update(overrides)
        return self.__class__.from_dict(data)
    # === Hash and Equality (for caching/deduplication) ===
    def __hash__(self) -> int:
        """Hash based on field values (works because frozen=True)."""
        values = tuple(getattr(self, f.name) for f in fields(self))
        return hash((self.__class__.__name__, values))
    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join(f'{f.name}={getattr(self, f.name)!r}' for f in fields(self))})"
    def __str__(self):
        return self.__repr__()
    # === Immutable Operations ===
    def replace(self, **changes) -> T:
        """Immutable clone with changes (dataclass-style name)."""
        data = self.to_dict()
        data.update(changes)
        return self.__class__.from_dict(data)
    # === Network/IPC Serialization ===
    def to_json(self, exclude_none: bool = False, indent: Optional[int] = None) -> str:
        """Serialize to JSON string."""
        return json.dumps(self.to_dict(exclude_none=exclude_none), indent=indent, separators=(',', ':') if indent is None else None)
    @classmethod
    def from_json(cls: Type[T], json_str: str) -> T:
        """Deserialize from JSON string."""
        return cls.from_dict(json.loads(json_str))
    def to_bytes(self, format: SerializationFormat = SerializationFormat.JSON) -> bytes:
        """Serialize to bytes for network transmission."""
        if format == SerializationFormat.JSON:
            return self.to_json().encode('utf-8')
        elif format == SerializationFormat.PICKLE:
            return pickle.dumps(self.to_dict())
        elif format == SerializationFormat.REPR:
            return repr(self.to_dict()).encode('utf-8')
        else:
            raise ValueError(f"Unsupported format: {format}")
    @classmethod
    def from_bytes(cls: Type[T], data: bytes, format: SerializationFormat = SerializationFormat.JSON) -> T:
        """Deserialize from bytes."""
        if format == SerializationFormat.JSON:
            return cls.from_json(data.decode('utf-8'))
        elif format == SerializationFormat.PICKLE:
            return cls.from_dict(pickle.loads(data))
        elif format == SerializationFormat.REPR:
            return cls.from_dict(eval(data.decode('utf-8')))  # Note: eval is dangerous
        else:
            raise ValueError(f"Unsupported format: {format}")
    # === Datagram Integration ===
    def to_datagram(self, sender: str, recipient: Optional[str] = None, 
                   msg_type: MessageType = MessageType.EVENT) -> Datagram:
        """Convert model to datagram for IPC."""
        return Datagram(
            msg_id=str(uuid.uuid4()),
            msg_type=msg_type,
            timestamp=datetime.now().timestamp(),
            sender=sender,
            recipient=recipient,
            payload={"model": self.__class__.__name__, "data": self.to_dict()}
        )
    @classmethod
    def from_datagram(cls: Type[T], datagram: Datagram) -> T:
        """Extract model from datagram payload."""
        if "data" not in datagram.payload:
            raise ValueError("Datagram payload missing 'data' field")
        return cls.from_dict(datagram.payload["data"])
    # === RPC Helpers ===
    def as_rpc_params(self) -> Dict[str, Any]:
        """Convert model to RPC parameter dictionary."""
        return self.to_dict(exclude_none=True)
    @classmethod
    def from_rpc_params(cls: Type[T], params: Dict[str, Any]) -> T:
        """Create model from RPC parameters."""
        return cls.from_dict(params)

@dataclass(frozen=True)
class FileModel(BaseModel):
    """Represents a file with validation."""
    file_path: pathlib.Path
    file_name: str = field(init=False, metadata={"validate": BaseModel.must_be_str})
    content_type: Optional[str] = None
    size_bytes: Optional[int] = field(default=None, metadata={"validate": BaseModel.non_negative})
    ALLOWED_MIME_TYPES = {
        ".txt": "text/plain",
        ".md": "text/markdown",
        ".py": "text/x-python",
    }
    def __post_init__(self):
        # Set derived field
        object.__setattr__(self, "file_name", self.file_path.name)
        super().__post_init__()
    @validate(lambda path: path.exists() and path.is_file())
    def validate_file_path(self, path: pathlib.Path) -> None:
        """Ensure file exists and is readable."""
        pass
    @validate(BaseModel.must_be_str)
    def validate_file_name(self, value: str) -> None:
        pass
    @validate(BaseModel.non_negative)
    def validate_file_size(self, value: int) -> None:
        pass
    def _validate_model(self) -> None:
        ext = self.file_path.suffix.lower()
        if ext not in self.ALLOWED_MIME_TYPES:
            raise ValueError(f"Unsupported file extension: {ext}")
        expected_mime = self.ALLOWED_MIME_TYPES[ext]
        actual_mime, _ = mimetypes.guess_type(self.file_path.name)
        if actual_mime != expected_mime:
            raise ValueError(f"File MIME type mismatch: expected {expected_mime}, got {actual_mime}")
        if self.content_type and self.content_type != actual_mime:
            raise ValueError(f"Declared content_type '{self.content_type}' does not match detected '{actual_mime}'")
        # Auto-set content_type if missing
        if self.content_type is None:
            object.__setattr__(self, "content_type", actual_mime)
    def read_content(self, encoding: str = "utf-8") -> str:
        """Read file content safely."""
        try:
            return self.file_path.read_text(encoding=encoding)
        except Exception as e:
            raise IOError(f"Cannot read file {self.file_path}: {e}")
    def get_stats(self) -> Dict[str, Any]:
        """Get file statistics."""
        stat = self.file_path.stat()
        return {
            "size_bytes": stat.st_size,
            "modified_time": stat.st_mtime,
            "created_time": stat.st_ctime,
            "is_readable": os.access(self.file_path, os.R_OK)
        }

@dataclass(frozen=True)
class Module(FileModel):
    """A Python source file plus an import-safe module name."""
    @validate(lambda v: v.suffix == ".py")
    def validate_file_path(self, v: pathlib.Path) -> None: ...
    @validate(lambda v: v.isidentifier())
    def validate_module_name(self, v: str) -> None: ...

def _install_model_module(name: str, fm: FileModel) -> None:
    """Create a real module that exposes the FileModule instance."""
    mod = types.ModuleType(name)
    mod.__file__ = str(fm.file_path)  # nicer for inspection / tracebacks
    mod.__loader__ = _util.FrozenImporter  # type: ignore
    mod.__package__ = None
    # expose the model instance under the same name as the file stem
    setattr(mod, fm.file_path.stem, fm)
    sys.modules[name] = mod

def create_model_from_file(file_path: pathlib.Path) -> tuple[str, FileModel] | tuple[None, None]:
    """Return (model_name, FileModule) for a single file."""
    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
        model_name = file_path.stem.capitalize() + "Model"
        instance = FileModel(file_path=file_path)  # file_name auto-filled
        return model_name, instance
    except Exception as e:
        logging.error("Failed to load %s: %s", file_path, e)
        return None, None

def load_files_as_models(root: pathlib.Path, exts: list[str]) -> dict[str, FileModel]:
    """Walk root and register FileModule instances as importable modules."""
    models: dict[str, FileModel] = {}
    for path in root.rglob("*"):
        if path.is_file() and path.suffix in exts:
            name, fm = create_model_from_file(path)
            if name and fm:
                models[name] = fm
                _install_model_module(name, fm)
    return models

@dataclass(frozen=True)
class MemoryStats(BaseModel):
    """Memory statistics with validation."""
    size_bytes: int
    object_count: int
    peak_memory: int
    traceback_info: Optional[str] = None
    timestamp: float = field(default_factory=time.time)
    
    @validate(lambda x: x >= 0)
    def validate_size_bytes(self, value: int) -> None:
        """Size must be non-negative."""
        pass
    @validate(lambda x: x >= 0)
    def validate_object_count(self, value: int) -> None:
        """Count must be non-negative."""
        pass
    def _validate_model(self):
        """Ensure peak >= current size."""
        if self.peak_memory < self.size_bytes:
            raise ValueError("Peak memory cannot be less than current size")

@dataclass(frozen=True)
class RPCRequest(BaseModel):
    """Typed RPC request model."""
    method: str
    params: Union[Dict[str, Any], List[Any], None] = None
    request_id: Optional[str] = None
    client_info: Optional[Dict[str, Any]] = None
    
    @validate(lambda x: len(x.strip()) > 0)
    def validate_method(self, value: str) -> None:
        """Method name cannot be empty."""
        pass

@dataclass(frozen=True)
class RPCResponse(BaseModel):
    """Typed RPC response model."""
    result: Optional[Any] = None
    error: Optional[Dict[str, Any]] = None
    request_id: Optional[str] = None
    execution_time_ms: Optional[float] = None
    
    def _validate_model(self):
        """Ensure exactly one of result or error is present."""
        if self.result is not None and self.error is not None:
            raise ValueError("Response cannot have both result and error")
        if self.result is None and self.error is None:
            raise ValueError("Response must have either result or error")
# ==============================================================================
# Type Variables (covariant/contravariant for morphological directionality)
# ==============================================================================

"""Core Operators:

Composition (@): Sequential application of operations
Tensor Product (*): Parallel combination of operations
Direct Sum (+): Alternative pathways of computation
Adjoint (†): Reversal/dual of operations

Algebraic Properties:

Associativity: (A @ B) @ C = A @ (B @ C)
Distributivity: A * (B + C) = (A * B) + (A * C)
Adjoint rules: (A @ B)† = B† @ A†"""

T = TypeVar('T')  # Type structure ['Topology']
V = TypeVar('V')  # Value space ['Morphology']
C = TypeVar('C')  # 'Computation'/control type ['Captaincy']
R = TypeVar('R')  # Result type
BYTE = TypeVar("BYTE", bound="ByteWord")
# Covariant/contravariant type variables for advanced type modeling
T_co = TypeVar('T_co', covariant=True)  # Covariant Type structure
V_co = TypeVar('V_co', covariant=True)  # Covariant Value space
C_co = TypeVar(
    'C_co', bound=Callable[..., Any], covariant=True
)  # Covariant Control space
T_anti = TypeVar('T_anti', contravariant=True)  # Contravariant Type structure
V_anti = TypeVar('V_anti', contravariant=True)  # Contravariant Value space
C_anti = TypeVar(
    'C_anti', bound=Callable[..., Any], contravariant=True
)  # Contravariant Computation space

# Pauli matrices for chiral, quantum mechanics (exactly what we are not doing)
# PAULI_X = np.array([[0, 1], [1, 0]], dtype=np.complex128)
# PAULI_Y = np.array([[0, -1j], [1j, 0]], dtype=np.complex128)
# PAULI_Z = np.array([[1, 0], [0, -1]], dtype=np.complex128)
# Instead, we are doing tesnsors from top-down, taking as a given Einsteins Summation

class WordAlignment(IntEnum):
    UNALIGNED = 1
    WORD = 2
    DWORD = 4
    QWORD = 8
    CACHE_LINE = 64
    PAGE = 4096

class WordSize(enum.IntEnum):
    BYTE = 1  # 8-bit
    SHORT = 2  # 16-bit
    INT = 4  # 32-bit
    LONG = 8  # 64-bit

class QuantumState(enum.Enum):
    # Wigner's Friend's enum (in the Indivisible Stochastic-sense)
    SUPERPOSITION = 1  # Known by handle only; congruent with 'MARKOVIAN'
    ENTANGLED = 2  # Referenced but not loaded; congruent with 'NON_MARKOVIAN' (reversable, given a certain energy expenditure)
    COLLAPSED = 4  # Fully materialized; a 'mere' Object, in the SmallTalk first class functions sense.
    DECOHERENT = 8  # Garbage collected; Dead or dying, only reversable insofar as re-running and yielding potentially alternative results (non-comutative 'arena', of sorts, with thermodynamcis being the only ledger of account)
    EIGENSTATE = 16

class OperatorType(Enum):
    """
    Fundamental operation types in our computational 'universe',
    referring explicitly to the universal-set [], and given the null set
    (a 00000000 ByteWord) as 'glue' (insofar as sheafification, groups,
    topos etc). The 'universe' of runtime, the applied set, is strictly-bounded
    and inertia-local, no relativistic effects outside of the 'relativistic
    effects' of morphological derivation (or time-like integration)* with
    respect to the cross-product of two cartesian coordinates in super position;
    a 'Born Rule'-type ontological scaffolding.
    """
    COMPOSITION = auto()  # Function composition (f >> g)
    TENSOR = auto()  # Tensor product (⊗)
    DIRECT_SUM = auto()  # Direct sum (⊕)
    OUTER = auto()  # Outer product (|ψ⟩⟨φ|)
    ADJOINT = auto()  # Hermitian adjoint (†)
    MEASUREMENT = auto()  # Quantum measurement (⟨M|ψ⟩)

class EntanglementType(enum.Enum):
    CODE_LINEAGE = "code_lineage"
    TEMPORAL_SYNC = "temporal_sync"
    SEMANTIC_BRIDGE = "semantic_bridge"
    PROBABILITY_FIELD = "probability_field"

class Morphology(enum.Enum):
    MORPHIC = 0  # Stable, low-energy state
    DYNAMIC = 1  # High-energy, potentially transformative state
    MARKOVIAN = -1  # Forward-evolving, irreversible
    NON_MARKOVIAN = math.e  # placeholder for sqrt(-1j)

class TorusWinding:
    NULL = 0b00  # (0,0) - topological glue
    W1 = 0b01  # (0,1) - first winding
    W2 = 0b10  # (1,0) - second winding
    W12 = 0b11  # (1,1) - both windings

    @staticmethod
    def to_str(winding: int) -> str:
        return {0b00: "NULL", 0b01: "W1", 0b10: "W2", 0b11: "W12"}[winding & 0b11]

class MorphicComplex:
    """Complex number with morphic properties."""

    __slots__ = ("real", "imag")

    def __init__(self, real: float, imag: float):
        self.real = real
        self.imag = imag

    def conjugate(self) -> "MorphicComplex":
        return MorphicComplex(self.real, -self.imag)

    def __add__(self, other: "MorphicComplex") -> "MorphicComplex":
        return MorphicComplex(self.real + other.real, self.imag + other.imag)

    def __sub__(self, other: "MorphicComplex") -> "MorphicComplex":
        return MorphicComplex(self.real - other.real, self.imag - other.imag)

    def __mul__(
        self, other: Union["MorphicComplex", float, int]
    ) -> "MorphicComplex":
        if isinstance(other, (int, float)):
            return MorphicComplex(self.real * other, self.imag * other)
        return MorphicComplex(
            self.real * other.real - self.imag * other.imag,
            self.real * other.imag + self.imag * other.real,
        )

    def __rmul__(self, other: Union[float, int]) -> "MorphicComplex":
        return self.__mul__(other)

    def __eq__(self, other) -> bool:
        if not isinstance(other, MorphicComplex):
            return False
        return (
            abs(self.real - other.real) < 1e-10 and abs(self.imag - other.imag) < 1e-10
        )

    def __hash__(self) -> int:
        return hash((self.real, self.imag))

    def __repr__(self) -> str:
        if self.imag == 0:
            return f"{self.real}"
        sign = "+" if self.imag >= 0 else ""
        return f"{self.real}{sign}{self.imag}j"

# ==============================================================================
# Matrix — Operator space
# ==============================================================================

class Matrix:
    """Simple matrix implementation using standard Python"""

    __slots__ = ("data", "rows", "cols")

    def __init__(self, data: List[List[Any]]):
        if not data:
            raise ValueError("Matrix data cannot be empty")
        cols = len(data[0])
        if any(len(row) != cols for row in data):
            raise ValueError("All rows must have the same length")
        self.data = data
        self.rows = len(data)
        self.cols = cols

    def __getitem__(self, idx: Tuple[int, int]) -> Any:
        i, j = idx
        if not (0 <= i < self.rows and 0 <= j < self.cols):
            raise IndexError(f"Matrix indices {i},{j} out of range")
        return self.data[i][j]
    def __setitem__(self, idx: Tuple[int, int], value: Any) -> None:
        i, j = idx
        if not (0 <= i < self.rows and 0 <= j < self.cols):
            raise IndexError(f"Matrix indices {i},{j} out of range")
        self.data[i][j] = value
    def __eq__(self, other) -> bool:
        if not isinstance(other, Matrix):
            return False
        if self.rows != other.rows or self.cols != other.cols:
            return False
        return all(
            self.data[i][j] == other.data[i][j]
            for i in range(self.rows)
            for j in range(self.cols)
        )
    def __matmul__(
        self, other: Union["Matrix", List[Any]]
    ) -> Union["Matrix", List[Any]]:
        if isinstance(other, list):
            if len(other) != self.cols:
                raise ValueError(
                    f"Dimensions don't match for matrix-vector multiplication: "
                    f"matrix cols={self.cols}, vector length={len(other)}"
                )
            return [
                sum(self.data[i][j] * other[j] for j in range(self.cols))
                for i in range(self.rows)
            ]
        else:
            if self.cols != other.rows:
                raise ValueError(
                    f"Dimensions don't match for matrix multiplication: "
                    f"first matrix cols={self.cols}, second matrix rows={other.rows}"
                )
            result = [
                [
                    sum(self.data[i][k] * other.data[k][j] for k in range(self.cols))
                    for j in range(other.cols)
                ]
                for i in range(self.rows)
            ]
            return Matrix(result)
    def trace(self) -> Any:
        if self.rows != self.cols:
            raise ValueError("Trace is only defined for square matrices")
        return sum(self.data[i][i] for i in range(self.rows))
    def transpose(self) -> "Matrix":
        return Matrix(
            [[self.data[j][i] for j in range(self.rows)] for i in range(self.cols)]
        )
    @staticmethod
    def zeros(rows: int, cols: int) -> "Matrix":
        if rows <= 0 or cols <= 0:
            raise ValueError("Matrix dimensions must be positive")
        return Matrix([[0 for _ in range(cols)] for _ in range(rows)])
    @staticmethod
    def identity(n: int) -> "Matrix":
        if n <= 0:
            raise ValueError("Matrix dimension must be positive")
        return Matrix([[1 if i == j else 0 for j in range(n)] for i in range(n)])
    def __repr__(self) -> str:
        return "\n".join([str(row) for row in self.data])

# ==============================================================================
# MorphologicalRule — Symbolic rewrite system
# ==============================================================================

class MorphologicalRule:
    __slots__ = ("symmetry", "conservation", "lhs", "rhs")
    def __init__(self, symmetry: str, conservation: str, lhs: str, rhs: List[str]):
        self.symmetry = symmetry
        self.conservation = conservation
        self.lhs = lhs
        self.rhs = rhs
    def apply(self, seq: List[str]) -> List[str]:
        if self.lhs in seq:
            idx = seq.index(self.lhs)
            return seq[:idx] + self.rhs + seq[idx + 1 :]
        return seq

class Frame(Generic[T, V, C]):
    """
    A Frame is the quantum bridge between CPython's memory model and our associative space.
    It represents a region of memory that can exist in multiple states and maintains
    quantum-like properties while mapping directly to CPython's object system.
    """
    def __init__(self):
        # Map to CPython's object structure
        self._py_object = ctypes.py_object()
        self._ref_count = ctypes.c_ssize_t()
        self._type_ptr = ctypes.c_void_p()
        # Quantum state management
        self._state = QuantumState.SUPERPOSITION
        self._observers: set[weakref.ref] = set()
        # Type-Value-Computation spaces
        self._type_space: Optional[T] = None
        self._value_space: Optional[V] = None
        self._compute_space: Optional[C] = None
    @property
    def state(self) -> QuantumState:
        return self._state
    def collapse(self) -> V:
        """Forces materialization of the value space."""
        if self._state == QuantumState.SUPERPOSITION:
            self._materialize()
        return self._value_space
    def _materialize(self) -> None:
        """Maps the quantum state to actual CPython objects."""
        if self._value_space is not None:
            self._py_object.value = self._value_space
            # Get actual CPython object internals
            obj_ptr = ctypes.cast(id(self._py_object.value), ctypes.c_void_p)
            # Map to PyObject structure
            self._ref_count.value = ctypes.pythonapi.Py_RefCnt(obj_ptr)
            self._type_ptr.value = ctypes.pythonapi.Py_TYPE(obj_ptr)
            self._state = QuantumState.COLLAPSED

class Field(Frame[T, V, C], ABC):
    """
    A Field represents a region of spacetime in our quantum memory model.
    It extends Frame with composition and transformation capabilities.
    """
    def __init__(self):
        super().__init__()
        self.entangled_fields: set[weakref.ref[Field]] = set()
    def entangle(self, other: Field) -> None:
        """Creates quantum entanglement between fields."""
        self.entangled_fields.add(weakref.ref(other))
        other.entangled_fields.add(weakref.ref(self))
        self._state = QuantumState.ENTANGLED
        other._state = QuantumState.ENTANGLED
    @abstractmethod
    def transform(self, operator: Callable[[V], V]) -> None:
        """Applies a transformation operator to the value space."""
        pass

class Space(Field[T, V, C]):
    """
    Space is the container for Fields and manages their interactions.
    It provides the high-level interface for our quantum memory model.
    """
    def __init__(self):
        super().__init__()
        self.fields: dict[str, Field] = {}
        
    def create_field(self, handle: str) -> Field:
        """Creates a new field in this space."""
        field = Field()
        self.fields[handle] = field
        return field
        
    def compose(self, other: Space) -> Space:
        """Composes two spaces, maintaining quantum properties."""
        new_space = Space()
        # Compose fields while preserving quantum states
        for handle, field in self.fields.items():
            if handle in other.fields:
                new_field = new_space.create_field(handle)
                new_field.entangle(field)
                new_field.entangle(other.fields[handle])
        return new_space

# ==============================================================================
# FutureParticiple Protocol — Core of deferred execution
# ==============================================================================


@runtime_checkable
class FutureParticiple(Protocol):
    """
    Protocol for objects that can be passed to future runtimes.
    The "gerund" of computational actions — time-independent reifications.
    """

    def __fps_serialize__(self) -> bytes:
        """Serialize to IR (assembly/SQL/.bin/etc)"""
        ...

    @classmethod
    def __fps_deserialize__(cls, data: bytes) -> "FutureParticiple":
        """Reconstruct from IR"""
        ...

    def __fps_bind__(self, **kwargs) -> "FutureParticiple":
        """Late binding: add arguments that don't exist yet"""
        ...

class FPSMixin:
    """
    Mixin that provides default FPS protocol implementation.
    Use via inheritance, not metaclass — cleaner for subinterpreters.
    """
    def __new__(mcs, name, bases, namespace, **kwargs):
        cls = super().__new__(mcs, name, bases, namespace)
        
        # Inject FPS protocol methods if not present
        if not hasattr(cls, '__fps_serialize__'):
            cls.__fps_serialize__ = mcs._default_serialize
        
        if not hasattr(cls, '__fps_deserialize__'):
            cls.__fps_deserialize__ = classmethod(mcs._default_deserialize)
        
        if not hasattr(cls, '__fps_bind__'):
            cls.__fps_bind__ = mcs._default_bind
        
        # Store original __init__ for replay
        cls.__fps_init_signature__ = inspect.signature(cls.__init__)
        
        return cls

    def __fps_serialize__(self) -> bytes:
        data = {
            "__class__": self.__class__.__name__,
            "__module__": self.__class__.__module__,
            "__dict__": {
                k: v for k, v in self.__dict__.items() if not k.startswith("_")
            },
        }
        return json.dumps(data).encode("utf-8")

    @classmethod
    def __fps_deserialize__(cls, data: bytes) -> "FPSMixin":
        obj_data = json.loads(data.decode("utf-8"))
        obj = cls.__new__(cls)
        for k, v in obj_data["__dict__"].items():
            setattr(obj, k, v)
        return obj

    def __fps_bind__(self, **kwargs) -> "FPSMixin":
         """Default binding: store kwargs for future resolution"""
        if not hasattr(self, "__fps_bindings__"):
            self.__fps_bindings__ = {}
        self.__fps_bindings__.update(kwargs)
        return self

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        # Ensure protocol compliance
        if not hasattr(cls, "__fps_serialize__"):
            cls.__fps_serialize__ = FPSMixin.__fps_serialize__
        if not hasattr(cls, "__fps_deserialize__"):
            cls.__fps_deserialize__ = classmethod(FPSMixin.__fps_deserialize__)
        if not hasattr(cls, "__fps_bind__"):
            cls.__fps_bind__ = FPSMixin.__fps_bind__



class ByteWordInstruction(enum.IntEnum):  # Opcode set for IR
    LOAD = 0x01
    COLLAPSE = 0x02
    ENTANGLE = 0x03
    MEASURE = 0x04


# ==============================================================================
# ByteWord — Atomic morphological unit (8-bit with T=4,V=3,C=1 decomposition)
# ==============================================================================


class ByteWord(FPSMixin):
    """
    Enhanced 8-bit word with FPS support.
    Now can be serialized to IR and passed through time.
    """

    __slots__ = (
        "raw",
        "value",
        "T",
        "V",
        "C",
        "_refcount",
        "_quantum_state",
        "_entangled_words",
        "__fps_bindings__",
        "_semantic_vector",
    )

    def __init__(self, raw: int):
        if not 0 <= raw <= 255:
            raise ValueError("ByteWord must be 8-bit (0-255)")
        self.raw = raw
        self.value = raw & 0xFF
        self.T = (raw >> 4) & 0x0F  # state_data
        self.V = (raw >> 1) & 0x07  # morphism
        self.C = raw & 0x01  # floor_morphic
        self._refcount = 1
        self._quantum_state = QuantumCoherenceState.SUPERPOSITION
        self._entangled_words: Set[int] = set()
        self.__fps_bindings__: Dict[str, Any] = {}
        self._semantic_vector: Any = None

    # Custom FPS for ByteWord (IR = 1-byte opcode + 1-byte operand)

    def __fps_serialize__(self) -> bytes:
        return bytes([ByteWordInstruction.LOAD, self.raw])

    @classmethod
    def __fps_deserialize__(cls, data: bytes) -> "ByteWord":
        if len(data) < 2 or data[0] != ByteWordInstruction.LOAD:
            raise ValueError("Invalid ByteWord IR")
        return cls(data[1])

    def __fps_bind__(self, **kwargs) -> "ByteWord":
        if "entangle_with" in kwargs:
            if not hasattr(self, "__fps_future_entanglements__"):
                self.__fps_future_entanglements__ = []
            self.__fps_future_entanglements__.append(kwargs["entangle_with"])
        if "semantic_vector" in kwargs:
            self._semantic_vector = kwargs["semantic_vector"]
        return self

    # Gerund properties (reified actions)

    @property
    def collapsing(self) -> ByteWordAction:
        return ByteWordAction(
            verb="collapse", subject=self, ir_opcode=ByteWordInstruction.COLLAPSE
        )

    @property
    def entangling(self) -> ByteWordAction:
        return ByteWordAction(
            verb="entangle_with", subject=self, ir_opcode=ByteWordInstruction.ENTANGLE
        )

    @property
    def measuring(self) -> ByteWordAction:
        return ByteWordAction(
            verb="measure", subject=self, ir_opcode=ByteWordInstruction.MEASURE
        )

    # Immediate execution methods (for backward compatibility)

    def collapse(self) -> "ByteWord":
        self._quantum_state = QuantumCoherenceState.COLLAPSED
        return self

    def entangle_with(self, other: "ByteWord") -> None:
        self._entangled_words.add(id(other))
        other._entangled_words.add(id(self))
        self._quantum_state = QuantumCoherenceState.ENTANGLED
        other._quantum_state = QuantumCoherenceState.ENTANGLED

    def measure(self) -> QuantumCoherenceState:
        return self._quantum_state


# ==============================================================================
# ByteWordAction — Reified gerund (the Future Participle itself)
# ==============================================================================

@dataclass(slots=True)
class ByteWordAction(FPSMixin):
    """
    Reified action (gerund) that can be passed through time.
    This IS the Future Participle.
    """

    verb: str
    subject: ByteWord
    ir_opcode: ByteWordInstruction
    arguments: Dict[str, Any] = field(default_factory=dict)

   def __init__(self, raw: int):
        if not 0 <= raw <= 255:
            raise ValueError("ByteWord must be 8-bit (0-255)")
        
        self.raw = raw
        self.value = raw & 0xFF
        
        # Decompose (T=4, V=3, C=1)
        self.T = (raw >> 4) & 0x0F  # state_data
        self.V = (raw >> 1) & 0x07  # morphism
        self.C = raw & 0x01         # floor_morphic
        
        self._refcount = 1
        self._quantum_state = QuantumState.SUPERPOSITION
        self._entangled_words = set()

    def __fps_serialize__(self) -> bytes:
        """Serialize action to IR assembly
        IR format: opcode + subject + args"""
        ir = bytearray([self.ir_opcode, self.subject.raw])
        for key, value in self.arguments.items():
            if isinstance(value, ByteWord):
                ir.append(value.raw)
            elif isinstance(value, int):
                ir.append(value & 0xFF)
        return bytes(ir)

    def bind(self, **kwargs) -> "ByteWordAction":
        self.arguments.update(kwargs)
        return self

    def execute(self) -> Any:
        method = getattr(self.subject, self.verb)
        return method(**self.arguments)

    # ========================================================================
    # Gerund Forms (FPS Verbs)
    # ========================================================================
    
    @property
    def collapsing(self) -> 'ByteWordAction':
        """Gerund: the act of collapsing (time-independent)"""
        return ByteWordAction(
            verb='collapse',
            subject=self,
            ir_opcode=ByteWordInstruction.COLLAPSE
        )
    
    @property
    def entangling(self) -> 'ByteWordAction':
        """Gerund: the act of entangling"""
        return ByteWordAction(
            verb='entangle',
            subject=self,
            ir_opcode=ByteWordInstruction.ENTANGLE
        )
    
    @property
    def measuring(self) -> 'ByteWordAction':
        """Gerund: the act of measuring"""
        return ByteWordAction(
            verb='measure',
            subject=self,
            ir_opcode=ByteWordInstruction.MEASURE
        )
    
    @property
    def collapse(self) -> 'ByteWord':
        """Execute collapse NOW"""
        self._quantum_state = QuantumState.COLLAPSED
        return self

    @property
    def entangle_with(self, other: 'ByteWord'):
        """Execute entanglement NOW"""
        self._entangled_words.add(id(other))
        other._entangled_words.add(id(self))
        self._quantum_state = QuantumState.ENTANGLED
        other._quantum_state = QuantumState.ENTANGLED

    def __fps_bind__(self, **kwargs) -> 'ByteWord':
        """Late binding for quantum entanglement, etc."""
        if 'entangle_with' in kwargs:
            # Future entanglement (handle not yet resolved)
            if not hasattr(self, '__fps_future_entanglements__'):
                self.__fps_future_entanglements__ = []
            self.__fps_future_entanglements__.append(kwargs['entangle_with'])
        
        if 'semantic_vector' in kwargs:
            # Deferred semantic embedding
            self._semantic_vector = kwargs['semantic_vector']
        
        return self
# ==============================================================================
# MorphologicalBasis — Evolvable structure
# ==============================================================================

@dataclass
class MorphologicalBasis(Generic[T, V, C]):
    """Defines a structured basis with symmetry evolution."""

    type_structure: T  # Topological/Type representation
    value_space: V  # State space
    compute_space: C  # Operator space

    def evolve(self, generator: Matrix, time: float) -> "MorphologicalBasis[T, V, C]":
        """Evolves the basis using a symmetry generator over time."""
        new_compute_space = self._transform_compute_space(generator, time)
        return MorphologicalBasis(
            self.type_structure, self.value_space, new_compute_space
        )

    def _transform_compute_space(self, generator: Matrix, time: float) -> C:
        """Transform the compute space using the generator"""
        if isinstance(self.compute_space, Matrix) and isinstance(generator, Matrix):
            # Identity matrix
            identity = Matrix.identity(generator.rows)
            # First-order: exp(tA) ≈ I + tA
            scaled_gen = Matrix(
                [
                    [generator[i, j] * time for j in range(generator.cols)]
                    for i in range(generator.rows)
                ]
            )
            result = Matrix(
                [
                    [identity.data[i][j] + scaled_gen.data[i][j] for j in range(identity.cols)]
                    for i in range(identity.rows)
                ]
            )
            return cast(C, result @ self.compute_space)
        raise NotImplementedError(
            f"Cannot evolve compute_space of type {type(self.compute_space)}"
        )

# ==============================================================================
# Morphism & HermitianMorphism — Directional transformation
# ==============================================================================

class Morphism(Generic[T_co, T_anti]):
    """Abstract morphism between type structures"""

    @abstractmethod
    def apply(self, source: T_anti) -> T_co:
        pass

    def __call__(self, source: T_anti) -> T_co:
        return self.apply(source)

    def compose(self, other: "Morphism[T_co, U]") -> "Morphism[U, T_anti]":
        # (self ∘ other)(x) = self(other(x))
        class ComposedMorphism(Morphism[T_co, T_anti]):
            def apply(self, source: T_anti) -> T_co:
                return self._self.apply(self._other.apply(source))

            def __init__(self, s, o):
                self._self = s
                self._other = o

        return ComposedMorphism(self, other)


class HermitianMorphism(Generic[T, V, C, T_anti, V_anti, C_anti]):
    """
    Represents a morphism with a Hermitian adjoint relationship.
    """

    def __init__(
        self,
        forward: Callable[[T, V], C],
        adjoint: Callable[[T_anti, V_anti], C_anti],
    ):
        self.forward = forward
        self.adjoint = adjoint

    def apply(self, source: T, value: V) -> C:
        return self.forward(source, value)

    def apply_adjoint(self, source: T_anti, value: V_anti) -> C_anti:
        return self.adjoint(source, value)

    def get_adjoint(self) -> "HermitianMorphism[V_anti, T_anti, C_anti, V, T, C]":
        return HermitianMorphism(self.adjoint, self.forward)

    def __call__(self, source: T, value: V) -> C:
        return self.apply(source, value)


# ==============================================================================
# Category — Structural container (minimal, protocol-safe)
# ==============================================================================

class Category(Generic[T_co, V_co, C_co]):
    def __init__(self, name: str):
        self.name = name
        self.objects: List[T_co] = []
        self.morphisms: Dict[Tuple[T_co, T_co], List[C_co]] = {}

    def add_object(self, obj: T_co) -> None:
        if obj not in self.objects:
            self.objects.append(obj)

    def add_morphism(self, source: T_co, target: T_co, morphism: C_co) -> None:
        if source not in self.objects:
            self.add_object(source)
        if target not in self.objects:
            self.add_object(target)
        key = (source, target)
        if key not in self.morphisms:
            self.morphisms[key] = []
        self.morphisms[key].append(morphism)

    def find_morphisms(self, source: T_co, target: T_co) -> List[C_co]:
        return self.morphisms.get((source, target), [])

# ==============================================================================
# Utility Functions
# ==============================================================================

def hash_state(value: Any) -> int:
    """Hash a state value in a deterministic way"""
    if isinstance(value, int):
        return value * 2654435761 % 2**32  # Knuth's multiplicative hash
    elif isinstance(value, str):
        return sum(ord(c) * (31**i) for i, c in enumerate(value)) % 2**32
    else:
        return hash(str(value)) % 2**32


def kronecker_field(q1: "MorphologicPyOb", q2: "MorphologicPyOb", temperature: float) -> float:
    dot = sum(a * b for a, b in zip(q1.state.vector, q2.state.vector))
    if temperature > 0.5:
        return math.cos(dot)
    return 1.0 if dot > 0.99 else 0.0


def elevate(data: Any, cls: Type) -> object:
    """Raise a dict or object to a registered morphological class."""
    if not hasattr(cls, "__msc_source__"):
        raise TypeError(f"{cls.__name__} is not a morphological class.")
    source = cls.__msc_source__
    kwargs = {k: getattr(data, k, data.get(k)) for k in source.__annotations__}
    return cls(**kwargs)


class PyWord(Generic[T]):
    """
    Aligned word-sized value optimized for hardware substrate.
    Each PyWord "knows its universe".
    """

    __slots__ = ('_value', '_alignment', '_arch', '_mem_model', '_byteword')

    def __init__(
        self,
        value: Union[int, bytes, bytearray, array.array, ByteWord],
        alignment: WordAlignment = WordAlignment.WORD,
    ):
        self._mem_model = MemoryModel.get_system_info()
        self._arch = ProcessorArchitecture.current()
        self._alignment = alignment

        # Handle ByteWord conversion
        if isinstance(value, ByteWord):
            self._byteword = value
            value = value.raw
        else:
            self._byteword = None

        aligned_size = self._calculate_aligned_size()
        self._value = self._allocate_aligned(aligned_size)
        self._store_value(value)

    def _calculate_aligned_size(self) -> int:
        base_size = max(self._mem_model.word_size, ctypes.sizeof(ctypes.c_size_t))
        return (base_size + self._alignment - 1) & ~(self._alignment - 1)

    def _allocate_aligned(self, size: int) -> ctypes.Array:
        class AlignedArray(ctypes.Structure):
            _pack_ = self._alignment
            _fields_ = [("data", ctypes.c_char * size)]

        return AlignedArray()

    def _store_value(self, value: Union[int, bytes, bytearray, array.array]) -> None:
        if isinstance(value, int):
            if self._arch in (
                ProcessorArchitecture.X86_64,
                ProcessorArchitecture.ARM64,
                ProcessorArchitecture.RISCV64,
            ):
                c_val = ctypes.c_uint64(value)
            else:
                c_val = ctypes.c_uint32(value)
            ctypes.memmove(
                ctypes.addressof(self._value),
                ctypes.addressof(c_val),
                ctypes.sizeof(c_val),
            )
        else:
            value_bytes = memoryview(value).tobytes()
            ctypes.memmove(ctypes.addressof(self._value), value_bytes, len(value_bytes))

    def get_raw_pointer(self) -> int:
        return ctypes.addressof(self._value)

    def as_memoryview(self) -> memoryview:
        return memoryview(self._value)

    @property
    def alignment(self) -> int:
        return self._alignment

    @property
    def architecture(self) -> ProcessorArchitecture:
        return self._arch

    @property
    def byteword(self) -> Optional[ByteWord]:
        return self._byteword

    def as_tstring(self) -> str:
        addr = self.get_raw_pointer()
        bw_str = f", BW={self._byteword.as_tstring()}" if self._byteword else ""
        return f"PyWord@0x{addr:016x}[{self._arch.name}:{self._alignment}B{bw_str}]"

    def __int__(self) -> int:
        if isinstance(self._value, ctypes.Array):
            return int.from_bytes(self._value.data, sys.byteorder)
        return int.from_bytes(self._value.tobytes(), sys.byteorder)

    def __bytes__(self) -> bytes:
        if isinstance(self._value, ctypes.Array):
            return bytes(self._value.data)
        return self._value.tobytes()

@dataclass
class QSD:
    state: complex
    dimensions: int = 2
    precision: float = 1e-12
    atoms: List[Any] = field(default_factory=list)
    relations: List[Any] = field(default_factory=list)
    _id: str = field(init=False, default=None)
    _parent: 'QSD' = field(init=False, default=None)
    _metadata: Dict[str, Any] = field(default_factory=dict)
    _children: List['QSD'] = field(default_factory=list)
    grammar_rules: List['GrammarRule'] = field(default_factory=list)
    case_base: Dict[str, Callable[..., bool]] = field(default_factory=dict)

    def __post_init__(self):
        self.state = complex(self.state) if not isinstance(self.state, complex) else self.state
        self._initialize_case_base()
        self.hash = hashlib.sha256(repr(self.state).encode()).hexdigest()

    def normalize(self):
        magnitude = abs(self.state)
        if magnitude == 0:
            raise ValueError("State cannot have zero magnitude.")
        self.state /= magnitude
        return self.state

    def project(self, angle):
        unit_vector = cmath.rect(1, angle)
        return (self.state * unit_vector.conjugate()).real

    def rotate(self, angle):
        self.state *= cmath.exp(1j * angle)
        return self.state

    def collapse(self):
        probabilities = [abs(self.project(2 * math.pi * i / self.dimensions)) ** 2 for i in range(self.dimensions)]
        cumulative = 0
        rng = math.fsum(probabilities) * random.random()
        for i, prob in enumerate(probabilities):
            cumulative += prob
            if rng < cumulative:
                return i

    @lru_cache(maxsize=128)
    def conjugate(self):
        return self.state.conjugate()

    def tensor_product(self, other: 'QSD'):
        if not isinstance(other, QSD):
            raise ValueError("Tensor product requires another QSD instance.")
        new_state = self.state * other.state
        new_dimensions = self.dimensions * other.dimensions
        return QSD(new_state, dimensions=new_dimensions, precision=min(self.precision, other.precision))

    def add_atom(self, atom):
        self.atoms.append(atom)

    def add_relation(self, relation):
        self.relations.append(relation)

    def process_atoms(self):
        # Placeholder for processing atoms
        processed_atoms = [atom.process() for atom in self.atoms]
        return processed_atoms

    def serialize(self):
        return {
            'atoms': self.atoms,
            'relations': self.relations,
            'metadata': self._metadata
        }

    def deserialize(self, data):
        self.atoms = data['atoms']
        self.relations = data['relations']
        self._metadata = data['metadata']

    @property
    def children(self):
        return self._children

    @children.setter
    def children(self, value):
        self._children = value

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value

    def _initialize_case_base(self):
        self.case_base = {
            '⊤': lambda x, _: x,
            '⊥': lambda _, y: y,
            '¬': lambda a: not a,
            '∧': lambda a, b: a and b,
            '∨': lambda a, b: a or b,
            '→': lambda a, b: (not a) or b,
            '↔': lambda a, b: (a and b) or (not a and not b),
        }

    def process_attributes(self, mapping_description: Dict[str, Any], input_data: Dict[str, Any]) -> None:
        """
        Use the `mapper` function to process input data and map it to attributes.
        
        Args:
            mapping_description (Dict[str, Any]): The mapping description for transformation.
            input_data (Dict[str, Any]): Data to be processed and mapped.
        """
        # Assuming mapper is defined elsewhere
        mapped_data = mapper(mapping_description, input_data)
        for key, value in mapped_data.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def encode(self) -> bytes:
        return json.dumps({
            'id': self.id,
            'attributes': self.__dict__
        }).encode()

    @classmethod
    def decode(cls, data: bytes) -> 'QSD':
        decoded_data = json.loads(data.decode())
        instance = cls(state=decoded_data['state'], dimensions=decoded_data['dimensions'], precision=decoded_data['precision'])
        instance.deserialize(decoded_data['attributes'])
        return instance

    def introspect(self) -> str:
        """
        Reflect on its own code structure via AST.
        """
        import inspect
        import ast
        source_code = inspect.getsource(QSD)
        tree = ast.parse(source_code)
        return ast.dump(tree)

    def __repr__(self):
        return f"{self.state} : {self.dimensions}"

    def __str__(self):
        return str(self.state)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, QSD) and self.hash == other.hash

    def __hash__(self) -> int:
        return int(self.hash, 16)

    def __getitem__(self, key):
        return self.state[key]

    def __setitem__(self, key, value):
        self.state[key] = value

    def __delitem__(self, key):
        del self.state[key]

    def __len__(self):
        return len(self.state)

    def __iter__(self):
        return iter(self.state)

    def __contains__(self, item):
        return item in self.state

    def __call__(self, *args, **kwargs):
        return self.state(*args, **kwargs)

    def __bytes__(self) -> bytes:
        return bytes(self.state)

    @property
    def memory_view(self) -> memoryview:
        if isinstance(self.state, (bytes, bytearray)):
            return memoryview(self.state)
        raise TypeError("Unsupported type for memoryview")

    async def send_message(self, message: Any, ttl: int = 3) -> None:
        if ttl <= 0:
            logging.info(f"Message {message} dropped due to TTL")
            return
        logging.info(f"Atom {self.id} received message: {message}")
        for sub in self.subscribers:
            await sub.receive_message(message, ttl - 1)

    async def receive_message(self, message: Any, ttl: int) -> None:
        logging.info(f"Atom {self.id} processing received message: {message} with TTL {ttl}")
        await self.send_message(message, ttl)

    def subscribe(self, atom: 'QSD') -> None:
        self.subscribers.add(atom)
        logging.info(f"Atom {self.id} subscribed to {atom.id}")

    def unsubscribe(self, atom: 'QSD') -> None:
        self.subscribers.discard(atom)
        logging.info(f"Atom {self.id} unsubscribed from {atom.id}")

    __add__ = lambda self, other: self.value + other
    __sub__ = lambda self, other: self.value - other
    __mul__ = lambda self, other: self.value * other
    __truediv__ = lambda self, other: self.value / other
    __floordiv__ = lambda self, other: self.value // other

    @staticmethod
    def serialize_data(data: Any) -> bytes:
        # Implement serialization logic here
        pass

    @staticmethod
    def deserialize_data(data: bytes) -> Any:
        # Implement deserialization logic here
        pass


#  十十十十十 TRANSPORT LAYER: JSON-RPC Server - BaseModel  十十十十十
_sandbox_commands = asyncio.Queue()  # In‐memory queue for sandbox commands
@dataclass(frozen=True)
class SandboxCommand(BaseModel):
    """A command to be executed by a sandboxed worker."""
    command_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    action: str
    params: Dict[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)
class JSONRPCError(Exception):
    """JSON-RPC 2.0 compliant error with BaseModel integration."""
    PARSE_ERROR = -32700
    INVALID_REQUEST = -32600
    METHOD_NOT_FOUND = -32601
    INVALID_PARAMS = -32602
    INTERNAL_ERROR = -32603
    VALIDATION_ERROR = -32001  # Custom
    def __init__(self, code: int, message: str, data: Any = None, request_id: Any = None):
        self.code = code
        self.message = message
        self.data = data
        self.request_id = request_id
        super().__init__(message)
    def to_dict(self) -> Dict[str, Any]:
        error = {"code": self.code, "message": self.message}
        if self.data is not None:
            error["data"] = self.data
        return error
@dataclass
class RPCConfig:
    """Server configuration."""
    host: str = "127.0.0.1"
    port: int = 8698
    max_content_length: int = 10_000_000
    request_timeout: float = 30.0
    enable_cors: bool = True
    debug: bool = False
    thread_pool_size: int = 4
    validate_requests: bool = True
    validate_responses: bool = True
@dataclass
class MethodInfo:
    """Metadata for a registered RPC method."""
    name: str
    func: Callable
    is_async: bool
    doc: Optional[str] = None
    input_model: Optional[Type[BaseModel]] = None
    output_model: Optional[Type[BaseModel]] = None
    raw_params: bool = False  # Skip model conversion for this method
class JSONRPCDispatcher:
    """JSON-RPC dispatcher with BaseModel integration."""
    def __init__(self, config: RPCConfig):
        self.config = config
        self.methods: Dict[str, MethodInfo] = {}
        self.middleware: List[Callable] = []
        self.executor = ThreadPoolExecutor(max_workers=config.thread_pool_size)
        self.request_count = 0
        self.error_count = 0
    def method(self, 
               name: Optional[str] = None, 
               input_model: Optional[Type[BaseModel]] = None,
               output_model: Optional[Type[BaseModel]] = None,
               raw_params: bool = False):
        """
        Register a JSON-RPC method with optional BaseModel validation.
        Args:
            name: Method name (defaults to function name)
            input_model: BaseModel class for parameter validation
            output_model: BaseModel class for response validation
            raw_params: Skip model conversion, pass raw params
        """
        def decorator(func: Callable):
            method_name = name or func.__name__
            # Auto-detect models from type hints if not provided
            if not raw_params and (input_model is None or output_model is None):
                hints = get_type_hints(func)
                # Try to find input model from first parameter
                if input_model is None:
                    params = list(inspect.signature(func).parameters.values())
                    if params and not params[0].name in ('self', 'cls'):
                        first_param_type = hints.get(params[0].name)
                        if (first_param_type and inspect.isclass(first_param_type) and 
                            issubclass(first_param_type, BaseModel)):
                            input_model = first_param_type
                # Try to find output model from return annotation
                if output_model is None:
                    return_type = hints.get('return')
                    if (return_type and inspect.isclass(return_type) and 
                        issubclass(return_type, BaseModel)):
                        output_model = return_type
            method_info = MethodInfo(
                name=method_name,
                func=func,
                is_async=asyncio.iscoroutinefunction(func),
                doc=inspect.getdoc(func),
                input_model=input_model,
                output_model=output_model,
                raw_params=raw_params
            )
            self.methods[method_name] = method_info
            logger.info(f"Registered {'async' if method_info.is_async else 'sync'} method: {method_name}")
            if input_model:
                logger.info(f"  Input model: {input_model.__name__}")
            if output_model:
                logger.info(f"  Output model: {output_model.__name__}")
            return func
        return decorator
    def middleware_handler(self, func: Callable):
        """Register middleware."""
        self.middleware.append(func)
        return func
    async def _prepare_params(self, method_info: MethodInfo, raw_params: Any) -> Any:
        """Convert raw parameters to BaseModel if configured."""
        if method_info.raw_params or not method_info.input_model:
            return raw_params
        try:
            if isinstance(raw_params, dict):
                return method_info.input_model.from_dict(raw_params)
            elif isinstance(raw_params, list):
                # For positional args, assume first arg is the model data
                if len(raw_params) == 1 and isinstance(raw_params[0], dict):
                    return method_info.input_model.from_dict(raw_params[0])
                return raw_params
            elif raw_params is None:
                # Try to create empty model
                return method_info.input_model.from_dict({})
            else:
                return raw_params
        except Exception as e:
            raise JSONRPCError(
                JSONRPCError.VALIDATION_ERROR,
                f"Parameter validation failed: {e}",
                {"model": method_info.input_model.__name__, "error": str(e)}
            )
    async def _validate_result(self, method_info: MethodInfo, result: Any) -> Any:
        """Validate and convert result using output model if configured."""
        if not self.config.validate_responses or not method_info.output_model:
            return result
        try:
            if isinstance(result, method_info.output_model):
                return result.to_dict()
            elif isinstance(result, dict):
                validated = method_info.output_model.from_dict(result)
                return validated.to_dict()
            else:
                # Try to wrap primitive results
                if hasattr(method_info.output_model, 'from_primitive'):
                    validated = method_info.output_model.from_primitive(result)
                    return validated.to_dict()
                return result
        except Exception as e:
            logger.warning(f"Response validation failed for {method_info.name}: {e}")
            return result  # Return unvalidated rather than fail
    async def _call_method(self, method_info: MethodInfo, params: Any) -> Any:
        """Call method with proper parameter handling."""
        try:
            # Prepare parameters
            processed_params = await self._prepare_params(method_info, params)
            # Determine how to call the function
            sig = inspect.signature(method_info.func)
            param_names = list(sig.parameters.keys())
            if isinstance(processed_params, BaseModel):
                # Pass BaseModel as single argument
                if method_info.is_async:
                    result = await method_info.func(processed_params)
                else:
                    loop = asyncio.get_event_loop()
                    result = await loop.run_in_executor(
                        self.executor, 
                        lambda: method_info.func(processed_params)
                    )
            elif isinstance(processed_params, dict):
                # Keyword arguments
                if method_info.is_async:
                    result = await method_info.func(**processed_params)
                else:
                    loop = asyncio.get_event_loop()
                    result = await loop.run_in_executor(
                        self.executor, 
                        lambda: method_info.func(**processed_params)
                    )
            elif isinstance(processed_params, list):
                # Positional arguments
                if method_info.is_async:
                    result = await method_info.func(*processed_params)
                else:
                    loop = asyncio.get_event_loop()
                    result = await loop.run_in_executor(
                        self.executor, 
                        lambda: method_info.func(*processed_params)
                    )
            else:
                # Single parameter
                if method_info.is_async:
                    result = await method_info.func(processed_params)
                else:
                    loop = asyncio.get_event_loop()
                    result = await loop.run_in_executor(
                        self.executor, 
                        lambda: method_info.func(processed_params)
                    )
            # Validate result if configured
            return await self._validate_result(method_info, result)
        except JSONRPCError:
            raise
        except Exception as e:
            logger.exception(f"Error executing method {method_info.name}: {e}")
            raise JSONRPCError(
                JSONRPCError.INTERNAL_ERROR,
                f"Method execution failed: {e}",
                {"method": method_info.name, "error": str(e)} if self.config.debug else None
            )
    async def dispatch_single(self, request_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Dispatch single request with BaseModel integration."""
        start_time = time.time()
        request_id = request_data.get("id")
        try:
            # Validate request format
            if self.config.validate_requests:
                try:
                    request = RPCRequest.from_dict({
                        "method": request_data.get("method"),
                        "params": request_data.get("params"),
                        "request_id": str(request_id) if request_id is not None else None,
                        "client_info": {"timestamp": time.time()}
                    })
                except Exception as e:
                    raise JSONRPCError(JSONRPCError.INVALID_REQUEST, f"Request validation failed: {e}")
            if request_data.get("jsonrpc") != "2.0":
                raise JSONRPCError(JSONRPCError.INVALID_REQUEST, "Invalid JSON-RPC version")
            method_name = request_data.get("method")
            if not method_name:
                raise JSONRPCError(JSONRPCError.INVALID_REQUEST, "Missing method")
            params = request_data.get("params")
            # Find method
            method_info = self.methods.get(method_name)
            if not method_info:
                raise JSONRPCError(JSONRPCError.METHOD_NOT_FOUND, f"Method '{method_name}' not found")
            # Run middleware
            for middleware in self.middleware:
                await middleware(request_data)
            # Execute method
            result = await self._call_method(method_info, params)
            execution_time = (time.time() - start_time) * 1000
            # Return response (skip for notifications)
            if request_id is not None:
                response_data = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": result
                }
                if self.config.debug:
                    response_data["_meta"] = {
                        "execution_time_ms": execution_time,
                        "method": method_name
                    }
                return response_data
            return None
        except JSONRPCError as e:
            self.error_count += 1
            if request_id is not None:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": e.to_dict()
                }
            return None
    async def dispatch(self, payload: Union[Dict, List]) -> Optional[Union[Dict, List]]:
        """Dispatch requests with BaseModel support."""
        self.request_count += 1
        try:
            if isinstance(payload, list):
                if not payload:
                    raise JSONRPCError(JSONRPCError.INVALID_REQUEST, "Empty batch request")
                
                results = await asyncio.gather(
                    *[self.dispatch_single(req) for req in payload],
                    return_exceptions=False
                )
                filtered_results = [r for r in results if r is not None]
                return filtered_results if filtered_results else None
            else:
                return await self.dispatch_single(payload)
        except Exception as e:
            logger.exception(f"Fatal error in dispatcher: {e}")
            return {
                "jsonrpc": "2.0",
                "id": None,
                "error": JSONRPCError(JSONRPCError.PARSE_ERROR, "Parse error").to_dict()
            }
    def get_stats(self) -> Dict[str, Any]:
        """Get detailed statistics."""
        return {
            "methods_registered": len(self.methods),
            "requests_processed": self.request_count,
            "errors_encountered": self.error_count,
            "active_threads": len(self.executor._threads) if self.executor._threads else 0,
            "validation_enabled": {
                "requests": self.config.validate_requests,
                "responses": self.config.validate_responses
            }
        }
    def list_methods(self) -> Dict[str, Any]:
        """List all methods with BaseModel info."""
        return {
            name: {
                "name": info.name,
                "async": info.is_async,
                "doc": info.doc,
                "input_model": info.input_model.__name__ if info.input_model else None,
                "output_model": info.output_model.__name__ if info.output_model else None,
                "raw_params": info.raw_params
            }
            for name, info in self.methods.items()
        }

# ============================================================================
# HTTP REQUEST HANDLER 
# ============================================================================

class JSONRPCRequestHandler(BaseHTTPRequestHandler):
    """HTTP request handler for JSON-RPC with BaseModel support."""
    
    def __init__(self, dispatcher: JSONRPCDispatcher, config: RPCConfig, *args, **kwargs):
        self.dispatcher = dispatcher
        self.config = config
        super().__init__(*args, **kwargs)
    
    def log_message(self, format, *args):
        """Override to use our logger."""
        logger.info(f"{self.address_string()} - {format % args}")
    
    def _send_cors_headers(self):
        """Send CORS headers if enabled."""
        if self.config.enable_cors:
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    
    def _send_json_response(self, data: Any, status: int = 200):
        """Send a JSON response."""
        response_body = json.dumps(data, indent=2 if self.config.debug else None).encode('utf-8')
        
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(response_body)))
        self._send_cors_headers()
        self.end_headers()
        self.wfile.write(response_body)
    
    def _send_error_response(self, message: str, status: int = 400):
        """Send an error response."""
        self._send_json_response({"error": message}, status)
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests."""
        self.send_response(204)
        self._send_cors_headers()
        self.end_headers()
    
    def do_GET(self):
        """Handle GET requests for introspection."""
        if self.path == '/health':
            self._send_json_response({"status": "healthy", "timestamp": time.time()})
        elif self.path == '/methods':
            self._send_json_response(self.dispatcher.list_methods())
        elif self.path == '/stats':
            self._send_json_response(self.dispatcher.get_stats())
        else:
            self._send_error_response("Not Found", 404)
    
    def do_POST(self):
        """Handle JSON-RPC POST requests."""
        try:
            # Check content length
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > self.config.max_content_length:
                self._send_error_response("Request entity too large", 413)
                return
            
            if content_length == 0:
                self._send_error_response("Empty request body", 400)
                return
            
            # Read and parse request
            raw_data = self.rfile.read(content_length)
            try:
                request_data = json.loads(raw_data.decode('utf-8'))
            except (json.JSONDecodeError, UnicodeDecodeError):
                error_response = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": JSONRPCError(JSONRPCError.PARSE_ERROR, "Parse error").to_dict()
                }
                self._send_json_response(error_response)
                return
            
            # Process request
            async def process_request():
                return await self.dispatcher.dispatch(request_data)
            
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                response = loop.run_until_complete(process_request())
                loop.close()
            except Exception as e:
                logger.exception(f"Error processing request: {e}")
                error_response = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": JSONRPCError(JSONRPCError.INTERNAL_ERROR, "Internal server error").to_dict()
                }
                self._send_json_response(error_response, 500)
                return
            
            # Send response
            if response is not None:
                self._send_json_response(response)
            else:
                self.send_response(204)
                self._send_cors_headers()
                self.end_headers()
                
        except Exception as e:
            logger.exception(f"Unhandled error in request handler: {e}")
            self._send_error_response("Internal server error", 500)
    # === Utility Methods ===
    def checksum(self, algorithm: str = 'md5') -> str:
        """Generate checksum of the model data."""
        data_str = json.dumps(self.to_dict(), sort_keys=True)
        if algorithm == 'md5':
            return hashlib.md5(data_str.encode()).hexdigest()
        elif algorithm == 'sha256':
            return hashlib.sha256(data_str.encode()).hexdigest()
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")

    def diff(self, other: 'BaseModel') -> Dict[str, Any]:
        """Return differences between this model and another."""
        if not isinstance(other, BaseModel):
            raise TypeError("Can only diff with another BaseModel")
        
        self_dict = self.to_dict()
        other_dict = other.to_dict()
        
        diff = {}
        all_keys = set(self_dict.keys()) | set(other_dict.keys())
        
        for key in all_keys:
            self_val = self_dict.get(key, '<MISSING>')
            other_val = other_dict.get(key, '<MISSING>')
            if self_val != other_val:
                diff[key] = {'self': self_val, 'other': other_val}
        
        return diff

    def schema(self, include_metadata: bool = False) -> Dict[str, Any]:
        """Generate JSON schema-like description."""
        schema = {
            'type': 'object',
            'title': self.__class__.__name__,
            'properties': {}
        }
        
        type_hints = get_type_hints(self.__class__)
        
        for field in fields(self):
            field_schema = {
                'type': str(type_hints.get(field.name, 'Any')).replace('typing.', '')
            }
            
            if field.default != field.default_factory():
                field_schema['default'] = field.default
                
            if include_metadata and field.metadata:
                field_schema['metadata'] = field.metadata
                
            schema['properties'][field.name] = field_schema
        
        return schema

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    server: Optional[HTTPServer]
    daemon_threads = True
class JSONRPCServer:
    """Threaded-server class with BaseModel integration."""

    def __init__(self, config: Optional[RPCConfig] = None):
        self.config = config or RPCConfig()
        self.dispatcher = JSONRPCDispatcher(self.config)
        self.server: Optional[ThreadingHTTPServer] = None
        self._running = False

    def method(self, name: Optional[str] = None, **kwargs):
        """Register RPC method decorator."""
        return self.dispatcher.method(name, **kwargs)

    def middleware(self, func: Callable):
        """Register middleware decorator."""
        return self.dispatcher.middleware_handler(func)

    def start(self):
        """Start the JSON-RPC server."""
        def handler_factory(*args, **kwargs):
            return JSONRPCRequestHandler(self.dispatcher, self.config, *args, **kwargs)

        server_address = (self.config.host, self.config.port)
        self.server = ThreadedHTTPServer(server_address, handler_factory)
        self._running = True

        logger.info(f"JSON-RPC server started on http://{self.config.host}:{self.config.port}")
        try:
            if self.server is None:
                raise RuntimeError("Server has not been initialized")
            self.server.serve_forever()
        except KeyboardInterrupt:
            logger.info("Keyboard interrupt received. Stopping server.")
            self.stop()

    def stop(self):
        """Stop the JSON-RPC server."""
        if self.server:
            self._running = False
            self.server.shutdown()
            self.server.server_close()
            logger.info("JSON-RPC server stopped")

class MonolithicServer:
    """
    The unified server class. Manages state, dispatchers, and the async loop.
    """
    def __init__(self, config: ServerConfig):
        self.config = config
        self.rpc_dispatcher = RpcDispatcher(config)
        self.sandbox_queue = asyncio.Queue()
        self._server_task: Optional[asyncio.Task] = None
        self._logger = get_logger()
        self._register_internal_methods()

    def method(self, name: Optional[str] = None):
        """Decorator to register a function as an RPC method."""
        return self.rpc_dispatcher.method(name)

    def _register_internal_methods(self):
        """Register built-in methods for server management."""
        @self.method("server.health")
        async def health(_: Any) -> Dict[str, Any]:
            return {"status": "ok", "timestamp": time.time()}

        @self.method("sandbox.enqueue")
        async def enqueue(cmd: SandboxCommand) -> Dict[str, Any]:
            await self.sandbox_queue.put(cmd)
            self._logger.info(f"Enqueued sandbox command: {cmd.action}")
            return {"status": "enqueued", "command_id": cmd.command_id}

        @self.method("sandbox.dequeue")
        async def dequeue(_: Any) -> Optional[Dict[str, Any]]:
            try:
                cmd = self.sandbox_queue.get_nowait()
                self._logger.info(f"Dequeued sandbox command: {cmd.action}")
                return cmd.to_dict()
            except asyncio.QueueEmpty:
                return None

    async def _handle_request(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        correlation_id = str(uuid.uuid4())
        logger = get_logger(correlation_id)
        peername = writer.get_extra_info('peername')
        logger.info(f"Connection from {peername}")

        response_body, status = b'', 204
        headers = [("Content-Type", "application/json"), ("Access-Control-Allow-Origin", "*")]

        try:
            request_line = await reader.readline()
            if not request_line: return
            
            method, path, _ = request_line.decode().split()
            
            # Read headers
            http_headers = {}
            while True:
                line = await reader.readline()
                if line == b'\r\n': break
                k, v = line.decode().strip().split(':', 1)
                http_headers[k.lower()] = v.strip()

            if method == 'POST' and path == '/rpc':
                content_len = int(http_headers.get('content-length', 0))
                if content_len > self.config.MAX_REQUEST_SIZE:
                    raise RpcError(INVALID_REQUEST, "Request body too large.")
                
                body = await reader.readexactly(content_len)
                payload = json.loads(body)

                if isinstance(payload, list):
                    tasks = [self.rpc_dispatcher.dispatch(p, logger) for p in payload]
                    results = [r for r in await asyncio.gather(*tasks) if r]
                    if results:
                        response_body = json.dumps(results).encode()
                        status = 200
                else:
                    result = await self.rpc_dispatcher.dispatch(payload, logger)
                    if result:
                        response_body = json.dumps(result).encode()
                        status = 200
            
            elif method == 'GET' and path == '/health':
                response_body = json.dumps({"status": "healthy"}).encode()
                status = 200

            elif method == 'OPTIONS' and path == '/rpc':
                headers.extend([
                    ("Access-Control-Allow-Methods", "POST, OPTIONS"),
                    ("Access-Control-Allow-Headers", "Content-Type"),
                ])
                status = 204 # No Content

            else:
                raise RpcError(METHOD_NOT_FOUND, "Not Found")

        except RpcError as e:
            status = 400 # Bad Request for most RPC errors
            response_body = json.dumps({"jsonrpc": "2.0", "id": None, "error": e.to_dict()}).encode()
        except Exception as e:
            logger.error(f"Unhandled error in request handler: {e}", exc_info=self.config.DEBUG)
            status = 500
            error = RpcError(INTERNAL_ERROR, "Internal Server Error").to_dict()
            response_body = json.dumps({"jsonrpc": "2.0", "id": None, "error": error}).encode()
        
        finally:
            writer.write(f"HTTP/1.1 {status} {http.HTTPStatus(status).phrase}\r\n".encode())
            writer.write(f"Content-Length: {len(response_body)}\r\n".encode())
            for k, v in headers: writer.write(f"{k}: {v}\r\n".encode())
            writer.write(b"\r\n")
            if response_body: writer.write(response_body)
            await writer.drain()
            writer.close()

    async def start(self):
        """Starts the server and listens for connections."""
        server = await asyncio.start_server(self._handle_request, self.config.HOST, self.config.PORT)
        addr = server.sockets[0].getsockname()
        self._logger.info(f"Monolithic server live on http://{addr[0]}:{addr[1]}")
        self._server_task = asyncio.create_task(server.serve_forever())
        try:
            await self._server_task
        except asyncio.CancelledError:
            self._logger.info("Server task cancelled.")
        finally:
            server.close()
            await server.wait_closed()

    def stop(self):
        """Stops the server gracefully."""
        if self._server_task and not self._server_task.done():
            self._server_task.cancel()
        self._logger.info("Server shutdown initiated.")
    async def handle_raw_socket_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """Handles a single incoming raw TCP socket connection."""
        logger = get_logger("Socket")
        addr = writer.get_extra_info('peername')
        logger.info(f"Connection from {addr}")
        try:
            while True:
                line = await reader.readline()
                if not line: break
                
                request = json.loads(line)
                response = await self.dispatcher.dispatch(request)
                if response:
                    writer.write(json.dumps(response).encode('utf-8') + b'\n')
                    await writer.drain()
        except ConnectionResetError:
            logger.warning(f"Client {addr} disconnected abruptly.")
        except Exception as e:
            logger.error(f"Error handling socket client: {e}", exc_info=self.config.debug)
            error_resp = JSONRPCError(-32000, "Socket processing error", str(e)).to_dict()
            writer.write(json.dumps({"jsonrpc": "2.0", "id": None, "error": error_resp}).encode('utf-8') + b'\n')
            await writer.drain()
        finally:
            logger.info(f"Closing connection from {addr}")
            writer.close()
            await writer.wait_closed()

    @staticmethod
    def to_str(winding: int) -> str:
        return {0b00: "NULL", 0b01: "W1", 0b10: "W2", 0b11: "W12"}[winding & 0b11]
