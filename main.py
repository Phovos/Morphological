#!/usr/bin/env -S uv run
# -*- coding: utf-8 -*-
# /* script
# requires-python = ">=3.14"
# dependencies = [
#     "uv==*.*",
# ]
#   "Morphological Source Code: MSC&QSD": >
#   "© 2026 `Phovos` (phovos@outlook.com)":
#     - https://gitlab.com/morphological/source/code
#     - https://github.com/Morphological-Source-Code
#     - https://reddit.com/r/morphological
#   © 2024-2026 Phovos; https://github.com/Phovos/Morphological-Source-Code
#   © 2023-2026 Moonlapsed; https://github.com/MOONLAPSED/cognosis
#   description: >
#     This project employs a layered licensing approach governed by the incl. Morphological LICENSE;
#     The architecture (MSC&QSD) distinguishes between:
#       (1) Individual source files, like this one (BSD 3-Clause)
#       (2) Distributed collective works (CC BY-NC-SA 4.0)
#       (3) Quine-generated outputs (CC0 1.0 + mandatory thermodynamic ledger)
#       (4) Private ensemble configurations (operator's IP, until revealed/released)
#           - Privacy of your Quineic-output is, therefore, your prerogative. CC0 carries, after 'escape'/release
# ------------------------------
# CPy3.14 std libs ONLY ;
# Platform(s): (5600xRyzen (NA); hypervisor)
# Win11: (production); Ubuntu-22.04: (dev, staging)
# Optional dependency handling: "also add to '/* script..' comment (just above)"
# ------------------------------
import ast, os, sys, pathlib, logging, threading, datetime, inspect, uuid, base64, json, asyncio, functools, time, random, queue, hashlib, math, cmath, hashlib, enum, re, types, dataclasses, typing, contextlib, collections, abc, io, string, itertools, operator, copy, weakref, gc, marshal, struct, array, mmap, ssl, socket, concurrent, multiprocessing, subprocess, tempfile, shutil, glob, fnmatch, csv, pickle, sqlite3, urllib, http, ftplib, smtplib, email, mimetypes, imaplib, mailbox, hmac, secrets, ipaddress, socketserver, http.server, xml, html, webbrowser, tkinter, ctypes, ctypes.wintypes, site   # noqa: E401, F401, F811, E702 # fmt: skip
from dataclasses import dataclass, field; from enum import Enum, auto, IntEnum; from types import SimpleNamespace, ModuleType; from functools import lru_cache; from decimal import Decimal, getcontext; from typing import Any, Dict, Optional, Set, Type, Union, Callable, List, Tuple, Generic, TypeVar, Protocol, runtime_checkable, cast, get_origin, get_args; from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer; from socketserver import ThreadingMixIn; from contextlib import contextmanager; from concurrent import interpreters; from concurrent.futures import ThreadPoolExecutor; # noqa: E401, F401, F811, E702 # fmt: skip
_LOGGER_INIT_LOCK = threading.Lock();Path= pathlib.Path(__file__).resolve(); Queue = queue.Queue ;  # noqa: E702 # fmt: skip;

# =================
# CORE MSC TYPES
# =================

# ── What a t-string actually IS ───────────────────────────────────────────
from string.templatelib import Template, Interpolation
name = "Observable"
variance = "covariant"
tmpl: Template = t"_{name}_co  [{variance}]"
# A Template is an iterable of alternating str and Interpolation chunks:
for part in tmpl:
    if isinstance(part, str):
        print(f"  literal:  {part!r}")
    else:  # Interpolation
        print(f"  interp:   value={part.value!r}  expr={part.expression!r}")

# Output:
#   literal:  '_'
#   interp:   value='Observable'  expr='name'
#   literal:  '_co  ['
#   interp:   value='covariant'   expr='variance'
#   literal:  ']'

# ── Why you can't just str() a Template ───────────────────────────────────
# str(tmpl)  →  TypeError (or returns something like "<Template ...>")
# This is intentional: t-strings keep values *separate* so a renderer
# can sanitize/escape/log them.  f"" would have already collapsed everything.

# ── _tv: the minimal "just give me the flat string" renderer ──────────────

def _tv(template: Template) -> str:
    return "".join(
        part if isinstance(part, str) else str(part.value) for part in template
    )
print(_tv(t"_{name}_co"))  # → '_Observable_co'

_F_ = TypeVar(
    "F", bound=any
)  # equiv to the function/combinator f (that is being computed); not VOID, identity; idempotent wrt 'a runtime'

# With an f-string the name is gone at parse time:
#   f"_{name}_co"  →  '_Observable_co'   (opaque string, can't inspect)
#
# With a t-string you still have the Template object before rendering,
# so you can do things like:

def validate_typevar_name(tmpl: Template) -> str:
    """Render, but assert no interpolated value is empty or contains spaces."""
    for part in tmpl:
        if isinstance(part, Interpolation):
            val = str(part.value)
            if not val or " " in val:
                raise ValueError(
                    f"TypeVar name fragment {part.expression!r} "
                    f"resolved to invalid segment: {val!r}"
                )
    return _tv(tmpl)

# ── Applied to TypeVars ──────────────────────────────────────────────
from typing import TypeVar, Callable, Union, Any
# ==== ENUMS, STATIC/DYNAMIC Holographic type system
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

_T = TypeVar('_T', bound=Any)
_V = TypeVar('_V', bound=Union[int, float, str, bool])
_C_anti = TypeVar('_C_anti', bound=Callable[..., Any], contravariant=True)
# The composite name is *readable* as a template before it collapses:
_C_super = TypeVar(
    validate_typevar_name(t"C|{_V.__name__}|{_T.__name__}|C_anti"),
    bound=Callable[..., Any],
)
print(_C_super.__name__)  # → 'C|_V|_T|C_anti'
# ── Bonus: a logging-aware renderer ───────────────────────────────────────
import logging
def _tv_debug(template: Template) -> str:
    """Like _tv but logs each interpolated segment - useful during refactors."""
    parts = []
    for part in template:
        if isinstance(part, str):
            parts.append(part)
        else:
            rendered = str(part.value)
            logging.debug("t-string segment  %r → %r", part.expression, rendered)
            parts.append(rendered)
    return "".join(parts)

class ExecutionMode(IntEnum):
    """Runtime architecture selection"""

    INTERPRETER = 0  # Sub-interpreter isolation
    THREAD = 1  # Threading fallback
    INLINE = 2  # Direct execution
    ASYNC = 3  # Async/await


class ByteWordFlavor(IntEnum):
    """Memory representation modes"""

    MUTABLE = 0  # Standard mutable dataclass
    IMMUTABLE = 1  # Frozen struct-like
    HOMOICONIC = 2  # Code-as-data representation
    POLYMORPHIC = 3  # Dynamic type identity


class WordSize(enum.IntEnum):
    """Standardized computational word sizes"""

    BYTE = 1  # 8-bit
    SHORT = 2  # 16-bit
    INT = 4  # 32-bit
    LONG = 8  # 64-bit


class WordAlignment(IntEnum):
    UNALIGNED = 1
    WORD = 2
    DWORD = 4
    QWORD = 8
    CACHE_LINE = 64
    PAGE = 4096


class QuantumState(enum.Enum):
    """
    Quantum states for chiral quines, inspired by Wigner's Friend and Barandes' stochastic mechanics, amongst others.
    Maps to Morphology (MARKOVIAN, NON_MARKOVIAN) for non-Markovian tape evolution.
    Each state represents a ByteWord's epistemic role in the T/V/C toople:
    - Type: Tape (poset/frozenset) evolves via chiral tx (-1, 0, 1).
    - Value: Semantic vector (posit) tracks position with chiral updates.
    - Code: QOperator evolves ByteWords as quantum-like states.

    Zeroth Law (Holographic Foundation):
    
    Symbols and observations are perceived as real due to intrinsic system properties, creating self-consistent realities. 
    """

    SUPERPOSITION = 1  # Handle-only state, like a MARKOVIAN (-1) ByteWord with chiral tx (-1), history-dependent.
    ENTANGLED = 2  # Referenced but not materialized, like NON_MARKOVIAN (math.e), reversible with energy cost.
    COLLAPSED = 4  # Materialized state, like a stable quine (SmallTalk object), executable after measurement.
    DECOHERENT = 8  # Garbage-collected state, reversible only by re-running with new chiral tape (thermodynamic cost).
    EIGENVECTOR = 16
    def measure(self) -> int:
        """
        Perform a measurement on the quantum state.
        Returns the index of the basis state that was measured.
        """
        # Calculate probabilities for each basis state
        probabilities = []
        for amp in self.amplitudes:
            # Probability is |amplitude|²
            prob = amp.real**2 + amp.imag**2
            probabilities.append(prob)
        # Simulate measurement using the probabilities
        import random
        r = random.random()
        cumulative_prob = 0
        for i, prob in enumerate(probabilities):
            cumulative_prob += prob
            if r <= cumulative_prob:
                return i
        # Fallback (shouldn't happen with normalized state)
        return len(self.amplitudes) - 1
    def superposition(self, other: 'QuantumState', coeff1: MorphicComplex, coeff2: MorphicComplex) -> 'QuantumState':
        """
        Create a superposition of two quantum states.
        |ψ⟩ = a|ψ₁⟩ + b|ψ₂⟩
        """
        if self.space.dimension != other.space.dimension:
            raise ValueError("Quantum states must belong to same Hilbert space")
        new_amplitudes = []
        for i in range(len(self.amplitudes)):
            new_amp = (self.amplitudes[i] * coeff1) + (other.amplitudes[i] * coeff2)
            new_amplitudes.append(new_amp)
        return QuantumState(new_amplitudes, self.space)
    def entangle(self, other: 'QuantumState') -> 'QuantumState':
        """
        Create an entangled state from two quantum states.
        |ψ⟩ = (|ψ₁⟩|0⟩ + |ψ₂⟩|1⟩)/√2
        This is a simplified version of entanglement for demonstration.
        """
        # For simplicity, we'll just return a superposition
        coeff = MorphicComplex(1/math.sqrt(2), 0)
        return self.superposition(other, coeff, coeff)

    def transition(self, operator: 'OperatorType') -> 'QuantumState':
        """
        Transition between quantum states based on OperatorType.
        - MEASUREMENT collapses SUPERPOSITION/ENTANGLED to COLLAPSED.
        - ADJOINT reverses COLLAPSED to ENTANGLED with energy cost.
        - DECOHERENT stays unless reset (re-run).
        """
        if operator == OperatorType.MEASUREMENT:
            if self in (QuantumState.SUPERPOSITION, QuantumState.ENTANGLED):
                return QuantumState.COLLAPSED
        elif operator == OperatorType.ADJOINT and self == QuantumState.COLLAPSED:
            return QuantumState.ENTANGLED
        elif self == QuantumState.DECOHERENT and operator == OperatorType.COMPOSITION:
            return QuantumState.SUPERPOSITION
        return self

class Morphology(enum.Enum):
    """
    Represents the floor morphic state of a BYTE_WORD.
    C = 0: Floor morphic state (stable, low-energy)
    C = 1: Dynamic or high-energy state
    The control bit (C) indicates whether other holoicons can point to this holoicon:
    - DYNAMIC (1): Other holoicons CAN point to this holoicon
    - MORPHIC (0): Other holoicons CANNOT point to this holoicon
    This ontology maps to thermodynamic character: intensive & extensive.
    A 'quine' (self-instantiated runtime) is a low-energy, intensive system,
    while a dynamic holoicon is a high-energy, extensive system inherently
    tied to its environment.
    """
    MORPHIC = 0      # Stable, low-energy state
    DYNAMIC = 1      # High-energy, potentially transformative state
    # Fundamental computational orientation and symmetry
    MARKOVIAN = -1    # Forward-evolving, irreversible
    NON_MARKOVIAN = cmath.sqrt(-1j)  # Reversible, with memory
    # Endianness representation
    LITTLE_ENDIAN = auto()  # LSB-first, canonical smaller representation
    BIG_ENDIAN = auto()  # MSB-first, extended representation

    # Bit masks
    LSB_MASK = 0b00001111  # Mask for Least Significant Bits
    MSB_MASK = 0b11110000  # Mask for Most Significant Bits

    @staticmethod
    def extract_lsb(state: Union[str, int, bytes], word_size: int) -> Any:
        """Extract least significant bit/byte based on word size"""
        if word_size == 1:
            return state[-1] if isinstance(state, str) else str(state)[-1]
        elif word_size == 2:
            return (
                state & 0xFF
                if isinstance(state, int)
                else state[-1]
                if isinstance(state, bytes)
                else state.encode()[-1]
            )

    def least_significant_unit(state: StateHash, word_size: int, 
                            MaxCache: int = 1_000) -> Any:
        """
        Extracts the least significant unit of a given state based on word_size.
        Uses an in-memory cache to avoid redundant computation.
        Args:
            state: The state to analyze.
            word_size: The size of the word (1=BYTE, 2=SHORT, 4=INT, 8=LONG).
            max_cache_size: Maximum size of the cache to prevent memory issues.
        Returns:
            The least significant unit of the state.
        """
        # Manage cache size
        if len(_lsu_cache) > MaxCache:
            # Clear 25% of the cache when it gets too big
            keys_to_remove = list(_lsu_cache.keys())[:MaxCache // 4]
            for key in keys_to_remove:
                _lsu_cache.pop(key)
        
        cache_key = (state, word_size)
        if cache_key in _lsu_cache:
            return _lsu_cache[cache_key]
        result = None
        if word_size == WordSize.BYTE:  # BYTE (8-bit)
            if isinstance(state, int):
                result = state & 0xFF  # Extract least significant byte
            elif isinstance(state, bytes):
                result = state[-1] if state else 0
            elif isinstance(state, str):
                result = ord(state[-1]) if state else 0
            else:
                # Handle other types by converting to bytes first
                result = int(hash_state(state) & 0xFF)
        elif word_size == WordSize.SHORT:  # SHORT (16-bit)
            if isinstance(state, int):
                result = state & 0xFFFF  # Extract least significant 2 bytes
            elif isinstance(state, bytes):
                result = int.from_bytes(state[-2:].rjust(2, b'\0'), byteorder='little')
            elif isinstance(state, str):
                encoded = state.encode()
                result = int.from_bytes(encoded[-2:].rjust(2, b'\0'), byteorder='little')
            else:
                # Handle other types by converting to bytes first
                result = int(hash_state(state) & 0xFFFF)
        elif word_size >= WordSize.INT:  # INT/LONG (32/64-bit)
            if isinstance(state, int):
                mask = (1 << (word_size * 8)) - 1
                result = state & mask
            elif isinstance(state, (str, bytes)):
                data = state.encode() if isinstance(state, str) else state
                hash_value = hashlib.sha256(data).digest()
                result = int.from_bytes(hash_value[:word_size], byteorder='little')
            elif isinstance(state, dict):
                if not state:
                    result = 0
                else:
                    # More sophisticated approach for dictionaries
                    key_hash = hash_state(tuple(sorted(str(k) for k in state.keys())))
                    val_hash = hash_state(tuple(str(v) for v in state.values()))
                    combined = (key_hash ^ val_hash) & ((1 << (word_size * 8)) - 1)
                    result = combined
            else:
                result = hash_state(state) & ((1 << (word_size * 8)) - 1)
        else:
            raise ValueError(f"Unsupported word_size: {word_size}")
        # Cache the result
        _lsu_cache[cache_key] = result
        return result



"""Core Operators:

Composition (@): Sequential application of operations
Tensor Product (*): Parallel combination of operations
Direct Sum (+): Alternative pathways of computation
Adjoint (†): Reversal/dual of operations

Algebraic Properties:

Associativity: (A @ B) @ C = A @ (B @ C)
Distributivity: A * (B + C) = (A * B) + (A * C)
Adjoint rules: (A @ B)† = B† @ A†"""
T = TypeVar('T')  # Type structure
V = TypeVar('V')  # Value space
C = TypeVar('C')  # Control/Computation space
# Covariant and contravariant versions
T_co = TypeVar('T_co', covariant=True)  # Type with covariance (Markovian)
V_co = TypeVar('V_co', covariant=True)  # Value with covariance (Markovian)
C_co = TypeVar('C_co', covariant=True)  # Control with covariance (Markovian)
T_anti = TypeVar('T_anti', contravariant=True)  # Type with contravariance
V_anti = TypeVar('V_anti', contravariant=True)  # Value with contravariance
C_anti = TypeVar('C_anti', contravariant=True)  # Control with contravariance
_C_ = TypeVar(
    'Dunder_C', covariant=True
)  # Morphic V-bit which replaes the MSB C bit in deputization cycle: < 0 _C_ _C_ _C_ | TTTT >


class Symmetry(Enum):
    TRANSLATION = "Translation"
    ROTATION = "Rotation"
    PHASE = "Phase"


class Conservation(Enum):
    INFORMATION = "Information"
    COHERENCE = "Coherence"
    BEHAVIORAL = "Behavioral"

def popcount(x: int) -> int:
    """Hamming weight for small ints."""
    return bin(x & 0xFF).count("1")


def phase_from_popcount(n: int) -> complex:
    """Map popcount -> 8th root of unity: exp(i * pi/4 * n)."""
    return cmath.exp(1j * (math.pi / 4.0) * (n % 8))

@runtime_checkable
class Symmetry(Protocol[T, V, C]):
    """
    Defines symmetry operations preserving structure under transformations.
    Implements Noether's theorem: symmetries imply conserved quantities.
    """

    def preserve_identity(self, type_structure: T) -> T:
        """Type-level identity preservation"""
        ...

    def preserve_content(self, value_space: V) -> V:
        """Value-level content preservation"""
        ...

    def preserve_behavior(self, computation: C) -> C:
        """Computation-level behavior preservation"""
        ...
def quantum_extract(state, word_size, extraction_strategy="entropy"):
    """
    Extract bits with cognitive awareness of extraction method
    Args:
        state: Input state (str, int, bytes)
        word_size: Desired word size
        extraction_strategy: 'entropy', 'locality', 'coherence'
    """
    strategies = {
        "entropy": lambda s: hashlib.sha256(str(s).encode()).digest()[-1],
        "locality": lambda s: (hash(s) & 0xFF) ^ word_size,
        "coherence": lambda s: sum(bin(ord(c)).count("1") for c in str(s)) % 256,
    }
    if word_size >= 3:
        # Use cryptographic hash for larger word sizes
        if isinstance(state, (str, bytes)):
            return hashlib.sha256(state.encode() if isinstance(state, str) else state).digest()[-1]
        return hash(state) & 0xFF  # Fallback hash strategy
    return strategies.get(extraction_strategy, strategies["entropy"])(state)


@dataclass
class OrderParameter:
    """Tracks symmetry breaking in a phase transition system."""

    value: complex
    preserved_symmetries: Set[str]
    broken_symmetries: Set[str]

    def break_symmetry(self, sym: str) -> None:
        """Move symmetry from preserved to broken."""
        if sym in self.preserved_symmetries:
            self.preserved_symmetries.remove(sym)
            self.broken_symmetries.add(sym)

    def restore_symmetry(self, sym: str) -> None:
        """Move symmetry from broken back to preserved."""
        if sym in self.broken_symmetries:
            self.broken_symmetries.remove(sym)
            self.preserved_symmetries.add(sym)

# ============================================================================
# QUANTUM OPERATOR ALGEBRA
# ============================================================================


class OperatorType(Enum):
    """Fundamental operation types in our computational 'universe', referring explicitly to the universal-set [], and given the null set (a 00000000 ByteWord) as 'glue' (insofar as sheafification, groups, topos etc). The 'universe' of runtime, the applied set, is strictly-bounded and inertia-local, no relativistic effects outside of the 'relativistic effects' of morphological derivation (or time-like integration)* with respect to the cross-product of two cartesian coordinates in super position; a 'Born Rule'-type ontological scaffolding."""

    COMPOSITION = auto()  # Function composition (f >> g)
    TENSOR = auto()  # Tensor product (⊗)
    DIRECT_SUM = auto()  # Direct sum (⊕)
    OUTER = auto()  # Outer product (|ψ⟩⟨φ|)
    ADJOINT = auto()  # Hermitian adjoint (†)
    MEASUREMENT = auto()  # Quantum measurement (⟨M|ψ⟩)

    SYMBOL_MAP: ClassVar[Dict['OperatorType', str]] = {
        COMPOSITION: '>>',
        TENSOR: '⊗',
        DIRECT_SUM: '⊕',
        OUTER: '|⟩⟨|',
        ADJOINT: '†',
        MEASUREMENT: 'M',
    }

    @property
    def symbol(self) -> str:
        return self.SYMBOL_MAP.get(self, str(self.value))

    def as_tstring(self) -> str:
        return f"{self.name} = {self.symbol}"

class QuineOperator:
    """Mapping from ByteWord states to themselves (linearized in C^256)"""

    def __init__(self, mapping: Dict[int, int]):
        self.mapping = mapping
        self.N = 256

    def build_matrix(self) -> list[list[complex]]:
        """Column-major sparse representation (256x256)"""
        M = [[0.0 + 0.0j] * self.N for _ in range(self.N)]
        for i in range(self.N):
            j = self.mapping.get(i, i)
            M[j][i] = 1.0
        return M

    @staticmethod
    def is_unitary(M: list[list[complex]], tol=1e-9) -> bool:
        N = len(M)
        for i in range(N):
            for j in range(N):
                s = sum(M[k][i].conjugate() * M[k][j] for k in range(N))
                if i == j and abs(s - 1.0) > tol:
                    return False
                elif i != j and abs(s) > tol:
                    return False
        return True

    @staticmethod
    def is_hermitian(M: list[list[complex]], tol=1e-9) -> bool:
        N = len(M)
        for i in range(N):
            for j in range(N):
                if abs(M[i][j] - M[j][i].conjugate()) > tol:
                    return False
        return True

# Pi with high precision
PI = Decimal('3.1415926535897932384626433832795028841971693993751058209749445923')
E = Decimal('2.7182818284590452353602874713526624977572470936999595749669676277')
I_UNIT = complex(0, 1)  # Standard imaginary unit for reference

@dataclass
class TranscendentalConstant:
    """Represents a transcendental constant like π or e with arbitrary precision"""
    symbol: str
    value: Decimal
    
    def __str__(self) -> str:
        return f"{self.symbol}({self.value})"

# Core transcendental constants
PI_CONST = TranscendentalConstant('π', PI)
E_CONST = TranscendentalConstant('e', E)
def fourier_coefficient(n: int, func: Callable[[float], PiComplex]) -> PiComplex:
    return PiComplex.from_polar(
        modulus=Decimal(1),
        argument=Decimal(2 * math.pi * n)
    )

class PiComplex(Generic[T, V, C]):
    """
    Complex number implementation with pi as a fundamental operator.
    The imaginary unit i is intrinsically tied to π through e^(iπ) = -1
    """
    def __init__(self, real: Union[int, float, Decimal] = 0, 
                 imag: Union[int, float, Decimal] = 0,
                 pi_factor: Union[int, float, Decimal] = 0,
                 e_factor: Union[int, float, Decimal] = 0):
        """
        Initialize with separate components for direct real, imaginary, 
        and transcendental factors (pi and e)
        """
        self.real = Decimal(str(real))
        self.imag = Decimal(str(imag))
        self.pi_factor = Decimal(str(pi_factor))
        self.e_factor = Decimal(str(e_factor))
        self._normalize()
    
    def _normalize(self) -> None:
        """
        Normalize representation by applying transcendental operations
        e^(iπ) = -1 means pi_factor of 1 contributes -1 to the real part
        """
        # Pi normalization (e^(iπ) = -1)
        if self.pi_factor != 0:
            # Each complete pi rotation contributes -1^n to real part
            whole_rotations = int(self.pi_factor)
            if whole_rotations != 0:
                factor = Decimal(-1) ** whole_rotations
                self.real *= factor
                self.imag *= factor
            
            # Remaining partial pi adds phase rotation
            partial_pi = self.pi_factor - whole_rotations
            if partial_pi != 0:
                # e^(i·partial_pi) gives cos(partial_pi) + i·sin(partial_pi)
                phase_real = Decimal(math.cos(float(partial_pi * PI)))
                phase_imag = Decimal(math.sin(float(partial_pi * PI)))
                
                # Complex multiplication
                new_real = self.real * phase_real - self.imag * phase_imag
                new_imag = self.real * phase_imag + self.imag * phase_real
                self.real, self.imag = new_real, new_imag
            
            self.pi_factor = Decimal(0)
        
        # E normalization
        if self.e_factor != 0:
            scale = Decimal(math.exp(float(self.e_factor)))
            self.real *= scale
            self.imag *= scale
            self.e_factor = Decimal(0)
    
    def inner_product(self, other: PiComplex) -> PiComplex:
        """
        Calculate Hilbert space inner product <self|other>
        In complex vector spaces, this is self.conjugate() * other
        """
        conj = self.conjugate()
        return PiComplex(
            real=conj.real * other.real + conj.imag * other.imag,
            imag=conj.real * other.imag - conj.imag * other.real
        )
    
    def conjugate(self) -> PiComplex:
        """Return complex conjugate"""
        return PiComplex(real=self.real, imag=-self.imag)
    
    def modulus(self) -> Decimal:
        """Return the modulus (magnitude)"""
        return Decimal(math.sqrt(float(self.real**2 + self.imag**2)))
    
    def argument(self) -> Decimal:
        """Return the argument (phase angle in radians)"""
        return Decimal(math.atan2(float(self.imag), float(self.real)))
    
    def __add__(self, other: Union[PiComplex, int, float, Decimal]) -> PiComplex:
        if isinstance(other, (int, float, Decimal)):
            return PiComplex(real=self.real + Decimal(str(other)), imag=self.imag)
        return PiComplex(
            real=self.real + other.real,
            imag=self.imag + other.imag,
            pi_factor=self.pi_factor + other.pi_factor,
            e_factor=self.e_factor + other.e_factor
        )
    
    def __mul__(self, other: Union[PiComplex, int, float, Decimal]) -> PiComplex:
        if isinstance(other, (int, float, Decimal)):
            other_val = Decimal(str(other))
            return PiComplex(
                real=self.real * other_val,
                imag=self.imag * other_val,
                pi_factor=self.pi_factor * other_val,
                e_factor=self.e_factor * other_val
            )
        
        # First normalize both numbers
        self._normalize()
        other_copy = PiComplex(
            other.real, other.imag, other.pi_factor, other.e_factor
        )
        other_copy._normalize()
        
        # Standard complex multiplication
        return PiComplex(
            real=self.real * other_copy.real - self.imag * other_copy.imag,
            imag=self.real * other_copy.imag + self.imag * other_copy.real
        )
    
    def __truediv__(self, other: Union[PiComplex, int, float, Decimal]) -> PiComplex:
        if isinstance(other, (int, float, Decimal)):
            other_val = Decimal(str(other))
            return PiComplex(
                real=self.real / other_val,
                imag=self.imag / other_val,
                pi_factor=self.pi_factor / other_val,
                e_factor=self.e_factor / other_val
            )
            
        # For complex division, multiply by conjugate of denominator
        self._normalize()
        other_copy = PiComplex(
            other.real, other.imag, other.pi_factor, other.e_factor
        )
        other_copy._normalize()
        
        denom = other_copy.real**2 + other_copy.imag**2
        return PiComplex(
            real=(self.real * other_copy.real + self.imag * other_copy.imag) / denom,
            imag=(self.imag * other_copy.real - self.real * other_copy.imag) / denom
        )
    
    def __neg__(self) -> PiComplex:
        return PiComplex(
            real=-self.real,
            imag=-self.imag,
            pi_factor=-self.pi_factor,
            e_factor=-self.e_factor
        )
    
    def __sub__(self, other: Union[PiComplex, int, float, Decimal]) -> PiComplex:
        return self + (-other if isinstance(other, PiComplex) else -Decimal(str(other)))
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PiComplex):
            return False
        self._normalize()
        other._normalize()
        return (self.real == other.real and 
                self.imag == other.imag)
    
    def __str__(self) -> str:
        self._normalize()  # Ensure normalized form for display
        if self.imag == 0:
            return f"{self.real}"
        if self.real == 0:
            return f"{self.imag}i"
        sign = "+" if self.imag >= 0 else "-"
        return f"{self.real} {sign} {abs(self.imag)}i"
    
    def __repr__(self) -> str:
        return f"PiComplex(real={self.real}, imag={self.imag})"
    
    @classmethod
    def from_polar(cls, modulus: Decimal, argument: Decimal) -> PiComplex:
        """Create complex number from polar coordinates"""
        return cls(
            real=modulus * Decimal(math.cos(float(argument))),
            imag=modulus * Decimal(math.sin(float(argument)))
        )
    
    @classmethod
    def from_pi_multiple(cls, multiple: Decimal) -> PiComplex:
        """Create complex number representing e^(i·π·multiple)"""
        return cls(pi_factor=multiple)
    
    @classmethod
    def i_unit(cls) -> PiComplex:
        """Return the imaginary unit i"""
        # i = e^(i·π/2)
        return cls.from_pi_multiple(Decimal('0.5'))

