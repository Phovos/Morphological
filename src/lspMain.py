#!/usr/bin/env -S uv run
from __future__ import annotations

# /* script
# requires-python = ">=3.12"
# dependencies = [
#     "uv==*.*",
# ]
# */
# Optional dependency handling (also add to '/* script..' comment, just above)
#   "© 2026 `Phovos` (phovos@outlook.com)":
#     - "Morphological Source Code: MSC&QSD"
#     - https://gitlab.com/morphological/source/code
#     - https://github.com/Morphological-Source-Code
#     - https://reddit.com/r/morphological
# © 2024-2026 https://github.com/Phovos/Morphological-Source-Code
# © 2023-2026 https://github.com/MOONLAPSED/cognosis
"""
Unified Polymorphic Atom Hierarchy
==================================

DOF -> Atom -> DataclassAtom -> HashDataclassAtom -> [Concrete X-Type Atoms]

C3 Linearization as Well-Ordered Time
-------------------------------------
The Method Resolution Order (MRO) is not merely an implementation detail;
it is the arrow of time for morphological computation. Every runtime entity
capable of being programmed with respect to a C3-linearized MRO is a
"flavor" or "x-type" of Atom. We bootstrap homoiconism in a brute-force,
if inelegant, fashion—getting closer to the metal with every super() call.

Microcanonical (NVE) Mechanics
------------------------------
The ByteWord System IS Microcanonical. No bath. No reservoir. Just bits
and their ghosts. This is not canonical (NVT) statistical mechanics where
temperature is imposed by an external bath. This is microcanonical (NVE):
Number of states fixed, Volume of morphospace fixed, Energy budget fixed.
Temperature emerges from the degeneracy structure of the ghost ensemble.

    N = 256 ByteWords (or however many you allocate)
    V = morphospace (discrete, finite, no continuous volume)
    E = initial energy (Landauer budget, fixed at start)

The system evolves:
    • Deterministically (bit operations, no randomness required)
    • Isoenergetically (energy conserved until Landauer payment)
    • Isolated (no exchange with external bath—the Python/SQL boundary
      is a measurement surface, not a thermal reservoir)

The ghosts aren't "coupled to a bath." They're intensive degrees of freedom
that haven't yet manifested extensively. They're still part of the system.
Not outside it.

WHAT "TEMPERATURE" EVEN MEANS HERE
-----------------------------------
In canonical (NVT), temperature is fixed by the bath. The system's energy
fluctuates to match. In microcanonical (NVE), temperature is derived:

    T = ∂S/∂E  (how entropy changes with energy)

For ByteWord(s), this becomes:

    T_morphic = ∂(# of ghost configurations) / ∂(# of active commanders)

"Temperature" is the degeneracy of the ghost ensemble. How many ways can
you arrange the bulk for a given number of active C-bits?

    • Low temp: Few ghosts, mostly observables, low entropy
    • High temp: Many ghosts, few observables, high entropy

But this T is internal. It's not imposed. It's emergent from the dynamics.

THE BYTEWORD ATOM
-----------------
PHYSICAL ATOM: ByteWord (8-bit minimal morphological unit)
Big-endian gauge topology: [C V V V | T T T T]
    C = Captain bit (thermodynamic phase boundary)
    V = Value field (3 bits, deputizable)
    T = Type field (4 bits: winding + arity)

This maps to three aspects of nominative invariance:
    Identity preservation:  T = Type structure (static)
    Content preservation:   V = Value space (dynamic)
    Behavioral preservation: C = Computation space (transformative)

1========10========20========30========40========50========60========70========80=====88
"""
# /// stdlib-only polymorphic atom hierarchy ///
# DOF -> Atom -> BaseModelAtom -> DataclassAtom -> [x-type]Atoms
# C3 linearized MRO throughout; every __init__ and __post_init__ chains
# via super() or explicit parent call so the MRO is a well-ordered time axis.
#
# Physics borrowings:
#   DOF          : Degrees of Freedom — microcanonical runtime container
#   Atom         : Base particle — quantum state, flavor, entanglement
#   BaseModelAtom: Pydantic-style validation/serialization shell
#   DataclassAtom: Mutable dataclass polymorph (primary)
#   ImmutableDataclassAtom : Frozen, hash-flavored struct
#   DataAtom     : Vanilla numeric substrate (complex, int, float)
#   DTOAtom      : Datagram/DTO highest polymorph for wire interchange
#   CodeAtom     : Homoiconic executable
#   InterpreterAtom : Isolated execution with fallback threading
# ---------------------------------------------------------------------------

import abc
import ast
import base64
import hashlib
import inspect
import json
import logging
import os
import pickle
import threading
import time
import typing
import uuid
import weakref
from dataclasses import dataclass, field, fields, MISSING
from enum import Enum, auto
from functools import wraps
from pathlib import Path
from typing import (
    Any,
    Callable,
    ClassVar,
    Dict,
    Generic,
    List,
    Optional,
    Protocol,
    Tuple,
    Type,
    TypeVar,
    Union,
    get_type_hints,
    runtime_checkable,
)

# ---------------------------------------------------------------------------
# 1.  OPTIONAL SUB-INTERPRETER PROBE (stdlib may or may not expose it yet)
# ---------------------------------------------------------------------------

try:
    from test.support import interpreters  # type: ignore[import-not-found]

    HAS_INTERPRETERS: bool = True
except ImportError:
    HAS_INTERPRETERS = False

# ---------------------------------------------------------------------------
# 2.  LOGGING
# ---------------------------------------------------------------------------

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# 3.  ENUMERATIONS
# ---------------------------------------------------------------------------


class QuantumState(Enum):
    """
    Quantum-like states for morphological atoms.
    SUPERPOSITION : Unresolved potential (lazy evaluation).
    COLLAPSED     : Definite value observed.
    ENTANGLED     : Correlated with another atom; non-separable.
    DECOHERED     : Lost phase coherence; classical limit.
    """

    SUPERPOSITION = auto()
    COLLAPSED = auto()
    ENTANGLED = auto()
    DECOHERED = auto()


class ByteWordFlavor(Enum):
    """
    Morphological flavor — determines structural constraints.
    MUTABLE      : Standard mutable atom.
    IMMUTABLE    : Frozen struct-like atom (hash-flavored).
    HOMOICONIC   : Code-as-data reflection enabled.
    POLYMORPHIC  : Runtime type identity changes allowed.
    HASH         : Canonical identity via cryptographic digest.
    """

    MUTABLE = auto()
    IMMUTABLE = auto()
    HOMOICONIC = auto()
    POLYMORPHIC = auto()
    HASH = auto()


