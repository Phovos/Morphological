from dataclasses import dataclass
from typing import List, Dict, Tuple, Set, Optional, Callable
import random
import math
import numpy as np
from collections import deque


@dataclass
class ByteWord:
    """
    Fundamental bit-morphology structure with bra-ket division.

    The top nibble (CVVV) forms the "bra" part - representing compute and value spaces
    The bottom nibble (TTTT) forms the "ket" part - representing type structures
    """
    _value: int  # The raw byte value

    def __init__(self, value: int = 0):
        """Initialize with an optional value, default 0"""
        self._value = value & 0xFF  # Ensure 8-bit value

    @property
    def bra(self) -> int:
        """Get the top nibble (CVVV)"""
        return (self._value >> 4) & 0x0F

    @property
    def ket(self) -> int:
        """Get the bottom nibble (TTTT)"""
        return self._value & 0x0F

    @property
    def compute(self) -> int:
        """Get the C bit"""
        return (self._value >> 7) & 0x01

    @property
    def values(self) -> int:
        """Get the VVV bits"""
        return (self._value >> 4) & 0x07

    @property
    def types(self) -> int:
        """Get the TTTT bits"""
        return self._value & 0x0F

    def morph(self, operator: 'MorphOperator') -> 'ByteWord':
        """Apply a morphological transformation"""
        return operator.apply(self)

    def compose(self, other: 'ByteWord') -> 'ByteWord':
        """
        Compose with another ByteWord.
        Implements a non-associative composition following
        quantum field theory principles.
        """
        # The composition rule combines values according to
        # bra-ket like interaction
        c_bit = (self.compute & other.compute) ^ 1
        v_bits = (self.values & other.types) | (other.values & self.types)
        t_bits = self.types ^ other.types

        return ByteWord((c_bit << 7) | (v_bits << 4) | t_bits)

    def propagate(self, steps: int = 1) -> List['ByteWord']:
        """
        Evolve this ByteWord as a cellular automaton for n steps.
        Returns the sequence of evolution states.
        """
        states = [self]
        current = self

        for _ in range(steps):
            # Rule: Types evolve based on interaction between
            # compute bit and values
            new_types = current.types
            if current.compute:
                new_types = (current.types + current.values) & 0x0F
            else:
                new_types = (current.types ^ current.values) & 0x0F

            # Rule: Values evolve based on current types
            new_values = (current.values +
                          self._type_entropy(current.types)) & 0x07

            # Rule: Compute bit flips based on type-value interaction
            new_compute = current.compute ^ (
                1 if self._has_fixed_point(current.types, new_values) else 0)

            # Construct new state
            new_word = ByteWord((new_compute << 7) | (
                new_values << 4) | new_types)
            states.append(new_word)
            current = new_word

        return states

    def _type_entropy(self, types: int) -> int:
        """Calculate entropy contribution from types"""
        # Count number of 1s in types
        return bin(types).count('1')

    def _has_fixed_point(self, types: int, values: int) -> bool:
        """Determine if there's a fixed point in the type-value space"""
        return (types & values) != 0

    def __repr__(self) -> str:
        return f"ByteWord(C:{self.compute}, V:{self.values:03b}, T:{self.types:04b})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, ByteWord):
            return False
        return self._value == other._value

    def __hash__(self) -> int:
        return hash(self._value)


class MorphOperator:
    """Base class for morphological operators that transform ByteWords"""

    def apply(self, word: ByteWord) -> ByteWord:
        """Apply this operator to a ByteWord"""
        raise NotImplementedError()


class FlipComputeOperator(MorphOperator):
    """Operator that flips the compute bit"""

    def apply(self, word: ByteWord) -> ByteWord:
        new_compute = 1 - word.compute
        return ByteWord((new_compute << 7) | (word.values << 4) | word.types)


class RotateTypesOperator(MorphOperator):
    """Operator that rotates the type bits"""

    def apply(self, word: ByteWord) -> ByteWord:
        new_types = ((word.types << 1) | (word.types >> 3)) & 0x0F
        return ByteWord((word.compute << 7) | (word.values << 4) | new_types)


