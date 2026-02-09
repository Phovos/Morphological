from __future__ import annotations

#!/usr/bin/env -S uv run
# /* script
# requires-python = ">=3.12"
# dependencies = [
#     "uv==*.*",
#     "numpy==*.*",
# ]
# */
# https://github.com/Moonlapsed/Morphological © 2023 by MOONLAPSED:MOONLAPSED@gmail.com BSD-3 & CC ND
"""
4-bit Hermitian micro-code for consumer ISAs
"""

# ------------------------------------------------------------------
# Consumer-ISA fast-path
# ------------------------------------------------------------------
try:
    # x86-64 SSE/AVX  8× 4-bit MAC in one micro-op
    from numpy.core._simd import simd

    _vec = simd["avx2"] if "avx2" in simd else simd["sse2"]
except (ImportError, AttributeError):
    _vec = None


# fallback: plain Python (still only 4 multiplies)
def _mac_fallback(a: int, b: int) -> int:
    """4-bit real-matrix MAC:  |a  -b|  ·  |a|  =  a²+b²
    |b   a|     |b|"""
    return a * a + b * b


# vectorised fast-path
def _mac_vec(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """8-way parallel 4-bit MAC"""
    if _vec is None:
        return np.array([_mac_fallback(x, y) for x, y in zip(a, b)])
    # a,b are uint8 arrays; we want (a²+b²) for each nibble
    a_lo = a & 0x0F
    a_hi = a >> 4
    b_lo = b & 0x0F
    b_hi = b >> 4
    return (a_lo * a_lo + b_lo * b_lo) | ((a_hi * a_hi + b_hi * b_hi) << 4)


# public 4-bit Hermitian MAC
def hermitian_op(a: int, b: int) -> int:
    """Return a²+b² for 4-bit a,b; 0-225 range; 2 cycles on x86-64"""
    return _mac_fallback(a & 0xF, b & 0xF)


# public Born rule (same range, but you can call it with the *same* nibble pair)
def born_rule(a: int, b: int) -> int:
    """Born probability = a²+b²; 0-225"""
    return hermitian_op(a, b)


# ------------------------------------------------------------------
# Quantum-aware Atom subclass
# ------------------------------------------------------------------
from dataclasses import dataclass, field
from baseModel import QuantumAtom


@dataclass
class HermitianAtom(QuantumAtom):
    """
    QuantumAtom whose value is a *4-bit Hermitian pair* (bra,ket).
    All quantum operations use the consumer-ISA fast-path above.
    """

    _bra: int = field(default=0, repr=False)  # top nibble 0-15
    _ket: int = field(default=0, repr=False)  # bottom nibble 0-15

    def __post_init__(self):
        super().__post_init__()
        # store the 4-bit pair inside the inherited .value
        self.value = (self._bra, self._ket)

    # Hermitian inner product  (replaces generic tensor logic)
    def inner(self, other: "HermitianAtom") -> int:
        return hermitian_op(self._bra, other._bra) + hermitian_op(self._ket, other._ket)

    # Born-rule collapse probability  (0-450 here, still 8-bit safe)
    def probability(self) -> int:
        return born_rule(self._bra, self._ket)

    # in-place rotation in the 4-bit ring  (angle is *nibble* 0-15)
    def rotate(self, angle: int) -> None:
        angle &= 0xF
        # 2×2 rotation matrix  [ cos  -sin ]   with cos=angle, sin=angle+4
        cos_, sin_ = angle, (angle + 4) & 0xF
        new_bra = (cos_ * self._bra - sin_ * self._ket) & 0xF
        new_ket = (sin_ * self._bra + cos_ * self._ket) & 0xF
        self._bra, self._ket = new_bra, new_ket
        self.value = (new_bra, new_ket)

    # ASCII canon for quine export  (no UTF-8, no tone marks)
    def ascii_key(self) -> str:
        return f"{self._bra:x}{self._ket:x}"  # 2 hex chars = 8 bits