class SerializationFormat(Enum):
    """Wire-format choices for datagram serialization."""

    JSON = auto()
    PICKLE = auto()
    REPR = auto()


class ExecutionMode(Enum):
    """InterpreterAtom execution strategy."""

    INLINE = auto()
    INTERPRETER = auto()
    THREADED = auto()


class RuntimeMode(Enum):
    """Runtime execution backend."""

    THREADED = auto()
    SUBINTERPRETER = auto()


# ---------------------------------------------------------------------------
# 4.  EXCEPTIONS
# ---------------------------------------------------------------------------


class ConfigurationError(ValueError):
    """Raised when a configuration atom violates its invariants."""

    pass


class MorphologicalError(TypeError):
    """Raised when structural typing or MRO invariants are violated."""

    pass


# ---------------------------------------------------------------------------
# 5.  TYPE HELPERS  (used by BaseModelAtom validation & schema)
# ---------------------------------------------------------------------------


def _matches_type(value: Any, expected_type: Any) -> bool:
    """
    Structural type matching with support for generics, Union, list, dict,
    tuple, and plain classes.  Any matches everything.
    """
    origin = typing.get_origin(expected_type)
    if origin is None:
        if expected_type is Any:
            return True
        try:
            return isinstance(value, expected_type)
        except TypeError:
            return True
    args = typing.get_args(expected_type)
    if origin is Union:
        return any(_matches_type(value, arg) for arg in args)
    if origin is list:
        if not isinstance(value, list):
            return False
        if not args:
            return True
        return all(_matches_type(v, args[0]) for v in value)
    if origin is dict:
        if not isinstance(value, dict):
            return False
        if len(args) < 2:
            return True
        return all(
            _matches_type(k, args[0]) and _matches_type(v, args[1])
            for k, v in value.items()
        )
    if origin is tuple:
        if not isinstance(value, tuple):
            return False
        if not args:
            return True
        if len(args) != len(value):
            return False
        return all(_matches_type(v, arg) for v, arg in zip(value, args))
    try:
        return isinstance(value, origin)
    except TypeError:
        return True


def _coerce(value: Any, field_type: Any) -> Any:
    """
    Attempt to coerce *value* into *field_type*.
    Handles Path, Union, list, dict, tuple, and primitive constructors.
    """
    origin = typing.get_origin(field_type)
    if origin is None:
        if field_type is Any:
            return value
        if field_type is Path and isinstance(value, (str, os.PathLike)):
            return Path(value)
        if isinstance(value, field_type):
            return value
        try:
            return field_type(value)
        except TypeError, ValueError:
            return value
    args = typing.get_args(field_type)
    if origin is Union:
        for arg in args:
            if arg is type(None) and value is None:
                return None
            try:
                return _coerce(value, arg)
            except TypeError, ValueError:
                continue
        return value
    if origin is list and isinstance(value, list):
        if not args:
            return value
        return [_coerce(v, args[0]) for v in value]
    if origin is dict and isinstance(value, dict):
        if len(args) < 2:
            return value
        return {_coerce(k, args[0]): _coerce(v, args[1]) for k, v in value.items()}
    if origin is tuple and isinstance(value, (list, tuple)):
        if not args:
            return tuple(value)
        return tuple(_coerce(v, arg) for v, arg in zip(value, args))
    return value


def _uncoerce(value: Any) -> Any:
    """
    Recursively convert Atom instances (and other rich objects) into
    plain Python containers for JSON serialization.
    """
    if isinstance(value, Atom):
        return value.to_dict()
    if isinstance(value, (list, tuple)):
        return [_uncoerce(v) for v in value]
    if isinstance(value, dict):
        return {k: _uncoerce(v) for k, v in value.items()}
    if isinstance(value, Enum):
        return value.name
    if isinstance(value, (Path, os.PathLike)):
        return str(value)
    return value


def _type_to_schema(field_type: Any) -> Dict[str, Any]:
    """Generate a primitive JSON-Schema fragment from a type hint."""
    origin = typing.get_origin(field_type)
    if field_type is Any:
        return {}
    if field_type in (str, bytes):
        return {"type": "string"}
    if field_type in (int,):
        return {"type": "integer"}
    if field_type in (float,):
        return {"type": "number"}
    if field_type in (bool,):
        return {"type": "boolean"}
    if origin is list:
        args = typing.get_args(field_type)
        item_schema = _type_to_schema(args[0]) if args else {}
        return {"type": "array", "items": item_schema}
    if origin is dict:
        return {"type": "object"}
    if origin is Union:
        args = typing.get_args(field_type)
        if type(None) in args:
            non_none = [a for a in args if a is not type(None)]
            if len(non_none) == 1:
                schema = _type_to_schema(non_none[0])
                schema["nullable"] = True
                return schema
        return {"anyOf": [_type_to_schema(a) for a in args]}
    return {"type": "object"}


