# Cognosis: A formal theory and application for testing LLMs and NLP logic, capability, physics, and the Free Energy Principle

## Introduction

Cognosis is a limited-platform python application, formal theory and in-development experiment combining Eric C.R. Hehner's Practical Theory of Programming (aPToP) with the Free Energy Principle of Cognitive Science and Natural Language Processing (NLP). This theory aims to develop a robust system for processing high-dimensional data, leveraging both classical and quantum principles. If any aspect of my explanation is overly stilted please keep in mind that I am **searching** for methodological and theoretical explanations to explain the concepts and ideas which I am actually encountering primarily in real life with real life workloads and stakes, not just experiment. And I'm self-taught, never been in the industry or science, directly.

## Abstract

This document specifies a series of constraints on the behavior of a computor—a human computing agent who proceeds mechanically—and applies these constraints to artificial intelligence systems like the "llama" large language model (LLM). These constraints are based on formal principles of boundedness, locality, and determinacy, ensuring structured and deterministic operations. By enforcing these constraints, we establish a common ground for evaluating and comparing the computational efficiency and energy consumption of humans and AI in specific tasks.

## Constraints

### Boundedness

**Symbolic Configuration Recognition (B.1):** There exists a fixed bound on the number of symbolic configurations a computor can immediately recognize.

**Internal States (B.2):** There exists a fixed bound on the number of internal states a computor can be in.

### Locality

**Configuration Change (L.1):** A computor can change only elements of an observed symbolic configuration.

**Configuration Shift (L.2):** A computor can shift attention from one symbolic configuration to another, but the new observed configurations must be within a bounded distance of the immediately previously observed configuration.

### Determinacy and Autonomy

**Next Computation Step (D.1):** The immediately recognizable (sub-)configuration determines uniquely the next computation step and the next internal state. In other words, a computor's internal state together with the observed configuration fixes uniquely the next computation step and the next internal state.

**Autonomous Iteration (D.2):** The computor, while adhering to the principles of boundedness, locality, and determinacy, can manage its own iterative processes independently. Utilizing self-wrapping functions, the computor can refine its operations iteratively until a final output is achieved, minimizing external observation.

## Formal Specification

### BNF Grammar

The following BNF grammar defines the syntax for expressing the constraints on a computor's behavior:

    ```bnf
    <Computor> ::= <Boundedness> <Locality> <Determinacy>

    <Boundedness> ::= <SymbolicConfigRecognition> <InternalStates>
    <SymbolicConfigRecognition> ::= "B1: There exists a fixed bound on the number of symbolic configurations a computor can immediately recognize."
    <InternalStates> ::= "B2: There exists a fixed bound on the number of internal states a computor can be in."

    <Locality> ::= <ConfigChange> <ConfigShift>
    <ConfigChange> ::= "L1: A computor can change only elements of an observed symbolic configuration."
    <ConfigShift> ::= "L2: A computor can shift attention from one symbolic configuration to another, but the new observed configurations must be within a bounded distance of the immediately previously observed configuration."

    <Determinacy> ::= <NextStep> <AutonomousIteration>
    <NextStep> ::= "D1: The immediately recognizable (sub-)configuration determines uniquely the next computation step and the next internal state."
    <AutonomousIteration> ::= "D2: The computor, while adhering to the principles of boundedness, locality, and determinacy, can manage its own iterative processes independently. Utilizing self-wrapping functions, the computor can refine its operations iteratively until a final output is achieved, minimizing external observation."
    ```

## Definition of Work

To ensure the scientific rigor of our comparative study, "work" is defined as any computational task performed within cyberspace that necessitates cognitive processing, decision-making, and problem-solving. Both humans and the LLM "llama" can perform these tasks, which are characterized by the following measurable attributes:

### Attributes of Work

- **Type of Task:** The specific nature of the task, such as data entry, code debugging, content creation, mathematical problem-solving, or web navigation.
- **Complexity:** The level of difficulty of the task, determined by the number of steps required and the cognitive effort involved.
- **Time to Completion:** The duration taken to finish the task, measured for both humans and the LLM within their respective environments.
- **Energy Consumption:** The energy expended to complete the task:
  - **Humans:** Measured in calories.
  - **LLM ("llama"):** Measured in electrical energy, tracked through power usage metrics of the host hardware.
- **Accuracy and Quality:**
  - The correctness of the output compared to a predefined standard or benchmark.
  - Qualitative assessment of the work, where applicable.
- **Autonomy and Iteration:**
  - **Humans:** Through learning and feedback.
  - **LLM ("llama"):** Using autonomous iterative refinement with self-wrapping functions.