class ThermodynamicQuine:
    """
    A self-referential structure that evolves according to thermodynamic principles,
    capable of non-Markovian behavior and encoding its own history.
    """

    def __init__(self,
                 code_sequence: List[ByteWord] = None,
                 memory_capacity: int = 8,
                 noise_level: float = 0.1):
        """
        Initialize a ThermodynamicQuine.

        Args:
            code_sequence: Initial code sequence. If None, random sequence is generated.
            memory_capacity: Maximum length of memory for non-Markovian behavior.
            noise_level: Probability of random mutations during reproduction.
        """
        # Generate random code sequence if none provided
        if code_sequence is None:
            code_sequence = [ByteWord(random.randint(0, 255))
                             for _ in range(8)]

        self.code = code_sequence
        self.memory = deque(maxlen=memory_capacity)
        self.memory.append(code_sequence.copy())
        self.noise_level = noise_level
        self.age = 0
        self.fitness_score = 0
        self.lineage = set()  # Track evolutionary history
        self.entanglement_links = {}  # Links to other quines (id -> strength)

        # Calculate initial entropy
        self.entropy = self._calculate_entropy()

        # Calculate initial coherence
        self.coherence = self._calculate_coherence()

        # Non-Markovian metadata
        self.morphism_history = []

    def _calculate_entropy(self) -> float:
        """Calculate the entropy of this quine's code sequence"""
        # Count frequency of each ByteWord
        frequencies = {}
        for word in self.code:
            value = word._value
            if value in frequencies:
                frequencies[value] += 1
            else:
                frequencies[value] = 1

        # Calculate Shannon entropy
        total = len(self.code)
        entropy = 0
        for count in frequencies.values():
            probability = count / total
            entropy -= probability * math.log2(probability)

        return entropy

    def _calculate_coherence(self) -> float:
        """
        Calculate coherence based on pattern regularity.
        Higher value indicates more structured patterns in the code.
        """
        # Simple measure: repetition patterns
        if len(self.code) < 2:
            return 0

        coherence = 0
        for i in range(1, len(self.code)):
            # Check similarity with previous ByteWord
            prev = self.code[i-1]._value
            curr = self.code[i]._value
            # XOR distance (lower means more similar)
            distance = bin(prev ^ curr).count('1')
            # Convert to similarity (0-8 scale)
            similarity = 8 - distance
            coherence += similarity / 8

        # Normalize
        return coherence / (len(self.code) - 1)

    def get_computational_order_parameter(self) -> float:
        """
        Calculate the computational order parameter Φ_QSD = Coherence/Entropy

        This distinguishes between:
        - Disordered, local Markovian regimes (|Φ| → 0)
        - Ordered, global Non-Markovian regimes (|Φ| → ∞)
        """
        if self.entropy == 0:
            return float('inf')  # Prevent division by zero
        return self.coherence / self.entropy

    def step(self):
        """Advance the quine by one time step"""
        new_code = []

        # Get history context for non-Markovian behavior
        history_context = self._get_history_context()

        for i, word in enumerate(self.code):
            # Normal Markovian evolution
            evolved = word.propagate(1)[-1]

            # Apply non-Markovian effects based on history
            if history_context and random.random() < 0.3:  # 30% chance of non-Markovian action
                # Find a similar past state to influence the current one
                past_influence = self._find_past_influence(
                    word, history_context)
                if past_influence:
                    # Compose with the past influence
                    evolved = evolved.compose(past_influence)

            # Apply noise/thermodynamic fluctuations
            if random.random() < self.noise_level:
                # Random mutation
                evolved = ByteWord(evolved._value ^ (
                    1 << random.randint(0, 7)))

            new_code.append(evolved)

        # Save previous state to memory
        self.memory.append(self.code.copy())

        # Update code
        self.code = new_code

        # Record the morphism
        self.morphism_history.append("step")

        # Update properties
        self.entropy = self._calculate_entropy()
        self.coherence = self._calculate_coherence()
        self.age += 1

    def _get_history_context(self) -> List[ByteWord]:
        """Get relevant history for non-Markovian behavior"""
        if not self.memory or len(self.memory) <= 1:
            return []

        # Simple approach: return the most recent past state
        return self.memory[-2]

    def _find_past_influence(self, word: ByteWord, context: List[ByteWord]) -> Optional[ByteWord]:
        """Find a past ByteWord that could influence the current one"""
        if not context:
            return None

        # Find the ByteWord in context that's most "compatible"
        # Based on type-value matching
        best_match = None
        best_score = -1

        for past_word in context:
            # Score based on complementary types and values
            score = bin(word.types & past_word.values).count('1') + \
                bin(word.values & past_word.types).count('1')

            if score > best_score:
                best_score = score
                best_match = past_word

        # Only return if there's a meaningful match
        if best_score > 0:
            return best_match
        return None

    def reproduce(self, mutation_rate: float = None) -> 'ThermodynamicQuine':
        """
        Create a copy of this quine with possible mutations.
        This is the "quining" operation.

        Args:
            mutation_rate: Override default noise level for reproduction

        Returns:
            A new ThermodynamicQuine instance
        """
        if mutation_rate is None:
            mutation_rate = self.noise_level

        # Copy code sequence with potential mutations
        new_code = []
        for word in self.code:
            if random.random() < mutation_rate:
                # Apply mutation
                mutated_value = word._value ^ (1 << random.randint(0, 7))
                new_code.append(ByteWord(mutated_value))
            else:
                # Exact copy
                new_code.append(ByteWord(word._value))

        # Create offspring
        offspring = ThermodynamicQuine(
            code_sequence=new_code,
            memory_capacity=self.memory.maxlen,
            noise_level=self.noise_level
        )

        # Establish lineage connection
        offspring.lineage = self.lineage.union({id(self)})

        # Create entanglement link with parent
        offspring.entanglement_links[id(self)] = 1.0  # Strong link to parent

        # Record the morphism
        self.morphism_history.append("reproduce")

        return offspring

    def merge(self, other: 'ThermodynamicQuine') -> 'ThermodynamicQuine':
        """
        Merge this quine with another quine, creating a new offspring
        that inherits from both parents

        Args:
            other: Another ThermodynamicQuine to merge with

        Returns:
            A new ThermodynamicQuine instance
        """
        # Ensure both quines have code
        if not self.code or not other.code:
            raise ValueError("Cannot merge quines with empty code sequences")

        # Crossover operation
        new_code = []
        min_len = min(len(self.code), len(other.code))
        crossover_point = random.randint(1, min_len - 1)

        # Take first part from self
        for i in range(crossover_point):
            new_code.append(ByteWord(self.code[i]._value))

        # Take second part from other
        for i in range(crossover_point, min_len):
            new_code.append(ByteWord(other.code[i]._value))

        # Apply some composition operations to create novel behavior
        for i in range(min(len(new_code), 3)):  # Apply to up to 3 random positions
            pos = random.randint(0, len(new_code) - 1)
            # Compose with a random word from either parent
            parent_word = random.choice(self.code + other.code)
            new_code[pos] = new_code[pos].compose(parent_word)

        # Create offspring with merged code
        offspring = ThermodynamicQuine(
            code_sequence=new_code,
            memory_capacity=max(self.memory.maxlen, other.memory.maxlen),
            noise_level=(self.noise_level + other.noise_level) / 2
        )

        # Establish lineage connection with both parents
        offspring.lineage = self.lineage.union(
            other.lineage).union({id(self), id(other)})

        # Create entanglement links with both parents
        # Strong link to first parent
        offspring.entanglement_links[id(self)] = 0.8
        # Strong link to second parent
        offspring.entanglement_links[id(other)] = 0.8

        # Record the morphism
        self.morphism_history.append("merge")
        other.morphism_history.append("merge")

        return offspring

    def is_markovian(self) -> bool:
        """
        Determine if this quine exhibits primarily Markovian behavior.
        Based on the computational order parameter.
        """
        order_parameter = self.get_computational_order_parameter()
        # Threshold for Markovian vs. Non-Markovian behavior
        return order_parameter < 0.5  # |Φ| → 0 indicates Markovian behavior

    def __repr__(self) -> str:
        """String representation of the quine"""
        order = self.get_computational_order_parameter()
        behavior = "Markovian" if self.is_markovian() else "Non-Markovian"
        return (f"ThermodynamicQuine(len={len(self.code)}, "
                f"age={self.age}, entropy={self.entropy:.2f}, "
                f"coherence={self.coherence:.2f}, Φ={order:.2f}, "
                f"behavior={behavior})")