# Operator for e^(i·π) = -1
def euler_identity(n: int = 1) -> PiComplex:
    """Returns e^(i·π·n)"""
    return PiComplex(pi_factor=Decimal(n))

# Hilbert space implementation for PiComplex values
class PiHilbertSpace(Generic[T, V, C]):
    """
    A finite-dimensional Hilbert space implementation using PiComplex numbers
    """
    def __init__(self, dimension: int):
        self.dimension = dimension
        self.basis_vectors = [self._create_basis_vector(i) for i in range(dimension)]
    
    def _create_basis_vector(self, index: int) -> list[PiComplex]:
        """Create a basis vector with 1 at position index and 0 elsewhere"""
        return [PiComplex(1 if i == index else 0) for i in range(self.dimension)]
    
    def inner_product(self, vec1: list[PiComplex], vec2: list[PiComplex]) -> PiComplex:
        """Calculate the inner product <vec1|vec2>"""
        if len(vec1) != self.dimension or len(vec2) != self.dimension:
            raise ValueError("Vectors must match the Hilbert space dimension")
        
        result = PiComplex()
        for i in range(self.dimension):
            result += vec1[i].conjugate() * vec2[i]
        return result
    
    def norm(self, vector: list[PiComplex]) -> Decimal:
        """Calculate the norm (length) of a vector"""
        return self.inner_product(vector, vector).modulus()
    
    def is_orthogonal(self, vec1: list[PiComplex], vec2: list[PiComplex]) -> bool:
        """Check if two vectors are orthogonal"""
        return self.inner_product(vec1, vec2).modulus() < Decimal('1e-10')
    
    def projection(self, vector: list[PiComplex], subspace_basis: list[list[PiComplex]]) -> list[PiComplex]:
        """Project a vector onto a subspace defined by orthonormal basis vectors"""
        result = [PiComplex(0) for _ in range(self.dimension)]
        
        for basis_vec in subspace_basis:
            # Calculate <basis_vec|vector> * |basis_vec>
            coef = self.inner_product(basis_vec, vector)
            for i in range(self.dimension):
                result[i] += coef * basis_vec[i]
        
        return result
    
    def apply_operator(self, operator: list[list[PiComplex]], vector: list[PiComplex]) -> list[PiComplex]:
        """Apply a linear operator (matrix) to a vector"""
        if len(operator) != self.dimension or any(len(row) != self.dimension for row in operator):
            raise ValueError("Operator dimensions must match Hilbert space dimension")
        
        result = [PiComplex(0) for _ in range(self.dimension)]
        for i in range(self.dimension):
            for j in range(self.dimension):
                result[i] += operator[i][j] * vector[j]
        
        return result

# Quantum state implementation for your framework
class QuantumState(Generic[T, V, C]):
    """
    A quantum state represented in a PiHilbert space with amplitude coefficients
    """
    def __init__(self, hilbert_space: PiHilbertSpace, initial_state: Optional[list[PiComplex]] = None):
        self.hilbert_space = hilbert_space
        self.dimension = hilbert_space.dimension
        
        if initial_state is None:
            # Default to |0⟩ state
            self.amplitudes = [PiComplex(1 if i == 0 else 0) for i in range(self.dimension)]
        else:
            if len(initial_state) != self.dimension:
                raise ValueError("Initial state dimension must match Hilbert space dimension")
            self.amplitudes = initial_state
            self._normalize_state()
    
    def _normalize_state(self) -> None:
        """Normalize the quantum state to ensure unit norm"""
        norm = self.hilbert_space.norm(self.amplitudes)
        if norm > Decimal('1e-10'):  # Avoid division by near-zero
            for i in range(self.dimension):
                self.amplitudes[i] /= norm
    
    def superposition(self, other: QuantumState, alpha: PiComplex, beta: PiComplex) -> QuantumState:
        """Create a superposition state α|self⟩ + β|other⟩"""
        if self.dimension != other.dimension:
            raise ValueError("Cannot create superposition of states with different dimensions")
        
        new_amplitudes = []
        for i in range(self.dimension):
            new_amplitudes.append(alpha * self.amplitudes[i] + beta * other.amplitudes[i])
        
        result = QuantumState(self.hilbert_space, new_amplitudes)
        result._normalize_state()
        return result
    
    def measure(self) -> tuple[int, Decimal]:
        """
        Simulate a measurement of the quantum state
        Returns the measured basis state index and its probability
        """
        import random
        
        # Calculate probabilities for each basis state
        probabilities = []
        for amp in self.amplitudes:
            prob = amp.modulus() ** 2
            probabilities.append(float(prob))
        
        # Normalize probabilities (they should sum to 1, but just in case)
        total = sum(probabilities)
        normalized_probs = [p/total for p in probabilities]
        
        # Simulate measurement
        outcome = random.choices(range(self.dimension), weights=normalized_probs, k=1)[0]
        
        # Return measured state and its probability
        return outcome, Decimal(str(normalized_probs[outcome]))
    
    def apply_gate(self, gate_matrix: list[list[PiComplex]]) -> QuantumState:
        """Apply a quantum gate (unitary operator) to the state"""
        new_amplitudes = self.hilbert_space.apply_operator(gate_matrix, self.amplitudes)
        return QuantumState(self.hilbert_space, new_amplitudes)
    
    def __str__(self) -> str:
        """String representation of the quantum state"""
        parts = []
        for i, amp in enumerate(self.amplitudes):
            if amp.modulus() > Decimal('1e-10'):
                parts.append(f"({amp})|{i}⟩")
        
        return " + ".join(parts) if parts else "0"

# Example quantum gates using PiComplex numbers
def hadamard_gate() -> list[list[PiComplex]]:
    """
    Hadamard gate H = 1/√2 * [[1, 1], [1, -1]]
    Creates superposition states
    """
    sqrt2_inv = PiComplex(Decimal('1') / Decimal('1.4142135623730951'))
    return [
        [sqrt2_inv, sqrt2_inv],
        [sqrt2_inv, -sqrt2_inv]
    ]

def phase_gate(phi: Decimal) -> list[list[PiComplex]]:
    """
    Phase gate [[1, 0], [0, e^(iφ)]]
    Introduces a phase shift
    """
    return [
        [PiComplex(1), PiComplex(0)],
        [PiComplex(0), PiComplex.from_polar(Decimal('1'), phi)]
    ]

def pi_phase_gate() -> list[list[PiComplex]]:
    """
    Special phase gate using π: [[1, 0], [0, e^(iπ)]] = [[1, 0], [0, -1]]
    """
    return [
        [PiComplex(1), PiComplex(0)],
        [PiComplex(0), PiComplex(pi_factor=1)]  # e^(iπ) = -1
    ]


async def quantum_circuit_demo():
    """Demonstrate quantum circuit operations using PiComplex numbers"""
    # Initialize a 2-qubit Hilbert space
    hilbert_space = PiHilbertSpace(2)
    
    # Create initial state |0⟩
    initial_state = QuantumState(hilbert_space)
    print("Initial state:", initial_state)
    
    # Apply Hadamard gate to create superposition
    h_gate = hadamard_gate()
    superposition_state = initial_state.apply_gate(h_gate)
    print("After Hadamard:", superposition_state)
    
    # Apply phase gate with π/2 phase
    p_gate = phase_gate(PI / Decimal('2'))
    phase_shifted = superposition_state.apply_gate(p_gate)
    print("After π/2 phase shift:", phase_shifted)
    
    # Perform multiple measurements
    measurements = []
    for _ in range(10):
        outcome, probability = phase_shifted.measure()
        measurements.append(outcome)
    
    print("Measurement outcomes:", measurements)
    
    # Demonstrate PiComplex arithmetic
    alpha = PiComplex(1, 1)  # 1 + i
    beta = PiComplex(pi_factor=1)  # e^(iπ) = -1
    product = alpha * beta
    print(f"Complex arithmetic: ({alpha}) * ({beta}) = {product}")

@dataclass
class QuantumObservable:
    """Represents a quantum observable in the QSD system"""
    name: str
    operator: Callable[[Any], Any]
    eigenvalues: List[complex] = field(default_factory=list)
    measurement_basis: Optional[List[Any]] = None
    last_measurement: Optional[Any] = None
    measurement_count: int = 0

@dataclass
class EntanglementMetadata:
    """Metadata for quantum entanglement between atoms"""
    entanglement_id: str
    entangled_atoms: Set[str] = field(default_factory=set)
    entanglement_type: EntanglementType = EntanglementType.CODE_LINEAGE
    correlation_strength: float = 1.0
    created_at: float = field(default_factory=time.time)
    bell_state: Optional[str] = None  # |Φ+⟩, |Φ-⟩, |Ψ+⟩, |Ψ-⟩




# =============
# Decorator spacetime/psi/phi
# =============
@dataclass
class Ornament:
    """
    Container for composable decorators with metadata.
    Enables declarative decorator ontology and introspection.
    """

    name: str
    decorator: Callable
    metadata: Dict[str, Any] = field(default_factory=dict)
    priority: int = 0  # Higher priority applied first
    enabled: bool = True

    def __call__(self, target: Callable) -> Callable:
        """Apply the decorator if enabled"""
        if self.enabled:
            return self.decorator(target)
        return target

    def __gt__(self, other: 'Ornament') -> bool:
        """Compare by priority for sorting"""
        return self.priority > other.priority


class OrnamentStack:
    """
    Manages ordered application of decorators with conflict resolution.
    Implements composition semantics for decorator chains.
    """

    def __init__(self):
        self._ornaments: List[Ornament] = []
        self._applied_cache: Dict[int, Callable] = {}

    def register(self, ornament: Ornament) -> None:
        """Add ornament to stack, maintaining priority order"""
        self._ornaments.append(ornament)
        self._ornaments.sort(reverse=True)  # High priority first
        self._applied_cache.clear()
        logger.debug(
            f"Registered ornament: {ornament.name} (priority={ornament.priority})"
        )

    def apply_all(self, target: Callable) -> Callable:
        """Apply all enabled ornaments in priority order"""
        cache_key = id(target)
        if cache_key in self._applied_cache:
            return self._applied_cache[cache_key]

        result = target
        for ornament in self._ornaments:
            if ornament.enabled:
                result = ornament(result)
                logger.debug(f"Applied ornament: {ornament.name}")

        self._applied_cache[cache_key] = result
        return result

    def get_metadata(self) -> Dict[str, Any]:
        """Extract combined metadata from all ornaments"""
        combined = {}
        for ornament in self._ornaments:
            combined[ornament.name] = ornament.metadata
        return combined
