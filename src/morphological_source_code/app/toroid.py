from __future__ import annotations
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# LICENSE © 2025: CC BY 4.0: PHOVOS:https://github.com/Phovos/Morphological
# ------------------------------------------------------------------------------
# Standard Library Imports - 3.13 std libs **ONLY**
# ------------------------------------------------------------------------------
"""
Toroidal Morphological Phase Transitions with Landau Theory
Standard library implementation of T/V/C ontology on toroidal fields
"""

import math
import random
from typing import List, Tuple, Dict, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import hashlib
import struct


class MorphologicalPhase(Enum):
    """Phase states in T/V/C morphological field"""
    DISORDERED = 0      # High entropy, no correlation
    QUIESCENT = 1       # Local order, partial correlation
    COHERENT = 2        # Global order, full correlation
    QUINIC = 3          # Perfect self-reproduction (ψ = ψ_child)


@dataclass
class LandauParameters:
    """Landau theory parameters for morphological phase transitions"""
    temperature: float  # Computational temperature (entropy rate)
    coupling: float     # Inter-ByteWord coupling strength
    field: float        # External morphological field
    alpha: float = 2.0  # Second-order term coefficient
    beta: float = 4.0   # Fourth-order term coefficient


class ToroidalByteWord:
    """8-bit word positioned on toroidal morphological field"""

    def __init__(self, value: int):
        if not 0 <= value <= 255:
            raise ValueError("ByteWord must be 8-bit (0-255)")

        self.raw_value = value

        # T/V/C tripartite decomposition (3+3+2 bits)
        self.type_bits = (value & 0b11100000) >> 5      # 3 bits: Type
        self.value_bits = (value & 0b00011100) >> 2     # 3 bits: Value
        self.compute_bits = value & 0b00000011          # 2 bits: Compute

        # Toroidal coordinates
        self._theta = self.type_bits * (2 * math.pi / 8)    # Major angle
        self._phi = self.value_bits * (2 * math.pi / 8)     # Minor angle
        self._r = 1.0 + (self.compute_bits / 4.0)           # Radial distance

        # Morphological state
        self.phase = MorphologicalPhase.DISORDERED
        self.order_parameter = 0.0
        self.winding_number = 0

    @property
    def toroidal_position(self) -> Tuple[float, float, float]:
        """Get (theta, phi, r) coordinates on torus"""
        return (self._theta, self._phi, self._r)

    @property
    def cartesian_position(self) -> Tuple[float, float, float]:
        """Convert toroidal to Cartesian coordinates"""
        R = 2.0  # Major radius
        r = 1.0  # Minor radius scale

        x = (R + r * self._r * math.cos(self._phi)) * math.cos(self._theta)
        y = (R + r * self._r * math.cos(self._phi)) * math.sin(self._theta)
        z = r * self._r * math.sin(self._phi)

        return (x, y, z)

    def morphological_distance(self, other: 'ToroidalByteWord') -> float:
        """Calculate morphological distance on torus surface"""
        # Toroidal distance accounting for wrapping
        theta_diff = min(abs(self._theta - other._theta),
                         2*math.pi - abs(self._theta - other._theta))
        phi_diff = min(abs(self._phi - other._phi),
                       2*math.pi - abs(self._phi - other._phi))
        r_diff = abs(self._r - other._r)

        return math.sqrt(theta_diff**2 + phi_diff**2 + r_diff**2)

    def field_strength(self, other: 'ToroidalByteWord') -> float:
        """Gravitational-like field strength between ByteWords"""
        distance = self.morphological_distance(other)

        # T/V/C alignment bonus
        t_alignment = 1.0 - abs(self.type_bits - other.type_bits) / 7.0
        v_alignment = 1.0 - abs(self.value_bits - other.value_bits) / 7.0
        c_alignment = 1.0 - abs(self.compute_bits - other.compute_bits) / 3.0

        alignment_factor = (t_alignment + v_alignment + c_alignment) / 3.0

        # Inverse square law with alignment modulation
        return alignment_factor / (distance**2 + 0.1)

    def church_encode_winding(self, path: List['ToroidalByteWord']) -> int:
        """Count winding number around torus using Church encoding"""
        if len(path) < 2:
            return 0

        total_winding = 0

        for i in range(len(path) - 1):
            current = path[i]
            next_word = path[i + 1]

            # Calculate angular changes (accounting for wrapping)
            d_theta = next_word._theta - current._theta
            d_phi = next_word._phi - current._phi

            # Normalize to [-π, π]
            if d_theta > math.pi:
                d_theta -= 2 * math.pi
            elif d_theta < -math.pi:
                d_theta += 2 * math.pi

            if d_phi > math.pi:
                d_phi -= 2 * math.pi
            elif d_phi < -math.pi:
                d_phi += 2 * math.pi

            # Church numeral: count significant angular changes
            if abs(d_theta) > math.pi/4 or abs(d_phi) > math.pi/4:
                total_winding += 1

        return total_winding

    def __repr__(self) -> str:
        return f"ToroidalByteWord(T={self.type_bits:03b}, V={self.value_bits:03b}, C={self.compute_bits:02b}, phase={self.phase.name})"


