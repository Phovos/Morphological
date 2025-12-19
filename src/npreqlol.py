# ----------  mini-dirac-jung-msc.py  ----------
from __future__ import annotations
import ast, json, enum, typing as t, numpy as np

class ByteWord:
    __slots__ = ("raw",)
    def __init__(self, raw: int): self.raw = raw & 0xFF
    def xor(self, other: "ByteWord") -> "ByteWord": return ByteWord(self.raw ^ other.raw)
    def __matmul__(self, other: "ByteWord") -> int: return self.xor(other).raw   # ⟨self|XOR|other⟩

T = np.zeros((256, 256), dtype=np.uint8)
for i in range(256):
    for j in range(256):
        T[i, j] = ByteWord(i) @ ByteWord(j)          # Heisenberg matrix mechanics

def eigen_classes(T: np.ndarray) -> list[set[int]]:
    """Dirac: derive equivalence classes from transition matrix."""
    sig = {i: tuple(T[i, :]) for i in range(256)}    # XOR signature
    buckets: dict[tuple, set[int]] = {}
    for i, s in sig.items():
        buckets.setdefault(s, set()).add(i)
    return list(buckets.values())

if __name__ == "__main__":
    classes = eigen_classes(T)
    print(f"Dirac-ByteWord classes: {len(classes)}")
    print("First 3 classes (sizes):", [len(c) for c in classes[:3]])
# ----------------------------------------------