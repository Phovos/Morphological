"""
ByteWord Cook & Mertz Binary Abelization
Hand-rolled FFT with XOR algebra over binary fields
pure std lib morphological mathematics
"""

import math
import cmath
from typing import List, Tuple, Union, Optional
from dataclasses import dataclass

class BinaryField:
    """GF(2^8) - Galois Field for binary operations"""
    
    # Primitive polynomial x^8 + x^4 + x^3 + x + 1 (0x11B)
    PRIMITIVE = 0x11B
    
    @staticmethod
    def multiply(a: int, b: int) -> int:
        """Multiply two elements in GF(2^8)"""
        result = 0
        while b:
            if b & 1:
                result ^= a
            a <<= 1
            if a & 0x100:  # If overflow, reduce by primitive polynomial
                a ^= BinaryField.PRIMITIVE
            b >>= 1
        return result & 0xFF
    
    @staticmethod
    def power(base: int, exp: int) -> int:
        """Compute base^exp in GF(2^8)"""
        if exp == 0:
            return 1
        result = 1
        base = base & 0xFF
        while exp > 0:
            if exp & 1:
                result = BinaryField.multiply(result, base)
            base = BinaryField.multiply(base, base)
            exp >>= 1
        return result


@dataclass
class ComplexByte:
    """Complex number representation for binary FFT"""
    real: int  # 0-255
    imag: int  # 0-255
    
    def __add__(self, other: 'ComplexByte') -> 'ComplexByte':
        return ComplexByte(
            self.real ^ other.real,  # XOR addition in binary field
            self.imag ^ other.imag
        )
    
    def __sub__(self, other: 'ComplexByte') -> 'ComplexByte':
        # In GF(2), subtraction is same as addition (XOR)
        return self + other
    
    def __mul__(self, other: 'ComplexByte') -> 'ComplexByte':
        # (a + bi)(c + di) = (ac - bd) + (ad + bc)i
        # In GF(2): - is +, so: (ac + bd) + (ad + bc)i
        real_part = BinaryField.multiply(self.real, other.real) ^ \
                   BinaryField.multiply(self.imag, other.imag)
        imag_part = BinaryField.multiply(self.real, other.imag) ^ \
                   BinaryField.multiply(self.imag, other.real)
        return ComplexByte(real_part, imag_part)
    
    def __str__(self) -> str:
        return f"{self.real:02x}+{self.imag:02x}i"