"""
===============================================================================
BYTEWORD MICROCANONICAL ENSEMBLE: A Morphological Source Code Artifact
===============================================================================
ARCHITECTURAL PRELUDE
===============================================================================

Quinic Statistical Dynamics Type System

The framework establishes a tripartite quantum field theoretical type system that 
enables recursive thermodynamic computing:

1. Type Structure (T) - Field Theoretic Layer:
   - Runtime field operators as type constructors
   - Fock space representations of type constraints
   - Creation/annihilation operators for type transitions
   Properties:
   - Intensive: Runtime coherence length, type density
   - Extensive: Total type space, aggregate type relationships

2. Value Space (V) - Statistical Ensemble Layer:
   - Quantum statistical distributions of runtime states
   - Entanglement preservation of value relationships
   - Coherent domains of value clusters
   Properties:
   - Intensive: Information density, state entropy density
   - Extensive: Total information content, system-wide entropy

3. Computation Space (C) - Dynamic Process Layer:
   - Quinic propagation operations
   - Thermodynamic coupling mechanisms
   - Distributed state resolution
   Properties:
   - Intensive: Computational temperature
   - Extensive: Net computational work

Relationships:
- T → V: Field operators collapse to statistical ensembles
- V → C: Statistical states enable quinic operations
- C → T: Dynamic processes modify field structure

This system enables:
1. Micro Level: Individual runtime quantum operations
2. Meso Level: Coherent domains of entangled runtimes
3. Macro Level: Emergent computational thermodynamics

The Atom() wrapper serves as a quinic runtime instance, capable of:
- Self-observation through type reflection
- State superposition in value space
- Thermodynamic interactions via computation space

Noetherian Symmetries in Second-Quantized QSD

The second quantization of runtime configuration space establishes fundamental 
symmetries that correspond to conserved computational quantities:

1. Translation Symmetry in Type Space (T):
   - Conserves computational momentum
   - Maintains type identity across runtime translations
   - Preserves boundary conditions during quinic operations
   
2. Rotation Symmetry in Value Space (V):
   - Conserves computational angular momentum
   - Preserves value relationships during state evolution
   - Maintains statistical ensemble invariants
   
3. Phase Symmetry in Computation Space (C):
   - Conserves computational charge
   - Preserves behavioral consistency during transformations
   - Maintains coherence in distributed operations

Each symmetry manifests in the QSD field as:
- Local symmetries: Within individual runtime instances
- Global symmetries: Across the entire computational ensemble
- Gauge symmetries: In the interaction between runtimes
Conservation Laws:
1. Information Conservation: From translational symmetry
2. Coherence Conservation: From rotational symmetry
3. Behavioral Conservation: From phase symmetry

These Noetherian invariants ensure that:
- Quinic operations preserve essential runtime properties
- Statistical ensembles maintain their collective behavior
- Thermodynamic interactions respect conservation principles

### The Shape of Information

Information, it seems, is not just a string of 0s and 1s. It's a morphological substrate that evolves within the constraints of time, space, and energy. In the same way that language molds our cognition, information molds our universe. It's the invisible hand shaping the foundations of reality, computation, and emergence. A continuous process of becoming, where each transition is not deterministic but probabilistic, tied to the very nature of quantum reality itself.

### Probabalistic statistical mechanics, and the thermodynamics of information

#### Quantum Informatic Foundations

    Information is not just an abstraction; it is a fundamental physical phenomenon intertwined with the fabric of reality itself. It shapes the emergence of complexity, language, and cognition.

In the grand landscape of quantum mechanics and computation, the N/P junction serves as a quantum binary ontology. It's not just a computational model; it represents the observable aspect of quantum informatics, where Planck-scale phenomena create perturbative states in Hilbert Space. Observing these phenomena is akin to negotiating quantum states via self-adjoint operators.
Morphology of Information

    Information and inertia form an intricate "shape" within the cosmos, an encoded structure existing beyond our 3+1D spacetime.

The "singularity" isn't merely a technological concept; it represents the continuous process of state transformation, where observation isn't just the result of an event, but part of a dynamic, ongoing negotiation of physical states.

#### Agentic Motility

    The ability of a system to "move" across states, evolve, and learn, mirrors the quantum concept of entanglement and state collapse.

Imagine a system that can learn to evolve, not through external forces but by agentic motility—its capacity to independently negotiate between deterministic structure and emergent complexity. This is the essence of cognitive plasticity at the computational level.

#### String theory, and the holographic icon; the holoicon

The nature of agentic motility—where a language model builds a robot, writes code, and the robot impacts the world—feels akin to spooky action at a distance. It's like entanglement; the process of wave function collapse is no longer just a digital phenomenon. This brings us closer to a fundamental idea: information as shape.

Consider the shape of information: scale-invariant, multilateral, and complex. It’s akin to a Bayesian topology or a quantum field theory—a fundamental, stochastic process. We observe how this information evolves, collapses, and interacts with its surroundings, branching out into new possibilities.

This isn't just abstract: it's encoded in the zeros and ones that form the morphology of computation. From inertia to complexity, from math to language—the very foundation of the cosmos exists encoded within binary form. The infinite set of reals between 0 and 1, encoded in binary code, represents all possible complexity within our universe. Yet, we can only see glimpses of this structure, its shape transcending dimensions.

When Maxwell’s Demon observes and collapses a system's state, we witness the quantum collapse—the very morphology of computation (temprature, canonically) forming in the thermodynamic process.

## Degrees of Freedom (DoF)

1. DoF as State/Logic Containers:

    Each DoF encapsulates both:
        State: Observable properties of the system (e.g., spin, phase, and degrees of freedom in the QuantumState).
        Logic: Transformative behaviors (e.g., compose, interact, entanglement logic).
    A DoF runtime becomes a self-contained microcosm of both declarative (state) and imperative (logic) programming, enabling homoiconic behaviors.

2. Quantum Time Slices and Homoiconism:

    Each QuantumState represents a slice of time/phase evolution, where:
        State: The intrinsic properties (spin, phase).
        Logic: The mechanisms governing state transitions (Hamiltonian dynamics, Pauli transformations).
    This builds a fractal-like architecture where every runtime and sub-runtime is both code and data.

3. Universal DoF Runtime:

    If every runtime is a DoF, it unifies:
        The elemental level (individual methods/behaviors as DoFs).
        The systemic level (entire runtime containers as DoFs).
        This fractal homoiconic structure mirrors the self-similar, hierarchical nature of cognition.

### DoF as the Morphological Bedrock

Morphological Source Code thrives on the interplay of state, logic, and structure. Here’s how DoF completes this triad:

1. Morphological Symmetry:

    A DoF embodies symmetry across:
        State: Static properties of a runtime.
        Logic: Dynamic behaviors or transformations.
    Morphological symmetry ensures that state and logic evolve consistently within and across runtimes.

2. Evolutionary Homoiconism:

    Every DoF is self-describing and self-transforming:
        A method DoF may encode its transformations as data, enabling introspection and modification.
        A runtime DoF is a meta-container, defining how its contained DoFs interact and evolve.
    This recursive relationship enables the quine-like behavior foundational to Morphological Source Code.

3. Multi-Axis Evolution:

    DoFs as independent axes enable multi-dimensional state evolution:
        For example, spin evolution could represent angular state changes, while phase evolution reflects temporal shifts.
        Together, they define a multi-faceted evolutionary trajectory.

---------------------
The ByteWord System IS Microcanonical. No bath. No reservoir. Just bits
and their ghosts. This is not canonical (NVT) statistical mechanics where
temperature is imposed by an external bath. This is microcanonical (NVE):
Number of states fixed, Volume of morphospace fixed, Energy budget fixed.
Temperature emerges from the degeneracy structure of the ghost ensemble.

In a ByteWord 'bulk':
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

@runtime_checkable
@dataclass
class __Atom__(Protocol):  # __Atom__ Decorator for Particles
    """
    Structural typing protocol for Atoms.
    Defines the minimal interface that an Atom must implement.
    Attributes:
        id (str): A unique identifier for the Atom instance.
    """
    id: str  # ADMIN-scoped attribute
    # ADMIN-scoped attributes
    # TODO: make this class call to the Quantum MRO C3 linearization module
    # To have an Atom is to have a Non-Markovian morphological body in an ordered, synchronous real-observable(s,) 'arrow of time' causality, and, indeed phenomenological existence; even if-only in the holes and flows of the electron pumping at the true morphological NP junction morphism regime.
    AtomType: Optional # type: ignore

    def __call__(self, cls):
        """
        Decorator to enhance a class with unique ID generation and homoiconic properties.
        Args:
            cls (Type): The class to be decorated as a homoiconic Atom.
        Returns:
            Type: The enhanced class with homoiconic properties.
        """
        original_init = cls.__init__

        @wraps(original_init)
        def new_init(self, *args, **kwargs):
            original_init(self, *args, **kwargs)
            if not hasattr(self, 'id'):
                self.id = hashlib.sha256(self.__class__.__name__.encode('utf-8')).hexdigest()

        cls.__init__ = new_init
        return cls

def ornament(
    dataclass_kwargs: Optional[dict] = None,
    frozen: bool = False,
    **kwargs
) -> Callable[[Type[T]], Type[T]]:
    """
    Master decorator to consolidate all decoration logic.
    Args:
        dataclass_kwargs (Optional[dict]): Keyword arguments to pass to @dataclass.
        frozen (bool): Whether to make the class immutable.
        **kwargs: Additional metadata or configurations.
    Returns:
        Callable[[Type[T]], Type[T]]: A decorator that applies the specified transformations.
    """
    def decorator(cls: Type[T]) -> Type[T]:
        # Step 1: Apply @dataclass if requested
        if dataclass_kwargs is not None:
            cls = dataclass(**dataclass_kwargs)(cls)

        # Step 2: Apply immutability if frozen=True
        if frozen:
            original_setattr = cls.__setattr__

            def __setattr__(self, name, value):
                if hasattr(self, name):
                    raise AttributeError(f"Cannot modify frozen attribute '{name}'")
                original_setattr(self, name, value)

            cls.__setattr__ = __setattr__

        # Step 3: Add unique ID generation to the class
        original_init = cls.__init__

        def new_init(self, *args, **kwargs):
            original_init(self, *args, **kwargs)
            if not hasattr(self, 'id'):
                self.id = hashlib.sha256(self.__class__.__name__.encode('utf-8')).hexdigest()

        cls.__init__ = new_init

        # Step 4: Ensure the class adheres to the __Atom__ protocol
        if not isinstance(cls, __Atom__):
            raise TypeError(f"Class {cls.__name__} does not conform to the __Atom__ protocol.")

        return cls

    return decorator
@dataclass
class State:
    type_space: T
    value_space: V
    computation_space: C
    symmetry: Symmetry
    conservation: Conservation
    order_parameter: Optional[OrderParameter] = None  # Track symmetry breaking

@dataclass
class MemoryModel:
    """Maps linear-virtual address space per the OS to Frames+Lifetimes+Arenas (linear allocator).."""

    ptr_size: int = ctypes.sizeof(ctypes.c_void_p)
    word_size: int = ctypes.sizeof(ctypes.c_size_t)
    cache_line_size: int = 64
    page_size: int = 4096

    @classmethod
    def get_system_info(cls) -> 'MemoryModel':
        try:
            with open(
                '/sys/devices/system/cpu/cpu0/cache/index0/coherency_line_size'
            ) as f:
                cache_line_size = int(f.read().strip())
        except (FileNotFoundError, ValueError):
            cache_line_size = 64
        return cls(
            ptr_size=ctypes.sizeof(ctypes.c_void_p),
            word_size=ctypes.sizeof(ctypes.c_size_t),
            cache_line_size=cache_line_size,
            page_size=cls.page_size,
        )

class MemoryState(StrEnum):
    QUANTUM = auto()  # Superposition state, uncommitted changes
    CLASSICAL = auto()  # Committed state (persisted to Git)
    CACHED = auto()  # Loaded from disk; may be out-of-date
    ALLOCATED = auto()  # Memory is allocated but not yet initialized
    INITIALIZED = auto()  # Memory is initialized with data
    PAGED = auto()  # Memory is paged to secondary storage
    SHARED = auto()  # Memory is shared between multiple runtimes
    DEALLOCATED = auto()  # Memory has been freed or process retired


@dataclass
class QuantumCell:  # complex embedding cell; 'measure theoretic' and so; analagous to Borel Set, QuantumCell.value() the sigma algebra
    address: int
    segment: int
    value: bytes = b'\x00' * WordSize.INT
    state: Optional[str] = None
    commit_hash: Optional[str] = None
    data: Optional[array.array] = None
    metadata: Optional[Dict] = None
class EmbeddingConfig:
    def __init__(self,
                 dimensions: int = 768,
                 precision: str = 'float32',
                 cache_path: str = 'runtime_cache.json'):
        self.dimensions = dimensions
        self.precision = precision
        self.cache_path = cache_path

    def get_format_char(self) -> str:
        return {'float32': 'f', 'float64': 'd', 'int32': 'i'}.get(self.precision, 'f')


@dataclass
class Document:
    content: str
    embedding: Optional[List[float]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    uuid: str = None

    def __post_init__(self):
        if self.uuid is None:
            self.uuid = str(uuid.uuid4())


class MerkleNode:
    def __init__(self, data: Any, children: Optional[List['MerkleNode']] = None):
        self.data = data
        self.children: List[MerkleNode] = children or []
        self.timestamp = datetime.now(timezone.utc).isoformat()
        self.uuid = str(uuid.uuid4())
        self.hash = self._calculate_hash()

    def _calculate_hash(self) -> str:
        hasher = hashlib.sha256()
        hasher.update(json.dumps(self.data, sort_keys=True).encode())
        for child in sorted(self.children, key=lambda c: c.hash):
            hasher.update(child.hash.encode())
        return hasher.hexdigest()

    def add_child(self, child: 'MerkleNode'):
        self.children.append(child)
        self.hash = self._calculate_hash()

    def __hash__(self):
        return hash(self.hash)

    def __eq__(self, other):
        return isinstance(other, MerkleNode) and self.hash == other.hash


class RuntimeState:
    def __init__(self):
        self.merkle_root: Optional[MerkleNode] = None
        self.state_history: List[str] = []


@dataclass
class MemoryVector:
    """
    Memory representation with quantum-inspired properties.
    Represents the quantum state of virtual memory regions
    Supports multiple flavors and state transitions.
    """

    coords: List[int]  # Byte coordinates
    weights: Optional[List[float]] = None  # Probability amplitudes
    flavor: ByteWordFlavor = ByteWordFlavor.MUTABLE
    address_space: complex  # Complex number representing memory location probability
    coherence: float  # Memory coherence across runtime boundaries
    entanglement: float  # Degree of entanglement with other memory regions
    state: MemoryState
    size: int  # Size of memory region in bytes

    def __post_init__(self):
        """Validate coordinates"""
        if not all(0 <= c <= 255 for c in self.coords):
            raise ValueError("Coordinates must be in range [0, 255]")

        if self.weights and len(self.weights) != len(self.coords):
            raise ValueError("Weights must match coordinate length")

    def copy(self) -> 'MemoryVector':
        """Deep copy"""
        return MemoryVector(
            coords=self.coords.copy(),
            weights=self.weights.copy() if self.weights else None,
            flavor=self.flavor,
        )

    def as_integer(self) -> int:
        """Pack coords as little-endian integer"""
        val = 0
        for i, byte in enumerate(self.coords):
            val |= (byte & 0xFF) << (8 * i)
        return val

    @classmethod
    def from_integer(cls, value: int, nbytes: int, **kwargs) -> 'MemoryVector':
        """Unpack integer to byte coords"""
        coords = [(value >> (8 * i)) & 0xFF for i in range(nbytes)]
        return cls(coords=coords, **kwargs)

    def to_bytes(self) -> bytes:
        """Convert to raw bytes"""
        return bytes(self.coords)

    @classmethod
    def from_bytes(cls, data: bytes, **kwargs) -> 'MemoryVector':
        """Construct from raw bytes"""
        return cls(coords=list(data), **kwargs)

    def parity(self) -> int:
        """Calculate parity (conserved quantity)"""
        return sum(bin(b).count('1') for b in self.coords) % 2

    def __repr__(self) -> str:
        hex_str = ' '.join(f'{b:02x}' for b in self.coords[:8])
        if len(self.coords) > 8:
            hex_str += '...'
        return f"MemoryVector([{hex_str}], flavor={self.flavor.name})"


class QuantumOpType(Enum):
    """Types of quantum operations"""

    IDENTITY = auto()  # No change
    HADAMARD = auto()  # Superposition
    PHASE = auto()  # Phase shift
    CNOT = auto()  # Controlled-NOT
    SWAP = auto()  # Swap bits
    MEASURE = auto()  # Collapse superposition


# Utility functions for bit operations
def pack_bits(bits: List[int]) -> BYTE:
    """Pack a list of bits into a BYTE"""
    result = BYTE()
    for i, bit in enumerate(bits[:8]):  # Ensure we don't exceed 8 bits
        if bit:
            result.set_bit(i, 1)
    return result


def unpack_bits(byte: BYTE) -> List[int]:
    """Unpack a BYTE into a list of 8 bits"""
    return [byte.get_bit(i) for i in range(8)]


class MorphicComplex:
    """Represents a complex number with morphic properties."""

    def __init__(self, real: float, imag: float):
        self.real = real
        self.imag = imag

    def conjugate(self) -> 'MorphicComplex':
        """Return the complex conjugate."""
        return MorphicComplex(self.real, -self.imag)

    def __add__(self, other: 'MorphicComplex') -> 'MorphicComplex':
        return MorphicComplex(self.real + other.real, self.imag + other.imag)

    def __sub__(self, other: 'MorphicComplex') -> 'MorphicComplex':
        return MorphicComplex(self.real - other.real, self.imag - other.imag)

    def __mul__(self, other: Union['MorphicComplex', float, int]) -> 'MorphicComplex':
        if isinstance(other, (int, float)):
            return MorphicComplex(self.real * other, self.imag * other)
        return MorphicComplex(
            self.real * other.real - self.imag * other.imag,
            self.real * other.imag + self.imag * other.real,
        )

    def __rmul__(self, other: Union[float, int]) -> 'MorphicComplex':
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
        if self.imag >= 0:
            return f"{self.real} + {self.imag}i"
        return f"{self.real} - {abs(self.imag)}i"


class Matrix:
    """Simple matrix implementation using standard Python"""

    def __init__(self, data: List[List[Any]]):
        if not data:
            raise ValueError("Matrix data cannot be empty")

        # Verify all rows have the same length
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
        self, other: Union['Matrix', List[Any]]
    ) -> Union['Matrix', List[Any]]:
        """Matrix multiplication operator @"""
        if isinstance(other, list):
            # Matrix @ vector
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
            # Matrix @ Matrix
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
        """Calculate the trace of the matrix"""
        if self.rows != self.cols:
            raise ValueError("Trace is only defined for square matrices")
        return sum(self.data[i][i] for i in range(self.rows))

    def transpose(self) -> 'Matrix':
        """Return the transpose of this matrix"""
        return Matrix(
            [[self.data[j][i] for j in range(self.rows)] for i in range(self.cols)]
        )

    @staticmethod
    def zeros(rows: int, cols: int) -> 'Matrix':
        """Create a matrix of zeros"""
        if rows <= 0 or cols <= 0:
            raise ValueError("Matrix dimensions must be positive")
        return Matrix([[0 for _ in range(cols)] for _ in range(rows)])

    @staticmethod
    def identity(n: int) -> 'Matrix':
        """Create an n×n identity matrix"""
        if n <= 0:
            raise ValueError("Matrix dimension must be positive")
        return Matrix([[1 if i == j else 0 for j in range(n)] for i in range(n)])

    def __repr__(self) -> str:
        return "\n".join([str(row) for row in self.data])


class HilbertSpace:
    """
    Represents a Hilbert space that uses MorphicComplex numbers for coordinates.
    """

    def __init__(self, dimension: int = 3):
        if dimension <= 0:
            raise ValueError("Hilbert space dimension must be positive")
        self.dimension = dimension
        self.basis_vectors = [self._create_basis_vector(i) for i in range(dimension)]

    def _create_basis_vector(self, index: int) -> List[MorphicComplex]:
        """Create a basis vector with a 1 at the specified index."""
        vector = [MorphicComplex(0, 0) for _ in range(self.dimension)]
        vector[index] = MorphicComplex(1, 0)
        return vector

    def inner_product(
        self, vec1: List[MorphicComplex], vec2: List[MorphicComplex]
    ) -> MorphicComplex:
        """
        Compute the inner product of two vectors in the Hilbert space.
        <u, v> = ∑ᵢ (u*ᵢ × vᵢ) where u*ᵢ is the complex conjugate
        """
        if len(vec1) != len(vec2) or len(vec1) != self.dimension:
            raise ValueError("Vectors must have the same dimension as the space")

        result = MorphicComplex(0, 0)
        for i in range(self.dimension):
            # For each component, compute u*ᵢ × vᵢ
            conj_u = vec1[i].conjugate()
            result = result + (conj_u * vec2[i])
        return result

    def norm(self, vector: List[MorphicComplex]) -> float:
        """Compute the norm (magnitude) of a vector."""
        inner = self.inner_product(vector, vector)
        return math.sqrt(inner.real)  # Inner product with self should be real

    def normalize(self, vector: List[MorphicComplex]) -> List[MorphicComplex]:
        """Return a normalized copy of the vector."""
        norm_val = self.norm(vector)
        if abs(norm_val) < 1e-10:
            raise ValueError("Cannot normalize zero vector")
        return [MorphicComplex(c.real / norm_val, c.imag / norm_val) for c in vector]

    def is_orthogonal(
        self, vec1: List[MorphicComplex], vec2: List[MorphicComplex]
    ) -> bool:
        """Check if two vectors are orthogonal."""
        inner = self.inner_product(vec1, vec2)
        return abs(inner.real) < 1e-10 and abs(inner.imag) < 1e-10

    def project(
        self, vector: List[MorphicComplex], subspace_basis: List[List[MorphicComplex]]
    ) -> List[MorphicComplex]:
        """Project a vector onto a subspace defined by a basis."""
        projection = [MorphicComplex(0, 0) for _ in range(self.dimension)]

        for basis_vec in subspace_basis:
            # Compute <v, basis> / <basis, basis>
            inner_v_basis = self.inner_product(vector, basis_vec)
            inner_basis_basis = self.inner_product(basis_vec, basis_vec).real

            if abs(inner_basis_basis) < 1e-10:
                raise ValueError("Basis vector must not be zero")

            # Compute the coefficient
            coeff = MorphicComplex(
                inner_v_basis.real / inner_basis_basis,
                inner_v_basis.imag / inner_basis_basis,
            )

            # Add the contribution of this basis vector to the projection
            for i in range(self.dimension):
                projection[i] = projection[i] + (basis_vec[i] * coeff)

        return projection

    def __eq__(self, other) -> bool:
        if not isinstance(other, HilbertSpace):
            return False
        return self.dimension == other.dimension


class BYTE(Generic[T, V, C]):
    """
    The most fundamental unit of computation in our system.
    Represents an 8-bit register that can be manipulated at the bit level.
    """

    def __init__(self, value: int = 0):
        # Ensure value is always an 8-bit word (0-255)
        self.value = value & 0xFF

    """
    Core Logic Definition (<C_C_VV|TTTT>):
        Structure: 8 bits
            Bit 7: C (Outer/Meta C)
            Bit 6: _C_ (Dunder C / Contextual Bit)
            Bits 5, 4: VV (Core Morphism)
            Bits 3-0: TTTT (Topology/State)
        Interpretation Rule:
            If C == 1 (Active State):
                Bit 6 (_C_) is the MSB of the 3-bit morphism VVV = _C_VV.
                There are 8 possible operations defined by VVV.
                The internal "anchor" state is not explicitly represented by _C_.
            If C == 0 (Settled/Anchored State):
                Bit 6 (_C_) represents the internal anchor state C_internal (0=Anchored/Static, 1=Pointable/Error?).
                The operation is determined solely by the 2-bit VV.
                There are 4 possible operations defined by VV.
        Operations (Placeholders): We need 8 ops for VVV and 4 for VV. Let's define simple ones for now:
            VVV (when C=1):
                000 (0): Identity (Target T unchanged)
                001 (1): Inc T ((T+1) & 0xF)
                010 (2): Dec T ((T-1) & 0xF)
                011 (3): Flip T (T ^ 0xF) (Pauli-X like)
                100 (4): Flip High Nibble T (T ^ 0b1100) (Pauli-Z like?)
                101 (5): Flip Low Nibble T (T ^ 0b0011)
                110 (6): Set T to 0
                111 (7): Set T to 15 (0xF)
            VV (when C=0):
                00 (0): Identity (Target T unchanged)
                01 (1): Flip T (T ^ 0xF)
                10 (2): Set T based on C_internal (T = _C_)
                11 (3): Rotate T Left (((T << 1) | (T >> 3)) & 0xF)
        Transformation: Source.transform(Target) applies the operation determined by Source's C and VVV/VV bits onto the Target's TTTT bits, returning a new ByteWord for the target. Crucially, the target's C, C, VV bits usually remain unchanged unless the operation specifically modifies them (none of our placeholders do).
    """

    def __repr__(self) -> str:
        return f"BYTE(0x{self.value:02x}, 0b{self.value:08b})"

    def __eq__(self, other) -> bool:
        if isinstance(other, BYTE):
            return self.value == other.value
        elif isinstance(other, int):
            return self.value == (other & 0xFF)
        return False

    def __hash__(self) -> int:
        return hash(self.value)

    # Bit-level operations
    def get_bit(self, position: int) -> int:
        """Get the bit at a specific position (0-7)"""
        if not 0 <= position <= 7:
            raise ValueError("Bit position must be between 0 and 7")
        return (self.value >> position) & 1

    def set_bit(self, position: int, bit_value: int) -> None:
        """Set the bit at a specific position (0-7)"""
        if not 0 <= position <= 7:
            raise ValueError("Bit position must be between 0 and 7")
        if bit_value == 1:
            self.value |= 1 << position
        else:
            self.value &= ~(1 << position)

    def flip_bit(self, position: int) -> None:
        """Flip the bit at a specific position (0-7)"""
        if not 0 <= position <= 7:
            raise ValueError("Bit position must be between 0 and 7")
        self.value ^= 1 << position

    # Bitwise operations
    def __and__(self, other: BYTE) -> BYTE:
        return BYTE(self.value & other.value)

    def __or__(self, other: BYTE) -> BYTE:
        return BYTE(self.value | other.value)

    def __xor__(self, other: BYTE) -> BYTE:
        return BYTE(self.value ^ other.value)

    def __invert__(self) -> BYTE:
        return BYTE(~self.value & 0xFF)  # Keep it 8-bit


_B_ = TypeVar("B", bound=BYTE)


@dataclass
class MorphologicalBasis(Generic[T, V, C], _B_):
    """Defines a structured basis with symmetry evolution."""

    type_structure: T  # Topological/Type representation
    value_space: V  # State space (e.g., physical degrees of freedom)
    compute_space: C  # Operator space (e.g., Lie Algebra of transformations)

    def evolve(self, generator: Matrix, time: float) -> 'MorphologicalBasis[T, V, C]':
        """Evolves the basis using a symmetry generator over time."""
        # Implement actual evolution logic based on the generator
        new_compute_space = self._transform_compute_space(generator, time)
        return MorphologicalBasis(
            self.type_structure, self.value_space, new_compute_space
        )

    def _transform_compute_space(self, generator: Matrix, time: float) -> C:
        """Transform the compute space using the generator"""
        # This would depend on the specific implementation of C
        # For demonstration, assuming C is a Matrix:
        if isinstance(self.compute_space, Matrix) and isinstance(generator, Matrix):
            # Simple time evolution using matrix exponential approximation
            # exp(tA) ≈ I + tA + (tA)²/2! + ...
            identity = Matrix.zeros(generator.rows, generator.cols)
            for i in range(identity.rows):
                identity.data[i][i] = 1

            scaled_gen = Matrix(
                [
                    [generator[i, j] * time for j in range(generator.cols)]
                    for i in range(generator.rows)
                ]
            )

            # First-order approximation: I + tA
            result = identity
            for i in range(result.rows):
                for j in range(result.cols):
                    result.data[i][j] += scaled_gen.data[i][j]

            return cast(C, result @ self.compute_space)

        return self.compute_space  # Default fallback


_MB_ = TypeVar("MB", bound=MorphologicalBasis)


@dataclass
class _Atom_(Generic[T, V, C], _MB_):
    """
    Represents a quantum state in a Hilbert space with complex amplitudes.
    """

    def __init__(self, amplitudes: List[MorphicComplex], space: HilbertSpace):
        if len(amplitudes) != space.dimension:
            raise ValueError("Number of amplitudes must match Hilbert space dimension")
        self.amplitudes = amplitudes
        self.space = space
        self.normalize()

    def normalize(self) -> None:
        """Normalize the state vector"""
        norm_squared = sum(amp.real**2 + amp.imag**2 for amp in self.amplitudes)
        norm = math.sqrt(norm_squared)
        if norm < 1e-10:
            raise ValueError("Cannot normalize zero state vector")
        self.amplitudes = [
            MorphicComplex(amp.real / norm, amp.imag / norm) for amp in self.amplitudes
        ]

    def measure(self) -> int:
        """
        Perform a measurement on the quantum state.
        Returns the index of the basis state that was measured.
        """
        # Calculate probabilities for each basis state
        probabilities = []
        for amp in self.amplitudes:
            # Probability is |amplitude|²
            prob = amp.real**2 + amp.imag**2
            probabilities.append(prob)

        # Simulate measurement using the probabilities
        r = random.random()
        cumulative_prob = 0
        for i, prob in enumerate(probabilities):
            cumulative_prob += prob
            if r <= cumulative_prob:
                return i

        # Fallback (shouldn't happen with normalized state)
        return len(self.amplitudes) - 1

    def superposition(
        self, other: 'QuantumState', coeff1: MorphicComplex, coeff2: MorphicComplex
    ) -> 'QuantumState':
        """
        Create a superposition of two quantum states.
        |ψ⟩ = a|ψ₁⟩ + b|ψ₂⟩
        """
        if self.space.dimension != other.space.dimension:
            raise ValueError("Quantum states must belong to same Hilbert space")

        new_amplitudes = []
        for i in range(len(self.amplitudes)):
            new_amp = (self.amplitudes[i] * coeff1) + (other.amplitudes[i] * coeff2)
            new_amplitudes.append(new_amp)

        return QuantumState(new_amplitudes, self.space)

    def entangle(self, other: 'QuantumState') -> 'QuantumState':
        """
        Create an entangled state from two quantum states.
        |ψ⟩ = (|ψ₁⟩|0⟩ + |ψ₂⟩|1⟩)/√2
        This is a simplified version of entanglement for demonstration.
        """
        # For simplicity, we'll just return a superposition
        coeff = MorphicComplex(1 / math.sqrt(2), 0)
        return self.superposition(other, coeff, coeff)

    def __eq__(self, other) -> bool:
        if not isinstance(other, QuantumState):
            return False
        if self.space.dimension != other.space.dimension:
            return False
        return all(
            self.amplitudes[i] == other.amplitudes[i]
            for i in range(self.space.dimension)
        )

    def __repr__(self) -> str:
        return f"QuantumState(amplitudes={self.amplitudes})"

    def tensor_product(self, other: 'QuantumState') -> 'QuantumState':
        """Create a tensor product state |ψ₁⟩ ⊗ |ψ₂⟩"""
        dim1, dim2 = len(self.amplitudes), len(other.amplitudes)
        new_dim = dim1 * dim2
        new_space = HilbertSpace(new_dim)
        new_amplitudes = []

        for i in range(dim1):
            for j in range(dim2):
                product = self.amplitudes[i] * other.amplitudes[j]
                new_amplitudes.append(product)

        return QuantumState(new_amplitudes, new_space)


# Roughly, T composed with V composed with C in binary WordSize bra-ket(s)-like format: <|C_C_VV|TTTT|>
_R_ = TypeVar(
    "R", bound=[BYTE, _Atom_, QuantumState, HilbertSpace, MorphicComplex]
)  # Results, roughly


def least_significant_unit(
    state: StateHash, word_size: int, MaxCache: int = 1_000
) -> Any:
    """
    Extracts the least significant unit of a given state based on word_size.
    Uses an in-memory cache to avoid redundant computation.

    Args:
        state: The state to analyze.
        word_size: The size of the word (1=BYTE, 2=SHORT, 4=INT, 8=LONG).
        max_cache_size: Maximum size of the cache to prevent memory issues.

    Returns:
        The least significant unit of the state.
    """
    # Manage cache size
    if len(_lsu_cache) > MaxCache:
        # Clear 25% of the cache when it gets too big
        keys_to_remove = list(_lsu_cache.keys())[: MaxCache // 4]
        for key in keys_to_remove:
            _lsu_cache.pop(key)

    cache_key = (state, word_size)
    if cache_key in _lsu_cache:
        return _lsu_cache[cache_key]

    result = None

    if word_size == WordSize.BYTE:  # BYTE (8-bit)
        if isinstance(state, int):
            result = state & 0xFF  # Extract least significant byte
        elif isinstance(state, bytes):
            result = state[-1] if state else 0
        elif isinstance(state, str):
            result = ord(state[-1]) if state else 0
        else:
            # Handle other types by converting to bytes first
            result = int(hash_state(state) & 0xFF)

    elif word_size == WordSize.SHORT:  # SHORT (16-bit)
        if isinstance(state, int):
            result = state & 0xFFFF  # Extract least significant 2 bytes
        elif isinstance(state, bytes):
            result = int.from_bytes(state[-2:].rjust(2, b'\0'), byteorder='little')
        elif isinstance(state, str):
            encoded = state.encode()
            result = int.from_bytes(encoded[-2:].rjust(2, b'\0'), byteorder='little')
        else:
            # Handle other types by converting to bytes first
            result = int(hash_state(state) & 0xFFFF)

    elif word_size >= WordSize.INT:  # INT/LONG (32/64-bit)
        if isinstance(state, int):
            mask = (1 << (word_size * 8)) - 1
            result = state & mask
        elif isinstance(state, (str, bytes)):
            data = state.encode() if isinstance(state, str) else state
            hash_value = hashlib.sha256(data).digest()
            result = int.from_bytes(hash_value[:word_size], byteorder='little')
        elif isinstance(state, dict):
            if not state:
                result = 0
            else:
                # More sophisticated approach for dictionaries
                key_hash = hash_state(tuple(sorted(str(k) for k in state.keys())))
                val_hash = hash_state(tuple(str(v) for v in state.values()))
                combined = (key_hash ^ val_hash) & ((1 << (word_size * 8)) - 1)
                result = combined
        else:
            result = hash_state(state) & ((1 << (word_size * 8)) - 1)
    else:
        raise ValueError(f"Unsupported word_size: {word_size}")

    # Cache the result
    _lsu_cache[cache_key] = result
    return result


class Category(Generic[T_co, V_co, C_co]):
    """
    Represents a mathematical category with objects and morphisms.
    """

    def __init__(self, name: str):
        self.name = name
        self.objects: List[T_co] = []
        self.morphisms: Dict[Tuple[T_co, T_co], List[C_co]] = {}

    def add_object(self, obj: T_co) -> None:
        """Add an object to the category."""
        if obj not in self.objects:
            self.objects.append(obj)

    def add_morphism(self, source: T_co, target: T_co, morphism: C_co) -> None:
        """Add a morphism between objects."""
        if source not in self.objects:
            self.add_object(source)
        if target not in self.objects:
            self.add_object(target)

        key = (source, target)
        if key not in self.morphisms:
            self.morphisms[key] = []
        self.morphisms[key].append(morphism)

    def compose(self, f: C_co, g: C_co) -> C_co:
        """
        Compose two morphisms.
        For morphisms f: A → B and g: B → C, returns g ∘ f: A → C
        """

        def composed(x):
            return g(f(x))

        return cast(C_co, composed)

    def find_morphisms(self, source: T_co, target: T_co) -> List[C_co]:
        """Find all morphisms between two objects."""
        return self.morphisms.get((source, target), [])


class Morphism(Generic[T_co, T_anti]):
    """Abstract morphism between type structures"""

    @abstractmethod
    def apply(self, source: T_anti) -> T_co:
        """Apply this morphism to transform source into target"""
        pass

    def __call__(self, source: T_anti) -> T_co:
        return self.apply(source)

    def compose(self, other: 'Morphism[U, T_co]') -> 'Morphism[U, T_anti]':
        """Compose this morphism with another (this ∘ other)"""
        # Type U is implied here
        original_self = self
        original_other = other

        class ComposedMorphism(Morphism[T_co, T_anti]):  # type: ignore
            def apply(self, source: T_anti) -> T_co:
                return original_self.apply(original_other.apply(source))

        return ComposedMorphism()

@dataclass
class GrammarRule:
    """
    Represents a single grammar rule in a context-free grammar.

    Attributes:
        lhs (str): Left-hand side of the rule.
        rhs (List[Union[str, 'GrammarRule']]): Right-hand side of the rule, which can be terminals or other rules.
    """
    lhs: str
    rhs: List[Union[str, 'GrammarRule']]

    def __repr__(self):
        """
        Provide a string representation of the grammar rule.

        Returns:
            str: The string representation.
        """
        rhs_str = ' '.join([str(elem) for elem in self.rhs])
        return f"{self.lhs} -> {rhs_str}"
class MorphicRule(GrammarRule, Protocol[T, V]):
    """
    Rules that map structural transformations in code morphologies.
    """

    def __init__(self, symmetry: str, conservation: str, lhs: Any, rhs: List[Any]):
        self.symmetry = symmetry  # e.g., "Translation", "Rotation", "Phase"
        self.conservation = (
            conservation  # e.g., "Information", "Coherence", "Behavioral"
        )
        self.lhs = lhs  # Left-hand side element (morphological pattern)
        self.rhs = rhs  # Right-hand side after transformation

    def apply(self, input_seq: List[Any]) -> List[Any]:
        """
        Applies the morphological transformation to an input sequence.
        """
        if self.lhs in input_seq:
            idx = input_seq.index(self.lhs)
            return input_seq[:idx] + [elem for elem in self.rhs] + input_seq[idx + 1 :]
        return input_seq

#------------------------------------------------------------------------------
@runtime_checkable
class AtomProtocol(Protocol[T, V]):
    """
    Minimal interface for atomic entities.
    Supports multiple representations and quantum-like state transitions.
    """
    id: str
    state: QuantumState
    flavor: ByteWordFlavor
    
    def encode(self) -> bytes:
        """Serialize to bytes"""
        ...
    
    @classmethod
    def decode(cls, data: bytes) -> 'AtomProtocol':
        """Deserialize from bytes"""
        ...
    
    def collapse(self) -> V:
        """Force state resolution (measurement)"""
        ...
    
    def entangle_with(self, other: 'AtomProtocol') -> None:
        """Create quantum entanglement"""
        ...

#------------------------------------------------------------------------------
# POLYMORPHIC BASE ATOM - Mutable/Immutable Toggle
#------------------------------------------------------------------------------
class BaseAtom(ABC, Generic[T, V]):
    """
    Abstract base for all atoms with polymorphic identity.
    Toggles between mutable dataclass and immutable struct modes.
    """
    __slots__ = ('_id', '_state', '_flavor', '_value', '_metadata', '_birth_time')
    # __slots__ = ('__weakref__',)  # if @frozen
    def __init__(
        self, 
        value: V,
        flavor: ByteWordFlavor = ByteWordFlavor.MUTABLE,
        state: QuantumState = QuantumState.SUPERPOSITION
    ):
        self._id = str(uuid.uuid4())
        self._state = state
        self._flavor = flavor
        self._value = value
        self._metadata: Dict[str, Any] = {}
        self._birth_time = time.time()
        
        # Apply flavor-specific initialization
        self._configure_flavor()

    def __post_init__(self):
        """Validate all fields after initialization."""
        annotations = self.__annotations__
        
        for field_name, expected_type in annotations.items():
            value = getattr(self, field_name)
            
            # === Type validation ===
            if not _matches_type(value, expected_type):
                raise TypeError(
                    f"{self.__class__.__name__}.{field_name}: expected {expected_type}, "
                    f"got {type(value).__name__}"
                )
            
            # === Metadata-based validation ===
            field_obj = next((f for f in fields(self) if f.name == field_name), None)
            if field_obj:
                validators = field_obj.metadata.get("validate")
                if validators:
                    for validator in (validators if isinstance(validators, (list, tuple)) else (validators,)):
                        validator(value)
            
            # === Method-based validation (validate_fieldname) ===
            validator_method = getattr(self, f'validate_{field_name}', None)
            if validator_method and callable(validator_method):
                # Support both direct callable and decorated methods with _validators
                if hasattr(validator_method, '_validators'):
                    for validator in validator_method._validators:
                        validator(value)
                else:
                    validator_method(value)
        
        # === Model-level validation ===
        if hasattr(self, '_validate_model'):
            self._validate_model()

    def _validate_model(self):
        """Override for model-level validation logic."""
        pass

    def _configure_flavor(self) -> None:
        """Apply flavor-specific configuration"""
        if self._flavor == ByteWordFlavor.IMMUTABLE:
            self._freeze()
        elif self._flavor == ByteWordFlavor.HOMOICONIC:
            self._enable_introspection()
        elif self._flavor == ByteWordFlavor.POLYMORPHIC:
            self._enable_dynamic_typing()
    
    def _freeze(self) -> None:
        """Make atom immutable (struct-like)"""
        original_setattr = self.__setattr__
        
        def frozen_setattr(name: str, value: Any) -> None:
            if name.startswith('_') and hasattr(self, name):
                raise AttributeError(f"Cannot modify frozen attribute: {name}")
            original_setattr(name, value)
        
        self.__setattr__ = frozen_setattr.__get__(self, type(self))
    
    def _enable_introspection(self) -> None:
        """Enable code-as-data reflection"""
        self._metadata['source'] = inspect.getsource(type(self))
        self._metadata['ast'] = ast.dump(ast.parse(self._metadata['source']))
    
    def _enable_dynamic_typing(self) -> None:
        """Enable runtime type identity changes"""
        self._metadata['type_history'] = [type(self._value).__name__]
    
    @property
    def id(self) -> str:
        return self._id
    
    @property
    def state(self) -> QuantumState:
        return self._state
    
    @property
    def flavor(self) -> ByteWordFlavor:
        return self._flavor
    
    @property
    def value(self) -> V:
        """Get value, potentially collapsing superposition"""
        if self._state == QuantumState.SUPERPOSITION:
            self._collapse_superposition()
        return self._value
    
    @value.setter
    def value(self, new_value: V) -> None:
        """Set value with flavor-specific checks"""
        if self._flavor == ByteWordFlavor.IMMUTABLE:
            raise AttributeError("Cannot modify immutable atom")
        
        if self._flavor == ByteWordFlavor.POLYMORPHIC:
            self._metadata['type_history'].append(type(new_value).__name__)
        
        self._value = new_value
    
    def _collapse_superposition(self) -> None:
        """Collapse quantum state to definite value"""
        if self._state == QuantumState.SUPERPOSITION:
            self._state = QuantumState.COLLAPSED
            logger.debug(f"Atom {self.id} collapsed to state: {self._value}")
    
    def collapse(self) -> V:
        """Force measurement/observation"""
        self._collapse_superposition()
        return self._value
    
    def entangle_with(self, other: 'BaseAtom') -> None:
        """Create entanglement relationship"""
        if not hasattr(self, '_entangled'):
            self._entangled: List[weakref.ref] = []
        self._entangled.append(weakref.ref(other))
        if not hasattr(other, '_entangled'):
            other._entangled = []
        other._entangled.append(weakref.ref(self))
        self._state = QuantumState.ENTANGLED
        other._state = QuantumState.ENTANGLED
        logger.debug(f"Entangled atoms: {self.id} <-> {other.id}")

    # === Core Serialization Methods ===
    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        """Create instance from dictionary with nested model support and coercion."""
        if not isinstance(data, dict):
            raise ValueError(f"Expected dict, got {type(data).__name__}")
        # Filter to only known fields
        field_names = {f.name for f in fields(cls)}
        init_data = {k: v for k, v in data.items() if k in field_names}
        # Get type hints for coercion
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
        """Convert to dictionary with nested model support."""
        result = {}
        for f in fields(self):
            value = getattr(self, f.name)
            if exclude_none and value is None:
                continue
            result[f.name] = _uncoerce(value)
        return result

    @abstractmethod
    def encode(self) -> bytes:
        """Serialize to bytes - subclass must implement"""
        pass
    
    @classmethod
    @abstractmethod
    def decode(cls, data: bytes) -> 'BaseAtom':
        """Deserialize from bytes - subclass must implement"""
        pass
    
    def to_dict(self) -> Dict[str, Any]:
        """Export to dictionary representation"""
        return {
            'id': self.id,
            'state': self.state.name,
            'flavor': self.flavor.name,
            'value': self._value,
            'metadata': self._metadata,
            'birth_time': self._birth_time
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BaseAtom':
        """Reconstruct from dictionary"""
        atom = cls(
            value=data['value'],
            flavor=ByteWordFlavor[data['flavor']],
            state=QuantumState[data['state']]
        )
        atom._metadata = data.get('metadata', {})
        atom._birth_time = data.get('birth_time', time.time())
        return atom
    
    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}("
                f"id={self.id[:8]}..., "
                f"state={self.state.name}, "
                f"flavor={self.flavor.name}, "
                f"value={self._value!r})")

    # === Shared Validators ===
    @staticmethod
    def must_be_str(x: Any) -> None:
        """Validator: ensure value is a string."""
        if not isinstance(x, str):
            raise ValueError(f"Expected a string, got {type(x).__name__}")

    @staticmethod
    def non_negative(x: Any) -> None:
        """Validator: ensure value is a non-negative number."""
        if not isinstance(x, (int, float)) or x < 0:
            raise ValueError(f"Expected a non-negative number, got {x!r}")

    @staticmethod
    def positive(x: Any) -> None:
        """Validator: ensure value is positive."""
        if not isinstance(x, (int, float)) or x <= 0:
            raise ValueError(f"Expected a positive number, got {x!r}")

    @staticmethod
    def non_empty_str(x: Any) -> None:
        """Validator: ensure value is a non-empty string."""
        if not isinstance(x, str) or not x.strip():
            raise ValueError(f"Expected a non-empty string, got {x!r}")


    # === Immutable Update Methods ===
    def replace(self, **changes) -> T:
        """Immutable clone with changes (dataclass-style)."""
        data = self.to_dict()
        data.update(changes)
        return self.__class__.from_dict(data)

    def clone(self, **overrides) -> T:
        """Create a copy with optional field overrides (alias for replace)."""
        return self.replace(**overrides)

    # === Multi-Layer Communication Support ===
    def to_datagram(self, format: SerializationFormat = SerializationFormat.JSON) -> bytes:
        """Serialize to bytes for datagram transmission (UDP, etc.)."""
        if format == SerializationFormat.JSON:
            return json.dumps(self.to_dict()).encode('utf-8')
        elif format == SerializationFormat.PICKLE:
            return pickle.dumps(self)
        elif format == SerializationFormat.REPR:
            return repr(self).encode('utf-8')
        else:
            raise ValueError(f"Unsupported format: {format}")

    @classmethod
    def from_datagram(cls: Type[T], data: bytes, format: SerializationFormat = SerializationFormat.JSON) -> T:
        """Deserialize from bytes datagram."""
        if format == SerializationFormat.JSON:
            return cls.from_dict(json.loads(data.decode('utf-8')))
        elif format == SerializationFormat.PICKLE:
            return pickle.loads(data)
        elif format == SerializationFormat.REPR:
            # This would require eval - not recommended for untrusted data
            raise NotImplementedError("REPR deserialization requires eval - unsafe")
        else:
            raise ValueError(f"Unsupported format: {format}")

    def to_json(self, **kwargs) -> str:
        """Serialize to JSON string."""
        return json.dumps(self.to_dict(), **kwargs)

    @classmethod
    def from_json(cls: Type[T], json_str: str) -> T:
        """Deserialize from JSON string."""
        return cls.from_dict(json.loads(json_str))

    def to_base64(self, format: SerializationFormat = SerializationFormat.JSON) -> str:
        """Encode as base64 string for text-based protocols."""
        return base64.b64encode(self.to_datagram(format)).decode('ascii')

    @classmethod
    def from_base64(cls: Type[T], b64_str: str, format: SerializationFormat = SerializationFormat.JSON) -> T:
        """Decode from base64 string."""
        return cls.from_datagram(base64.b64decode(b64_str), format)

    # === Identity and Hashing ===
    def fingerprint(self) -> str:
        """Generate a content-based fingerprint for caching/deduplication."""
        content = json.dumps(self.to_dict(), sort_keys=True, separators=(',', ':'))
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def checksum(self) -> str:
        """Generate a checksum for data integrity verification."""
        return hashlib.md5(self.to_datagram()).hexdigest()

    # === RPC/REST Helpers ===
    @classmethod
    def get_schema(cls) -> Dict[str, Any]:
        """Generate a basic schema for API documentation."""
        schema = {
            "type": "object",
            "properties": {},
            "required": []
        }
        
        field_types = get_type_hints(cls)
        for f in fields(cls):
            field_type = field_types.get(f.name, Any)
            schema["properties"][f.name] = _type_to_schema(field_type)
            if f.default == f.default_factory == dataclass.MISSING:
                schema["required"].append(f.name)
        
        return schema

    def validate_partial(self, **partial_data) -> Dict[str, Any]:
        """Validate partial data without creating instance (useful for PATCH operations)."""
        field_types = get_type_hints(self.__class__)
        validated = {}
        
        for field_name, value in partial_data.items():
            if field_name in field_types:
                expected_type = field_types[field_name]
                if not _matches_type(value, expected_type):
                    raise TypeError(f"{field_name}: expected {expected_type}, got {type(value).__name__}")
                validated[field_name] = _coerce(value, expected_type)
            else:
                raise ValueError(f"Unknown field: {field_name}")
        
        return validated

    # === Debug and Development Helpers ===
    def diff(self, other: 'BaseModel') -> Dict[str, Dict[str, Any]]:
        """Compare with another instance and return differences."""
        if not isinstance(other, self.__class__):
            raise TypeError(f"Can only diff with same type, got {type(other)}")
        
        diffs = {}
        for f in fields(self):
            self_val = getattr(self, f.name)
            other_val = getattr(other, f.name)
            if self_val != other_val:
                diffs[f.name] = {"self": self_val, "other": other_val}
        
        return diffs

    def __repr__(self) -> str:
        """Clean representation for debugging and repr-based serialization."""
        kv = ", ".join(f"{f.name}={getattr(self, f.name)!r}" for f in fields(self))
        return f"{self.__class__.__name__}({kv})"

    def __str__(self) -> str:
        return self.__repr__()

def _type_to_schema(tp: Any) -> Dict[str, Any]:
    """Convert Python type to JSON schema format."""
    if tp is str:
        return {"type": "string"}
    elif tp is int:
        return {"type": "integer"}
    elif tp is float:
        return {"type": "number"}
    elif tp is bool:
        return {"type": "boolean"}
    elif tp is list or get_origin(tp) is list:
        args = get_args(tp)
        item_schema = _type_to_schema(args[0]) if args else {"type": "any"}
        return {"type": "array", "items": item_schema}
    elif tp is dict or get_origin(tp) is dict:
        return {"type": "object"}
    elif get_origin(tp) is Union:
        # Handle Optional and Union types
        args = get_args(tp)
        if len(args) == 2 and type(None) in args:
            # Optional type
            non_none_type = next(arg for arg in args if arg is not type(None))
            schema = _type_to_schema(non_none_type)
            schema["nullable"] = True
            return schema
        else:
            # Union type - return anyOf
            return {"anyOf": [_type_to_schema(arg) for arg in args]}
    elif inspect.isclass(tp) and issubclass(tp, BaseModel):
        return tp.get_schema()
    else:
        return {"type": "any"}

class Atom(Generic[T, V, C]):
    """
    Abstract Base Class for all Atom types.

    Atoms are the smallest units of data or executable code, and this interface
    defines common operations such as encoding, decoding, execution, and conversion
    to data classes.

    Attributes:
        grammar_rules (List[GrammarRule]): List of grammar rules defining the syntax of the Atom.
    """

    __slots__ = (
        "_id",
        "_value",
        "_type",
        "_metadata",
        "_children",
        "_parent",
        "hash",
        "tag",
        "children",
        "metadata",
    )
    type: Union[str, str]
    value: Union[T, V, C] = field(default=None)
    grammar_rules: List[GrammarRule] = field(default_factory=list)
    id: str = field(init=False)
    case_base: Dict[str, Callable[..., bool]] = field(default_factory=dict)

    # use __slots__ & list comprehension for (meta) 'atomic init', instead of:
    # tag: str = ''
    # children: List['Atom'] = field(default_factory=list)
    # metadata: Dict[str, Any] = field(default_factory=dict)
    # hash: str = field(init=False)
    def __init__(self, value: Union[T, V, C], type: Union[DataType, AtomType]):
        self._value = value
        self._type = type
        self._metadata = {}
        self._children = []
        self._parent = None
        self.hash = hashlib.sha256(repr(self._value).encode()).hexdigest()
        self.tag = ""
        self.children = []
        self.metadata = {}

    # relational atomistic logic (inherent when num atoms > 1)
    def __post_init__(self):
        self.case_base = {
            "⊤": lambda x, _: x,
            "⊥": lambda _, y: y,
            "¬": lambda a: not a,
            "∧": lambda a, b: a and b,
            "∨": lambda a, b: a or b,
            "→": lambda a, b: (not a) or b,
            "↔": lambda a, b: (a and b) or (not a and not b),
        }

    reflexivity: Callable[[T], bool] = lambda x: x == x
    symmetry: Callable[[T, T], bool] = lambda x, y: x == y
    transitivity: Callable[[T, T, T], bool] = lambda x, y, z: x == y and y == z
    transparency: Callable[[Callable[..., T], T, T], T] = lambda f, x, y: (
        f(True, x, y) if x == y else None
    )

    def process_attributes(
        self, mapping_description: Dict[str, Any], input_data: Dict[str, Any]
    ) -> None:
        """
        Use the `mapper` function to process input data and map it to attributes.

        Args:
            mapping_description (Dict[str, Any]): The mapping description for transformation.
            input_data (Dict[str, Any]): Data to be processed and mapped.
        """
        mapped_data = mapper(mapping_description, input_data)
        for key, value in mapped_data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        # Log or process additional logic if required

    def encode(self) -> bytes:
        return json.dumps({"id": self.id, "attributes": self.attributes}).encode()

    @classmethod
    def decode(cls, data: bytes) -> "Atom":
        decoded_data = json.loads(data.decode())
        return cls(id=decoded_data["id"], **decoded_data["attributes"])

    def introspect(self) -> str:
        """
        Reflect on its own code structure via AST.
        """
        source = inspect.getsource(self.__class__)
        return ast.dump(ast.parse(source))

    def __repr__(self):
        return f"{self.value} : {self.type}"

    def __str__(self):
        return str(self.value)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Atom) and self.hash == other.hash

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

    def __buffer__(self, flags: int) -> memoryview:  # Buffer protocol
        return memoryview(self.value)

    async def send_message(self, message: Any, ttl: int = 3) -> None:
        if ttl <= 0:
            logging.info(f"Message {message} dropped due to TTL")
            return
        logging.info(f"Atom {self.id} received message: {message}")
        for sub in self.subscribers:
            await sub.receive_message(message, ttl - 1)

    async def receive_message(self, message: Any, ttl: int) -> None:
        logging.info(
            f"Atom {self.id} processing received message: {message} with TTL {ttl}"
        )
        await self.send_message(message, ttl)

    def subscribe(self, atom: "Atom") -> None:
        self.subscribers.add(atom)
        logging.info(f"Atom {self.id} subscribed to {atom.id}")

    def unsubscribe(self, atom: "Atom") -> None:
        self.subscribers.discard(atom)
        logging.info(f"Atom {self.id} unsubscribed from {atom.id}")

    __getitem__ = lambda self, key: self.value[key]
    __setitem__ = lambda self, key, value: setattr(self.value, key, value)
    __delitem__ = lambda self, key: delattr(self.value, key)
    __len__ = lambda self: len(self.value)
    __iter__ = lambda self: iter(self.value)
    __contains__ = lambda self, item: item in self.value
    __call__ = lambda self, *args, **kwargs: self.value(*args, **kwargs)
    __add__ = lambda self, other: self.value + other
    __sub__ = lambda self, other: self.value - other
    __mul__ = lambda self, other: self.value * other
    __truediv__ = lambda self, other: self.value / other
    __floordiv__ = lambda self, other: self.value // other

    @staticmethod
    def serialize_data(data: Any) -> bytes:
        return msgpack.packb(data, use_bin_type=True)
        pass

    @staticmethod
    def deserialize_data(data: bytes) -> Any:
        return msgpack.unpackb(data, raw=False)
        pass

#------------------------------------------------------------------------------
# CONCRETE ATOM IMPLEMENTATIONS
#------------------------------------------------------------------------------
@dataclass
class DataAtom(BaseAtom[type, Any]):
    """Concrete atom for data storage with validation"""
    
    def __init__(
        self, 
        value: Any,
        expected_type: Optional[Type] = None,
        flavor: ByteWordFlavor = ByteWordFlavor.MUTABLE,
        state: QuantumState = QuantumState.COLLAPSED
    ):
        super().__init__(value, flavor, state)
        self._expected_type = expected_type or type(value)
        self._validate()
    
    def _validate(self) -> None:
        """Type validation"""
        if not isinstance(self._value, self._expected_type):
            raise TypeError(
                f"Value {self._value!r} does not match expected type {self._expected_type}"
            )
    
    def encode(self) -> bytes:
        """JSON encoding for data atoms"""
        return json.dumps(self.to_dict()).encode('utf-8')
    
    @classmethod
    def decode(cls, data: bytes) -> 'DataAtom':
        """JSON decoding"""
        dict_data = json.loads(data.decode('utf-8'))
        return cls.from_dict(dict_data)

@dataclass
class CodeAtom(BaseAtom[Callable, Callable]):
    """Atom representing executable code (homoiconic)"""
    
    def __init__(
        self,
        value: Callable,
        flavor: ByteWordFlavor = ByteWordFlavor.HOMOICONIC,
        state: QuantumState = QuantumState.SUPERPOSITION
    ):
        if not callable(value):
            raise TypeError("CodeAtom requires callable value")
        super().__init__(value, flavor, state)
    
    def execute(self, *args, **kwargs) -> Any:
        """Execute the contained code"""
        self.collapse()  # Force resolution
        return self._value(*args, **kwargs)
    
    def encode(self) -> bytes:
        """Encode as source code"""
        try:
            source = inspect.getsource(self._value)
            return source.encode('utf-8')
        except (OSError, TypeError):
            # Fallback for lambdas or built-ins
            return repr(self._value).encode('utf-8')
    
    @classmethod
    def decode(cls, data: bytes) -> 'CodeAtom':
        """Reconstruct from source"""
        source = data.decode('utf-8')
        code_obj = compile(source, '<atom>', 'exec')
        namespace = {}
        exec(code_obj, namespace)
        # Extract first callable
        func = next((v for v in namespace.values() if callable(v)), None)
        if func is None:
            raise ValueError("No callable found in decoded source")
        return cls(func)

#------------------------------------------------------------------------------
# INTERPRETER-FIRST EXECUTION ENGINE
#------------------------------------------------------------------------------
@dataclass
class InterpreterConfig:
    """Configuration for sub-interpreter execution"""
    mode: ExecutionMode = ExecutionMode.INTERPRETER
    shared_memory_size: int = 8192
    timeout: float = 10.0
    enable_lazy_verification: bool = True
    fallback_to_threading: bool = True

class InterpreterAtom(BaseAtom[Callable, Any]):
    """
    Atom that executes in isolated sub-interpreter.
    Falls back to threading if interpreter creation fails.
    """
    
    def __init__(
        self,
        value: Callable,
        config: Optional[InterpreterConfig] = None,
        flavor: ByteWordFlavor = ByteWordFlavor.POLYMORPHIC,
        state: QuantumState = QuantumState.SUPERPOSITION
    ):
        super().__init__(value, flavor, state)
        self.config = config or InterpreterConfig()
        self._interp: Optional[interpreters.Interpreter] = None
        self._thread: Optional[threading.Thread] = None
        self._result: Optional[Any] = None
        self._error: Optional[Exception] = None
        self._channels: Optional[Tuple] = None
    
    def _create_interpreter(self) -> bool:
        """Attempt to create sub-interpreter"""
        try:
            self._interp = interpreters.create()
            recv_ch, send_ch = interpreters.create_channel()
            self._channels = (recv_ch, send_ch)
            logger.info(f"Created sub-interpreter for atom {self.id[:8]}")
            return True
        except Exception as e:
            logger.warning(f"Failed to create sub-interpreter: {e}")
            if self.config.fallback_to_threading:
                logger.info("Falling back to threading mode")
                return False
            raise
    
    def _execute_in_interpreter(self) -> None:
        """Execute code in sub-interpreter"""
        if self._interp is None or self._channels is None:
            raise RuntimeError("Interpreter not initialized")
        
        recv_ch, send_ch = self._channels
        
        # Prepare worker function
        def worker():
            try:
                result = self._value()
                send_ch.send(json.dumps({'status': 'success', 'result': result}))
            except Exception as e:
                send_ch.send(json.dumps({'status': 'error', 'error': str(e)}))
        
        # Execute in thread within interpreter
        try:
            thread = self._interp.call_in_thread(worker)
            thread.join(timeout=self.config.timeout)
            
            if thread.is_alive():
                raise TimeoutError(f"Execution exceeded {self.config.timeout}s")
            
            # Retrieve result
            response = json.loads(recv_ch.recv(timeout=1.0))
            if response['status'] == 'success':
                self._result = response['result']
            else:
                self._error = RuntimeError(response['error'])
                
        except Exception as e:
            self._error = e
            logger.exception(f"Interpreter execution failed for atom {self.id[:8]}")
    
    def _execute_in_thread(self) -> None:
        """Fallback: execute in thread"""
        def worker():
            try:
                self._result = self._value()
            except Exception as e:
                self._error = e
        
        self._thread = threading.Thread(target=worker, daemon=True)
        self._thread.start()
        self._thread.join(timeout=self.config.timeout)
        
        if self._thread.is_alive():
            logger.warning(f"Thread execution timeout for atom {self.id[:8]}")
            self._error = TimeoutError(f"Execution exceeded {self.config.timeout}s")
    
    def execute(self) -> Any:
        """Execute with interpreter-first strategy"""
        self.collapse()  # Force state resolution
        
        if self.config.mode == ExecutionMode.INLINE:
            # Direct execution (no isolation)
            return self._value()
        
        # Attempt interpreter execution
        if self.config.mode == ExecutionMode.INTERPRETER:
            if self._create_interpreter():
                self._execute_in_interpreter()
            elif self.config.fallback_to_threading:
                self._execute_in_thread()
            else:
                raise RuntimeError("Interpreter creation failed and fallback disabled")
        else:
            # Threading mode
            self._execute_in_thread()
        
        # Check for errors
        if self._error:
            raise self._error
        
        return self._result
    
    def cleanup(self) -> None:
        """Clean up interpreter resources"""
        if self._interp and not self._interp.is_running():
            self._interp.close()
            logger.debug(f"Closed interpreter for atom {self.id[:8]}")
    
    def encode(self) -> bytes:
        """Encode with execution metadata"""
        data = self.to_dict()
        data['config'] = {
            'mode': self.config.mode.name,
            'timeout': self.config.timeout
        }
        return json.dumps(data).encode('utf-8')
    
    @classmethod
    def decode(cls, data: bytes) -> 'InterpreterAtom':
        """Reconstruct with config"""
        dict_data = json.loads(data.decode('utf-8'))
        config_data = dict_data.pop('config', {})
        config = InterpreterConfig(
            mode=ExecutionMode[config_data.get('mode', 'INTERPRETER')],
            timeout=config_data.get('timeout', 10.0)
        )
        atom = cls.from_dict(dict_data)
        atom.config = config
        return atom

@dataclass
class InterpreterConfig:
    """Configuration for sub-interpreter execution"""

    mode: ExecutionMode = ExecutionMode.INTERPRETER
    shared_memory_size: int = 8192
    timeout: float = 10.0
    enable_lazy_verification: bool = True
    fallback_to_threading: bool = True


class InterpreterAtom(BaseAtom[Callable, Any]):
    """
    Atom that executes in isolated sub-interpreter.
    Falls back to threading if interpreter creation fails.
    """

    def __init__(
        self,
        value: Callable,
        config: Optional[InterpreterConfig] = None,
        flavor: ByteWordFlavor = ByteWordFlavor.POLYMORPHIC,
        state: QuantumState = QuantumState.SUPERPOSITION,
    ):
        super().__init__(value, flavor, state)
        self.config = config or InterpreterConfig()
        self._interp: Optional[interpreters.Interpreter] = None
        self._thread: Optional[threading.Thread] = None
        self._result: Optional[Any] = None
        self._error: Optional[Exception] = None
        self._channels: Optional[Tuple] = None

    def _create_interpreter(self) -> bool:
        """Attempt to create sub-interpreter"""
        try:
            self._interp = interpreters.create()
            recv_ch, send_ch = interpreters.create_channel()
            self._channels = (recv_ch, send_ch)
            logger.info(f"Created sub-interpreter for atom {self.id[:8]}")
            return True
        except Exception as e:
            logger.warning(f"Failed to create sub-interpreter: {e}")
            if self.config.fallback_to_threading:
                logger.info("Falling back to threading mode")
                return False
            raise

    def _execute_in_interpreter(self) -> None:
        """Execute code in sub-interpreter"""
        if self._interp is None or self._channels is None:
            raise RuntimeError("Interpreter not initialized")

        recv_ch, send_ch = self._channels

        # Prepare worker function
        def worker():
            try:
                result = self._value()
                send_ch.send(json.dumps({'status': 'success', 'result': result}))
            except Exception as e:
                send_ch.send(json.dumps({'status': 'error', 'error': str(e)}))

        # Execute in thread within interpreter
        try:
            thread = self._interp.call_in_thread(worker)
            thread.join(timeout=self.config.timeout)

            if thread.is_alive():
                raise TimeoutError(f"Execution exceeded {self.config.timeout}s")

            # Retrieve result
            response = json.loads(recv_ch.recv(timeout=1.0))
            if response['status'] == 'success':
                self._result = response['result']
            else:
                self._error = RuntimeError(response['error'])

        except Exception as e:
            self._error = e
            logger.exception(f"Interpreter execution failed for atom {self.id[:8]}")

    def _execute_in_thread(self) -> None:
        """Fallback: execute in thread"""

        def worker():
            try:
                self._result = self._value()
            except Exception as e:
                self._error = e

        self._thread = threading.Thread(target=worker, daemon=True)
        self._thread.start()
        self._thread.join(timeout=self.config.timeout)

        if self._thread.is_alive():
            logger.warning(f"Thread execution timeout for atom {self.id[:8]}")
            self._error = TimeoutError(f"Execution exceeded {self.config.timeout}s")

    def execute(self) -> Any:
        """Execute with interpreter-first strategy"""
        self.collapse()  # Force state resolution

        if self.config.mode == ExecutionMode.INLINE:
            # Direct execution (no isolation)
            return self._value()

        # Attempt interpreter execution
        if self.config.mode == ExecutionMode.INTERPRETER:
            if self._create_interpreter():
                self._execute_in_interpreter()
            elif self.config.fallback_to_threading:
                self._execute_in_thread()
            else:
                raise RuntimeError("Interpreter creation failed and fallback disabled")
        else:
            # Threading mode
            self._execute_in_thread()

        # Check for errors
        if self._error:
            raise self._error

        return self._result

    def cleanup(self) -> None:
        """Clean up interpreter resources"""
        if self._interp and not self._interp.is_running():
            self._interp.close()
            logger.debug(f"Closed interpreter for atom {self.id[:8]}")

    def encode(self) -> bytes:
        """Encode with execution metadata"""
        data = self.to_dict()
        data['config'] = {'mode': self.config.mode.name, 'timeout': self.config.timeout}
        return json.dumps(data).encode('utf-8')

    @classmethod
    def decode(cls, data: bytes) -> 'InterpreterAtom':
        """Reconstruct with config"""
        dict_data = json.loads(data.decode('utf-8'))
        config_data = dict_data.pop('config', {})
        config = InterpreterConfig(
            mode=ExecutionMode[config_data.get('mode', 'INTERPRETER')],
            timeout=config_data.get('timeout', 10.0),
        )
        atom = cls.from_dict(dict_data)
        atom.config = config
        return atom


class PyObj:
    """Abstract base class for Python object representation"""

    pass


@dataclass
class CPythonFrame(PyObj):
    """
    Quantum-informed object representation
    Maps directly to CPython's PyObject structure with quantum properties
    """

    type_ptr: int  # Memory address of type object
    value: V
    type: Type[T]
    refcount: int = field(default=1)
    ttl: Optional[int] = None
    state: QuantumState = field(default=QuantumState.SUPERPOSITION)

    # Add a quantum byte to represent the quantum state evolution
    quantum_byte: QuantumByte = field(default=None)

    def setattr(self, name, value):
        return super().__setattr__(name, value)

    @classmethod
    def from_object(cls, obj: object) -> 'CPythonFrame':
        """Extract CPython frame data from any Python object"""
        # Create a quantum byte based on the object's hash
        obj_hash = (
            hash(obj)
            if hasattr(obj, '__hash__') and obj.__hash__ is not None
            else id(obj)
        )
        q_byte = QuantumByte(state=obj_hash & 0xFF)

        return cls(
            type_ptr=id(type(obj)),
            value=obj,
            type=type(obj),
            refcount=sys.getrefcount(obj) - 1,
            quantum_byte=q_byte,
        )

    def __post_init__(self):
        """Initialize with timestamp and quantum properties"""
        self._birth_timestamp = time.time()
        self._state = QuantumState.CLASSICAL  # Initialize default state
        self._value = self.value  # Initialize _value from the provided value

        # Initialize quantum byte if not provided
        if self.quantum_byte is None:
            # Create a quantum byte from the hash of the value
            value_hash = (
                hash(self.value)
                if hasattr(self.value, '__hash__') and self.value.__hash__ is not None
                else id(self.value)
            )
            self.quantum_byte = QuantumByte(state=value_hash & 0xFF)

        if self.ttl is not None:
            self._ttl_expiration = self._birth_timestamp + self.ttl
            self._ttl_expiration_timestamp = time.time()
        else:
            self._ttl_expiration = None

        if self.state == QuantumState.SUPERPOSITION:
            # Initialize superposition with multiple potential states
            # by evolving the quantum byte
            states = self.quantum_byte.evolve(5)  # Generate 5 potential states
            self._superposition = [self.value] + [
                states[i] for i in range(1, len(states))
            ]
            self._superposition_timestamp = time.time()
        else:
            self._superposition = None

        if self.state == QuantumState.ENTANGLED:
            self._entanglement = [self.value]
            self._entanglement_timestamp = time.time()
        else:
            self._entanglement = None

        if self.type.__module__ == 'builtins':
            """All 'knowledge' aka data is treated as python modules and these are the flags for controlling what is canon."""
            self._is_primitive = True
            self._primitive_type = self.type.__name__
            self._primitive_value = self.value
        else:
            self._is_primitive = False

    @property
    def refcount(self) -> int:
        """Reference count tracking"""
        return self._refcount

    @refcount.setter
    def refcount(self, value: int) -> None:
        """Set the reference count"""
        self._refcount = value

    @property
    def state(self) -> QuantumState:
        """Current quantum-like state"""
        return self._state if self._state is not None else QuantumState.CLASSICAL

    def collapse(self) -> V:
        """
        Force state resolution using Born rule-like probability
        Collapses superposition based on entropy values
        """
        if self._state != QuantumState.COLLAPSED:
            if self._state == QuantumState.SUPERPOSITION and self._superposition:
                # Use entropy to guide probability of collapse
                # This mimics the Born rule from quantum mechanics
                weights = []
                for _ in range(len(self._superposition)):
                    self.quantum_byte.rotate()  # Rotate to get a new state
                    weights.append(self.quantum_byte.entropy())

                # Normalize weights to sum to 1.0
                total = sum(weights) or 1.0  # Avoid division by zero
                normalized_weights = [w / total for w in weights]

                # Choose a value based on weights
                chosen_index = random.choices(
                    range(len(self._superposition)), weights=normalized_weights, k=1
                )[0]

                self._value = self._superposition[chosen_index]

            self._state = QuantumState.COLLAPSED

        return self._value

    def entangle_with(self, other: 'CPythonFrame') -> None:
        """
        Create quantum entanglement with another object.
        Entangled objects share quantum state evolution.
        """
        if self._entanglement is None:
            self._entanglement = [self.value]
        if other._entanglement is None:
            other._entanglement = [other.value]

        # Entangle quantum byte states through XOR operation
        # This creates a shared quantum state
        entangled_state = (self.quantum_byte.state ^ other.quantum_byte.state) & 0xFF
        self.quantum_byte.state = entangled_state
        other.quantum_byte.state = entangled_state

        # Share superposition states between objects
        self._entanglement.extend(other._entanglement)
        other._entanglement = self._entanglement
        self.state = other.state = QuantumState.ENTANGLED

    def check_ttl(self) -> bool:
        """Check if TTL expired and collapse state if necessary."""
        if self.ttl is not None and time.time() >= self._ttl_expiration:
            self.collapse()
            return True
        return False

    def observe(self) -> V:
        """
        Collapse state upon observation if necessary.
        This implements Born rule by using the quantum byte's entropy.
        """
        self.check_ttl()

        if self.state == QuantumState.SUPERPOSITION:
            # Before collapsing, evolve the quantum state to mimic wave function dynamics
            self.quantum_byte.rotate()

            # Calculate probability distribution based on entropy
            entropy = self.quantum_byte.entropy()
            collapse_prob = entropy / math.log(2)  # Normalized entropy

            # Collapse with probability proportional to entropy
            if random.random() <= collapse_prob:
                self.collapse()
        elif self.state == QuantumState.ENTANGLED:
            # Evolve entangled state when observed
            self.quantum_byte.rotate()
            self.collapse()

        return self.value

    def get_measurement_histogram(self, measurements: int = 100) -> dict:
        """
        Perform multiple measurements to build a probability histogram.
        This helps visualize the Born rule distribution.
        """
        if self.state == QuantumState.COLLAPSED:
            return {str(self.value): measurements}

        # Save original state to restore after measurements
        original_state = self.state
        original_value = self.value

        # Create a copy of superposition/entanglement
        if self._superposition:
            original_superposition = self._superposition.copy()
        if hasattr(self, '_entanglement') and self._entanglement:
            original_entanglement = self._entanglement.copy()

        # Perform measurements
        results = {}
        for _ in range(measurements):
            # Need to reset state for each measurement
            if original_state == QuantumState.SUPERPOSITION:
                self._state = QuantumState.SUPERPOSITION
                self._superposition = original_superposition.copy()
            elif original_state == QuantumState.ENTANGLED:
                self._state = QuantumState.ENTANGLED
                self._entanglement = original_entanglement.copy()

            # Observe (which may collapse)
            result = str(self.observe())
            results[result] = results.get(result, 0) + 1

        # Restore original state
        self._state = original_state
        self._value = original_value

        return results


class QuantumOperator:
    """
    Represents a quantum operator as a matrix in a Hilbert space.
    """

    def __init__(
        self,
        hilbert_space: HilbertSpace,
        matrix: Optional[List[List[MorphicComplex]]] = None,
    ):
        self.hilbert_space = hilbert_space
        dim = hilbert_space.dimension

        if matrix:
            if len(matrix) != dim or any(len(row) != dim for row in matrix):
                raise ValueError("Operator matrix must match Hilbert space dimension")
            self.matrix = matrix
        else:
            # Default to identity operator
            self.matrix = [
                [MorphicComplex(1 if i == j else 0, 0) for j in range(dim)]
                for i in range(dim)
            ]

    def apply_to(self, state: QuantumState) -> None:
        """Apply this operator to a quantum state, modifying it in place"""
        if state.space.dimension != self.hilbert_space.dimension:
            raise ValueError("Hilbert space dimensions don't match")

        result = []
        for i in range(self.hilbert_space.dimension):
            amplitude = MorphicComplex(0, 0)
            for j in range(self.hilbert_space.dimension):
                amplitude = amplitude + (self.matrix[i][j] * state.amplitudes[j])
            result.append(amplitude)

        state.amplitudes = result
        state.normalize()

    def apply(self, state_vector: List[MorphicComplex]) -> List[MorphicComplex]:
        """Apply this operator to a raw state vector, returning a new vector"""
        if len(state_vector) != self.hilbert_space.dimension:
            raise ValueError("Vector dimension doesn't match Hilbert space dimension")

        result = []
        for i in range(self.hilbert_space.dimension):
            amplitude = MorphicComplex(0, 0)
            for j in range(self.hilbert_space.dimension):
                amplitude = amplitude + (self.matrix[i][j] * state_vector[j])
            result.append(amplitude)

        return result

    def __mul__(self, other: Union['QuantumOperator', float, int]) -> 'QuantumOperator':
        """Multiply by another operator or a scalar"""
        if isinstance(other, (int, float)):
            # Scalar multiplication
            result = [
                [self.matrix[i][j] * other for j in range(self.hilbert_space.dimension)]
                for i in range(self.hilbert_space.dimension)
            ]
            return QuantumOperator(self.hilbert_space, result)

        elif isinstance(other, QuantumOperator):
            # Operator composition (matrix multiplication)
            if self.hilbert_space.dimension != other.hilbert_space.dimension:
                raise ValueError("Hilbert space dimensions don't match")

            dim = self.hilbert_space.dimension
            result = [[MorphicComplex(0, 0) for _ in range(dim)] for _ in range(dim)]

            for i in range(dim):
                for j in range(dim):
                    for k in range(dim):
                        result[i][j] = result[i][j] + (
                            self.matrix[i][k] * other.matrix[k][j]
                        )

            return QuantumOperator(self.hilbert_space, result)

    def __rmul__(self, other: Union[float, int]) -> 'QuantumOperator':
        """Right multiplication by a scalar"""
        return self.__mul__(other)

    def __add__(self, other: 'QuantumOperator') -> 'QuantumOperator':
        """Add two operators"""
        if self.hilbert_space.dimension != other.hilbert_space.dimension:
            raise ValueError("Hilbert space dimensions don't match")

        result = [
            [
                self.matrix[i][j] + other.matrix[i][j]
                for j in range(self.hilbert_space.dimension)
            ]
            for i in range(self.hilbert_space.dimension)
        ]

        return QuantumOperator(self.hilbert_space, result)

    def __sub__(self, other: 'QuantumOperator') -> 'QuantumOperator':
        """Subtract an operator from this one"""
        if self.hilbert_space.dimension != other.hilbert_space.dimension:
            raise ValueError("Hilbert space dimensions don't match")

        result = [
            [
                self.matrix[i][j] - other.matrix[i][j]
                for j in range(self.hilbert_space.dimension)
            ]
            for i in range(self.hilbert_space.dimension)
        ]

        return QuantumOperator(self.hilbert_space, result)

    def __neg__(self) -> 'QuantumOperator':
        """Negate this operator"""
        return self.__mul__(-1)

    def is_hermitian(self) -> bool:
        """Check if this operator is Hermitian (self-adjoint)"""
        dim = self.hilbert_space.dimension
        for i in range(dim):
            for j in range(dim):
                # Check if M[i,j] = M[j,i]*
                if self.matrix[i][j] != self.matrix[j][i].conjugate():
                    return False
        return True

    def is_unitary(self) -> bool:
        """Check if this operator is unitary"""
        dim = self.hilbert_space.dimension
        # Create matrix of inner products
        product = [[MorphicComplex(0, 0) for _ in range(dim)] for _ in range(dim)]

        for i in range(dim):
            for j in range(dim):
                for k in range(dim):
                    conj = self.matrix[k][i].conjugate()
                    product[i][j] = product[i][j] + (conj * self.matrix[k][j])

        # Check if it equals the identity matrix
        identity = [
            [MorphicComplex(1 if i == j else 0, 0) for j in range(dim)]
            for i in range(dim)
        ]
        return all(
            abs(product[i][j].real - identity[i][j].real) < 1e-10
            and abs(product[i][j].imag - identity[i][j].imag) < 1e-10
            for i in range(dim)
            for j in range(dim)
        )

    def __repr__(self) -> str:
        return f"QuantumOperator(matrix={self.matrix})"


class DensityMatrix:
    """
    Represents the quantum state as a density matrix,
    enabling mixed state representations.
    """

    def __init__(self, atoms: List[_Atom_]):
        self.atoms = atoms
        # Assuming all atoms have quantum states
        quantum_states = [atom.quantum_state for atom in atoms if atom.quantum_state]
        if not quantum_states:
            raise ValueError("No quantum states found in atoms")
        self.matrix = self._construct_matrix(quantum_states)

    def _construct_matrix(self, states: List[QuantumState]) -> Matrix:
        """Construct a density matrix from quantum states"""
        n = len(states)
        matrix_data = [[MorphicComplex(0, 0) for _ in range(n)] for _ in range(n)]

        for i, state1 in enumerate(states):
            for j, state2 in enumerate(states):
                # Simple outer product
                inner_product = state1.space.inner_product(
                    state1.amplitudes, state2.amplitudes
                )
                matrix_data[i][j] = inner_product

        return Matrix(matrix_data)

    def trace(self) -> MorphicComplex:
        """Calculate the trace of the density matrix"""
        return self.matrix.trace()

    def __repr__(self) -> str:
        return f"DensityMatrix(matrix={self.matrix})"


class PauliOperators:
    """
    Implementation of Pauli matrices as fundamental quantum operators.
    These form a basis for quantum operations.
    """

    @staticmethod
    def create_hilbert_space() -> HilbertSpace:
        """Create a 2-dimensional Hilbert space for qubit operations"""
        return HilbertSpace(2)

    @staticmethod
    def identity(space: HilbertSpace) -> QuantumOperator:
        """Identity matrix"""
        I = [
            [MorphicComplex(1, 0), MorphicComplex(0, 0)],
            [MorphicComplex(0, 0), MorphicComplex(1, 0)],
        ]
        return QuantumOperator(space, I)

    @staticmethod
    def pauli_x(space: HilbertSpace) -> QuantumOperator:
        """Pauli X (NOT gate)"""
        X = [
            [MorphicComplex(0, 0), MorphicComplex(1, 0)],
            [MorphicComplex(1, 0), MorphicComplex(0, 0)],
        ]
        return QuantumOperator(space, X)

    @staticmethod
    def pauli_y(space: HilbertSpace) -> QuantumOperator:
        """Pauli Y"""
        Y = [
            [MorphicComplex(0, 0), MorphicComplex(0, -1)],
            [MorphicComplex(0, 1), MorphicComplex(0, 0)],
        ]
        return QuantumOperator(space, Y)

    @staticmethod
    def pauli_z(space: HilbertSpace) -> QuantumOperator:
        """Pauli Z"""
        Z = [
            [MorphicComplex(1, 0), MorphicComplex(0, 0)],
            [MorphicComplex(0, 0), MorphicComplex(-1, 0)],
        ]
        return QuantumOperator(space, Z)

    @staticmethod
    def hadamard(space: HilbertSpace) -> QuantumOperator:
        """Hadamard gate - creates superposition"""
        coeff = 1 / math.sqrt(2)
        H = [
            [MorphicComplex(coeff, 0), MorphicComplex(coeff, 0)],
            [MorphicComplex(coeff, 0), MorphicComplex(-coeff, 0)],
        ]
        return QuantumOperator(space, H)


class CompositeOperator:
    """Represents a sequence of operators composed together"""

    def __init__(self, operators: List[QuantumOperator]):
        # Verify all operators use the same Hilbert space
        if not all(
            op.hilbert_space.dimension == operators[0].hilbert_space.dimension
            for op in operators
        ):
            raise ValueError("All operators must use the same Hilbert space")

        self.operators = operators
        self.hilbert_space = operators[0].hilbert_space

    def apply_to(self, state: QuantumState) -> None:
        """Apply the sequence of operators to a quantum state"""
        for op in reversed(self.operators):  # Apply in reverse order (right to left)
            op.apply_to(state)

    def to_matrix(self) -> QuantumOperator:
        """Convert this composite operator to a single matrix operator"""
        # Start with the identity matrix
        identity = PauliOperators.identity(self.hilbert_space)
        result = identity

        # Multiply all operators together
        for op in reversed(self.operators):  # Apply in reverse order (right to left)
            result = op * result

        return result


class QuantumAlgorithm(ABC):
    """Abstract base class for quantum algorithms"""

    @abstractmethod
    def initialize(self, hilbert_space: HilbertSpace) -> QuantumState:
        """Initialize the quantum state for this algorithm"""
        pass

    @abstractmethod
    def apply_circuit(self, state: QuantumState) -> QuantumState:
        """Apply the quantum circuit for this algorithm"""
        pass

    @abstractmethod
    def measure_result(self, state: QuantumState) -> Any:
        """Extract the classical result from the quantum state"""
        pass

    def run(self, hilbert_space: HilbertSpace) -> Any:
        """Run the complete algorithm"""
        state = self.initialize(hilbert_space)
        final_state = self.apply_circuit(state)
        return self.measure_result(final_state)


class Oracle(Generic[T_co, V_co, C_co, T_anti, V_anti, C_anti], ABC):
    """
    An Oracle is a generator that transforms between types in the category.
    It maintains the state of its first input and provides morphisms.
    """

    def __init__(self):
        self.initialized = False
        self.first_input = None
        self.state = {}

    def __iter__(self):
        return self

    def __next__(self):
        raise StopIteration("Oracle must be used as a generator")

    def send(self, value: Any) -> Any:
        """Send value to the oracle, preserving first input state."""
        if not self.initialized:
            self.first_input = value
            self.initialized = True
            result = self.initialize_state(value)
        else:
            # Apply the same transformation as was done on first input
            result = self.apply_morphism(value)

        return result

    @abstractmethod
    def initialize_state(self, value: Any) -> Any:
        """Initialize the oracle state with the first input."""
        pass

    @abstractmethod
    def apply_morphism(self, value: Any) -> Any:
        """Apply the oracle's morphism to subsequent inputs."""
        pass

    def throw(self, typ, val=None, tb=None):
        raise StopIteration("Oracle terminated")

    def close(self):
        self.initialized = False
        self.first_input = None
        self.state = {}


