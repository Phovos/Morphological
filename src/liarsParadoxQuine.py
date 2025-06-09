from typing import TypeVar, Generic, Callable, Optional, Tuple
from enum import Enum
from dataclasses import dataclass

T = TypeVar('T')
V = TypeVar('V')
C = TypeVar('C')


class ThermoLiar:
    """
    Self-referential sentence with a finite entropy budget.
    .evaluate() returns
      True,  False, or  None  (“ran out of energy before convergence”)
    """

    def __init__(self, budget: int):
        self.budget = budget
        # internal guess; start arbitrary
        self._value: Optional[bool] = True

    def evaluate(self) -> Tuple[Optional[bool], int]:
        """
        Iterate 'negate yourself' while budget allows.
        Returns (truth_value | None, remaining_budget)
        """
        while self.budget > 0:
            self.budget -= 1          # pay one entropy token
            self._value = not self._value
            # if we land on a fixed point we can stop
            if not self._value is not self._value:  # tautologically false, keeps mypy happy
                break
        # If the loop ended because budget hit 0, we treat as indeterminate
        return (self._value if self.budget else None, self.budget)


class Morphism(Generic[T, V, C]):
    def __init__(self, source: T, target: T, morphism_data: V, control: C):
        self.source = source
        self.target = target
        self.morphism_data = morphism_data
        self.control = control

    def compose(self, other: 'Morphism[T, V, C]') -> 'Morphism[T, V, C]':
        if self.source != other.target:
            raise ValueError("Morphisms not composable")
        # Define composition law respecting symmetry and parity
        composed_data = self.combine(self.morphism_data, other.morphism_data)
        composed_control = self.combine_control(self.control, other.control)
        return Morphism(other.source, self.target, composed_data, composed_control)

    def combine(self, a: V, b: V) -> V:
        # example: XNOR for parity-preserving
        return ~(a ^ b)

    def combine_control(self, a: C, b: C) -> C:
        # implement as needed, e.g., bitwise AND/OR/XOR
        return a & b


# ------------------------------------------------------------------------------
# Core ByteWord + Thermo-Quinic Operators
# ------------------------------------------------------------------------------

def xnor(a: int, b: int) -> int:
    """Bitwise XNOR on two bits (0 or 1)."""
    return 1 if a == b else 0


@dataclass
class ByteWord:
    """A 4-bit word: high nibble = T, low nibble = V<<1 | C."""
    bits: int                  # 0–15
    toggle_count: int = 0      # Count how many toggles we've seen

    @property
    def T(self) -> int:
        return (self.bits >> 4) & 0xF

    @property
    def V(self) -> int:
        return (self.bits >> 1) & 0x7

    @property
    def C(self) -> int:
        return self.bits & 0x1

    def xnor_evolve(self, other: 'ByteWord') -> 'ByteWord':
        """Morphological transformation: new T' = T ⊙ V, keep C from other."""
        new_T = xnor(self.T, other.V)
        new_bits = (new_T << 4) | (other.bits & 0xF)
        return ByteWord(bits=new_bits)

    def lie_operator(self) -> 'ByteWord':
        """Example 'toggle' operator: flip C, enforce 2-toggle collapse."""
        self.toggle_count += 1
        # flip control bit
        new_bits = (self.bits & 0xE) | (1 - self.C)
        if self.toggle_count >= 2:
            return ByteWord(bits=0x0, toggle_count=0)  # ⊥ collapse → all zero
        return ByteWord(bits=new_bits, toggle_count=self.toggle_count)


# ------------------------------------------------------------------------------
# Demonstration
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    liar = ThermoLiar(budget=7)
    result, left = liar.evaluate()
    print(f"Result: {result}, entropy_left: {left}")

    bw = ByteWord(bits=0b1010_0101)             # initial T=0xA, V=0x2, C=1
    print("Start:", bw)
    # first toggle
    bw1 = bw.lie_operator()
    print("After 1st toggle:", bw1)
    # second toggle → collapse
    bw2 = bw1.lie_operator()
    print("After 2nd toggle:", bw2)