def mapper(
    mapping_description: Dict[str, Any], input_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Simple attribute mapper for morphological transformations.
    Supports callable specs, string key lookups, and literal values.
    """
    result: Dict[str, Any] = {}
    for key, spec in mapping_description.items():
        if callable(spec):
            result[key] = spec(input_data)
        elif isinstance(spec, str):
            result[key] = input_data.get(spec)
        else:
            result[key] = spec
    return result


# ---------------------------------------------------------------------------
# 6.  DEGREES OF FREEDOM (DOF)  —  morphological bedrock
# ---------------------------------------------------------------------------

T = TypeVar("T")
V = TypeVar("V")
C = TypeVar("C")


class DOF:
    """
    Degree of Freedom.  The root runtime container.

    Each DoF encapsulates both:
        State : Observable properties (spin, phase, temporal position).
        Logic : Transformative behaviors (compose, interact, evolve).

    A DoF runtime is a self-contained microcosm of both declarative (state)
    and imperative (logic) programming, enabling homoiconic behaviors.

    Microcanonical ensemble semantics:
        N = fixed number of states
        V = fixed morphospace volume (discrete, finite)
        E = fixed Landauer energy budget
    Temperature emerges from ghost degeneracy — never imposed by a bath.
    """

    __slots__ = ("_birth_time_mono", "_dof_id", "_metadata", "_ghost_config")

    def __init__(self) -> None:
        # Idempotent init: safe to call multiple times (e.g. from dataclass
        # __post_init__ chains that may bypass this __init__).
        if hasattr(self, "_dof_id"):
            return
        # Monotonic time: immune to NTP skew, the true arrow of time.
        self._birth_time_mono: float = time.monotonic()
        self._dof_id: str = uuid.uuid4().hex
        self._metadata: Dict[str, Any] = {}
        self._ghost_config: Dict[str, Any] = {}

    @property
    def birth_time_mono(self) -> float:
        """Monotonic timestamp at creation.  Immutable arrow of time."""
        return self._birth_time_mono

    @property
    def dof_id(self) -> str:
        """Unique identifier for this degree of freedom."""
        return self._dof_id

    def entropy(self) -> float:
        """
        Microcanonical entropy: degeneracy of ghost configurations.
        Concrete atoms override with their ensemble cardinality.
        """
        return 0.0

    def temperature(self) -> float:
        """Emergent temperature from internal dynamics, not external bath."""
        return 0.0

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"dof_id={self._dof_id[:8]}..., "
            f"birth={self._birth_time_mono:.6f})"
        )


# ---------------------------------------------------------------------------
# 7.  ATOM  —  base polymorphic unit
# ---------------------------------------------------------------------------


class Atom(DOF, Generic[T, V]):
    """
    Base Atom.  The smallest unit of data or executable code.

    Merges quantum state mechanics, flavor-based configuration, entanglement,
    TTL messaging, and relational logic into the DOF runtime.

    ByteWord topology: [C V V V | T T T T]
        C = Captain bit  (computation space, transformative)
        V = Value field  (content space, dynamic)
        T = Type field   (identity space, static)
    """

    __slots__ = (
        "_id",
        "_state",
        "_flavor",
        "_value",
        "_type_history",
        "_entangled",
        "_subscribers",
        "_ttl",
        "_hash_cache",
        "_initialized",
    )

    # Relational atomistic logic — inherent when num atoms > 1
    case_base: ClassVar[Dict[str, Callable[..., Any]]] = {
        "⊤": lambda x, _: x,
        "⊥": lambda _, y: y,
        "¬": lambda a: not a,
        "∧": lambda a, b: a and b,
        "∨": lambda a, b: a or b,
        "→": lambda a, b: (not a) or b,
        "↔": lambda a, b: (a and b) or (not a and not b),
    }

    # Morphological symmetry axioms
    reflexivity: ClassVar[Callable[[T], bool]] = lambda x: x == x
    symmetry: ClassVar[Callable[[T, T], bool]] = lambda x, y: x == y
    transitivity: ClassVar[Callable[[T, T, T], bool]] = lambda x, y, z: (
        x == y and y == z
    )
    transparency: ClassVar[Callable[[Callable[..., T], T, T], Optional[T]]] = (
        lambda f, x, y: f(True, x, y) if x == y else None
    )

    def __init__(
        self,
        value: V,
        flavor: ByteWordFlavor = ByteWordFlavor.MUTABLE,
        state: QuantumState = QuantumState.SUPERPOSITION,
        ttl: int = 3,
    ) -> None:
        super().__init__()
        self._initialize_atom(value, flavor, state, ttl)

    def _initialize_atom(
        self, value: V, flavor: ByteWordFlavor, state: QuantumState, ttl: int
    ) -> None:
        """Idempotent atom initializer; safe for dataclass __post_init__ reuse."""
        self._id: str = uuid.uuid4().hex
        self._state: QuantumState = state
        self._flavor: ByteWordFlavor = flavor
        self._value: V = value
        self._type_history: List[str] = [
            type(value).__name__ if value is not None else "NoneType"
        ]
        self._entangled: List[weakref.ref] = []
        self._subscribers: set = set()
        self._ttl: int = ttl
        self._hash_cache: Optional[int] = None
        self._initialized: bool = False
        self._configure_flavor()

    # --- Flavor configuration ------------------------------------------------

    def _configure_flavor(self) -> None:
        """Apply flavor-specific initialization.  Extensible via super()."""
        if self._flavor == ByteWordFlavor.IMMUTABLE:
            self._freeze()
        elif self._flavor == ByteWordFlavor.HOMOICONIC:
            self._enable_introspection()
        elif self._flavor == ByteWordFlavor.POLYMORPHIC:
            self._enable_dynamic_typing()

    def _freeze(self) -> None:
        """Struct-like immutability.  Override __setattr__ for this instance."""
        original_setattr = self.__setattr__

        def frozen_setattr(name: str, value: Any) -> None:
            if hasattr(self, name) and not name.startswith("_"):
                raise AttributeError(f"Cannot modify frozen attribute: {name}")
            original_setattr(name, value)

        self.__setattr__ = frozen_setattr.__get__(self, type(self))  # type: ignore[method-assign]

    def _enable_introspection(self) -> None:
        """Code-as-data reflection.  Capture source and AST."""
        try:
            source = inspect.getsource(type(self))
            self._metadata["source"] = source
            self._metadata["ast"] = ast.dump(ast.parse(source))
        except OSError, TypeError:
            self._metadata["source"] = "<unavailable>"
            self._metadata["ast"] = "<unavailable>"

    def _enable_dynamic_typing(self) -> None:
        """Enable runtime type identity evolution tracking."""
        self._metadata["type_history"] = self._type_history

    # --- Quantum mechanics ---------------------------------------------------

    @property
    def id(self) -> str:
        """Unique atom identifier."""
        return self._id

    @property
    def state(self) -> QuantumState:
        """Current quantum state."""
        return self._state

    @property
    def flavor(self) -> ByteWordFlavor:
        """Structural flavor."""
        return self._flavor

    @property
    def observed(self) -> V:
        """
        Observed value.  Collapses superposition on first access.
        Measurement changes state.
        """
        if self._state == QuantumState.SUPERPOSITION:
            self._collapse_superposition()
        return self._value

    def _collapse_superposition(self) -> None:
        """Force state resolution.  Irreversible measurement."""
        if self._state == QuantumState.SUPERPOSITION:
            self._state = QuantumState.COLLAPSED
            logger.debug(f"Atom {self.id} collapsed to: {self._value!r}")

    def collapse(self) -> V:
        """Explicit measurement operation."""
        self._collapse_superposition()
        return self._value

    def entangle_with(self, other: Atom) -> None:
        """
        Create quantum entanglement.  Correlated measurement outcomes.
        Neither atom can be described independently after this.
        """
        if not isinstance(other, Atom):
            raise TypeError("Can only entangle with another Atom")

        self._entangled.append(weakref.ref(other))
        if not hasattr(other, "_entangled"):
            other._entangled = []
        other._entangled.append(weakref.ref(self))

        self._state = QuantumState.ENTANGLED
        other._state = QuantumState.ENTANGLED
        logger.debug(f"Entangled: {self.id[:8]} <-> {other.id[:8]}")

    # --- Messaging with TTL --------------------------------------------------

    async def send_message(self, message: Any, ttl: Optional[int] = None) -> None:
        """
        Broadcast message to subscribers with Time-To-Live.
        Prevents infinite loops in cyclic topologies.
        """
        ttl = self._ttl if ttl is None else ttl
        if ttl <= 0:
            logger.info(f"Message {message!r} dropped (TTL expired)")
            return

        logger.info(f"Atom {self.id[:8]} sending: {message!r}")
        for sub in list(self._subscribers):
            if isinstance(sub, Atom):
                await sub.receive_message(message, ttl - 1)

    async def receive_message(self, message: Any, ttl: int) -> None:
        """Process incoming message and propagate."""
        logger.info(f"Atom {self.id[:8]} received: {message!r} (TTL={ttl})")
        await self.send_message(message, ttl)

    def subscribe(self, atom: Atom) -> None:
        """Add subscriber for message propagation."""
        self._subscribers.add(atom)
        logger.info(f"Atom {self.id[:8]} subscribed to {atom.id[:8]}")

    def unsubscribe(self, atom: Atom) -> None:
        """Remove subscriber."""
        self._subscribers.discard(atom)
        logger.info(f"Atom {self.id[:8]} unsubscribed from {atom.id[:8]}")

    # --- Serialization interface ---------------------------------------------

    @abc.abstractmethod
    def encode(self) -> bytes:
        """Serialize to bytes.  Subclass must implement."""
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def decode(cls: Type[T], data: bytes) -> T:
        """Deserialize from bytes.  Subclass must implement."""
        raise NotImplementedError

    def to_dict(self) -> Dict[str, Any]:
        """Dictionary representation for interop."""
        return {
            "id": self.id,
            "state": self.state.name,
            "flavor": self.flavor.name,
            "value": self._value,
            "metadata": self._metadata,
            "birth_time_mono": self._birth_time_mono,
            "type_history": self._type_history,
        }

    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        """Reconstruct from dictionary."""
        atom = cls(
            value=data["value"],
            flavor=ByteWordFlavor[data["flavor"]],
            state=QuantumState[data["state"]],
        )
        atom._metadata = data.get("metadata", {})
        atom._birth_time_mono = data.get("birth_time_mono", time.monotonic())
        atom._type_history = data.get("type_history", [type(atom._value).__name__])
        return atom

    # --- Container & call protocols ------------------------------------------

    def __getitem__(self, key: Any) -> Any:
        return self._value[key]

    def __setitem__(self, key: Any, value: Any) -> None:
        self._value[key] = value

    def __delitem__(self, key: Any) -> None:
        del self._value[key]

    def __len__(self) -> int:
        return len(self._value)

    def __iter__(self):
        return iter(self._value)

    def __contains__(self, item: Any) -> bool:
        return item in self._value

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self._value(*args, **kwargs)

    def __bytes__(self) -> bytes:
        return (
            bytes(self._value) if isinstance(self._value, (bytes, bytearray)) else b""
        )

    @property
    def memory_view(self) -> memoryview:
        if isinstance(self._value, (bytes, bytearray)):
            return memoryview(self._value)
        raise TypeError("Unsupported type for memoryview")

    def __buffer__(self, flags: int) -> memoryview:  # PEP 688
        return memoryview(self._value)

    # --- Rich comparison & hashing -------------------------------------------

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Atom):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        if self._hash_cache is None:
            self._hash_cache = hash(self.id)
        return self._hash_cache

    # --- Introspection -------------------------------------------------------

    def introspect(self) -> str:
        """Reflect on its own code structure via AST."""
        try:
            source = inspect.getsource(self.__class__)
            return ast.dump(ast.parse(source))
        except OSError, TypeError:
            return "<introspection unavailable>"

    def process_attributes(
        self, mapping_description: Dict[str, Any], input_data: Dict[str, Any]
    ) -> None:
        """
        Use the mapper function to process input data and map it to attributes.
        """
        mapped_data = mapper(mapping_description, input_data)
        for key, value in mapped_data.items():
            if hasattr(self, key):
                setattr(self, key, value)

    # --- Repr ----------------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"id={self.id[:8]}..., "
            f"state={self.state.name}, "
            f"flavor={self.flavor.name}, "
            f"value={self._value!r})"
        )

    def __str__(self) -> str:
        return self.__repr__()


# ---------------------------------------------------------------------------
# 8.  BASE MODEL ATOM  —  validation, serialization, schema
# ---------------------------------------------------------------------------


class BaseModelAtom(Atom[Any, Any]):
    """
    Pydantic-style semantics with stdlib-only implementation.
    Provides field-level validation, deterministic serialization, schema
    generation, and immutable update operations.
    """

    __slots__ = ("__weakref__",)

    # --- Shared validators ---------------------------------------------------

    @staticmethod
    def must_be_str(x: Any) -> None:
        if not isinstance(x, str):
            raise ValueError(f"Expected a string, got {type(x).__name__}")

    @staticmethod
    def non_negative(x: Any) -> None:
        if not isinstance(x, (int, float)) or x < 0:
            raise ValueError(f"Expected a non-negative number, got {x!r}")

    @staticmethod
    def positive(x: Any) -> None:
        if not isinstance(x, (int, float)) or x <= 0:
            raise ValueError(f"Expected a positive number, got {x!r}")

    @staticmethod
    def non_empty_str(x: Any) -> None:
        if not isinstance(x, str) or not x.strip():
            raise ValueError(f"Expected a non-empty string, got {x!r}")

    # --- Validation chain ----------------------------------------------------

    def _validate_fields(self) -> None:
        """
        Validate all annotated fields after initialization.
        Called from DataclassAtom.__post_init__ via C3 MRO.
        """
        annotations = getattr(self, "__annotations__", {})
        for field_name, expected_type in annotations.items():
            # Skip ClassVar and private machinery
            if field_name.startswith("_"):
                continue
            try:
                value = getattr(self, field_name)
            except AttributeError:
                continue

            # Type validation
            if not _matches_type(value, expected_type):
                raise TypeError(
                    f"{self.__class__.__name__}.{field_name}: expected {expected_type}, "
                    f"got {type(value).__name__}"
                )

            # Metadata-based validation (dataclasses.field metadata)
            if dataclasses.is_dataclass(self.__class__):
                dc_field = next((f for f in fields(self) if f.name == field_name), None)
                if dc_field and dc_field.metadata:
                    validators = dc_field.metadata.get("validate")
                    if validators:
                        for validator in (
                            validators
                            if isinstance(validators, (list, tuple))
                            else (validators,)
                        ):
                            validator(value)

            # Method-based validation: validate_<field_name>
            validator_method = getattr(self, f"validate_{field_name}", None)
            if validator_method and callable(validator_method):
                if hasattr(validator_method, "_validators"):
                    for validator in validator_method._validators:
                        validator(value)
                else:
                    validator_method(value)

        # Model-level validation hook
        if hasattr(self, "_validate_model"):
            self._validate_model()

    def _validate_model(self) -> None:
        """Override for model-level validation logic."""
        pass

    # --- Core serialization --------------------------------------------------

    def to_dict(self, exclude_none: bool = False) -> Dict[str, Any]:
        """Convert to dictionary with nested model support."""
        result: Dict[str, Any] = {}
        if not dataclasses.is_dataclass(self):
            # Fallback to Atom.to_dict for non-dataclass instances
            return super().to_dict()

        for f in fields(self):
            value = getattr(self, f.name)
            if exclude_none and value is None:
                continue
            result[f.name] = _uncoerce(value)
        return result

    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        """Create instance from dictionary with nested model support and coercion."""
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

    # --- Immutable update ----------------------------------------------------

    def replace(self: T, **changes: Any) -> T:
        """Immutable clone with changes (dataclass-style)."""
        data = self.to_dict()
        data.update(changes)
        return self.__class__.from_dict(data)

    def clone(self: T, **overrides: Any) -> T:
        """Create a copy with optional field overrides (alias for replace)."""
        return self.replace(**overrides)

    # --- Multi-layer communication (datagrams) -------------------------------

    def to_datagram(
        self, format: SerializationFormat = SerializationFormat.JSON
    ) -> bytes:
        """Serialize to bytes for datagram transmission (UDP, etc.)."""
        if format == SerializationFormat.JSON:
            return json.dumps(self.to_dict()).encode("utf-8")
        elif format == SerializationFormat.PICKLE:
            return pickle.dumps(self)
        elif format == SerializationFormat.REPR:
            return repr(self).encode("utf-8")
        else:
            raise ValueError(f"Unsupported format: {format}")

    @classmethod
    def from_datagram(
        cls: Type[T],
        data: bytes,
        format: SerializationFormat = SerializationFormat.JSON,
    ) -> T:
        """Deserialize from bytes datagram."""
        if format == SerializationFormat.JSON:
            return cls.from_dict(json.loads(data.decode("utf-8")))
        elif format == SerializationFormat.PICKLE:
            return pickle.loads(data)
        elif format == SerializationFormat.REPR:
            raise NotImplementedError("REPR deserialization requires eval — unsafe")
        else:
            raise ValueError(f"Unsupported format: {format}")

    def to_json(self, *, indent: Optional[int] = None, sort_keys: bool = False) -> str:
        """Serialize to JSON string.  Deterministic if sort_keys=True."""
        return json.dumps(
            self.to_dict(),
            indent=indent,
            sort_keys=sort_keys,
            separators=(",", ":") if indent is None else None,
            ensure_ascii=False,
        )

    @classmethod
    def from_json(cls: Type[T], data: Union[str, bytes]) -> T:
        """Deserialize from JSON string/bytes."""
        if isinstance(data, (bytes, bytearray)):
            data = data.decode("utf-8")
        return cls.from_dict(json.loads(data))

    def to_base64(self, format: SerializationFormat = SerializationFormat.JSON) -> str:
        """Encode as base64 string for text-based protocols."""
        return base64.b64encode(self.to_datagram(format)).decode("ascii")

    @classmethod
    def from_base64(
        cls: Type[T],
        b64_str: str,
        format: SerializationFormat = SerializationFormat.JSON,
    ) -> T:
        """Decode from base64 string."""
        return cls.from_datagram(base64.b64decode(b64_str), format)

    # --- Identity & integrity ------------------------------------------------

    def fingerprint(self) -> str:
        """Content-based fingerprint for caching/deduplication."""
        content = json.dumps(self.to_dict(), sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def checksum(self) -> str:
        """Generate a checksum for data integrity verification."""
        return hashlib.md5(self.to_datagram()).hexdigest()

    # --- Schema & partial validation -----------------------------------------

    @classmethod
    def get_schema(cls) -> Dict[str, Any]:
        """Generate a basic schema for API documentation."""
        schema: Dict[str, Any] = {"type": "object", "properties": {}, "required": []}
        field_types = get_type_hints(cls)
        for f in fields(cls):
            field_type = field_types.get(f.name, Any)
            schema["properties"][f.name] = _type_to_schema(field_type)
            if f.default == f.default_factory == MISSING:
                schema["required"].append(f.name)
        return schema

    def validate_partial(self, **partial_data: Any) -> Dict[str, Any]:
        """
        Validate partial data without creating instance.
        Useful for PATCH operations.
        """
        field_types = get_type_hints(self.__class__)
        validated: Dict[str, Any] = {}
        for field_name, value in partial_data.items():
            if field_name in field_types:
                expected_type = field_types[field_name]
                if not _matches_type(value, expected_type):
                    raise TypeError(
                        f"{field_name}: expected {expected_type}, got {type(value).__name__}"
                    )
                validated[field_name] = _coerce(value, expected_type)
            else:
                raise ValueError(f"Unknown field: {field_name}")
        return validated

    # --- Diff ----------------------------------------------------------------

    def diff(self: T, other: T) -> Dict[str, Dict[str, Any]]:
        """Compare with another instance and return differences."""
        if not isinstance(other, self.__class__):
            raise TypeError(f"Can only diff with same type, got {type(other)}")
        diffs: Dict[str, Dict[str, Any]] = {}
        if not dataclasses.is_dataclass(self):
            return diffs
        for f in fields(self):
            self_val = getattr(self, f.name)
            other_val = getattr(other, f.name)
            if self_val != other_val:
                diffs[f.name] = {"self": self_val, "other": other_val}
        return diffs


# ---------------------------------------------------------------------------
# 9.  DATACLASS ATOM  —  mutable polymorphic base
# ---------------------------------------------------------------------------


@dataclass(slots=True)
class DataclassAtom(BaseModelAtom, Generic[T, V]):
    """
    Primary dataclass Atom.  The polymorphic base for dataclass-derived atoms.
    Mutable by default.  Not hash-flavored.

    Fields are ordered so that flavor precedes value; this ensures the
    flavor setter (if any) is populated before value assignment during
    generated __init__.
    """

    flavor: ByteWordFlavor = ByteWordFlavor.MUTABLE
    state: QuantumState = QuantumState.SUPERPOSITION
    ttl: int = 3
    value: Any = None

    def __post_init__(self) -> None:
        """
        Synchronize dataclass fields to Atom internal storage,
        initialize DOF/Atom internals that dataclass init bypassed,
        then run the validation chain.
        """
        # Sync dataclass fields -> Atom internals (uses object.__setattr__
        # so this path remains safe for frozen subclasses).
        object.__setattr__(self, "_flavor", self.flavor)
        object.__setattr__(self, "_state", self.state)
        object.__setattr__(self, "_ttl", self.ttl)
        object.__setattr__(self, "_value", self.value)

        # Initialize internals idempotently
        if not hasattr(self, "_id"):
            object.__setattr__(self, "_id", uuid.uuid4().hex)
            object.__setattr__(
                self,
                "_type_history",
                [type(self.value).__name__ if self.value is not None else "NoneType"],
            )
            object.__setattr__(self, "_entangled", [])
            object.__setattr__(self, "_subscribers", set())
            object.__setattr__(self, "_hash_cache", None)
            object.__setattr__(self, "_initialized", False)
            if not hasattr(self, "_dof_id"):
                DOF.__init__(self)

        # C3 validation chain
        self._validate_fields()
        self._validate_model()
        object.__setattr__(self, "_initialized", True)


# ---------------------------------------------------------------------------
# 10.  IMMUTABLE DATACLASS ATOM  —  hash-flavored struct
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class ImmutableDataclassAtom(DataclassAtom):
    """
    Hash-flavored dataclass Atom.  Immutable struct.
    Canonical identity suitable for dictionary keys and deduplication.
    """

    flavor: ByteWordFlavor = ByteWordFlavor.IMMUTABLE

    def __post_init__(self) -> None:
        super().__post_init__()
        # Precompute hash for canonical identity; stored in slot via
        # object.__setattr__ because we are inside frozen dataclass init.
        object.__setattr__(self, "_hash_cache", hash(self.id))


# ---------------------------------------------------------------------------
# 11.  DATA ATOM  —  vanilla data with structural numeric support
# ---------------------------------------------------------------------------


@dataclass(slots=True)
class DataAtom(DataclassAtom):
    """
    Vanilla data Atom with structural support for numeric primitives.
    Complex, integer, and float fields default to None but are
    type-validated when populated.
    """

    complex_value: Optional[complex] = None
    int_value: Optional[int] = None
    float_value: Optional[float] = None
    expected_type: Optional[Type] = None

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.expected_type is not None and self.value is not None:
            if not isinstance(self.value, self.expected_type):
                raise TypeError(
                    f"Value {self.value!r} does not match expected type {self.expected_type}"
                )

    def encode(self) -> bytes:
        """JSON encoding for data atoms."""
        return json.dumps(self.to_dict()).encode("utf-8")

    @classmethod
    def decode(cls: Type[T], data: bytes) -> T:
        """JSON decoding."""
        dict_data = json.loads(data.decode("utf-8"))
        return cls.from_dict(dict_data)


# ---------------------------------------------------------------------------
# 12.  DTO ATOM  —  datagram / DTO highest polymorph
# ---------------------------------------------------------------------------


@dataclass(slots=True)
class DTOAtom(DataAtom):
    """
    Data Transfer Object Atom.  Highest polymorph for mutable data
    interchange.  Optimized for wire serialization and LSP ontology.
    """

    def to_dto_dict(self) -> Dict[str, Any]:
        """DTO-optimized serialization excluding internal ghost state."""
        return self.to_dict(exclude_none=True)

    def to_datagram(
        self, format: SerializationFormat = SerializationFormat.JSON
    ) -> bytes:
        """Serialize to datagram bytes using DTO filter."""
        if format == SerializationFormat.JSON:
            return json.dumps(self.to_dto_dict()).encode("utf-8")
        return super().to_datagram(format)

    @classmethod
    def from_datagram(
        cls: Type[T],
        data: bytes,
        format: SerializationFormat = SerializationFormat.JSON,
    ) -> T:
        """Deserialize from datagram bytes."""
        if format == SerializationFormat.JSON:
            return cls.from_dict(json.loads(data.decode("utf-8")))
        return super().from_datagram(data, format)


# ---------------------------------------------------------------------------
# 13.  CODE ATOM  —  homoiconic executable
# ---------------------------------------------------------------------------


@dataclass(slots=True)
class CodeAtom(DataclassAtom):
    """
    Homoiconic code Atom.  Executable code as data.
    Supports source introspection and dynamic execution.
    """

    value: Callable = field(default=lambda: None)

    def __post_init__(self) -> None:
        if not callable(self.value):
            raise TypeError("CodeAtom requires callable value")
        super().__post_init__()
        object.__setattr__(self, "_flavor", ByteWordFlavor.HOMOICONIC)
        self._enable_introspection()

    def execute(self, *args: Any, **kwargs: Any) -> Any:
        """Execute contained code, forcing state collapse."""
        self.collapse()
        return self.value(*args, **kwargs)

    def encode(self) -> bytes:
        try:
            source = inspect.getsource(self.value)
            return source.encode("utf-8")
        except OSError, TypeError:
            return repr(self.value).encode("utf-8")

    @classmethod
    def decode(cls: Type[T], data: bytes) -> T:
        source = data.decode("utf-8")
        code_obj = compile(source, "<atom>", "exec")
        namespace: Dict[str, Any] = {}
        exec(code_obj, namespace)
        func = next((v for v in namespace.values() if callable(v)), None)
        if func is None:
            raise ValueError("No callable found in decoded source")
        return cls(value=func)


# ---------------------------------------------------------------------------
# 14.  INTERPRETER CONFIG  &  INTERPRETER ATOM
# ---------------------------------------------------------------------------


@dataclass(slots=True)
class InterpreterConfig:
    """Configuration for sub-interpreter execution."""

    mode: ExecutionMode = ExecutionMode.INTERPRETER
    shared_memory_size: int = 8192
    timeout: float = 10.0
    enable_lazy_verification: bool = True
    fallback_to_threading: bool = True


@dataclass(slots=True)
class InterpreterAtom(CodeAtom):
    """
    Atom that executes in isolated sub-interpreter.
    Falls back to threading if interpreter creation fails.
    """

    config: Optional[InterpreterConfig] = None
    execution_mode: ExecutionMode = ExecutionMode.INTERPRETER
    timeout: float = 10.0

    def __post_init__(self) -> None:
        super().__post_init__()
        object.__setattr__(self, "_interp", None)
        object.__setattr__(self, "_thread", None)
        object.__setattr__(self, "_result", None)
        object.__setattr__(self, "_error", None)
        object.__setattr__(self, "_channels", None)
        if self.config is None:
            object.__setattr__(self, "config", InterpreterConfig(timeout=self.timeout))

    def _create_interpreter(self) -> bool:
        """Attempt to create sub-interpreter."""
        if not HAS_INTERPRETERS:
            logger.warning("Sub-interpreters not available in this runtime")
            return False
        try:
            self._interp = interpreters.create()
            # Channel creation would go here if fully implemented
            logger.info(f"Created sub-interpreter for atom {self.id[:8]}")
            return True
        except Exception as e:
            logger.warning(f"Failed to create sub-interpreter: {e}")
            if self.config and self.config.fallback_to_threading:
                logger.info("Falling back to threading mode")
            return False

    def _execute_in_thread(self) -> None:
        """Fallback: execute in daemon thread."""

        def worker() -> None:
            try:
                self._result = self.value()
            except Exception as e:
                self._error = e

        self._thread = threading.Thread(target=worker, daemon=True)
        self._thread.start()
        assert self.config is not None
        self._thread.join(timeout=self.config.timeout)
        if self._thread.is_alive():
            logger.warning(f"Thread execution timeout for atom {self.id[:8]}")
            self._error = TimeoutError(f"Execution exceeded {self.config.timeout}s")

    def execute(self) -> Any:
        """Execute with interpreter-first strategy."""
        self.collapse()
        cfg = self.config
        assert cfg is not None

        if cfg.mode == ExecutionMode.INLINE:
            return self.value()

        if cfg.mode == ExecutionMode.INTERPRETER and self._create_interpreter():
            # Full sub-interpreter path elided for stdlib-only draft;
            # in a complete build the interpreter channel logic goes here.
            self._execute_in_thread()
        else:
            self._execute_in_thread()

        if self._error:
            raise self._error
        return self._result

    def cleanup(self) -> None:
        """Clean up interpreter resources."""
        if HAS_INTERPRETERS and self._interp is not None:
            try:
                if not self._interp.is_running():
                    self._interp.close()
                    logger.debug(f"Closed interpreter for atom {self.id[:8]}")
            except Exception:
                pass

    def encode(self) -> bytes:
        data = self.to_dict()
        data["config"] = {
            "mode": self.config.mode.name if self.config else "THREADED",
            "timeout": self.config.timeout if self.config else 10.0,
        }
        return json.dumps(data).encode("utf-8")

    @classmethod
    def decode(cls: Type[T], data: bytes) -> T:
        dict_data = json.loads(data.decode("utf-8"))
        config_data = dict_data.pop("config", {})
        atom = cls.from_dict(dict_data)
        if atom.config is not None:
            atom.config.mode = ExecutionMode[config_data.get("mode", "INTERPRETER")]
            atom.config.timeout = config_data.get("timeout", 10.0)
        return atom


# ---------------------------------------------------------------------------
# 15.  GRAMMAR RULE  &  MORPHIC RULE
# ---------------------------------------------------------------------------


@dataclass(slots=True)
class GrammarRule:
    """
    Represents a single grammar rule in a context-free grammar.
    """

    lhs: str
    rhs: List[Union[str, GrammarRule]]

    def __repr__(self) -> str:
        rhs_str = " ".join(str(elem) for elem in self.rhs)
        return f"{self.lhs} -> {rhs_str}"


@dataclass(slots=True)
class MorphicRule(GrammarRule):
    """
    Rules that map structural transformations in code morphologies.
    """

    symmetry: str = "Translation"
    conservation: str = "Information"

    def apply(self, input_seq: List[Any]) -> List[Any]:
        """Apply the morphological transformation to an input sequence."""
        if self.lhs in input_seq:
            idx = input_seq.index(self.lhs)
            return input_seq[:idx] + [elem for elem in self.rhs] + input_seq[idx + 1 :]
        return input_seq


# ---------------------------------------------------------------------------
# 16.  __ATOM__ PROTOCOL  &  ORNAMENT DECORATOR
# ---------------------------------------------------------------------------


@runtime_checkable
class __Atom__(Protocol):
    """
    Structural typing protocol for Atom conformance.
    Any ornamented class must expose at minimum an *id*.
    """

    id: str


def ornament(
    frozen: bool = False,
    final: bool = False,
    slots: bool = True,
    dataclass_kwargs: Optional[Dict[str, Any]] = None,
    **metadata: Any,
) -> Callable[[Type[T]], Type[T]]:
    """
    Master decorator consolidating all Atom decoration logic.

    Replaces the excessive stack of:
        @final
        @dataclass(frozen=True, slots=True)
        @__Atom__
    with a single @ornament(...) call.

    Steps
        1. Apply @final if requested.
        2. Apply @dataclass with merged kwargs.
        3. Wrap __post_init__ to inject idempotency-safe ID generation.
        4. Attach ornament metadata to the class.
    """

    def decorator(cls: Type[T]) -> Type[T]:
        # Step 1: finality
        if final:
            cls = typing.final(cls)

        # Step 2: dataclass
        dc_kwargs = dict(dataclass_kwargs or {})
        if frozen:
            dc_kwargs["frozen"] = True
        if slots:
            dc_kwargs["slots"] = True
        cls = dataclass(**dc_kwargs)(cls)

        # Step 3: wrap __post_init__ for ID injection
        original_post_init = getattr(cls, "__post_init__", lambda self: None)

        @wraps(original_post_init)
        def new_post_init(self: Any) -> None:
            if not hasattr(self, "_id"):
                object.__setattr__(self, "_id", uuid.uuid4().hex)
            original_post_init(self)

        cls.__post_init__ = new_post_init  # type: ignore[attr-defined]

        # Step 4: metadata & protocol conformance check
        cls._ornament = metadata  # type: ignore[attr-defined]
        if not isinstance(cls, __Atom__):
            # Structural check: ensure 'id' attribute exists or will exist
            if "id" not in getattr(cls, "__annotations__", {}):
                raise MorphologicalError(
                    f"Class {cls.__name__} missing required 'id' field for __Atom__ protocol"
                )

        return cls

    return decorator


# ---------------------------------------------------------------------------
# 17.  LSP ONTOLOGY DTOs  (immutable dataclass atoms)
# ---------------------------------------------------------------------------


@ornament(frozen=True, final=True)
class AnalyzerConfig(ImmutableDataclassAtom):
    """
    Immutable configuration for static analysis engine.
    Enforces security boundaries and resource limits.
    """

    allowed_source_roots: Tuple[Path, ...] = field(default_factory=tuple)
    max_file_size_bytes: int = 1 * 1024 * 1024  # 1 MiB
    max_request_body_size: int = 10 * 1024 * 1024  # 10 MiB
    source_encoding: str = "utf-8"
    allowed_extensions: Tuple[str, ...] = (".py", ".md", ".txt")
    hmac_secret_key: bytes = field(default_factory=lambda: os.urandom(32))

    def _validate_model(self) -> None:
        if not self.allowed_source_roots:
            raise ConfigurationError("allowed_source_roots cannot be empty")
        for p in self.allowed_source_roots:
            if not p.is_absolute():
                raise ConfigurationError(f"Path not absolute: {p}")
            if not p.exists() or not p.is_dir():
                raise ConfigurationError(f"Path does not exist or not a directory: {p}")
        if self.max_file_size_bytes <= 0:
            raise ConfigurationError("max_file_size_bytes must be positive")


@ornament(frozen=False, slots=True)
class RuntimeConfig(DataclassAtom):
    """Configuration for runtime execution."""

    mode: RuntimeMode = RuntimeMode.THREADED
    max_workers: int = 4
    shared_memory_size: int = 8192

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.mode == RuntimeMode.SUBINTERPRETER and not HAS_INTERPRETERS:
            logger.warning(
                "Sub-interpreters not available, falling back to THREADED mode"
            )
            self.mode = RuntimeMode.THREADED


@ornament(frozen=True, final=True)
class SourceRequest(ImmutableDataclassAtom):
    """Immutable analysis request."""

    source_path: Path = field(default_factory=Path)
    request_id: uuid.UUID = field(default_factory=uuid.uuid4)

    def __post_init__(self) -> None:
        super().__post_init__()
        if isinstance(self.source_path, str):
            object.__setattr__(self, "source_path", Path(self.source_path))


@ornament(frozen=True, final=True)
class AnalysisMetadata(ImmutableDataclassAtom):
    """Metadata for analysis results."""

    request_id: uuid.UUID = field(default_factory=uuid.uuid4)
    source_path: Path = field(default_factory=Path)
    source_hash_sha256: str = ""
    analysis_timestamp_utc: float = 0.0
    engine_version: str = "1.0.0"

    def __post_init__(self) -> None:
        super().__post_init__()
        if isinstance(self.source_path, str):
            object.__setattr__(self, "source_path", Path(self.source_path))


@ornament(frozen=True, final=True)
class SemanticGraph(ImmutableDataclassAtom):
    """Analysis result with semantic information."""

    source_artifact_hash: str = ""
    processed_at_unix_ts: float = 0.0
    engine_version: str = ""
    graph_data: Dict[str, Any] = field(default_factory=dict)
    signature_hmac_sha256: str = ""


@ornament(frozen=True, final=True)
class AnalysisResult(ImmutableDataclassAtom):
    """Complete analysis result with metadata."""

    metadata: AnalysisMetadata = field(default_factory=lambda: AnalysisMetadata())
    semantic_graph: Dict[str, Any] = field(default_factory=dict)

    def to_markdown(self) -> str:
        lines: List[str] = []
        meta = self.metadata
        sg = self.semantic_graph

        lines.append(f"# Python Module: `{meta.source_path.name}`")
        lines.append(f"- **Hash**: `{meta.source_hash_sha256[:16]}`")
        lines.append(f"- **Analyzed**: `{time.ctime(meta.analysis_timestamp_utc)}`")
        lines.append("")

        lines.append("## Functions")
        for f in sg.get("functions", []):
            args = ", ".join(f["args"])
            decs = " ⟶ " + ", ".join(f["decorators"]) if f.get("decorators") else ""
            line = f"- `{f['name']}({args})` (line {f['lineno']}){decs}"
            lines.append(line)

        lines.append("\n## Classes")
        for c in sg.get("classes", []):
            bases = " → " + ", ".join(c["bases"]) if c.get("bases") else ""
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


@ornament(frozen=True, final=True)
class MarkdownSection(ImmutableDataclassAtom):
    title: str = ""
    level: int = 0
    start_line: int = 0
    end_line: int = 0
    parent_section: Optional[str] = None


@ornament(frozen=True, final=True)
class MarkdownGraph(ImmutableDataclassAtom):
    sections: List[MarkdownSection] = field(default_factory=list)
    links: List[Dict[str, Any]] = field(default_factory=list)
    backlinks: List[str] = field(default_factory=list)
    path_hierarchy: List[str] = field(default_factory=list)


@ornament(frozen=True, final=True)
class LspMessage(ImmutableDataclassAtom):
    jsonrpc: str = "2.0"
    id: Optional[int] = None
    method: Optional[str] = None
    params: Optional[Dict[str, Any]] = None
    result: Optional[Any] = None
    error: Optional[Dict[str, Any]] = None


# ---------------------------------------------------------------------------
# 18.  MODULE EXPORTS  (optional __all__ for literate clarity)
# ---------------------------------------------------------------------------

__all__ = [
    # Enums
    "QuantumState",
    "ByteWordFlavor",
    "SerializationFormat",
    "ExecutionMode",
    "RuntimeMode",
    # Exceptions
    "ConfigurationError",
    "MorphologicalError",
    # Bedrock
    "DOF",
    "Atom",
    "BaseModelAtom",
    "DataclassAtom",
    "ImmutableDataclassAtom",
    "DataAtom",
    "DTOAtom",
    "CodeAtom",
    "InterpreterAtom",
    "InterpreterConfig",
    # Grammar
    "GrammarRule",
    "MorphicRule",
    # Decoration
    "__Atom__",
    "ornament",
    # LSP DTOs
    "AnalyzerConfig",
    "RuntimeConfig",
    "SourceRequest",
    "AnalysisMetadata",
    "SemanticGraph",
    "AnalysisResult",
    "MarkdownSection",
    "MarkdownGraph",
    "LspMessage",
]