class OracleGenerator(Generic[T, V, C]):
    """
    A generator-based oracle that remembers its first input and produces
    transformations based on it.
    """

    def __init__(self, transform_func: callable):
        self.transform_func = transform_func
        self.first_input: Optional[T] = None
        self.state: Dict[str, Any] = {}

    def __call__(self, input_value: T) -> Iterator[V]:
        """Makes the oracle callable as a generator"""
        if self.first_input is None:
            self.first_input = input_value
            self.state['initialized'] = True

        # The actual generator implementation using yield
        yield from self._oracle_generator(input_value)

    def _oracle_generator(self, input_value: T) -> Iterator[V]:
        """The actual generator implementation"""
        # Always transform based on the first input that was received
        reference = self.first_input

        # Initial yield of the transformation of the current input
        yield self.transform_func(input_value, reference)

        # Subsequent yields will be transformations of the reference input
        while True:
            # This creates the quine-like behavior - self-replication of output
            yield self.transform_func(reference, reference)


class MorphismOracle(OracleGenerator[T, V, C]):
    """
    Specialized oracle that applies category-theoretic morphisms as transformations.
    """

    def __init__(self, category: 'Category[T, V, C]'):
        self.category = category
        super().__init__(self._apply_morphism)

    def _apply_morphism(self, source: T, reference: T) -> V:
        """Apply available morphisms from the category"""
        morphisms = self.category.find_morphisms(reference, source)
        if morphisms:
            # Apply the first available morphism
            return morphisms[
                0
            ]  # Assuming morphism application is encoded in the morphism object
        return None  # No applicable morphism found