class MorphologicalField:
    """Toroidal field of interacting ByteWords with Landau phase dynamics"""

    def __init__(self, size: int, landau_params: LandauParameters):
        self.size = size
        self.landau = landau_params
        self.words: List[ToroidalByteWord] = []
        self.time_step = 0

        # Initialize random field
        for _ in range(size):
            word = ToroidalByteWord(random.randint(0, 255))
            self.words.append(word)

    def compute_local_order_parameter(self, word: ToroidalByteWord, radius: float = 1.0) -> float:
        """Compute local order parameter using T/V/C correlations"""
        neighbors = [w for w in self.words
                     if w != word and word.morphological_distance(w) < radius]

        if not neighbors:
            return 0.0

        # Correlation in T/V/C space
        correlations = []
        for neighbor in neighbors:
            t_corr = 1.0 - abs(word.type_bits - neighbor.type_bits) / 7.0
            v_corr = 1.0 - abs(word.value_bits - neighbor.value_bits) / 7.0
            c_corr = 1.0 - abs(word.compute_bits - neighbor.compute_bits) / 3.0

            total_corr = (t_corr + v_corr + c_corr) / 3.0
            correlations.append(total_corr)

        return sum(correlations) / len(correlations)

    def landau_free_energy(self, order_param: float) -> float:
        """Landau free energy as function of order parameter"""
        # F = ½α(T-Tc)m² + ¼βm⁴ - hm
        # where m is order parameter, h is external field

        critical_temp = 1.0  # Normalize critical temperature
        reduced_temp = self.landau.temperature - critical_temp

        quadratic_term = 0.5 * self.landau.alpha * reduced_temp * order_param**2
        quartic_term = 0.25 * self.landau.beta * order_param**4
        field_term = -self.landau.field * order_param

        return quadratic_term + quartic_term + field_term

    def update_phases(self):
        """Update morphological phases using Landau theory"""
        for word in self.words:
            # Compute local order parameter
            local_order = self.compute_local_order_parameter(word)
            word.order_parameter = local_order

            # Determine phase based on order parameter and free energy
            free_energy = self.landau_free_energy(local_order)

            if local_order < 0.2:
                word.phase = MorphologicalPhase.DISORDERED
            elif local_order < 0.6:
                word.phase = MorphologicalPhase.QUIESCENT
            elif local_order < 0.9:
                word.phase = MorphologicalPhase.COHERENT
            else:
                # Check for quinic condition: ψ(t) == ψ(runtime) == ψ(child)
                if self.check_quinic_stability(word):
                    word.phase = MorphologicalPhase.QUINIC
                else:
                    word.phase = MorphologicalPhase.COHERENT

    def check_quinic_stability(self, word: ToroidalByteWord) -> bool:
        """Check if word satisfies quinic stability condition"""
        # Create "child" word through morphological reproduction
        child_value = self.reproduce_word(word)
        child_word = ToroidalByteWord(child_value)

        # Check if parent and child have same morphological signature
        parent_signature = (word.type_bits, word.value_bits, word.compute_bits)
        child_signature = (child_word.type_bits,
                           child_word.value_bits, child_word.compute_bits)

        # Perfect quine: ψ(t) == ψ(runtime) == ψ(child)
        return parent_signature == child_signature

    def reproduce_word(self, word: ToroidalByteWord) -> int:
        """Reproduce word through morphological transformation"""
        # Use hash-based reproduction to create deterministic "child"
        parent_data = struct.pack('B', word.raw_value)
        hash_obj = hashlib.sha256(parent_data)
        child_bytes = hash_obj.digest()

        # Extract child value from hash
        return child_bytes[0]  # First byte as child value

    def evolve_step(self):
        """Single evolution step of morphological field"""
        self.time_step += 1

        # Update phases based on current state
        self.update_phases()

        # Apply morphological dynamics (non-associative evolution)
        self.apply_toroidal_dynamics()

        # Adjust Landau parameters based on system state
        self.adjust_temperature()

    def apply_toroidal_dynamics(self):
        """Apply toroidal field dynamics with non-associative composition"""
        for i, word in enumerate(self.words):
            # Find nearest neighbors on torus
            neighbors = sorted(
                [(j, w, word.morphological_distance(w))
                 for j, w in enumerate(self.words) if j != i],
                key=lambda x: x[2]
            )[:3]  # Top 3 nearest neighbors

            if len(neighbors) >= 2:
                # Create orbital path around torus
                path = [word] + [n[1]
                                 for n in neighbors] + [word]  # Close the loop

                # Compute winding number using Church encoding
                winding = word.church_encode_winding(path)
                word.winding_number = winding

                # Non-associative composition based on winding
                if winding > 2:  # High winding = phase transition trigger
                    # Modify word through toroidal transformation
                    new_theta = (word._theta + 0.1 *
                                 math.sin(winding)) % (2 * math.pi)
                    new_phi = (word._phi + 0.1 *
                               math.cos(winding)) % (2 * math.pi)

                    # Map back to T/V/C bits
                    new_type = int((new_theta / (2 * math.pi)) * 8) % 8
                    new_value = int((new_phi / (2 * math.pi)) * 8) % 8

                    # Reconstruct ByteWord
                    new_raw = (new_type << 5) | (
                        new_value << 2) | word.compute_bits
                    self.words[i] = ToroidalByteWord(new_raw)

    def adjust_temperature(self):
        """Adjust computational temperature based on system dynamics"""
        # Count phase populations
        phase_counts = {phase: 0 for phase in MorphologicalPhase}
        total_order = 0.0

        for word in self.words:
            phase_counts[word.phase] += 1
            total_order += word.order_parameter

        avg_order = total_order / len(self.words)

        # Cooling schedule: reduce temperature as order increases
        if avg_order > 0.7:  # High order = cool down
            self.landau.temperature *= 0.98
        elif avg_order < 0.3:  # Low order = heat up
            self.landau.temperature *= 1.02

        # Prevent temperature from going too extreme
        self.landau.temperature = max(0.1, min(2.0, self.landau.temperature))

    def get_phase_statistics(self) -> Dict[str, float]:
        """Get current phase transition statistics"""
        phase_counts = {phase.name: 0 for phase in MorphologicalPhase}
        total_order = 0.0
        quinic_count = 0

        for word in self.words:
            phase_counts[word.phase.name] += 1
            total_order += word.order_parameter
            if word.phase == MorphologicalPhase.QUINIC:
                quinic_count += 1

        total_words = len(self.words)

        return {
            'avg_order_parameter': total_order / total_words,
            'temperature': self.landau.temperature,
            'quinic_fraction': quinic_count / total_words,
            'phase_fractions': {name: count/total_words for name, count in phase_counts.items()},
            'time_step': self.time_step
        }

    def __repr__(self) -> str:
        stats = self.get_phase_statistics()
        return f"MorphologicalField(size={self.size}, T={stats['temperature']:.3f}, quinic={stats['quinic_fraction']:.3f})"


