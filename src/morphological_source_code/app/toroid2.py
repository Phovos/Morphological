from __future__ import annotations
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# LICENSE © 2025: CC BY 4.0: PHOVOS:https://github.com/Phovos/Morphological
#------------------------------------------------------------------------------
# Standard Library Imports - 3.13 std libs **ONLY**
#------------------------------------------------------------------------------
import math
from typing import Optional, List, Dict, Tuple
from enum import Enum

class ToroidalDirection(Enum):
    """Directions on the torus surface for ByteWord navigation"""
    MAJOR_POSITIVE = 0b00   # +θ (around major circumference)
    MAJOR_NEGATIVE = 0b01   # -θ 
    MINOR_POSITIVE = 0b10   # +φ (around minor circumference)
    MINOR_NEGATIVE = 0b11   # -φ

class SpinorState(Enum):
    """Spinor orientations in morphological space"""
    UP_UP = 0b00      # |↑↑⟩ - both spins aligned
    UP_DOWN = 0b01    # |↑↓⟩ - opposite spins
    DOWN_UP = 0b10    # |↓↑⟩ - opposite spins  
    DOWN_DOWN = 0b11  # |↓↓⟩ - both spins aligned

class ByteWordTorus:
    """
    8-bit morphological quine with torus-spinor topology
    
    Bit Layout:
    [7:6] = ToroidalDirection (2 bits) - where to wind
    [5:4] = SpinorState (2 bits) - quantum spin configuration
    [3:0] = ChurchWinding (4 bits) - how many times to wind (0-15)
    """
    
    def __init__(self, data: int = 0b00000000):
        assert 0 <= data <= 255, "ByteWord must fit in 8 bits"
        self.data = data
        self._neighbors: Dict[ToroidalDirection, Optional['ByteWordTorus']] = {
            ToroidalDirection.MAJOR_POSITIVE: None,
            ToroidalDirection.MAJOR_NEGATIVE: None,
            ToroidalDirection.MINOR_POSITIVE: None,
            ToroidalDirection.MINOR_NEGATIVE: None
        }
        self._entanglement_cache = {}
    
    @property
    def direction(self) -> ToroidalDirection:
        """Extract toroidal direction from bits [7:6]"""
        return ToroidalDirection((self.data >> 6) & 0b11)
    
    @property
    def spinor(self) -> SpinorState:
        """Extract spinor state from bits [5:4]"""
        return SpinorState((self.data >> 4) & 0b11)
    
    @property
    def church_winding(self) -> int:
        """Extract Church winding number from bits [3:0]"""
        return self.data & 0b1111
    
    def set_direction(self, direction: ToroidalDirection) -> 'ByteWordTorus':
        """Set toroidal direction, return new ByteWord"""
        new_data = (self.data & 0b00111111) | (direction.value << 6)
        return ByteWordTorus(new_data)
    
    def set_spinor(self, spinor: SpinorState) -> 'ByteWordTorus':
        """Set spinor state, return new ByteWord"""
        new_data = (self.data & 0b11001111) | (spinor.value << 4)
        return ByteWordTorus(new_data)
    
    def set_winding(self, winding: int) -> 'ByteWordTorus':
        """Set Church winding number, return new ByteWord"""
        assert 0 <= winding <= 15, "Winding must fit in 4 bits"
        new_data = (self.data & 0b11110000) | winding
        return ByteWordTorus(new_data)
    
    def link_neighbor(self, direction: ToroidalDirection, neighbor: 'ByteWordTorus'):
        """Create bidirectional torus link"""
        self._neighbors[direction] = neighbor
        # Create reverse link
        reverse_dir = {
            ToroidalDirection.MAJOR_POSITIVE: ToroidalDirection.MAJOR_NEGATIVE,
            ToroidalDirection.MAJOR_NEGATIVE: ToroidalDirection.MAJOR_POSITIVE,
            ToroidalDirection.MINOR_POSITIVE: ToroidalDirection.MINOR_NEGATIVE,
            ToroidalDirection.MINOR_NEGATIVE: ToroidalDirection.MINOR_POSITIVE
        }
        neighbor._neighbors[reverse_dir[direction]] = self
    
    def church_encode(self, n: int) -> 'ByteWordTorus':
        """
        Church encoding: represent integer n as winding number
        If n > 15, we wind around the torus to neighboring ByteWords
        """
        if n <= 15:
            return self.set_winding(n)
        
        # For larger numbers, we need to wind to neighbors
        base_winding = n % 16
        overflow = n // 16
        
        result = self.set_winding(base_winding)
        
        # Propagate overflow by winding to neighbors
        if overflow > 0 and self._neighbors[self.direction]:
            result._entanglement_cache['overflow'] = overflow
            neighbor_result = self._neighbors[self.direction].church_encode(overflow)
            result._entanglement_cache['overflow_neighbor'] = neighbor_result
        
        return result
    
    def church_decode(self) -> int:
        """
        Decode Church winding back to integer
        Follows winding path through torus topology
        """
        base_value = self.church_winding
        
        # Add overflow from entangled neighbors
        if 'overflow' in self._entanglement_cache:
            overflow_value = self._entanglement_cache['overflow']
            return base_value + (overflow_value * 16)
        
        return base_value
    
    def compose(self, other: 'ByteWordTorus') -> 'ByteWordTorus':
        """
        Non-associative composition using torus-spinor dynamics
        
        The magic happens here: we use topological winding + spinor interactions
        to create non-linear, non-associative morphological combinations
        """
        # Spinor interaction matrix (Pauli-like but morphological)
        spinor_interaction = {
            (SpinorState.UP_UP, SpinorState.UP_UP): SpinorState.UP_UP,
            (SpinorState.UP_UP, SpinorState.UP_DOWN): SpinorState.DOWN_UP,
            (SpinorState.UP_UP, SpinorState.DOWN_UP): SpinorState.UP_DOWN,
            (SpinorState.UP_UP, SpinorState.DOWN_DOWN): SpinorState.DOWN_DOWN,
            
            (SpinorState.UP_DOWN, SpinorState.UP_UP): SpinorState.DOWN_UP,
            (SpinorState.UP_DOWN, SpinorState.UP_DOWN): SpinorState.UP_UP,
            (SpinorState.UP_DOWN, SpinorState.DOWN_UP): SpinorState.DOWN_DOWN,
            (SpinorState.UP_DOWN, SpinorState.DOWN_DOWN): SpinorState.UP_DOWN,
            
            (SpinorState.DOWN_UP, SpinorState.UP_UP): SpinorState.UP_DOWN,
            (SpinorState.DOWN_UP, SpinorState.UP_DOWN): SpinorState.DOWN_DOWN,
            (SpinorState.DOWN_UP, SpinorState.DOWN_UP): SpinorState.UP_UP,
            (SpinorState.DOWN_UP, SpinorState.DOWN_DOWN): SpinorState.DOWN_UP,
            
            (SpinorState.DOWN_DOWN, SpinorState.UP_UP): SpinorState.DOWN_DOWN,
            (SpinorState.DOWN_DOWN, SpinorState.UP_DOWN): SpinorState.UP_DOWN,
            (SpinorState.DOWN_DOWN, SpinorState.DOWN_UP): SpinorState.DOWN_UP,
            (SpinorState.DOWN_DOWN, SpinorState.DOWN_DOWN): SpinorState.UP_UP,
        }
        
        # Calculate new spinor state
        new_spinor = spinor_interaction[(self.spinor, other.spinor)]
        
        # Calculate winding composition (non-associative!)
        # This is where the "PacMan world" behavior emerges
        winding_sum = (self.church_winding + other.church_winding) % 16
        
        # Direction is influenced by spinor interaction
        if new_spinor in [SpinorState.UP_UP, SpinorState.DOWN_DOWN]:
            # Parallel spins = same direction
            new_direction = self.direction
        else:
            # Anti-parallel spins = perpendicular direction
            direction_rotation = {
                ToroidalDirection.MAJOR_POSITIVE: ToroidalDirection.MINOR_POSITIVE,
                ToroidalDirection.MAJOR_NEGATIVE: ToroidalDirection.MINOR_NEGATIVE,
                ToroidalDirection.MINOR_POSITIVE: ToroidalDirection.MAJOR_POSITIVE,
                ToroidalDirection.MINOR_NEGATIVE: ToroidalDirection.MAJOR_NEGATIVE,
            }
            new_direction = direction_rotation[self.direction]
        
        # Create result ByteWord
        result = ByteWordTorus(0)
        result = result.set_direction(new_direction)
        result = result.set_spinor(new_spinor)
        result = result.set_winding(winding_sum)
        
        # Handle "hole" dynamics - if winding sum creates overflow,
        # we create entanglement with neighbors
        total_winding = self.church_winding + other.church_winding
        if total_winding > 15:
            overflow = total_winding - 15
            result._entanglement_cache['hole'] = overflow
            
            # Pass overflow to neighbor (PacMan world behavior!)
            target_neighbor = result._neighbors.get(new_direction)
            if target_neighbor:
                result._entanglement_cache['hole_neighbor'] = target_neighbor
                # The neighbor gets "excited" by receiving the overflow
                target_neighbor._entanglement_cache['excitation'] = overflow
        
        return result
    
    def propagate(self, steps: int = 1) -> List['ByteWordTorus']:
        """
        Propagate through torus topology following winding directions
        This implements the "high-energy neighbors" behavior you described
        """
        states = [self]
        current = self
        
        for step in range(steps):
            # Follow the winding direction
            next_neighbor = current._neighbors.get(current.direction)
            
            if next_neighbor is None:
                # No neighbor in this direction, try perpendicular
                perp_directions = [
                    ToroidalDirection.MINOR_POSITIVE if current.direction in [
                        ToroidalDirection.MAJOR_POSITIVE, ToroidalDirection.MAJOR_NEGATIVE
                    ] else ToroidalDirection.MAJOR_POSITIVE
                ]
                for perp_dir in perp_directions:
                    next_neighbor = current._neighbors.get(perp_dir)
                    if next_neighbor:
                        break
            
            if next_neighbor:
                # Energy transfer: compose with neighbor
                current = current.compose(next_neighbor)
            else:
                # Isolated: self-compose (idempotent behavior)
                current = current.compose(current)
            
            states.append(current)
        
        return states
    
    def to_float(self) -> float:
        """Convert to float using torus coordinates"""
        # Major angle (θ) from direction and winding
        theta = (self.direction.value * math.pi/2) + (self.church_winding * math.pi/8)
        
        # Minor angle (φ) from spinor state
        phi = self.spinor.value * math.pi/2
        
        # Torus surface coordinates -> single float value
        major_radius = 2.0
        minor_radius = 1.0
        
        x = (major_radius + minor_radius * math.cos(phi)) * math.cos(theta)
        y = (major_radius + minor_radius * math.cos(phi)) * math.sin(theta)
        z = minor_radius * math.sin(phi)
        
        # Project to single dimension (could use different projections)
        return (x + y + z) / 3.0
    
    def says(self) -> str:
        """What this ByteWord says about itself"""
        return (f"ByteWordTorus({self.direction.name}, {self.spinor.name}, "
                f"winding={self.church_winding}) -> {self.to_float():.3f}")
    
    def __repr__(self):
        return f"ByteWordTorus(0b{self.data:08b}) = {self.says()}"