class QuineOracle(Oracle[T_co, V_co, C_co, T_anti, V_anti, C_anti]):
    """
    A Quine Oracle is an oracle that produces itself (or a representation of itself)
    as part of its output, creating a self-referential system.
    """

    def initialize_state(self, value: Any) -> Any:
        # Store the input value's state hash
        if hasattr(value, 'value'):
            self.state['hash'] = hash_state(value.value)
        else:
            self.state['hash'] = hash_state(value)

        # For a quine, we return a representation that includes itself
        return self.create_quine_output(value)

    def apply_morphism(self, value: Any) -> Any:
        # For subsequent inputs, apply the same transformation
        return self.create_quine_output(value)

    def create_quine_output(self, value: Any) -> Any:
        """Create a self-referential output that contains a representation of itself."""
        # Example implementation - this would be customized based on your specific needs
        if isinstance(value, BYTE):
            # Apply a specific transformation for BYTE objects
            # that preserves the "quineness" - self-reference
            transformed = BYTE(value.value ^ self.state['hash'] & 0xFF)
            return (transformed, self)
        else:
            # Generic handling for other types
            return (value, self)


class HermitianMorphism(Generic[T, V, C, T_anti, V_anti, C_anti]):
    """
    Represents a morphism with a Hermitian adjoint relationship between
    covariant and contravariant types.
    """

    def __init__(
        self, forward: Callable[[T, V], C], adjoint: Callable[[T_anti, V_anti], C_anti]
    ):
        self.forward = forward
        self.adjoint = adjoint

    def apply(self, source: T, value: V) -> C:
        """Apply the forward morphism"""
        return self.forward(source, value)

    def apply_adjoint(self, source: T_anti, value: V_anti) -> C_anti:
        """Apply the adjoint (contravariant) morphism"""
        return self.adjoint(source, value)

    @classmethod
    def from_byte_operation(
        cls, operation: int
    ) -> 'HermitianMorphism[BYTE, int, BYTE, BYTE, int, BYTE]':
        """
        Create a Hermitian morphism from a BYTE operation code.
        Uses the C, _C_, VV, TTTT bit structure from your BYTE class.
        """

        def forward(byte: BYTE, value: int) -> BYTE:
            # Extract the C bit to determine operation mode
            c_bit = byte.get_bit(7)
            if c_bit == 1:
                # Active state: Use _C_ as MSB of 3-bit morphism
                _c_ = byte.get_bit(6)
                vv = (byte.get_bit(5) << 1) | byte.get_bit(4)
                vvv = (_c_ << 2) | vv
                # Apply the VVV operation to TTTT bits of value
                return cls._apply_vvv_op(vvv, value)
            else:
                # Settled state: Use only 2-bit VV for operations
                vv = (byte.get_bit(5) << 1) | byte.get_bit(4)
                return cls._apply_vv_op(vv, value)

        def adjoint(byte: BYTE, value: int) -> BYTE:
            # The adjoint is the reverse operation
            # This is a simplified std lib version not full multiplication by the conjugate transpose
            result = forward(byte, value)
            result.flip_bit(7)  # Flip the C bit as part of adjoint
            return result

        return cls(forward, adjoint)

    def adjoint(self) -> 'HermitianMorphism[V_anti, T_anti, C_anti, V_co, T_co, C_co]':
        """
        Create the Hermitian adjoint (contravariant dual) of this morphism.
        The adjoint reverses the morphism direction and applies the conjugate operation.
        """

        # Create the adjoint transformation function
        def adjoint_transform(target: V_anti) -> T_anti:
            # This is where we implement the specific adjoint matrix math with potential extension to other libs
            if hasattr(self.transform, 'conjugate'):
                return self.transform.conjugate()(target)
            else:
                # Generic fallback for non-complex transformations
                return target

        return HermitianMorphism(self.codomain, self.domain, adjoint_transform)

    @staticmethod
    def _apply_vvv_op(vvv: int, value: int) -> BYTE:
        """Apply the 3-bit VVV operation to a value"""
        t = value & 0xF  # Extract TTTT bits
        if vvv == 0:  # Identity
            result = t
        elif vvv == 1:  # Inc T
            result = (t + 1) & 0xF
        elif vvv == 2:  # Dec T
            result = (t - 1) & 0xF
        elif vvv == 3:  # Flip T (Pauli-X like)
            result = t ^ 0xF
        elif vvv == 4:  # Flip High Nibble (Pauli-Z like)
            result = t ^ 0b1100
        elif vvv == 5:  # Flip Low Nibble
            result = t ^ 0b0011
        elif vvv == 6:  # Set T to 0
            result = 0
        elif vvv == 7:  # Set T to 15
            result = 0xF
        return BYTE(result)

    @staticmethod
    def _apply_vv_op(vv: int, value: int) -> BYTE:
        """Apply the 2-bit VV operation to a value"""
        t = value & 0xF  # Extract TTTT bits
        if vv == 0:  # Identity
            result = t
        elif vv == 1:  # Flip T
            result = t ^ 0xF
        elif vv == 2:  # Set T based on C_internal
            _c_ = (value >> 6) & 1  # Extract _C_ bit
            result = _c_
        elif vv == 3:  # Rotate T Left
            result = ((t << 1) | (t >> 3)) & 0xF
        return BYTE(result)


