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
import math
import random
from typing import Tuple, Dict
from dataclasses import dataclass
from enum import Enum


class MorphologicalPhase(Enum):
    """Phase states in the T/V/C morphological field"""

    DISORDERED = "disordered"  # High entropy, no quine stability
    CRITICAL = "critical"  # Phase boundary, maximum susceptibility
    ORDERED = "ordered"  # Low entropy, stable quines
    SUPERFLUID = "superfluid"  # Zero entropy, perfect quines


@dataclass
class OrderParameter:
    """Landau order parameter for morphological phase transitions"""

    magnitude: float
    phase: float

    @property
    def complex_amplitude(self) -> complex:
        return self.magnitude * complex(math.cos(self.phase), math.sin(self.phase))


class ToroidalByteWord:
    """8-bit word on toroidal morphological field"""

    def __init__(self, value: int):
        if not 0 <= value <= 255:
            raise ValueError("ByteWord must be 8-bit (0-255)")

        self.raw_value = value
        # T/V/C decomposition
        self.type_bits = (value & 0b11100000) >> 5  # 3 bits
        self.value_bits = (value & 0b00011100) >> 2  # 3 bits
        self.compute_bits = value & 0b00000011  # 2 bits

        # Toroidal coordinates
        self.theta = self.type_bits * (2 * math.pi / 8)  # Major angle
        self.phi = self.value_bits * (2 * math.pi / 8)  # Minor angle
        self.r = 1 + (self.compute_bits / 4)  # Radial distance

    def toroidal_distance(self, other: 'ToroidalByteWord') -> float:
        """Distance on torus surface with proper wrapping"""
        # Angular distances with wrapping
        theta_diff = min(
            abs(self.theta - other.theta), 2 * math.pi - abs(self.theta - other.theta)
        )
        phi_diff = min(
            abs(self.phi - other.phi), 2 * math.pi - abs(self.phi - other.phi)
        )
        r_diff = abs(self.r - other.r)

        return math.sqrt(theta_diff**2 + phi_diff**2 + r_diff**2)

    def morphological_coupling(self, other: 'ToroidalByteWord') -> float:
        """J coupling strength for Landau free energy"""
        distance = self.toroidal_distance(other)
        # Exponential decay with distance (like spin interactions)
        return math.exp(-distance / 0.5)  # Characteristic length scale

    def local_field_strength(self) -> float:
        """Local morphological field h at this position"""
        # Field varies across torus - creates inhomogeneity
        return 0.1 * math.sin(self.theta) * math.cos(self.phi)


class MorphologicalFieldSystem:
    """System of interacting morphological byte-words on torus"""

    def __init__(self, num_words: int = 64, temperature: float = 1.0):
        self.words = [
            ToroidalByteWord(random.randint(0, 255)) for _ in range(num_words)
        ]
        self.temperature = temperature
        self.coupling_strength = 1.0
        self.external_field = 0.0

        # Landau parameters
        self.a = 1.0  # Quadratic coefficient
        self.b = 1.0  # Quartic coefficient (stability)
        self.c = 0.1  # Coupling coefficient

    def compute_order_parameter(self) -> OrderParameter:
        """Compute complex order parameter ψ = |ψ|e^(iφ)"""
        # Average over all words weighted by their morphological alignment
        total_magnitude = 0.0
        total_phase = 0.0

        for word in self.words:
            # Order parameter contribution from each word
            local_mag = (word.type_bits + word.value_bits + word.compute_bits) / 24.0
            local_phase = word.theta + word.phi  # Phase from torus position

            total_magnitude += local_mag
            total_phase += local_phase

        avg_magnitude = total_magnitude / len(self.words)
        avg_phase = total_phase / len(self.words)

        return OrderParameter(avg_magnitude, avg_phase % (2 * math.pi))

    def landau_free_energy(self, order_param: OrderParameter) -> float:
        """Landau free energy F = a|ψ|² + b|ψ|⁴ - h|ψ| + J∑ψᵢψⱼ"""
        psi_mag = order_param.magnitude

        # Standard Landau terms
        free_energy = (
            self.a * psi_mag**2 + self.b * psi_mag**4 - self.external_field * psi_mag
        )

        # Interaction terms between words
        interaction_energy = 0.0
        for i, word1 in enumerate(self.words):
            for j, word2 in enumerate(self.words[i + 1 :], i + 1):
                coupling = word1.morphological_coupling(word2)
                # Local order parameters
                psi1 = (word1.type_bits + word1.value_bits) / 16.0
                psi2 = (word2.type_bits + word2.value_bits) / 16.0
                interaction_energy += self.coupling_strength * coupling * psi1 * psi2

        return free_energy - interaction_energy

    def susceptibility(self) -> float:
        """Morphological susceptibility χ = ∂²F/∂h²"""
        # Numerical derivative of order parameter w.r.t. external field
        h_original = self.external_field
        dh = 0.01

        self.external_field = h_original + dh
        order_plus = self.compute_order_parameter()

        self.external_field = h_original - dh
        order_minus = self.compute_order_parameter()

        self.external_field = h_original

        dpsi_dh = (order_plus.magnitude - order_minus.magnitude) / (2 * dh)
        return dpsi_dh / self.temperature  # Fluctuation-dissipation theorem

    def detect_phase_transition(self) -> Tuple[MorphologicalPhase, float]:
        """Detect current phase based on order parameter and susceptibility"""
        order_param = self.compute_order_parameter()
        chi = self.susceptibility()

        # Critical temperature estimate
        T_c = self.a / (2 * self.coupling_strength)

        if abs(self.temperature - T_c) < 0.1 and chi > 10:
            phase = MorphologicalPhase.CRITICAL
        elif order_param.magnitude < 0.1:
            phase = MorphologicalPhase.DISORDERED
        elif order_param.magnitude > 0.8 and self.temperature < 0.1:
            phase = MorphologicalPhase.SUPERFLUID
        else:
            phase = MorphologicalPhase.ORDERED

        return phase, order_param.magnitude

    def quine_stability_test(self) -> bool:
        """Test if ψ(t) == ψ(runtime) == ψ(child) (morphogenic fixity)"""
        # Sample system at different times/states
        initial_order = self.compute_order_parameter()

        # Evolve system slightly
        self.temperature *= 0.99
        runtime_order = self.compute_order_parameter()

        # Create "child" system with same parameters
        child_system = MorphologicalFieldSystem(len(self.words), self.temperature)
        child_order = child_system.compute_order_parameter()

        # Reset temperature
        self.temperature /= 0.99

        # Check if order parameters are approximately equal
        tolerance = 0.05
        initial_stable = (
            abs(initial_order.magnitude - runtime_order.magnitude) < tolerance
        )
        runtime_stable = (
            abs(runtime_order.magnitude - child_order.magnitude) < tolerance
        )

        return initial_stable and runtime_stable

    def phase_diagram_point(self) -> Dict[str, float]:
        """Return current point in phase diagram"""
        phase, order_mag = self.detect_phase_transition()
        return {
            'temperature': self.temperature,
            'external_field': self.external_field,
            'order_parameter': order_mag,
            'free_energy': self.landau_free_energy(self.compute_order_parameter()),
            'susceptibility': self.susceptibility(),
            'phase': phase.value,
            'quine_stable': self.quine_stability_test(),
        }


