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

from __future__ import annotations
import json
import pathlib
from typing import Dict, List

"""
Dirac ↔ MSC dictionary – bare-metal proof
ByteWord transition matrix IS Heisenberg's matrix
"""


# ----------  1. 8-bit morphological atom  ----------
class ByteWord:
    __slots__ = ("raw",)

    def __init__(self, raw: int) -> None:
        self.raw = raw & 0xFF

    def xor(self, other: "ByteWord") -> "ByteWord":
        return ByteWord(self.raw ^ other.raw)

    def __repr__(self) -> str:
        return f"BW(0x{self.raw:02X})"


# ----------  2. Build Heisenberg's table (256×256)  ----------
def build_transition_matrix() -> List[List[int]]:
    """T[i][j] = ⟨i|XOR|j⟩   (matrix element = XOR amplitude)"""
    return [[ByteWord(i).xor(ByteWord(j)).raw for j in range(256)] for i in range(256)]


# ----------  3. Diagonalise → find eigen-morphemes  ----------
def eigen_morphemes(matrix: List[List[int]]) -> Dict[int, List[int]]:
    """
    Group indices whose XOR *row* is identical.
    These are equivalence classes under the observable.
    """
    signature: Dict[str, List[int]] = {}
    for idx in range(256):
        row = tuple(matrix[idx])  # observable signature
        signature.setdefault(row, []).append(idx)
    # Map signature-hash → list of ByteWord indices
    return {hash(k): v for k, v in signature.items()}


# ----------  4. Dump proof  ----------
def main() -> None:
    T = build_transition_matrix()
    print("Heisenberg transition matrix (slice 0..15):")
    for row in T[:16]:
        print(" ".join(f"{val:02X}" for val in row))

    eigen = eigen_morphemes(T)
    print(f"\nEigen-morpheme classes (total {len(eigen)}):")
    for sig, members in eigen.items():
        print(
            f"  Sig {sig}: {len(members)} members → {members[:8]}{'...' if len(members) > 8 else ''}"
        )

    # NULL-glued set construction (Dirac → MSC)
    null_glued = []
    for members in eigen.values():
        for idx in members:
            null_glued.append(idx)
            null_glued.append(0x00)  # NULL separator
    print(f"\nNULL-glued set (first 64 bytes): {null_glued[:64]}")

    # Serialize the matrix for later use
    pathlib.Path("heisenberg_matrix.json").write_text(json.dumps(T))
    print("\nMatrix saved to heisenberg_matrix.json")


if __name__ == "__main__":
    main()