class Condition(Generic[T, V, C], ABC):
    """Represents a state or condition in the system."""

    attributes: Dict[str, Any]

    @abstractmethod
    def __repr__(self):
        return f"Condition({self.attributes})"


class Action(Condition[T, V, C], ABC):
    """Abstract base class for an elementary action or reaction."""

    @abstractmethod
    def execute(self, input_condition: Condition) -> Condition:
        """Transform an input condition into an output condition."""
        pass


class Reaction(Action[T, V, C], ABC):
    """Concrete implementation of an elementary reaction."""

    transformation: Callable[[Condition], Condition]

    @abstractmethod
    def execute(self, input_condition: Condition) -> Condition:
        output_condition = self.transformation(input_condition)
        print(f"Reaction: {input_condition} -> {output_condition}")
        return output_condition


@dataclass
class Agency:
    """Represents an invariant agency catalyzing actions."""

    name: str
    rules: Dict[str, Action[T, V, C]] = field(default_factory=dict)

    def perform_action(
        self, action_key: str, input_condition: Condition[T, V, C]
    ) -> Condition[T, V, C]:
        if action_key not in self.rules:
            raise ValueError(
                f"Action {action_key} is not defined for agency {self.name}."
            )
        action = self.rules[action_key]
        print(f"Agency '{self.name}' performing action '{action_key}'...")
        return action.execute(input_condition)

    def add_action(self, action_key: str, action: Action[T, V, C]):
        self.rules[action_key] = action
        print(f"Action '{action_key}' added to agency '{self.name}'.")


@dataclass
class QuantumTimeSlice(Generic[Q, C]):
    """Represents a quantum-classical bridge timepoint"""

    quantum_state: Q
    classical_state: C
    density_matrix: List[List[complex]]
    timestamp: datetime
    coherence_time: timedelta
    entropy: float


class QuantumTemporalMRO:
    """Handles quantum temporal evolution and entropy calculations."""

    def __init__(self, hilbert_dimension: int = 2):
        self.hilbert_dimension = hilbert_dimension
        self.hbar = 1.0  # Reduced Planck's constant
        self.k_boltzmann = 1.0  # Boltzmann constant

    def create_initial_density_matrix(self, dimension: int) -> List[List[complex]]:
        """Creates a pure state density matrix |0⟩⟨0|"""
        return [
            [complex(1, 0) if i == j == 0 else complex(0, 0) for j in range(dimension)]
            for i in range(dimension)
        ]

    def create_random_hamiltonian(self, dimension: int) -> List[List[complex]]:
        """Creates a random Hermitian matrix as Hamiltonian"""
        H = [[complex(0, 0) for _ in range(dimension)] for _ in range(dimension)]
        for i in range(dimension):
            H[i][i] = complex(random(), 0)
            for j in range(i + 1, dimension):
                real, imag = random() - 0.5, random() - 0.5
                H[i][j] = complex(real, imag)
                H[j][i] = complex(real, -imag)
        return H

    def compute_von_neumann_entropy(self, density_matrix: List[List[complex]]) -> float:
        """Calculates von Neumann entropy S = -Tr(ρ ln ρ)"""
        eigenvalues = self.find_eigenvalues(density_matrix)
        entropy = sum(
            -p * math.log(p) for p in (ev.real for ev in eigenvalues if ev.real > 1e-10)
        )
        return entropy

    @staticmethod
    def _combinations(items, k):
        """Generate k-combinations of items"""
        if k == 0:
            yield []
            return
        if not items:
            return
        first, rest = items[0], items[1:]
        # Combinations that include the first element
        for c in QuantumTemporalMRO._combinations(rest, k - 1):
            yield [first] + c
        # Combinations that don't include the first element
        yield from QuantumTemporalMRO._combinations(rest, k)

    @staticmethod
    def determinant(matrix: List[List[complex]]) -> complex:
        """Calculate determinant of a matrix using recursive expansion"""
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        if n == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

        det = complex(0)
        for j in range(n):
            minor = [[matrix[i][k] for k in range(n) if k != j] for i in range(1, n)]
            det += matrix[0][j] * ((-1) ** j) * QuantumTemporalMRO.determinant(minor)
        return det

    def lindblad_evolution(
        self,
        density_matrix: List[List[complex]],
        hamiltonian: List[List[complex]],
        duration: timedelta,
    ) -> List[List[complex]]:
        """Implement Lindblad master equation evolution over a small time duration"""
        dt = duration.total_seconds()
        n = len(density_matrix)

        commutator = self.matrix_subtract(
            self.matrix_multiply(hamiltonian, density_matrix),
            self.matrix_multiply(density_matrix, hamiltonian),
        )

        gamma = 0.1
        lindblad_term = [[complex(0, 0) for _ in range(n)] for _ in range(n)]

        for i in range(n):
            for j in range(i):
                L = [[complex(0, 0) for _ in range(n)] for _ in range(n)]
                L[i][j] = complex(1, 0)
                lindblad_term = self.matrix_add(
                    lindblad_term,
                    self.matrix_subtract(
                        self.matrix_multiply(
                            L,
                            self.matrix_multiply(
                                density_matrix, self.conjugate_transpose(L)
                            ),
                        ),
                        self.scalar_multiply(
                            0.5,
                            self.matrix_add(
                                self.matrix_multiply(
                                    self.matrix_multiply(
                                        self.conjugate_transpose(L), L
                                    ),
                                    density_matrix,
                                ),
                                self.matrix_multiply(
                                    density_matrix,
                                    self.matrix_multiply(
                                        self.conjugate_transpose(L), L
                                    ),
                                ),
                            ),
                        ),
                    ),
                )

        drho_dt = self.matrix_add(
            self.scalar_multiply(-1j / self.hbar, commutator),
            self.scalar_multiply(gamma, lindblad_term),
        )
        return self.matrix_add(density_matrix, self.scalar_multiply(dt, drho_dt))

    @staticmethod
    def find_eigenvalues(
        matrix: List[List[complex]], max_iterations: int = 100, tolerance: float = 1e-10
    ) -> List[complex]:
        """Find eigenvalues using the Durand-Kerner method."""
        n = len(matrix)
        roots = [complex(random(), random()) for _ in range(n)]
        coeffs = QuantumTemporalMRO.characteristic_equation_coeffs(matrix)

        for _ in range(max_iterations):
            max_change = 0
            for i in range(n):
                numerator = sum(
                    coeffs[k] * (roots[i] ** (n - 1 - k)) for k in range(n + 1)
                )
                denominator = complex(1) * math.prod(
                    roots[i] - roots[j] if i != j else 1 for j in range(n)
                )
                correction = numerator / (
                    denominator if abs(denominator) > tolerance else complex(tolerance)
                )
                max_change = max(max_change, abs(correction))
                roots[i] -= correction
            if max_change < tolerance:
                break
        return sorted(roots, key=lambda x: x.real)

    @staticmethod
    def characteristic_equation_coeffs(matrix: List[List[complex]]) -> List[complex]:
        """Calculates coefficients of the characteristic polynomial of a matrix"""
        n = len(matrix)
        if n == 1:
            return [complex(1), -matrix[0][0]]

        def minor(matrix: List[List[complex]], i: int, j: int) -> List[List[complex]]:
            return [
                [matrix[row][col] for col in range(len(matrix)) if col != j]
                for row in range(len(matrix))
                if row != i
            ]

        coeffs = [complex(1)]
        for k in range(1, n + 1):
            coeff = sum(
                QuantumTemporalMRO.determinant(
                    [[matrix[i][j] for j in range(n) if j in indices] for i in indices]
                )
                for indices in QuantumTemporalMRO._combinations(range(n), k)
            )
            coeffs.append((-1) ** k * coeff)
        return coeffs

    @staticmethod
    def matrix_multiply(
        A: List[List[complex]], B: List[List[complex]]
    ) -> List[List[complex]]:
        """Multiplies two matrices."""
        return [
            [sum(A[i][k] * B[k][j] for k in range(len(A))) for j in range(len(B[0]))]
            for i in range(len(A))
        ]

    @staticmethod
    def matrix_add(
        A: List[List[complex]], B: List[List[complex]]
    ) -> List[List[complex]]:
        """Adds two matrices."""
        return [[a + b for a, b in zip(A_row, B_row)] for A_row, B_row in zip(A, B)]

    @staticmethod
    def scalar_multiply(
        scalar: complex, matrix: List[List[complex]]
    ) -> List[List[complex]]:
        """Multiplies a matrix by a scalar."""
        return [[scalar * element for element in row] for row in matrix]

    @staticmethod
    def conjugate_transpose(matrix: List[List[complex]]) -> List[List[complex]]:
        """Calculates the conjugate transpose of a matrix."""
        return [
            [matrix[j][i].conjugate() for j in range(len(matrix))]
            for i in range(len(matrix[0]))
        ]

    @staticmethod
    def matrix_subtract(
        A: List[List[complex]], B: List[List[complex]]
    ) -> List[List[complex]]:
        """Subtracts matrix B from matrix A."""
        return [[a - b for a, b in zip(A_row, B_row)] for A_row, B_row in zip(A, B)]


class QuantumStateVector:
    """Represents a quantum state vector with amplitudes in a Hilbert space."""

    def __init__(self, amplitudes: List[MorphicComplex], space: HilbertSpace):
        """
        Initialize a quantum state vector.

        Args:
            amplitudes: List of complex amplitudes for each basis state
            space: The Hilbert space this state belongs to
        """
        self.amplitudes = amplitudes
        self.space = space

        # Verify dimensions match
        if len(amplitudes) != space.dimension:
            raise ValueError(
                f"Amplitudes length ({len(amplitudes)}) must match space dimension ({space.dimension})"
            )

        # Normalize the state vector
        self._normalize()

    def _normalize(self):
        """Normalize the state vector so probabilities sum to 1."""
        norm_squared = sum(amp.real**2 + amp.imag**2 for amp in self.amplitudes)
        norm = math.sqrt(norm_squared)

        if norm > 0:
            for i in range(len(self.amplitudes)):
                self.amplitudes[i] = MorphicComplex(
                    self.amplitudes[i].real / norm, self.amplitudes[i].imag / norm
                )

    def measure(self) -> int:
        """
        Perform a measurement on the quantum state.
        Returns the index of the basis state that was measured.
        """
        # Calculate probabilities for each basis state
        probabilities = []
        for amp in self.amplitudes:
            # Probability is |amplitude|²
            prob = amp.real**2 + amp.imag**2
            probabilities.append(prob)

        # Simulate measurement using the probabilities
        r = 0.5
        cumulative_prob = 0
        for i, prob in enumerate(probabilities):
            cumulative_prob += prob
            if r <= cumulative_prob:
                return i
        return len(self.amplitudes) - 1

    def superposition(
        self,
        other: 'QuantumStateVector',
        coeff1: MorphicComplex,
        coeff2: MorphicComplex,
    ) -> 'QuantumStateVector':
        """
        Create a superposition of two quantum states.
        |ψ⟩ = a|ψ₁⟩ + b|ψ₂⟩
        """
        if self.space.dimension != other.space.dimension:
            raise ValueError("Quantum states must belong to same Hilbert space")
        new_amplitudes = []
        for i in range(len(self.amplitudes)):
            new_amp = (self.amplitudes[i] * coeff1) + (other.amplitudes[i] * coeff2)
            new_amplitudes.append(new_amp)
        return QuantumStateVector(new_amplitudes, self.space)

    def entangle(self, other: 'QuantumStateVector') -> 'QuantumStateVector':
        """
        Create an entangled state from two quantum states.
        |ψ⟩ = (|ψ₁⟩|0⟩ + |ψ₂⟩|1⟩)/√2
        This is a simplified version of entanglement for demonstration.
        """
        # For simplicity, we'll just return a superposition
        coeff = MorphicComplex(1 / math.sqrt(2), 0)
        return self.superposition(other, coeff, coeff)


# ------------------------------------------------------------------------------
# OPERATOR SYSTEM - Noetherian Transformations
# ------------------------------------------------------------------------------
class OperatorBase(ABC):
    """Abstract base for operators acting on memory vectors"""

    @property
    @abstractmethod
    def symbol(self) -> str:
        """Operator symbol"""
        pass

    @abstractmethod
    def apply(self, state: MemoryVector) -> MemoryVector:
        """Apply operator to state"""
        pass

    def is_noetherian(self, other: 'OperatorBase', test_size: int = 50) -> bool:
        """Check if operators commute (Noether symmetry)"""
        for i in range(1, test_size):
            vec = MemoryVector.from_integer(i, nbytes=2)
            a = self.apply(other.apply(vec))
            b = other.apply(self.apply(vec))
            if a.coords != b.coords:
                return False
        return True

    def conserved_quantity(self) -> Optional[str]:
        """Associated conserved quantity (Noether's theorem)"""
        return None