class CookMertzRootsOfUnity:
    """Cook & Mertz approach to roots of unity in binary fields"""
    
    def __init__(self, n: int):
        """Initialize for n-point transform where n is power of 2"""
        assert n & (n - 1) == 0, "n must be power of 2"
        self.n = n
        self.log_n = n.bit_length() - 1
        self._compute_primitive_root()
        self._precompute_twiddle_factors()
    
    def _compute_primitive_root(self):
        """Find primitive nth root of unity in GF(2^8)"""
        # For binary fields, we use a generator element
        # This is a simplified approach - in practice you'd use 
        # more sophisticated primitive root finding
        self.primitive_root = 3  # Generator for small cases
        
        # Ensure it has order n
        order = 1
        current = self.primitive_root
        while current != 1 and order < 256:
            current = BinaryField.multiply(current, self.primitive_root)
            order += 1
        
        if order < self.n:
            # Fall back to a simple approach for demonstration
            self.primitive_root = 2
    
    def _precompute_twiddle_factors(self):
        """Precompute all twiddle factors w^k for k = 0 to n-1"""
        self.twiddles = []
        for k in range(self.n):
            # w^k where w is primitive nth root of unity
            power = BinaryField.power(self.primitive_root, k * (256 // self.n))
            # Convert to complex representation
            # Use bit manipulation to create imaginary part
            real_part = power
            imag_part = (power >> 4) ^ (power << 4) & 0xFF
            self.twiddles.append(ComplexByte(real_part, imag_part))
    
    def get_twiddle(self, k: int) -> ComplexByte:
        """Get k-th twiddle factor"""
        return self.twiddles[k % self.n]


class ByteWordFFT:
    """Hand-rolled FFT for ByteWord morphological transformations"""
    
    def __init__(self, size: int = 8):
        """Initialize FFT for given size (must be power of 2)"""
        self.size = size
        self.roots = CookMertzRootsOfUnity(size)
        self._bit_reverse_table = self._compute_bit_reverse_table()
    
    def _compute_bit_reverse_table(self) -> List[int]:
        """Precompute bit-reversed indices for FFT"""
        table = []
        log_size = self.size.bit_length() - 1
        for i in range(self.size):
            reversed_i = 0
            for bit in range(log_size):
                if i & (1 << bit):
                    reversed_i |= (1 << (log_size - 1 - bit))
            table.append(reversed_i)
        return table
    
    def _bit_reverse_permute(self, data: List[ComplexByte]) -> List[ComplexByte]:
        """Apply bit-reversal permutation"""
        return [data[self._bit_reverse_table[i]] for i in range(len(data))]
    
    def fft(self, data: List[int]) -> List[ComplexByte]:
        """
        Forward FFT using Cook & Mertz binary approach
        Input: list of integers (ByteWord values)
        Output: list of ComplexByte (frequency domain)
        """
        # Pad to power of 2 if necessary
        padded_size = 1 << (len(data) - 1).bit_length()
        if padded_size != len(data):
            data = data + [0] * (padded_size - len(data))
            self.size = padded_size
            self.roots = CookMertzRootsOfUnity(padded_size)
            self._bit_reverse_table = self._compute_bit_reverse_table()
        
        # Convert to ComplexByte
        complex_data = [ComplexByte(x & 0xFF, (x >> 8) & 0xFF) if x > 255 
                       else ComplexByte(x, 0) for x in data]
        
        # Bit-reversal permutation
        complex_data = self._bit_reverse_permute(complex_data)
        
        # Cooley-Tukey FFT algorithm
        log_n = self.size.bit_length() - 1
        
        for stage in range(log_n):
            step_size = 1 << (stage + 1)
            half_step = step_size >> 1
            
            for group in range(0, self.size, step_size):
                for i in range(half_step):
                    j = group + i
                    k = j + half_step
                    
                    # Twiddle factor
                    twiddle_index = (i * self.size) // step_size
                    w = self.roots.get_twiddle(twiddle_index)
                    
                    # Butterfly operation
                    u = complex_data[j]
                    v = complex_data[k] * w
                    
                    complex_data[j] = u + v
                    complex_data[k] = u - v  # In GF(2), - is same as +
        
        return complex_data
    
    def ifft(self, freq_data: List[ComplexByte]) -> List[int]:
        """
        Inverse FFT - transforms back to time domain
        """
        # For inverse, we use conjugate of twiddle factors
        # In binary fields, conjugate is just bit complement of imaginary part
        conjugated = []
        for cb in freq_data:
            conjugated.append(ComplexByte(cb.real, cb.imag ^ 0xFF))
        
        # Forward FFT with conjugated data
        result = self.fft([cb.real for cb in conjugated])
        
        # Convert back to integers and scale (in GF(2), scaling is identity)
        return [cb.real for cb in result]


class ByteWord:
    """
    ByteWord with Cook & Mertz morphological transformations
    """
    
    def __init__(self, value: int):
        self.value = value & 0xFF
        self._fft_cache = None
        self._morphological_signature = None
    
    def __str__(self) -> str:
        return f"ByteWord(0b{self.value:08b})"
    
    def __eq__(self, other) -> bool:
        return isinstance(other, ByteWord) and self.value == other.value
    
    @property
    def morphological_spectrum(self) -> List[ComplexByte]:
        """Get FFT representation of this ByteWord"""
        if self._fft_cache is None:
            fft = ByteWordFFT(8)
            # Convert single byte to 8-bit array
            bits = [(self.value >> i) & 1 for i in range(8)]
            self._fft_cache = fft.fft(bits)
        return self._fft_cache
    
    def compose_spectral(self, other: 'ByteWord') -> 'ByteWord':
        """
        Compose two ByteWords in frequency domain
        This is where Cook & Mertz magic happens!
        """
        my_spectrum = self.morphological_spectrum
        other_spectrum = other.morphological_spectrum
        
        # Pointwise multiplication in frequency domain
        composed_spectrum = []
        for i in range(len(my_spectrum)):
            composed_spectrum.append(my_spectrum[i] * other_spectrum[i])
        
        # Transform back to time domain
        fft = ByteWordFFT(8)
        time_domain = fft.ifft(composed_spectrum)
        
        # Reconstruct byte from bits
        result_value = 0
        for i, bit in enumerate(time_domain[:8]):
            if bit & 1:  # Take LSB
                result_value |= (1 << i)
        
        return ByteWord(result_value)
    
    def compose(self, other: 'ByteWord') -> 'ByteWord':
        """Standard XOR composition"""
        return ByteWord(self.value ^ other.value)
    
    def morphological_convolution(self, other: 'ByteWord') -> 'ByteWord':
        """
        True morphological convolution using Cook & Mertz
        This is the deep morphological operation!
        """
        # Pad to avoid circular convolution artifacts
        fft = ByteWordFFT(16)  # Larger size for linear convolution
        
        # Convert to bit arrays
        my_bits = [(self.value >> i) & 1 for i in range(8)] + [0] * 8
        other_bits = [(other.value >> i) & 1 for i in range(8)] + [0] * 8
        
        # FFT both sequences
        my_fft = fft.fft(my_bits)
        other_fft = fft.fft(other_bits)
        
        # Pointwise multiply
        conv_fft = [a * b for a, b in zip(my_fft, other_fft)]
        
        # IFFT back
        conv_result = fft.ifft(conv_fft)
        
        # Take first 8 bits and reconstruct
        result_value = 0
        for i in range(8):
            if conv_result[i] & 1:
                result_value |= (1 << i)
        
        return ByteWord(result_value)
    
    def propagate(self, steps: int = 1) -> List['ByteWord']:
        """
        Morphological propagation using spectral evolution
        """
        current = self
        evolution = [current]
        
        for step in range(steps):
            # Get spectral representation
            spectrum = current.morphological_spectrum
            
            # Apply morphological evolution operator in frequency domain
            evolved_spectrum = []
            for i, freq_component in enumerate(spectrum):
                # Phase rotation + amplitude modulation
                phase_shift = ComplexByte((freq_component.real + i) & 0xFF,
                                        (freq_component.imag + step) & 0xFF)
                evolved_spectrum.append(freq_component * phase_shift)
            
            # Transform back
            fft = ByteWordFFT(8)
            evolved_bits = fft.ifft(evolved_spectrum)
            
            # Reconstruct ByteWord
            evolved_value = 0
            for i, bit in enumerate(evolved_bits[:8]):
                if bit & 1:
                    evolved_value |= (1 << i)
            
            current = ByteWord(evolved_value)
            evolution.append(current)
        
        return evolution
    
    def to_float(self) -> float:
        """Convert to float using spectral energy"""
        spectrum = self.morphological_spectrum
        # Compute spectral energy
        energy = sum(BinaryField.multiply(cb.real, cb.real) ^ 
                    BinaryField.multiply(cb.imag, cb.imag) 
                    for cb in spectrum)
        return energy / 255.0
    
    @classmethod
    def from_float(cls, f: float) -> 'ByteWord':
        """Create ByteWord from float using spectral synthesis"""
        # Clamp and quantize
        f = max(0, min(1, f))
        value = int(f * 255)
        return cls(value)


# Demo the system
if __name__ == "__main__":
    print("=== ByteWord Cook & Mertz Binary Abelization Demo ===\n")
    
    # Create some ByteWords
    word1 = ByteWord(0b10101010)
    word2 = ByteWord(0b11001100)
    
    print(f"Word1: {word1}")
    print(f"Word2: {word2}")
    print(f"Word1 spectrum: {[str(cb) for cb in word1.morphological_spectrum]}")
    print()
    
    # Standard composition (XOR)
    composed = word1.compose(word2)
    print(f"Standard compose: {composed}")
    
    # Spectral composition (Cook & Mertz)
    spectral_composed = word1.compose_spectral(word2)
    print(f"Spectral compose: {spectral_composed}")
    
    # Morphological convolution
    convolved = word1.morphological_convolution(word2)
    print(f"Morphological convolution: {convolved}")
    print()
    
    # Propagation
    evolution = word1.propagate(steps=5)
    print("Morphological evolution:")
    for i, evolved in enumerate(evolution):
        print(f"  Step {i}: {evolved} -> {evolved.to_float():.3f}")
    print()
    
    # Demonstrate binary field operations
    print("=== Binary Field Operations ===")
    bf = BinaryField()
    print(f"3 * 5 in GF(2^8) = {bf.multiply(3, 5):02x}")
    print(f"2^7 in GF(2^8) = {bf.power(2, 7):02x}")
    
    print("\n象演旋态，炁流归一 - Morphological FFT achieved!")