def demonstrate_phase_transitions():
    """Demonstrate morphological phase transitions"""
    print("=== Morphological Phase Transition Analysis ===\n")

    system = MorphologicalFieldSystem(num_words=32)

    # Temperature sweep to find phase transitions
    temperatures = [2.0, 1.5, 1.0, 0.8, 0.6, 0.4, 0.2, 0.1, 0.05]

    print("T\t|ψ|\tPhase\t\tχ\tQuine\tF")
    print("-" * 60)

    for T in temperatures:
        system.temperature = T
        point = system.phase_diagram_point()

        print(
            f"{T:.2f}\t{point['order_parameter']:.3f}\t"
            f"{point['phase']:<12}\t{point['susceptibility']:.1f}\t"
            f"{point['quine_stable']}\t{point['free_energy']:.2f}"
        )

    print("\n=== Critical Phenomena Analysis ===")

    # Find critical temperature by susceptibility peak
    critical_temps = []
    for T in [i / 100 for i in range(50, 150, 5)]:  # Fine scan around T~1
        system.temperature = T
        chi = system.susceptibility()
        if chi > 5.0:  # High susceptibility indicates criticality
            critical_temps.append(T)

    if critical_temps:
        T_critical = sum(critical_temps) / len(critical_temps)
        print(f"Estimated critical temperature: T_c ≈ {T_critical:.3f}")

        # Test quine stability at critical point
        system.temperature = T_critical
        is_quine_stable = system.quine_stability_test()
        print(f"Quine stability at T_c: {is_quine_stable}")

        if is_quine_stable:
            print("✓ Perfect quines achieved at critical temperature!")
            print("  Morphogenic fixity: ψ(t) = ψ(runtime) = ψ(child)")
        else:
            print("✗ Quines unstable at critical point - need parameter tuning")

    print("\n=== Topological Winding Analysis ===")

    # Analyze winding numbers around torus
    winding_theta = 0
    winding_phi = 0

    for i in range(len(system.words)):
        curr_word = system.words[i]
        next_word = system.words[(i + 1) % len(system.words)]

        # Compute winding contribution
        dtheta = next_word.theta - curr_word.theta
        dphi = next_word.phi - curr_word.phi

        # Handle wrapping
        if dtheta > math.pi:
            dtheta -= 2 * math.pi
        elif dtheta < -math.pi:
            dtheta += 2 * math.pi

        if dphi > math.pi:
            dphi -= 2 * math.pi
        elif dphi < -math.pi:
            dphi += 2 * math.pi

        winding_theta += dtheta
        winding_phi += dphi

    winding_theta /= 2 * math.pi
    winding_phi /= 2 * math.pi

    print(f"Winding number (θ): {winding_theta:.2f}")
    print(f"Winding number (φ): {winding_phi:.2f}")
    print(f"Total topological charge: {abs(winding_theta) + abs(winding_phi):.2f}")


if __name__ == "__main__":
    demonstrate_phase_transitions()