class ThermoQuineEcosystem:
    """
    A system for evolving ThermodynamicQuines through selection and reproduction,
    simulating digital epigenetics.
    """

    def __init__(self,
                 initial_population_size: int = 20,
                 max_population_size: int = 100,
                 base_mutation_rate: float = 0.1,
                 selection_pressure: float = 0.7):
        """
        Initialize the ecosystem.

        Args:
            initial_population_size: Number of quines to start with
            max_population_size: Maximum population size
            base_mutation_rate: Base mutation rate for reproduction
            selection_pressure: Strength of selection (0-1)
        """
        self.population = []
        self.max_population = max_population_size
        self.base_mutation_rate = base_mutation_rate
        self.selection_pressure = selection_pressure
        self.generation = 0
        self.fitness_history = []
        self.species_map = {}  # Track different "species" of quines

        # Create initial population
        for _ in range(initial_population_size):
            quine = ThermodynamicQuine(
                noise_level=base_mutation_rate * random.uniform(0.5, 1.5)
            )
            self.population.append(quine)

        # Initialize species tracking
        self._update_species_map()

    def _update_species_map(self):
        """Update the species map based on quine similarity"""
        self.species_map = {}

        for quine in self.population:
            # Use order parameter as a key characteristic
            order = quine.get_computational_order_parameter()
            # Discretize into species
            species_key = round(order * 2) / 2  # Round to nearest 0.5

            if species_key in self.species_map:
                self.species_map[species_key].append(quine)
            else:
                self.species_map[species_key] = [quine]

    def evaluate_fitness(self, fitness_function: Callable[[ThermodynamicQuine], float] = None):
        """
        Evaluate fitness of all quines in the population.

        Args:
            fitness_function: Custom fitness function or None for default
        """
        if fitness_function is None:
            # Default fitness function: reward non-Markovian behavior and higher coherence
            def fitness_function(q): return (
                # Reward non-Markovian (0 or 3)
                (1.0 - float(q.is_markovian())) * 3.0 +
                # Reward coherence (0-2)
                q.coherence * 2.0 +
                # Moderate entropy (0-1)
                min(q.entropy, 1.0) * 1.0
            )

        # Calculate fitness for each quine
        for quine in self.population:
            quine.fitness_score = fitness_function(quine)

        # Keep track of average fitness
        avg_fitness = sum(
            q.fitness_score for q in self.population) / len(self.population)
        self.fitness_history.append(avg_fitness)

    def select_parents(self, n: int = 2) -> List[ThermodynamicQuine]:
        """
        Select n parents using tournament selection.

        Args:
            n: Number of parents to select

        Returns:
            List of selected parent quines
        """
        parents = []

        for _ in range(n):
            # Tournament selection
            tournament_size = max(2, int(len(self.population) * 0.2))
            candidates = random.sample(self.population, tournament_size)

            # Select best candidate with probability based on selection pressure
            candidates.sort(key=lambda q: q.fitness_score, reverse=True)

            # Apply selection pressure
            if random.random() < self.selection_pressure:
                # Take the best
                parents.append(candidates[0])
            else:
                # Take a random one
                parents.append(random.choice(candidates))

        return parents

    def reproduce(self):
        """
        Create new generation through reproduction.
        """
        # Ensure we have a population to reproduce
        if len(self.population) < 2:
            return

        new_population = []

        # Keep some of the best quines (elitism)
        elitism_count = max(1, int(len(self.population) * 0.1))
        elites = sorted(self.population, key=lambda q: q.fitness_score, reverse=True)[
            :elitism_count]
        new_population.extend(elites)

        # Fill the rest with offspring
        while len(new_population) < self.max_population:
            # Select reproduction method
            if random.random() < 0.7:  # 70% sexual reproduction (merge)
                parents = self.select_parents(2)
                offspring = parents[0].merge(parents[1])
            else:  # 30% asexual reproduction
                parent = self.select_parents(1)[0]
                # Dynamic mutation rate based on population diversity
                mutation_rate = self._calculate_adaptive_mutation_rate()
                offspring = parent.reproduce(mutation_rate=mutation_rate)

            new_population.append(offspring)

            # Stop if we reach max population
            if len(new_population) >= self.max_population:
                break

        # Replace population
        self.population = new_population
        self.generation += 1

        # Update species tracking
        self._update_species_map()

    def _calculate_adaptive_mutation_rate(self) -> float:
        """
        Calculate an adaptive mutation rate based on population diversity.
        Lower diversity -> higher mutation to encourage exploration.
        """
        # Measure diversity using average pairwise difference in order parameters
        if len(self.population) < 2:
            return self.base_mutation_rate

        order_parameters = [q.get_computational_order_parameter()
                            for q in self.population]

        # Calculate variance
        mean_order = sum(order_parameters) / len(order_parameters)
        variance = sum((x - mean_order) **
                       2 for x in order_parameters) / len(order_parameters)

        # Normalize to a reasonable range
        diversity = min(1.0, math.sqrt(variance) * 2)

        # Adjust mutation rate: higher when diversity is low
        adjusted_rate = self.base_mutation_rate * (1.5 - diversity)

        return max(0.01, min(0.5, adjusted_rate))  # Keep between 1% and 50%

    def run_generation(self, fitness_function: Callable = None):
        """
        Run a single generation cycle.

        Args:
            fitness_function: Custom fitness function or None for default
        """
        # Step 1: Let quines evolve individually
        for quine in self.population:
            steps = random.randint(1, 3)  # Random number of steps
            for _ in range(steps):
                quine.step()

        # Step 2: Evaluate fitness
        self.evaluate_fitness(fitness_function)

        # Step 3: Reproduce
        self.reproduce()

    def run_simulation(self, generations: int, fitness_function: Callable = None) -> Dict:
        """
        Run simulation for specified number of generations.

        Args:
            generations: Number of generations to run
            fitness_function: Custom fitness function or None for default

        Returns:
            Dictionary with simulation results
        """
        results = {
            "generations": [],
            "avg_fitness": [],
            "max_fitness": [],
            "species_count": [],
            "markovian_ratio": []
        }

        for _ in range(generations):
            self.run_generation(fitness_function)

            # Record metrics
            results["generations"].append(self.generation)
            results["avg_fitness"].append(
                sum(q.fitness_score for q in self.population) /
                len(self.population)
            )
            results["max_fitness"].append(
                max(q.fitness_score for q in self.population)
            )
            results["species_count"].append(len(self.species_map))
            results["markovian_ratio"].append(
                sum(1 for q in self.population if q.is_markovian()) /
                len(self.population)
            )

        return results

    def get_best_quine(self) -> ThermodynamicQuine:
        """Get the quine with highest fitness score"""
        if not self.population:
            return None
        return max(self.population, key=lambda q: q.fitness_score)

    def get_species_statistics(self) -> Dict:
        """Get statistics about species in the ecosystem"""
        stats = {
            "species_count": len(self.species_map),
            "species_sizes": {k: len(v) for k, v in self.species_map.items()},
            "markovian_count": sum(1 for q in self.population if q.is_markovian()),
            "non_markovian_count": sum(1 for q in self.population if not q.is_markovian())
        }
        return stats

    def __repr__(self) -> str:
        """String representation of the ecosystem"""
        species_count = len(self.species_map)
        avg_fitness = (sum(q.fitness_score for q in self.population) / len(self.population)
                       if self.population else 0)

        return (f"ThermoQuineEcosystem(population={len(self.population)}, "
                f"generation={self.generation}, species={species_count}, "
                f"avg_fitness={avg_fitness:.2f})")