def demonstrate_phase_transitions():
    """Demonstrate morphological phase transitions with Landau theory"""
    print("=== Toroidal Morphological Phase Transitions ===\n")

    # Initialize field with Landau parameters
    landau_params = LandauParameters(
        temperature=1.5,    # Start above critical temperature
        coupling=0.8,       # Strong coupling
        field=0.1           # Weak external field
    )

    field = MorphologicalField(size=50, landau_params=landau_params)

    print("Initial state:")
    print(f"Field: {field}")
    print(f"Statistics: {field.get_phase_statistics()}\n")

    # Evolve system and track phase transitions
    print("Evolution trace:")
    for step in range(20):
        field.evolve_step()

        if step % 5 == 0:
            stats = field.get_phase_statistics()
            print(f"Step {step:2d}: T={stats['temperature']:.3f}, "
                  f"Order={stats['avg_order_parameter']:.3f}, "
                  f"Quinic={stats['quinic_fraction']:.3f}")

    print(f"\nFinal field: {field}")

    # Analyze quinic words
    quinic_words = [w for w in field.words if w.phase ==
                    MorphologicalPhase.QUINIC]
    print(
        f"\nFound {len(quinic_words)} quinic words (perfect self-reproduction):")
    for i, word in enumerate(quinic_words[:3]):  # Show first 3
        child_value = field.reproduce_word(word)
        child = ToroidalByteWord(child_value)
        print(f"  {i+1}. Parent: {word}")
        print(f"     Child:  {child}")
        print(f"     Match:  {word.raw_value == child.raw_value}")

    return field


if __name__ == "__main__":
    # Run demonstration
    final_field = demonstrate_phase_transitions()

    print("\n=== Phase Transition Analysis ===")
    final_stats = final_field.get_phase_statistics()

    print(f"Final temperature: {final_stats['temperature']:.4f}")
    print(f"Average order parameter: {final_stats['avg_order_parameter']:.4f}")
    print(f"Quinic fraction: {final_stats['quinic_fraction']:.4f}")

    print("\nPhase distribution:")
    for phase, fraction in final_stats['phase_fractions'].items():
        print(f"  {phase}: {fraction:.1%}")

    if final_stats['quinic_fraction'] > 0:
        print(
            f"\n🎉 SUCCESS: Achieved {final_stats['quinic_fraction']:.1%} quinic stability!")
        print("Perfect quines demonstrated: ψ(t) == ψ(runtime) == ψ(child)")
    else:
        print("\n🔄 System still evolving toward quinic stability...")