class XOROperator(OperatorBase):
    """Involutory XOR mask operator"""

    def __init__(self, mask: List[int]):
        self.mask = mask

    @property
    def symbol(self) -> str:
        return 'XOR'

    def apply(self, state: MemoryVector) -> MemoryVector:
        """XOR coords with mask"""
        mask = self.mask
        coords = state.coords

        # Broadcast mask to match length
        if len(mask) < len(coords):
            mask = (mask * ((len(coords) + len(mask) - 1) // len(mask)))[: len(coords)]
        else:
            mask = mask[: len(coords)]

        new_coords = [c ^ m for c, m in zip(coords, mask)]
        return MemoryVector(coords=new_coords, flavor=state.flavor)

    def is_involutory(self) -> bool:
        """XOR twice returns identity"""
        return True

    def conserved_quantity(self) -> Optional[str]:
        """Parity conservation if mask has even popcount"""
        total_pop = sum(bin(m).count('1') for m in self.mask)
        return 'parity' if total_pop % 2 == 0 else None


# ============================================================================
# 0. XOR LORENTZ GROUP — The Fiber Bundle Structure
# ============================================================================


class XorLorentz:
    """
    The XOR-Lorentz group: discrete bit-shift transformations that preserve
    the ByteWord's topological invariants (holonomy modulo 2).

    This is NOT an analogy — this is a GROUP:
        • Composition: apply shifts sequentially
        • Identity: shift by 0 steps
        • Inverse: shift by (field_size - steps)
        • Closure: shifting stays in the field

    The inner product is valued in the 8th roots of unity because:
        ⟨a,b⟩ = exp(i · popcount(a ⊕ b) · π/4)

    popcount(a ⊕ b) ranges 0-8 (since a,b are 8-bit ByteWords):
        π/4 = 45° increments
        Result: phases at 0°, 45°, 90°, 135°, 180°, 225°, 270°, 315°

    This bridges:
        C=1 (integer, discrete, bit)
        C=0 (coefficient, continuous, phase)
    """

    @staticmethod
    def bracket(a: int, b: int) -> complex:
        """
        Inner product ⟨a,b⟩ = exp(i · popcount(a ⊕ b) · π/4).

        a ⊕ b = XOR difference = Hamming distance in bit space
        popcount = number of bits different = "interval" in discrete spacetime
        π/4 phase = 8th roots of unity
        """
        return cmath.exp(1j * bin(a ^ b).count("1") * math.pi / 4)

    @staticmethod
    def metric_dot(a: int, b: int) -> float:
        """
        Metric dot product: cos(popcount(a⊕b) · π/4).

        Returns a real value in [-1, 1]:
            +1.0 = identical or complementary (0 or 8 bits different)
            0.0 = orthogonal (2 or 6 bits different)
            -1.0 = opposite (4 bits different)
        """
        d = bin(a ^ b).count("1")
        return math.cos(d * math.pi / 4)

    @staticmethod
    def popcount_distance(a: int, b: int) -> int:
        """The Hamming distance = number of differing bits."""
        return bin(a ^ b).count("1")

    @staticmethod
    def boost(v: int, steps: int = 1) -> int:
        """
        Lorentz boost = cyclic left-shift of V-field (bits 6-4).

        Lorentz boosts mix space and time — shifting the V-field can
        carry information to the MSB (C-bit), changing the observer state.
        """
        v_field = (v >> 4) & 0b111
        v_new = ((v_field << steps) | (v_field >> (3 - steps))) & 0b111
        return (v & ~0b01110000) | (v_new << 4)

    @staticmethod
    def rotate(v: int, steps: int = 1) -> int:
        """
        Spatial rotation = cyclic left-shift of T-field (bits 3-0).

        Rotations mix spatial dimensions without affecting the observer.
        """
        t_field = v & 0b1111
        t_new = ((t_field << steps) | (t_field >> (4 - steps))) & 0b1111
        return (v & ~0b00001111) | t_new

    @staticmethod
    def parity(v: int) -> int:
        """Toggle the C-bit (Captain bit, bit 7)."""
        return v ^ 0b10000000

    @staticmethod
    def holonomy_phase(word: ByteWord) -> complex:
        """
        Compute the holonomy phase of a ByteWord.

        Holonomy = parallel transport around a closed loop in the bit-space.
        For an 8-bit word, the holonomy is the XOR of all bits, expressed as
        a phase φ ∈ {0, π}. This is the topological invariant.
        """
        bits = bin(word.value).count("1")
        return cmath.exp(1j * bits * math.pi)

    @staticmethod
    def holonomy_value(word: ByteWord) -> int:
        """Holonomy as an integer: 0 or 1 (trivial or non-trivial)."""
        return bin(word.value).count("1") % 2

    @staticmethod
    def is_in_same_fiber(a: ByteWord, b: ByteWord) -> bool:
        """Two ByteWords are in the same fiber if they share holonomy."""
        return XorLorentz.holonomy_value(a) == XorLorentz.holonomy_value(b)


# ============================================================================
# 0. THE MORPHOLOGICAL CLOCK — Ψ and Entropic Duration
# ============================================================================


@dataclass
class MorphologicalClock:
    """
    The Morphological Clock measures not "what time is it" but
    "how much becoming remains."

    Ψ (Psi) is the thermodynamic toll of staying charged — of remaining
    in a high-energy phase rather than collapsing to 0x00 or 0xFF.

    Time is not spent in ticks, but in entropy paid for persistence.

    Properties:
        • Not linear — recursive and branching
        • Not evenly spaced — phase-driven, not uniform
        • Not shared — local to each runtime quantum
        • Not imposed — emergent from ByteWord behavior
    """

    psi_budget: float  # Remaining Ψ (Landauer budget)
    entropy: float = 0.0  # Accumulated entropy
    phase: int = 0  # Current phase in morphogenetic cycle
    history: List[int] = field(default_factory=list)  # Trace of states

    # Landauer constant: kT ln 2 at T=300K in joules
    LANDAUER_UNIT: float = 2.85e-21  # Joules per bit erased

    def spend(self, bits_erased: int) -> bool:
        """
        Spend Ψ to erase bits. Returns True if budget remains,
        False if exhausted (runtime death).
        """
        cost = bits_erased * self.LANDAUER_UNIT
        if self.psi_budget < cost:
            return False
        self.psi_budget -= cost
        self.entropy += bits_erased
        self.history.append(self.phase)
        self.phase += 1
        return True

    def reset_phase(self) -> None:
        """Cycle the morphological clock (e.g., after witness collapse)."""
        self.phase = 0

    @property
    def is_exhausted(self) -> bool:
        return self.psi_budget <= 0

    @property
    def effective_temperature(self) -> float:
        """
        T_eff = Ψ_remaining / entropy (when entropy > 0).

        As entropy grows and Ψ shrinks, the system "cools" —
        less free energy available per degree of disorder.
        """
        if self.entropy == 0:
            return float('inf')
        return self.psi_budget / self.entropy

    def __repr__(self) -> str:
        return (
            f"Clock(Ψ={self.psi_budget:.2e}J, S={self.entropy:.2f}, "
            f"phase={self.phase}, T_eff={self.effective_temperature:.2e})"
        )


# ============================================================================
# SECTION 4: MICROCANONICAL THERMODYNAMICS — Emergent, Not Imposed
# ============================================================================


@dataclass
class MicrocanonicalEnsemble:
    """
    The ByteWord System IS Microcanonical.

    N = number of ByteWords (fixed)
    V = morphospace volume (fixed, 256^N)
    E = total Landauer budget (fixed at initialization)

    Temperature is DERIVED, not imposed:
        T = ∂S/∂E

    T_morphic = ∂(# ghost configurations) / ∂(# active commanders)
    """

    words: List[ByteWord]
    total_energy: float  # Total Landauer budget for the ensemble
    energy_consumed: float = 0.0  # Cumulative energy spent

    def count_ghosts(self) -> int:
        """Number of ghost states (bra=0, ket≠0)."""
        return sum(1 for w in self.words if w.is_ghost)

    def count_charged(self) -> int:
        """Number of charged states (between null and witness)."""
        return sum(1 for w in self.words if w.is_charged)

    def count_active_commanders(self) -> int:
        """Number of words with active C-bit."""
        return sum(1 for w in self.words if w.c_bit)

    def count_deputies(self, level: int) -> int:
        """Count deputies at a given V-level (0=V₀, 1=V₁, 2=V₂)."""
        if level == 0:
            return sum(1 for w in self.words if w.v_field == 0b001)
        elif level == 1:
            return sum(1 for w in self.words if (w.v_field & 0b011) == 0b010)
        elif level == 2:
            return sum(1 for w in self.words if (w.v_field & 0b111) == 0b100)
        return 0

    @property
    def total_agency(self) -> int:
        """Total agency in the ensemble (sum of has_agency)."""
        return sum(w.agency for w in self.words)

    @property
    def total_structure(self) -> int:
        """Total structure in the ensemble (sum of ket values)."""
        return sum(w.structure for w in self.words)

    @property
    def total_potency(self) -> int:
        """Total potency (sum of structure²)."""
        return sum(w.potency for w in self.words)

    @property
    def entropy(self) -> float:
        """
        Shannon entropy of the ByteWord distribution.

        S = -Σ p(b) log₂ p(b)

        This is the morphological entropy — how evenly distributed
        are the ByteWord states?
        """
        n = len(self.words)
        if n == 0:
            return 0.0
        counter = Counter(w.value for w in self.words)
        total = float(n)
        return -sum((c / total) * math.log2(c / total) for c in counter.values())

    @property
    def temperature(self) -> float:
        """
        Microcanonical temperature: T = ∂S/∂E

        Approximated as the ratio of ghost degeneracy to active commanders.
        T_morphic = ∂(# ghost configs) / ∂(# active commanders)

        Low T: few ghosts, many observables, low entropy
        High T: many ghosts, few observables, high entropy

        If no commanders are active, temperature is undefined (returns inf).
        """
        ghosts = self.count_ghosts()
        commanders = self.count_active_commanders()
        if commanders == 0:
            return float('inf') if ghosts > 0 else 0.0
        return ghosts / commanders

    @property
    def free_energy(self) -> float:
        """
        Morphological free energy: F = E - T·S (in Landauer units).

        This is the "excess Nan-Nul flux" — energy available for
        deputization before detritus (energy ≤ 0) is reached.
        """
        return (
            self.total_energy - self.energy_consumed - (self.temperature * self.entropy)
        )

    @property
    def is_thermalized(self) -> bool:
        """Has the ensemble reached a stationary distribution?"""
        return self.free_energy <= 0

    def distribution(self) -> Dict[int, float]:
        """Return the empirical distribution μ(b) over ByteWord values."""
        n = len(self.words)
        if n == 0:
            return {}
        counter = Counter(w.value for w in self.words)
        return {k: v / n for k, v in counter.items()}

    def energy_landscape(self, T: float = 1.0) -> Dict[int, float]:
        """
        Compute the emergent energy landscape: E(b) = -T log μ(b).

        Energy is MEASURED from the stationary distribution, not imposed.
        This is the statistical mechanics inversion:
            probability comes first, energy comes second.
        """
        dist = self.distribution()
        if not dist:
            return {}
        return {b: -T * math.log(p) if p > 0 else float('inf') for b, p in dist.items()}

    def __repr__(self) -> str:
        return (
            f"Ensemble(N={len(self.words)}, ghosts={self.count_ghosts()}, "
            f"charged={self.count_charged()}, commanders={self.count_active_commanders()}, "
            f"T={self.temperature:.3f}, S={self.entropy:.3f}, F={self.free_energy:.2e})"
        )


# ============================================================================
# SECTION 5: BYTEWORD VIRTUAL MACHINE — The ISA in Action
# ============================================================================


class LandauerTracker:
    """
    Tracks Landauer expenditure across VM operations.

    Every logically irreversible operation (those that erase bits)
    costs kT ln 2 per bit erased. This is the thermodynamic bookkeeping
    that makes heat death a well-defined halting condition.
    """

    def __init__(self, initial_budget: float = 1e-17):  # ~10,000 Landauer units at 300K
        self.budget = initial_budget
        self.spent = 0.0

    def spend(self, bits: int) -> bool:
        """Try to spend `bits` Landauer units. Returns False if exhausted."""
        cost = bits * 2.85e-21  # kT ln 2 at 300K
        if self.budget < cost:
            return False
        self.budget -= cost
        self.spent += cost
        return True

    @property
    def remaining(self) -> float:
        return self.budget

    def __repr__(self) -> str:
        return f"Landauer(budget={self.budget:.2e}J, spent={self.spent:.2e}J)"


class PyWord(Generic[T]):
    """
    [[PyWord]] represents a word-sized value optimized for CPython.
    It manages alignment according to the system's memory model and
    provides conversion between Python and C types.
    """

    __slots__ = ('_value', '_alignment', '_arch', '_mem_model')

    def __init__(
        self,
        value: Union[int, bytes, bytearray, array.array],
        alignment: WordAlignment = WordAlignment.WORD,
    ):
        self._mem_model = MemoryModel.get_system_info()
        self._arch = ProcessorArchitecture.current()
        self._alignment = alignment
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

        return AlignedArray()  # type: ignore

    def _store_value(self, value: Union[int, bytes, bytearray, array.array]) -> None:  # type: ignore
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

    def as_buffer(self) -> ctypes.Array:
        return (ctypes.c_char * self._calculate_aligned_size()).from_buffer(self._value)

    @property
    def alignment(self) -> int:
        return self._alignment

    @property
    def architecture(self) -> ProcessorArchitecture:
        return self._arch

    def __int__(self) -> int:
        if isinstance(self._value, ctypes.Array):
            return int.from_bytes(self._value.data, sys.byteorder)  # type: ignore
        return int.from_bytes(self._value.tobytes(), sys.byteorder)

    def __bytes__(self) -> bytes:
        if isinstance(self._value, ctypes.Array):
            return bytes(self._value.data)  # type: ignore
        return self._value.tobytes()

class ByteWordOperator:
    """
    Operator represented as a (possibly partial) mapping over {0..255}.
    If mapping covers all 256 inputs and produces a bijection -> permutation.
    Permutation operators are unitary on the one-hot lift.
    """

    def __init__(self, mapping: Optional[Dict[int, int]] = None):
        # mapping: input_raw -> output_raw
        self.mapping: Dict[int, int] = dict(mapping or {})

    @classmethod
    def xor_mask(cls, mask: int) -> "ByteWordOperator":
        """Build XOR-by-constant operator: f(x) = x ^ mask for all 0..255."""
        m = {i: i ^ (mask & 0xFF) for i in BYTE_RANGE}
        return cls(m)

    @classmethod
    def from_function(cls, f) -> "ByteWordOperator":
        """Build operator by applying Python callable f over 0..255."""
        m = {i: f(i) & 0xFF for i in BYTE_RANGE}
        return cls(m)

    def apply_raw(self, r: int) -> int:
        """Apply operator to a raw byte value; identity if unmapped."""
        return self.mapping.get(r, r)

    def apply(self, bw: ByteWord) -> ByteWord:
        return ByteWord(self.apply_raw(bw.raw))

    def domain(self) -> Iterable[int]:
        return self.mapping.keys()

    def image(self) -> Iterable[int]:
        return self.mapping.values()

    def is_permutation(self) -> bool:
        """Full-space bijection check."""
        if len(self.mapping) != BYTE_SPACE:
            return False
        vals = set(self.mapping.values())
        return len(vals) == BYTE_SPACE and all(0 <= v < BYTE_SPACE for v in vals)

    def inverse_mapping(self) -> Optional[Dict[int, int]]:
        """Return inverse mapping if bijection, else None."""
        if not self.is_permutation():
            return None
        inv = {v: k for k, v in self.mapping.items()}
        return inv

    def is_involution(self) -> bool:
        """Check f(f(x)) == x for all domain (involution property)."""
        # For unmapped inputs identity holds; check all 0..255
        for i in BYTE_RANGE:
            j = self.apply_raw(i)
            k = self.apply_raw(j)
            if k != i:
                return False
        return True

    def is_unitary(self) -> bool:
        """Permutation matrices are unitary in the one-hot lift."""
        return self.is_permutation()

    def is_hermitian(self) -> bool:
        """
        On the one-hot lift, a permutation matrix is Hermitian iff it equals its
        transpose (i.e., it's a product of disjoint transpositions and fixed pts).
        For permutations, this is equivalent to being an involution:
            P = P^T  <=>  P^2 = I and P == P^{-1}
        """
        return self.is_involution()

    def adjoint_operator(self) -> Optional["ByteWordOperator"]:
        """Adjoint (conjugate transpose) in one-hot basis: inv permutation if exists."""
        inv = self.inverse_mapping()
        if inv is None:
            # For partial or non-bijective, adjoint not defined easily here.
            return None
        return ByteWordOperator(inv)

    def spectrum_sample(self, samples: int = 16) -> List[complex]:
        """
        Rough spectrum-ish probe: for small N we can compute behavior of operator
        on basis vectors and the popcount-phase overlaps. This is *not* a true
        eigenvalue decomposition but a quick sketch using the popcount-phase kernel.
        """
        # pick some inputs and compute phi(x, f(x))
        out = []
        for i in range(min(samples, BYTE_SPACE)):
            a = ByteWord(i)
            b = self.apply(a)
            out.append(a.phase_with(b))
        return out

    def __repr__(self):
        k = len(self.mapping)
        return (
            f"<ByteWordOperator mapped={k} entries permutation={self.is_permutation()}>"
        )

class QuantumNumber:
    def __init__(self, hilbert_space: HilbertSpace):
        self.hilbert_space = hilbert_space
        self.amplitudes = [complex(0, 0)] * hilbert_space.dimension
        self._quantum_numbers = None
    @property
    def quantum_numbers(self):
        return self._quantum_numbers
    @quantum_numbers.setter
    def quantum_numbers(self, numbers: QuantumNumbers):
        n, l, m, s = numbers
        if self.hilbert_space.is_fermionic():
            # Fermionic quantum number constraints
            if not (n > 0 and 0 <= l < n and -l <= m <= l and s in (-0.5, 0.5)):
                raise ValueError("Invalid fermionic quantum numbers")
        elif self.hilbert_space.is_bosonic():
            # Bosonic quantum number constraints
            if not (n >= 0 and l >= 0 and m >= 0 and s == 0):
                raise ValueError("Invalid bosonic quantum numbers")
        self._quantum_numbers = numbers

def evaluate_fitness(state: QuantumState, fitness_function: Callable[[QuantumState], float]) -> float:
    return fitness_function(state)

def probabilistic_prune(states: List[QuantumState], threshold: float) -> List[QuantumState]:
    return [state for state in states if evaluate_fitness(state, example_fitness_function) >= threshold]

def example_fitness_function(state: QuantumState) -> float:
    """Example fitness function based on entropy and coherence."""
    return 1 / (state.entropy + 1) * state.fitness_score

class QNumber(NamedTuple):  # 
    n: int     # Principal quantum number
    l: int     # Azimuthal quantum number
    m: int     # Magnetic quantum number
    s: float   # Spin quantum number


# ======================
# Torus (chiral Hamming)
# ======================
class TorusWinding(enum.Enum):
    """4-state Church-Turing torus winding states as binary pairs (w₁,w₂). A ∅,null-'glue', Byte is valueless from the 'character' standpoint, but it can take-part in set-builder notation, where Extensive ByteWords point to it, creating second order logical operands at 'runtime'."""
    NULL = (0, 0)      # ∅ — topological glue
    AXIS_1 = (1, 0)    # winding along first axis
    AXIS_2 = (0, 1)    # winding along second axis  
    TWISTED = (1, 1)   # both axes wound
    def __init__(self, w1: int, w2: int):
        self.w1 = w1
        self.w2 = w2
    @classmethod
    def from_bits(cls, t_bits: int) -> 'TorusWinding':
        """Convert 4-bit T field to torus winding state"""
        # Extract w1, w2 from lower 2 bits of T field
        w1 = (t_bits >> 1) & 1
        w2 = t_bits & 1
        return cls((w1, w2))
    
    def to_bits(self) -> int:
        """Convert torus winding to 4-bit T field"""
        return (self.w1 << 1) | self.w2
    
    def xor(self, other: 'TorusWinding') -> 'TorusWinding':
        """XOR operation on torus winding pairs - the fundamental unitary operator"""
        new_w1 = self.w1 ^ other.w1
        new_w2 = self.w2 ^ other.w2
        return TorusWinding((new_w1, new_w2))

class SparseUnitaryOperator:
    """
    req. TorusWinding
    Sparse, self-adjoint operators representing involutory morphisms:
    (A ∘ A = I). Useful for stable oscillators and cycle preservation.
    """
    def __init__(self, mask_w1: bool, mask_w2: bool):
        self.mask_w1 = mask_w1
        self.mask_w2 = mask_w2
        self._involution_check()

    def _involution_check(self):
        test = ByteWord(0b10110011)
        once = self.apply(test)
        twice = self.apply(once)
        assert test.winding == twice.winding, "Operator not involutory"

    def apply(self, word: ByteWord) -> ByteWord:
        new_w1 = word.w1 ^ self.mask_w1
        new_w2 = word.w2 ^ self.mask_w2
        new_torus = (word.torus_raw & 0b1100) | (int(new_w2) << 1) | int(new_w1)
        new_raw = (word.raw & 0b11110000) | new_torus
        return ByteWord(new_raw)

    def __repr__(self):
        return f"SparseUnitaryOperator(mask_w1={self.mask_w1}, mask_w2={self.mask_w2})"

class TorusTraversal:
    """
    Traverses a list of ByteWords across a morphic torus,
    detecting cycles, direction changes, and topological echoes.
    """
    def __init__(self, words: List[ByteWord]):
        self.words = words
        self.current_index = 0
        self.trajectory: List[TorusWinding] = []

    def step(self) -> Optional[ByteWord]:
        if self.current_index >= len(self.words):
            return None

        current = self.words[self.current_index]
        self.trajectory.append(current.winding)

        if current.winding == TorusWinding.NULL:
            self.current_index += 1
        elif current.winding == TorusWinding.W1:
            self.current_index = (self.current_index + 1) % len(self.words)
        elif current.winding == TorusWinding.W2:
            self.current_index = (self.current_index + 2) % len(self.words)
        else:
            self.current_index = (self.current_index + 3) % len(self.words)

        return current

    def detect_cycle(self) -> Optional[int]:
        if len(self.trajectory) < 2:
            return None
        for cycle_len in range(1, len(self.trajectory) // 2 + 1):
            if self.trajectory[-cycle_len:] == self.trajectory[-2*cycle_len:-cycle_len]:
                return cycle_len
        return None

# ===========
# MRO CLASSES
# ===========
class QuantumTemporalMRO:
    """Quantum-aware temporal method resolution"""
    
    def __init__(self, hilbert_dimension: int = 2):
        self.hilbert_dimension = hilbert_dimension
        self.temperature = 1.0
        self.hbar = 1.0
        self.k_boltzmann = 1.0
        
    def characteristic_equation_coeffs(self, matrix: List[List[complex]]) -> List[complex]:
        """Calculate coefficients of characteristic equation using recursion"""
        n = len(matrix)
        if n == 1:
            return [1, -matrix[0][0]]
            
        def minor(matrix: List[List[complex]], i: int, j: int) -> List[List[complex]]:
            return [[matrix[row][col] for col in range(len(matrix)) if col != j]
                    for row in range(len(matrix)) if row != i]
                    
        def determinant(matrix: List[List[complex]]) -> complex:
            if len(matrix) == 1:
                return matrix[0][0]
            if len(matrix) == 2:
                return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
            det = complex(0)
            for j in range(len(matrix)):
                det += matrix[0][j] * ((-1) ** j) * determinant(minor(matrix, 0, j))
            return det
            
        coeffs = [complex(1)]
        for k in range(1, n + 1):
            submatrices = []
            for indices in self._combinations(range(n), k):
                submatrix = [[matrix[i][j] for j in indices] for i in indices]
                submatrices.append(submatrix)
            
            coeff = sum(determinant(submatrix) for submatrix in submatrices)
            coeffs.append((-1) ** k * coeff)
            
        return coeffs
    
    def _combinations(self, items, r):
        """Generate combinations without using itertools"""
        if r == 0:
            yield []
            return
        for i in range(len(items)):
            for comb in self._combinations(items[i + 1:], r - 1):
                yield [items[i]] + comb

    def find_eigenvalues(self, matrix: List[List[complex]], max_iterations: int = 100, tolerance: float = 1e-10) -> List[complex]:
        """Find eigenvalues using QR algorithm with shifts"""
        n = len(matrix)
        if n == 1:
            return [matrix[0][0]]
        
        # Convert characteristic equation coefficients to polynomial
        coeffs = self.characteristic_equation_coeffs(matrix)
        
        # Find roots using Durand-Kerner method
        roots = [complex(random(), random()) for _ in range(n)]  # Initial guesses
        
        def evaluate_poly(x: complex) -> complex:
            result = complex(0)
            for i, coeff in enumerate(coeffs):
                result += coeff * (x ** (len(coeffs) - 1 - i))
            return result
        
        for _ in range(max_iterations):
            max_change = 0
            new_roots = []
            
            for i in range(n):
                numerator = evaluate_poly(roots[i])
                denominator = complex(1)
                for j in range(n):
                    if i != j:
                        denominator *= (roots[i] - roots[j])
                
                if abs(denominator) < tolerance:
                    denominator = complex(tolerance)
                    
                correction = numerator / denominator
                new_root = roots[i] - correction
                max_change = max(max_change, abs(correction))
                new_roots.append(new_root)
            
            roots = new_roots
            if max_change < tolerance:
                break
                
        return sorted(roots, key=lambda x: x.real)

    def compute_von_neumann_entropy(self, density_matrix: List[List[complex]]) -> float:
        """Calculate von Neumann entropy S = -Tr(ρ ln ρ) using eigenvalues"""
        eigenvalues = self.find_eigenvalues(density_matrix)
        entropy = 0.0
        for eigenval in eigenvalues:
            p = eigenval.real  # Eigenvalues should be real for density matrix
            if p > 1e-10:  # Avoid log(0)
                entropy -= p * math.log(p)
        return entropy

    def create_random_hamiltonian(self, dimension: int) -> List[List[complex]]:
        """Creates a random Hermitian matrix to serve as Hamiltonian"""
        H = [[complex(0, 0) for _ in range(dimension)] for _ in range(dimension)]
        
        for i in range(dimension):
            H[i][i] = complex(random(), 0)  # Real diagonal
            for j in range(i + 1, dimension):
                real = random() - 0.5
                imag = random() - 0.5
                H[i][j] = complex(real, imag)
                H[j][i] = complex(real, -imag)  # Hermitian conjugate
                
        return H

    def create_initial_density_matrix(self, dimension: int) -> List[List[complex]]:
        """Creates a pure state density matrix |0⟩⟨0|"""
        return [[complex(1, 0) if i == j == 0 else complex(0, 0) 
                for j in range(dimension)] for i in range(dimension)]

    @staticmethod
    def matrix_multiply(A: List[List[complex]], B: List[List[complex]]) -> List[List[complex]]:
        """Multiplies two matrices."""
        n = len(A)
        result = [[sum(A[i][k] * B[k][j] for k in range(n)) 
                  for j in range(n)] for i in range(n)]
        return result

    @staticmethod
    def matrix_add(A: List[List[complex]], B: List[List[complex]]) -> List[List[complex]]:
        """Adds two matrices."""
        return [[a + b for a, b in zip(A_row, B_row)] 
                for A_row, B_row in zip(A, B)]

    @staticmethod
    def matrix_subtract(A: List[List[complex]], B: List[List[complex]]) -> List[List[complex]]:
        """Subtracts matrix B from matrix A."""
        return [[a - b for a, b in zip(A_row, B_row)] 
                for A_row, B_row in zip(A, B)]

    @staticmethod
    def scalar_multiply(scalar: complex, matrix: List[List[complex]]) -> List[List[complex]]:
        """Multiplies a matrix by a scalar."""
        return [[scalar * element for element in row] for row in matrix]

    @staticmethod
    def conjugate_transpose(matrix: List[List[complex]]) -> List[List[complex]]:
        """Calculates the conjugate transpose of a matrix."""
        return [[matrix[j][i].conjugate() for j in range(len(matrix))] 
                for i in range(len(matrix[0]))]

    def lindblad_evolution(self, 
                          density_matrix: List[List[complex]], 
                          hamiltonian: List[List[complex]], 
                          duration: timedelta) -> List[List[complex]]:
        """Implement Lindblad master equation evolution"""
        dt = duration.total_seconds()
        n = len(density_matrix)
        
        # Commutator [H,ρ]
        commutator = self.matrix_subtract(
            self.matrix_multiply(hamiltonian, density_matrix),
            self.matrix_multiply(density_matrix, hamiltonian)
        )
        
        # Create simple Lindblad operators
        lindblad_ops = []
        for i in range(n):
            for j in range(i):
                L = [[complex(0, 0) for _ in range(n)] for _ in range(n)]
                L[i][j] = complex(1, 0)
                lindblad_ops.append(L)
        
        gamma = 0.1  # Decoherence rate
        lindblad_term = [[complex(0, 0) for _ in range(n)] for _ in range(n)]
        
        for L in lindblad_ops:
            L_dag = self.conjugate_transpose(L)
            LdL = self.matrix_multiply(L_dag, L)
            
            term1 = self.matrix_multiply(L, self.matrix_multiply(density_matrix, L_dag))
            term2 = self.scalar_multiply(0.5, self.matrix_add(
                self.matrix_multiply(LdL, density_matrix),
                self.matrix_multiply(density_matrix, LdL)
            ))
            
            lindblad_term = self.matrix_add(
                lindblad_term,
                self.matrix_subtract(term1, term2)
            )
        
        drho_dt = self.matrix_add(
            self.scalar_multiply(-1j / self.hbar, commutator),
            self.scalar_multiply(gamma, lindblad_term)
        )
        
        return self.matrix_add(
            density_matrix,
            self.scalar_multiply(dt, drho_dt)
        )

class QOpType(Enum):
    """Types of quinic/quantum operations"""
    IDENTITY = auto()     # No change
    HADAMARD = auto()     # Superposition
    PHASE = auto()        # Phase shift
    CNOT = auto()         # Controlled-NOT
    SWAP = auto()         # Swap bits
    MEASURE = auto()      # Collapse superposition

@dataclass
class QCell:
    """Second-order finite difference with future support for inner products."""
    address: int
    segment: int
    value: bytes = b'\x00' * WordSize.INT
    state: Optional[str] = None
    commit_hash: Optional[str] = None
    data: Optional[array.array] = None
    metadata: Optional[Dict] = None

class MorphicComplex:
    """Represents a complex number with morphic properties.
    Derivations/alternatives (irrational-attractor, state::logic bisector, the bifurcation basis?):
    # self.mophology = morphism.morphology(strenum)
    # NON_MARKOVIAN = math.log(2).as_integer_ratio()  # Information-theoretic entropy baseline
    # MARKOVIAN = 1 / (math.exp(-1))  # Fermi-Dirac 'occupation probability'
    # NON_MARKOVIAN = 1 / (1 - math.exp(-1))  # Bose-Einstein 'bosonic correlation'
    # MARKOVIAN = (1 - 5 ** 0.5) / 2  # Inverse golden ratio (entropy-dominant)
    # NON_MARKOVIAN = (1 + 5 ** 0.5) / 2  # Phi as self-organizing structure
    # MARKOVIAN = 1 / (1 + math.exp(-1))  # Logistic
    # MARKOVIAN triggers a lossless (bijective) mapping.
    # NON_MARKOVIAN triggers a lossy (entropic) mapping with a "feedback term."
    def evolve(state: int, morphic: Morphology) -> int:
        if morphic == Morphology.MARKOVIAN:
            return state ^ 0b1111  # XNOR-like forward evolution
        elif morphic == Morphology.NON_MARKOVIAN:
            return int(state * math.e % 256)  # Feedback-dominated evolution
        return state"""
    def __init__(self, real: float, imag: float):
        self.real = real
        self.imag = imag
    def conjugate(self) -> 'MorphicComplex':
        """Return the complex conjugate."""
        return MorphicComplex(self.real, -self.imag)
    def __add__(self, other: 'MorphicComplex') -> 'MorphicComplex':
        return MorphicComplex(self.real + other.real, self.imag + other.imag)
    def __sub__(self, other: 'MorphicComplex') -> 'MorphicComplex':
        return MorphicComplex(self.real - other.real, self.imag - other.imag)
    def __mul__(self, other: Union['MorphicComplex', float, int]) -> 'MorphicComplex':
        if isinstance(other, (int, float)):
            return MorphicComplex(self.real * other, self.imag * other)
        return MorphicComplex(
            self.real * other.real - self.imag * other.imag,
            self.real * other.imag + self.imag * other.real
        )
    def __rmul__(self, other: Union[float, int]) -> 'MorphicComplex':
        return self.__mul__(other)
    def __eq__(self, other) -> bool:
        if not isinstance(other, MorphicComplex):
            return False
        return (abs(self.real - other.real) < 1e-10 and 
                abs(self.imag - other.imag) < 1e-10)
    def __hash__(self) -> int:
        return hash((self.real, self.imag))
    def __repr__(self) -> str:
        if self.imag >= 0:
            return f"{self.real} + {self.imag}i"
        return f"{self.real} - {abs(self.imag)}i"
class Matrix:
    """Simple matrix implementation using standard Python"""
    def __init__(self, data: List[List[Any]]):
        if not data:
            raise ValueError("Matrix data cannot be empty")
        # Verify all rows have the same length
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
        return all(self.data[i][j] == other.data[i][j] 
                  for i in range(self.rows) 
                  for j in range(self.cols))
    def __matmul__(self, other: Union['Matrix', List[Any]]) -> Union['Matrix', List[Any]]:
        """Matrix multiplication operator @"""
        if isinstance(other, list):
            # Matrix @ vector
            if len(other) != self.cols:
                raise ValueError(f"Dimensions don't match for matrix-vector multiplication: "
                                f"matrix cols={self.cols}, vector length={len(other)}")
            return [sum(self.data[i][j] * other[j] for j in range(self.cols)) 
                    for i in range(self.rows)]
        else:
            # Matrix @ Matrix
            if self.cols != other.rows:
                raise ValueError(f"Dimensions don't match for matrix multiplication: "
                                f"first matrix cols={self.cols}, second matrix rows={other.rows}")
            result = [[sum(self.data[i][k] * other.data[k][j] 
                          for k in range(self.cols))
                      for j in range(other.cols)]
                      for i in range(self.rows)]
            return Matrix(result)
    def trace(self) -> Any:
        """Calculate the trace of the matrix"""
        if self.rows != self.cols:
            raise ValueError("Trace is only defined for square matrices")
        return sum(self.data[i][i] for i in range(self.rows))
    def transpose(self) -> 'Matrix':
        """Return the transpose of this matrix"""
        return Matrix([[self.data[j][i] for j in range(self.rows)] 
                      for i in range(self.cols)])
    @staticmethod
    def zeros(rows: int, cols: int) -> 'Matrix':
        """Create a matrix of zeros"""
        if rows <= 0 or cols <= 0:
            raise ValueError("Matrix dimensions must be positive")
        return Matrix([[0 for _ in range(cols)] for _ in range(rows)])
    @staticmethod
    def identity(n: int) -> 'Matrix':
        """Create an n×n identity matrix"""
        if n <= 0:
            raise ValueError("Matrix dimension must be positive")
        return Matrix([[1 if i == j else 0 for j in range(n)] for i in range(n)])
    def __repr__(self) -> str:
        return "\n".join([str(row) for row in self.data])
class HilbertSpace:
    """
    Represents a Hilbert space that uses MorphicComplex numbers for coordinates.
    """
    def __init__(self, dimension: int = 3):
        if dimension <= 0:
            raise ValueError("Hilbert space dimension must be positive")
        self.dimension = dimension
        self.basis_vectors = [self._create_basis_vector(i) for i in range(dimension)]
    def _create_basis_vector(self, index: int) -> List[MorphicComplex]:
        """Create a basis vector with a 1 at the specified index."""
        vector = [MorphicComplex(0, 0) for _ in range(self.dimension)]
        vector[index] = MorphicComplex(1, 0)
        return vector
    def inner_product(self, vec1: List[MorphicComplex], vec2: List[MorphicComplex]) -> MorphicComplex:
        """
        Compute the inner product of two vectors in the Hilbert space.
        <u, v> = ∑ᵢ (u*ᵢ × vᵢ) where u*ᵢ is the complex conjugate
        """
        if len(vec1) != len(vec2) or len(vec1) != self.dimension:
            raise ValueError("Vectors must have the same dimension as the space")
        result = MorphicComplex(0, 0)
        for i in range(self.dimension):
            # For each component, compute u*ᵢ × vᵢ
            conj_u = vec1[i].conjugate()
            result = result + (conj_u * vec2[i])
        return result
    def norm(self, vector: List[MorphicComplex]) -> float:
        """Compute the norm (magnitude) of a vector."""
        inner = self.inner_product(vector, vector)
        return math.sqrt(inner.real)  # Inner product with self should be real
    def normalize(self, vector: List[MorphicComplex]) -> List[MorphicComplex]:
        """Return a normalized copy of the vector."""
        norm_val = self.norm(vector)
        if abs(norm_val) < 1e-10:
            raise ValueError("Cannot normalize zero vector")
        return [MorphicComplex(c.real/norm_val, c.imag/norm_val) for c in vector]
    def is_orthogonal(self, vec1: List[MorphicComplex], vec2: List[MorphicComplex]) -> bool:
        """Check if two vectors are orthogonal."""
        inner = self.inner_product(vec1, vec2)
        return abs(inner.real) < 1e-10 and abs(inner.imag) < 1e-10
    def project(self, vector: List[MorphicComplex], subspace_basis: List[List[MorphicComplex]]) -> List[MorphicComplex]:
        """Project a vector onto a subspace defined by a basis."""
        projection = [MorphicComplex(0, 0) for _ in range(self.dimension)]
        for basis_vec in subspace_basis:
            # Compute <v, basis> / <basis, basis>
            inner_v_basis = self.inner_product(vector, basis_vec)
            inner_basis_basis = self.inner_product(basis_vec, basis_vec).real
            if abs(inner_basis_basis) < 1e-10:
                raise ValueError("Basis vector must not be zero")
            # Compute the coefficient
            coeff = MorphicComplex(inner_v_basis.real / inner_basis_basis, 
                                  inner_v_basis.imag / inner_basis_basis)
            # Add the contribution of this basis vector to the projection
            for i in range(self.dimension):
                projection[i] = projection[i] + (basis_vec[i] * coeff)
        return projection
    def __eq__(self, other) -> bool:
        if not isinstance(other, HilbertSpace):
            return False
        return self.dimension == other.dimension

# ============================================================================
# 0. MEMORY VECTOR (Lattice Coordinates)
# ============================================================================


@dataclass
class MemoryVector:
    """Lattice coordinate for ByteWords in Hilbert space"""

    coords: List[int]
    weights: Optional[List[float]] = None

    def copy(self) -> 'MemoryVector':
        return MemoryVector(
            self.coords.copy(), None if self.weights is None else self.weights.copy()
        )

    def as_ket(self) -> str:
        """Dirac notation"""
        hex_coords = ','.join(f"0x{c:02x}" for c in self.coords)
        if self.weights:
            w_str = ','.join(f"{w:.3f}" for w in self.weights)
            return f"|ψ⟩ = [{hex_coords}] @ [{w_str}]"
        return f"|ψ⟩ = [{hex_coords}]"

    def to_bitvector(self, width=8) -> List[int]:
        out = []
        for b in self.coords:
            for i in range(width):
                out.append((b >> i) & 1)
        return out

    def as_integer(self) -> int:
        val = 0
        for i, b in enumerate(self.coords):
            val |= (b & 0xFF) << (8 * i)
        return val

    @classmethod
    def from_integer(cls, v: int, nbytes: int):
        coords = [(v >> (8 * i)) & 0xFF for i in range(nbytes)]
        return cls(coords)

    def parity(self) -> int:
        """Conserved quantity"""
        return sum(b.bit_count() for b in self.coords) % 2

    def to_bytewords(self) -> List[ByteWord]:
        """Convert memory vector to ByteWords"""
        return [ByteWord(c) for c in self.coords]


# ============================================================================
# 0. HERMITIAN OPERATORS
# ============================================================================


class OperatorBase(Protocol[O_co]):
    """Protocol for hermitian operators"""

    symbol: str

    def action_signature(self) -> str:
        return f"{self.symbol}: MemoryVector -> MemoryVector"

    def apply(self, state: MemoryVector) -> MemoryVector: ...
    def conserved_quantity(self) -> Optional[str]: ...


class XORMask:
    """Involutory hermitian operator (X² = I)"""

    symbol = 'XOR'

    def __init__(self, mask: Sequence[int]):
        self.mask = list(mask)

    def transformation(self) -> str:
        mask_hex = ','.join(f"0x{m:02x}" for m in self.mask)
        return f"XOR[{mask_hex}]: |ψ⟩ → |ψ ⊕ mask⟩"

    def apply(self, state: MemoryVector) -> MemoryVector:
        mask = self.mask
        coords = state.coords
        if len(mask) != len(coords):
            mask = (list(mask) * ((len(coords) + len(mask) - 1) // len(mask)))[
                : len(coords)
            ]
        return MemoryVector([x ^ y for x, y in zip(coords, mask)])

    def is_involutory(self) -> bool:
        return True

    def conserved_quantity(self) -> Optional[str]:
        total_pop = sum(m.bit_count() for m in self.mask)
        return 'parity' if total_pop % 2 == 0 else None


class Measurement:
    """Projective measurement operator"""

    symbol = 'MEASURE'

    def __init__(self, projector_mask: Sequence[int]):
        self.pmask = list(projector_mask)

    def projection(self) -> str:
        mask_hex = ','.join(f"0x{m:02x}" for m in self.pmask)
        return f"M[{mask_hex}]: |ψ⟩ → P|ψ⟩ with probability |⟨ψ|P|ψ⟩|²"

    def apply(self, state: MemoryVector) -> MemoryVector:
        coords = state.coords.copy()
        if len(self.pmask) < len(coords):
            pm = (
                self.pmask * ((len(coords) + len(self.pmask) - 1) // len(self.pmask))
            )[: len(coords)]
        else:
            pm = self.pmask[: len(coords)]
        coords = [c & m for c, m in zip(coords, pm)]
        bits_total = sum(b.bit_count() for b in state.coords)
        bits_kept = sum(b.bit_count() for b in coords)
        prob = bits_kept / bits_total if bits_total > 0 else 0.0
        return MemoryVector(coords, weights=[prob])


# ============================================================================
# CANTOR ALLOCATOR (Rational Path Measure)
# ============================================================================
@dataclass
class CantorNode:  # path encoding and exact rational intervals/measures
    """Node in measure-preserving binary tree"""
    path_bits: int  # binary path where 0->left, 1->right (length = depth)
    depth: int
    measure: Fraction
    parent: Optional["CantorNode"] = None

    def fork(self) -> Tuple["CantorNode", "CantorNode"]:
        d = self.depth + 1
        left_bits = (self.path_bits << 1) | 0
        right_bits = (self.path_bits << 1) | 1
        m = Fraction(self.measure, 2)
        left = CantorNode(left_bits, d, m, parent=self)
        right = CantorNode(right_bits, d, m, parent=self)
        return left, right

    def key(self) -> str:
        """Canonical key for SQL use: depth:hex(path_bits)."""
        return f"{self.depth}:{self.path_bits:x}"

    def interval(self) -> Tuple[Fraction, Fraction]:
        """
        Compute the closed interval [a,b] in [0,1] that this cylinder corresponds
        to in the ternary Cantor construction. We map binary path bits {0,1}
        to ternary digits {0,2} respectively. Exact arithmetic via Fraction.
        """
        a = Fraction(0, 1)
        denom = Fraction(1, 1)
        for i in range(1, self.depth + 1):
            denom *= 3
        # compute left endpoint
        left = Fraction(0, 1)
        for i in range(self.depth):
            bit = (self.path_bits >> (self.depth - 1 - i)) & 0x1
            digit = 0 if bit == 0 else 2
            left += Fraction(digit, 3 ** (i + 1))
        right = left + Fraction(1, 3**self.depth)
        return left, right

    def fork(self) -> Tuple[CantorNode, CantorNode]:
        depth = self.depth + 1
        left_bits = (self.path_bits << 1) | 0
        right_bits = (self.path_bits << 1) | 1
        m = self.measure / 2
        left = CantorNode(left_bits, depth, m, parent=self)
        right = CantorNode(right_bits, depth, m, parent=self)
        return left, right

    def to_binary_index(self) -> int:
        return self.path_bits

    def as_tstring(self) -> str:  # 3.12 f'string version
        return f"Node(depth={self.depth}, idx=0x{self.path_bits:x}, μ={self.measure})"

    def __repr__(self):
        a, b = self.interval() if self.depth <= 20 else (Fraction(0), Fraction(0))
        return (
            f"CantorNode(depth={self.depth}, idx={self.path_bits}, mu={self.measure}, "
            f"interval=[{a},{b}])"
        )

class MorphologicalDerivative:
    """
    Morphological derivatives describe time-like bitwise mutations.

    Δ¹: Elementary bit flip.
    Δ²: Merge via XOR (gradient-neutral collapse).
    Δⁿ: History-driven operator chain (≤16 morphs).
    """
    def __init__(self, order: int = 1):
        if order > 16:
            raise ValueError("Derivative order must be ≤ 16")
        self.order = order
        self.chain: List[ByteWord] = []

    def delta_1(self, word: ByteWord) -> ByteWord:
        flip_mask = 1 << random.randint(0, 1)
        new_torus = word.torus_raw ^ flip_mask
        new_raw = (word.raw & 0b11110000) | (new_torus & 0b00001111)
        result = ByteWord(new_raw)
        self.chain.append(result)
        return result

    def delta_2(self, word1: ByteWord, word2: ByteWord) -> ByteWord:
        result = word1.xor_cascade(word2)
        self.chain.append(result)
        return result

    def delta_n(self, word: ByteWord, steps: int) -> ByteWord:
        current = word
        for _ in range(min(steps, 16)):
            current = self.delta_1(current)
        return current

# ============================================================================
# SQL SPINOR BOUNDARY (Persistence)
# ============================================================================


def init_sqlite(conn: sqlite3.Connection):
    """Initialize spinor boundary database schema"""
    conn.execute("""
    CREATE TABLE IF NOT EXISTS byteword_artifact (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cantor_path TEXT NOT NULL,
        raw INTEGER NOT NULL,
        C INTEGER NOT NULL,
        V INTEGER NOT NULL,
        T INTEGER NOT NULL,
        w1 INTEGER NOT NULL,
        w2 INTEGER NOT NULL,
        measure_num INTEGER NOT NULL,
        measure_den INTEGER NOT NULL,
        value_blob BLOB,
        ref_addr TEXT,
        code_hash TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_path ON byteword_artifact(cantor_path);"
    )
    conn.commit()


def persist_byteword(
    conn: sqlite3.Connection,
    node: CantorNode,
    bw: ByteWord,
    value_blob: Optional[bytes] = None,
    ref_addr: Optional[str] = None,
    code_hash: Optional[str] = None,
):
    """Persist ByteWord + Cantor measure into SQL"""
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO byteword_artifact
        (cantor_path, raw, C, V, T, w1, w2, measure_num, measure_den, value_blob, ref_addr, code_hash)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            f"{node.depth}:{node.path_bits:x}",
            bw.raw,
            bw.C,
            bw.V,
            bw.T,
            bw.w1,
            bw.w2,
            node.measure.numerator,
            node.measure.denominator,
            value_blob,
            ref_addr,
            code_hash,
        ),
    )
    conn.commit()


def rehydrate_row(row: sqlite3.Row) -> Tuple[CantorNode, ByteWord]:
    """Reconstruct CantorNode and ByteWord from SQL row"""
    parts = row['cantor_path'].split(':')
    depth = int(parts[0])
    bits = int(parts[1], 16)
    mu = Fraction(row['measure_num'], row['measure_den'])
    node = CantorNode(bits, depth, mu)
    bw = ByteWord(row['raw'])
    return node, bw