# Example: Create torus field with multiple ByteWords
def create_torus_field(size: int = 4) -> List[List[ByteWordTorus]]:
    """Create a torus field of ByteWords with proper topology"""
    field = []
    
    # Create grid of ByteWords
    for i in range(size):
        row = []
        for j in range(size):
            # Initialize with position-dependent values
            direction = ToroidalDirection(i % 4)
            spinor = SpinorState(j % 4) 
            winding = (i + j) % 16
            
            word = ByteWordTorus(0)
            word = word.set_direction(direction)
            word = word.set_spinor(spinor)
            word = word.set_winding(winding)
            
            row.append(word)
        field.append(row)
    
    # Link neighbors to create torus topology
    for i in range(size):
        for j in range(size):
            current = field[i][j]
            
            # Major direction links (wrapping around)
            right = field[i][(j + 1) % size]
            left = field[i][(j - 1) % size]
            current.link_neighbor(ToroidalDirection.MAJOR_POSITIVE, right)
            current.link_neighbor(ToroidalDirection.MAJOR_NEGATIVE, left)
            
            # Minor direction links (wrapping around)
            down = field[(i + 1) % size][j]
            up = field[(i - 1) % size][j]
            current.link_neighbor(ToroidalDirection.MINOR_POSITIVE, down)
            current.link_neighbor(ToroidalDirection.MINOR_NEGATIVE, up)
    
    return field

# Demonstration
if __name__ == "__main__":
    # Create a small torus field
    torus_field = create_torus_field(3)
    
    # Pick a ByteWord and show its evolution
    origin = torus_field[0][0]
    print(f"Origin: {origin}")
    
    # Compose with neighbor (this creates the "PacMan world" behavior)
    neighbor = torus_field[0][1]
    composition = origin.compose(neighbor)
    print(f"Composed: {composition}")
    
    # Propagate through the torus (energy flowing to neighbors)
    evolution = composition.propagate(steps=5)
    print("\nEvolution through torus:")
    for i, state in enumerate(evolution):
        print(f"Step {i}: {state}")
    
    # Church encoding example
    print(f"\nChurch encoding 23: {origin.church_encode(23)}")
    print(f"Decoded: {origin.church_encode(23).church_decode()}")