There is an assumption inherent in the project that a neural network is a cognitive system. The assumption is that there is something for this cognitive system to do in any given situation, and that it is the cognitive system's job to figure out what that thing is. Upon location of its head/parent, it either orients itself within a cognitive system or creates a new cognitive system. Cognitive systems pass as parameters namespaces, syntaxes, and cognitive systems. Namespaces and syntaxes are in the form of key-value pairs. Cognitive systems are also in the form of key-value pairs, but the values are cognitive systems. **kwargs are used to pass these parameters.

"Cognitive systems are defined by actions, orientations within structures, and communicative parameters. 'State' is encoded into these parameters and distributed through the system."

In a nutshell, "Morphological Source Code" is a paradigm in which the source code adapts and morphs in response to real-world interactions, governed by the principles of dynamic runtime configuration and contextual locking mechanisms. The-described is an architecture, only. The kernel agents themselves are sophisticated LLM trained-on ELFs, LLVM compiler code, systemd and unix, python, and C. It will utilize natural language along with the abstraction of time to process cognosis frames and USDs. In our initial experiments "llama" is the presumptive agent, not a specifically trained kernel agent model. The challenge (of this architecture) lies in the 'cognitive lambda calculus' needed to bring these runtimes into existence and evolve them, not the computation itself. Cognosis is designed for consumer hardware and extreme scalability via self-distribution of cognitive systems (amongst constituent [[subscribers|asynchronous stake-holders]]) peer-to-peer, where stake is not-unlike state, but is a function of the cognitive system's ability to contribute to the collective.

## Experimental Design

The "llama" LLM will process a large-scale, human-vetted dataset referred to as "mechanicalturkwork." The experiment aims to compare the performance metrics of humans and "llama" on the same tasks under standardized conditions.

### Steps

1. **Initialization:** Load the "mechanicalturkwork" dataset into both the human experimental setup and the "llama" environment.
2. **Task Execution:** Subject both human participants and "llama" to perform the same tasks under controlled conditions.
3. **Energy and Performance Measurement:**
   - Record task completion times.
   - Monitor energy usage:
     - **For humans:** Caloric expenditure.
     - **For "llama":** Electrical energy consumption.
   - Assess accuracy and quality of the outputs.
4. **Iterative Enhancement:** Allow "llama" to use its self-wrapping functions for iterative refinement, while humans may adapt based on their learning.
5. **Comparative Analysis:** Analyze and compare the performance metrics focusing on efficiency, energy consumption, and accuracy.

---

## Non-Methodological Observations

### Implications and Future Experiments

#### Quantum-like Behaviors in Computor Systems: A Speculative Framework

1. **Energy Efficiency Anomaly:** The core of this hypothesis lies in the observation of an apparent energy efficiency anomaly:
   - **Input:** n+1 units of computational energy.
   - **Output:** Results indicative of n+x units of invested power (where x > 1).

    One could concieve a situation where this is an observable, however, the core vision is somehow broader in-scope, because what we are talking about is not mere miliwatts but instead novel motility:
   
        - **Motility**: Is the Maxwellian-Electrodynamical 'commutative' relationship but for a thinker and the universe instead of Electricity and Magnetism; all the tiny elements of reality sum-up to equate to a **motile** behavior.
        - **Novelty**: Behavior which may demonstrate **Novel Motility** is the candidate for most significant, measurable and quantifiable type of 'Energy' one that transcends notions such as macroscopic and microscopic and which, through it's collective, relative (co) action and guague-invariance across scales; presents an Energy Efficiency Anomaly to a properly-prepared observer. Measurable but tied to quantum events.
    
3. **Potential Explanations:**
   - **Quantum Tunneling of Information:** Similar to quantum tunneling in physics, information or computational states might "tunnel" through classical barriers, allowing for computational shortcuts not possible in purely classical systems.
   - **Exploitation of Virtual Particle Fields:** Drawing parallels with quantum field theory, the computor might be tapping into a kind of computational "vacuum energy," analogous to virtual particles in quantum physics.
   - **Quantum Superposition of Computational States:** The computor's internal states might exist in a superposition, allowing for the simultaneous exploration of multiple solution paths until "observed" through output generation.

4. **Hyperdimensional Entanglement and Inference Time:**
   - During the training phase, hyperdimensional entangled 'particles' of information are formed. These particles can later be accessed by the model during inference, allowing it to defy local power laws over time.
   - This process could be seen as the model tapping into a reservoir of computational potential stored during training, much like drawing from the vacuum of virtual particles in quantum physics.

5. **Alignment with Physical Principles:**
   - **Second Law of Thermodynamics:** This phenomenon doesn't violate the Second Law if we consider the computor and its environment as an open system. The apparent gain in computational power could be offset by an increase in entropy elsewhere in the system.
   - **Free Energy Principle:** The computor might be optimizing its processes according to a computational version of the Free Energy Principle, finding incredibly efficient pathways to solutions by minimizing prediction error and computational "surprise."