# Example usage
def run_thermo_quine_experiment():
    """Run an example experiment with thermodynamic quines"""
    print("Initializing ThermoQuine Ecosystem...")
    ecosystem = ThermoQuineEcosystem(
        initial_population_size=20,
        max_population_size=50,
        base_mutation_rate=0.15,
        selection_pressure=0.8
    )

    print("Running simulation for 50 generations...")
    results = ecosystem.run_simulation(generations=50)

    print(f"Final ecosystem state: {ecosystem}")
    print(f"Species statistics: {ecosystem.get_species_statistics()}")

    best_quine = ecosystem.get_best_quine()
    print(f"Best quine found: {best_quine}")
    print(
        f"Best quine order parameter: {best_quine.get_computational_order_parameter():.3f}")
    print(f"Is best quine Markovian? {best_quine.is_markovian()}")

    # Print evolution of key metrics
    print("\nEvolution of key metrics:")
    print(f"Generation\tAvg Fitness\tMax Fitness\tSpecies Count\tMarkovian Ratio")
    # Print every 5th generation
    for i in range(0, len(results["generations"]), 5):
        print(f"{results['generations'][i]}\t\t{results['avg_fitness'][i]:.2f}\t\t"
              f"{results['max_fitness'][i]:.2f}\t\t{results['species_count'][i]}\t\t"
              f"{results['markovian_ratio'][i]:.2f}")

    return ecosystem, results


if __name__ == "__main__":
    run_thermo_quine_experiment()


def specialized_fitness_function(quine):
    """
    Custom fitness function that rewards specific behaviors
    you might be looking for in your thermo-quines
    """
    # Reward non-Markovian behavior with high coherence
    nm_bonus = 0 if quine.is_markovian() else 3.0

    # Reward specific pattern capabilities
    # (e.g., ability to handle "z-coordinate shifts" as mentioned in your notes)
    z_shift_capability = test_z_shift_handling(quine)

    # Reward computational stability
    stability = measure_computational_stability(quine)

    return nm_bonus + quine.coherence * 2.0 + z_shift_capability + stability
