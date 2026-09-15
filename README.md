# AutoWannier

> Physics-aware autonomous construction and validation of Wannier tight-binding models.

AutoWannier is a research project exploring how to select, construct, and validate effective electronic models from first-principles electronic-structure information. Its intended role is a **decision + validation + optimization + diagnosis layer** above Wannier90.

**Status: Concept / pre-alpha research project.** This README defines scientific scope and a proposed development path. All software capabilities described below are planned unless explicitly stated otherwise; no autonomous AI Wannierization system is claimed to exist yet.

The repository also contains [materials-symmetry](materials-symmetry/README.md), a runnable
package for ordinary, magnetic, and spin-space symmetry analysis. It has its own installation
instructions, POSCAR examples, and Markdown report skill. The pre-alpha status above refers to
AutoWannier.

## Motivation

Turning a first-principles calculation into an effective tight-binding (TB) Hamiltonian requires substantial scientific judgment. A researcher must choose the target energy range and low-energy degrees of freedom, select Wannier projections and `num_wann`, and set outer disentanglement and frozen windows. They must decide whether ligand orbitals are necessary, check orbital character and symmetry, inspect spin–orbit coupling (SOC) splittings and band crossings, and diagnose failures before adjusting the setup.

Wannier90 provides the numerical machinery for constructing localized Wannier functions from a specified setup. AutoWannier asks how the setup should be chosen and how the resulting model should be judged:

> How can a machine determine a physically meaningful effective subspace?
>
> Can Wannier tight-binding construction become an autonomous, self-validating and self-correcting scientific workflow?

A reproducible answer would help make effective-model construction more systematic, expose the reasons for failed models, and reduce repeated manual decisions across materials. Autonomy remains a research target, not an established capability.

Existing automated Wannierization methods and workflow tools are part of the starting point. For example, Wannier90 already documents SCDM and projectability-based approaches in its [official tutorials](https://wannier90.readthedocs.io/en/latest/user_guide/wannier90/files/). AutoWannier should build on and compare against existing methods and reuse workflow infrastructure where appropriate. Its proposed research focus is the connection between target physics, subspace selection, validation, and corrective decisions; no novelty or superiority over existing workflows is claimed here.

## Scientific Objective

> Can an automated system construct a minimal, physically faithful Wannier tight-binding model from first-principles electronic-structure information, validate it against the parent calculation, diagnose failures, and improve the model with minimal human intervention?

“Minimal” must be defined relative to specified observables, an energy range, and accuracy tolerances. It does not mean selecting the smallest basis regardless of lost physics. Fidelity to a parent calculation also does not establish the accuracy of that calculation relative to experiment.

### Effective degrees of freedom

The central modeling question is:

> Which electronic degrees of freedom are necessary and sufficient for the target physics?

For a transition-metal compound, candidate descriptions might include:

```text
transition-metal d
transition-metal d + ligand p
a smaller {dxy, dxz, dyz} low-energy subspace
```

These are candidate representations, not universal prescriptions. Hybridization, spin structure, symmetry, and the intended observables should inform their comparison. This connects parameter tuning to effective-model construction: choosing a representation of electronic structure within a low-energy Hilbert space, including effective or emergent degrees of freedom that need not correspond to pure atomic orbitals.

### Beyond band fitting

“Physically faithful” means more than a small band-energy error. A possible future objective is

$$
\mathcal L =
\lambda_E\mathcal L_{\mathrm{band}}
+\lambda_P\mathcal L_{\mathrm{subspace}}
+\lambda_\Omega\mathcal L_{\mathrm{spread}}
+\lambda_S\mathcal L_{\mathrm{symmetry}}
+\lambda_L\mathcal L_{\mathrm{locality}}
+\lambda_{\mathrm{phys}}\mathcal L_{\mathrm{physics}}.
$$

The terms would assess energies, subspace fidelity, Wannier spreads, symmetry, real-space locality, and target physical observables. **This is a research framework, not an implemented or finalized loss function.** Definitions, units, normalization, weights, and acceptance thresholds remain open. Some requirements may be hard constraints rather than weighted penalties; model size and fidelity may require a multi-objective comparison.

## Concept

The proposed workflow begins with a scientific target and electronic-structure evidence. A crystal structure alone would first require a suitable electronic-structure calculation.

```text
Crystal structure / electronic structure + target physics
                         |
                         v
             Electronic-structure analysis
                         |
                         v
             Effective-subspace proposal <--------------+
                         |                              |
                         v                              |
              Wannier input construction <---------+   |
                         |                         |   |
                         v                         |   |
                     Wannier90                     |   |
                         |                         |   |
                         v                         |   |
              Tight-binding Hamiltonian            |   |
                         |                         |   |
                         v                         |   |
                 Physics validation                |   |
                         |                         |   |
                 +-------+-------+                 |   |
                 |               |                 |   |
                PASS            FAIL               |   |
                 |               |                 |   |
                 v               v                 |   |
        Model + report        Diagnosis            |   |
                                 |                 |   |
                                 v                 |   |
                      Parameter / subspace update--+---+
```

PASS would mean meeting declared criteria within a stated validation domain, not universal physical correctness. Retries should have explicit budgets and stopping rules; unresolved failures should return evidence and uncertainty rather than an unjustified successful model.

AutoWannier aims to become a framework for:

- Automated Wannier input construction and TB Hamiltonian extraction.
- DFT/Wannier band comparison and real-space Hamiltonian analysis.
- Localization, spread, orbital/subspace fidelity, and symmetry-aware validation.
- Automated parameter optimization, failure diagnosis, and self-correcting workflows.
- Eventually, physics-aware ML/AI decision making.

### Future user experience — FUTURE VISION

```text
Target:
Construct a minimal Wannier TB model within ±2 eV of EF.

AutoWannier:
1. analyzes orbital-resolved electronic structure;
2. proposes a candidate low-energy subspace;
3. constructs Wannier90 inputs;
4. performs Wannierization;
5. reconstructs the TB band structure;
6. evaluates physical fidelity;
7. diagnoses discrepancies;
8. updates the model;
9. returns the final Hamiltonian and validation report.
```

**This is a research target, not the current implemented interface.** A real request would also need target observables, tolerances, and an explicit energy-reference convention.

## What AutoWannier Is NOT

AutoWannier is not:

- A replacement for Wannier90.
- A replacement for Quantum ESPRESSO, VASP, or other DFT packages.
- An LLM wrapper around shell commands.
- A generic materials chatbot.
- A black-box model that simply predicts `.win` files.
- Currently a production-ready high-throughput package.

> The scientific objective is not to teach an LLM how to write Wannier90 syntax.
> The objective is to investigate automated identification and validation of effective electronic degrees of freedom.

## Validation Philosophy

Visual agreement between band plots is useful evidence, but insufficient validation. The planned validation framework has three levels; **none of the validators below is claimed to be implemented**.

| Level | Planned checks | Intended interpretation |
| --- | --- | --- |
| Numerical correctness | Wannier convergence; Hamiltonian Hermiticity; Fourier reconstruction consistency; hopping decay; numerical stability | Establish internal consistency and characterize localization and numerical sensitivity. |
| Electronic-structure fidelity | Eigenvalue errors; target energy-window accuracy; crossings and degeneracies; subspace/projector similarity; orbital character | Test whether the selected representation retains the relevant parent electronic structure. |
| Physical fidelity — longer-term | Crystal, time-reversal, and inversion symmetry where applicable; spin structure; SOC splitting; Berry quantities; Fermi surfaces; topology | Test the symmetries and observables required by the scientific target. |

Comparisons should use consistent energy references, coordinates, spin conventions, and sampling, including validation k-points beyond a fitted band path. Near crossings and degeneracies, sorted eigenvalues alone cannot establish state or subspace fidelity. Gauge-dependent orbital labels and matrix elements need an explicit comparison convention; projector comparisons require compatible underlying spaces.

Only symmetries present in the parent system should be imposed. Some targets may not admit a localized representation with every requested symmetry in the chosen subspace; diagnosis should distinguish such limitations from numerical failure.

`seedname_hr.dat` alone is not sufficient for every proposed check. Orbital/subspace validation needs additional wavefunction or projection information, and Berry-related observables may need position or other operator matrix elements and gauge information. Missing evidence should be reported as unassessed, not treated as a passed check.

### Mathematical convention

The intended real-space representation is

$$
H_{mn}(\mathbf R)=\langle 0m|\hat H|\mathbf R n\rangle,
$$

with the lattice Fourier convention

$$
H_{mn}(\mathbf k)=\sum_{\mathbf R}H_{mn}(\mathbf R)e^{i\mathbf k\cdot\mathbf R}.
$$

Here, $m,n$ label Wannier basis states and $\mathbf R$ is a lattice translation. AutoWannier plans to build its initial TB representation and validation infrastructure around `seedname_hr.dat`. Its file representation includes Wigner–Seitz degeneracy information that must be handled in reconstruction; the equation above is not a prescription to sum raw file entries without their weights. See the [Wannier90 file specification](https://wannier90.readthedocs.io/en/latest/user_guide/wannier90/files/#seedname_hrdat).

Detailed conventions for units, reciprocal coordinates, basis phases, orbital ordering, spinors, and interpolation options belong in future formal documentation.

## Planned Architecture

**Conceptual architecture only: the following modules and interfaces do not describe an existing package tree.**

```text
autowannier
|
+-- dft
|   +-- interfaces
|   +-- parsers
+-- wannier
|   +-- input builder
|   +-- runner
|   +-- output parser
+-- tb
|   +-- Hamiltonian
|   +-- interpolation
+-- validation
|   +-- bands
|   +-- subspace
|   +-- symmetry
|   +-- locality
+-- optimization
+-- diagnosis
+-- agent
+-- execution
    +-- local
    +-- HPC
```

The physics engine and decision layer must remain decoupled. The longer-term system would separate responsibilities as follows; arrows indicate coordination, while the earlier workflow shows data flow.

```text
                         AutoWannier
                              |
             +----------------+----------------+
             |                                 |
             v                                 v
   Physics / Numerical Layer             Decision Layer
             |                         optimizer / ML / agent
             |                                 |
             +----------------+----------------+
                              |
                              v
                       Wannier Workflow
                              |
                 +------------+------------+
                 |                         |
                 v                         v
       Quantum ESPRESSO / DFT          Wannier90
```

> AI should propose scientific decisions; deterministic physics software should perform the electronic-structure calculations; physics-based validators should judge the result.

The physics and validation layers should work independently of AI. A decision policy would consume structured evidence and propose changes; it would not replace the numerical solvers or decide success without validation.

### Execution model

```text
             AutoWannier
                  |
          ExecutionBackend
          /              \
         v                v
       Local             HPC
    Linux / WSL        Slurm
```

Local Linux or WSL is the planned setting for development, testing, and Wannier/TB analysis, with suitably sized baseline calculations run locally. A future HPC backend would handle larger DFT jobs and high-throughput workloads. Access to a supercomputer is not a conceptual requirement. Neither backend is implemented.

## Roadmap

Phases describe research milestones, not released features or delivery dates. **Phase 0 is current; Phases 1–7 are planned.**

### Phase 0 — Foundations

Define scientific scope, establish the conceptual software architecture, specify physical conventions, and formulate validation criteria. Establishing a reproducible local development environment is a remaining foundation task, not a completed setup. The present contribution is the README design; no baseline result is claimed.

### Phase 1 — Single-System Baseline: Silicon

Build a deterministic, reproducible end-to-end baseline:

```text
Si
 |
 v
Quantum ESPRESSO
 |
 v
pw2wannier90
 |
 v
Wannier90
 |
 v
seedname_hr.dat
 |
 v
Python TB reconstruction
 |
 v
DFT/Wannier validation
```

This is a conceptual sequence, not a complete command recipe. The milestone is agreement between independent TB reconstruction, Wannier interpolation, and the parent bands under documented conventions and tolerances, accompanied by reproducible inputs and provenance.

Silicon is **a controlled benchmark for developing and validating the computational infrastructure**, not the final research subject. It provides a bounded starting point before transition-metal, magnetic, SOC, and more complex entangled electronic structures. The objective of this phase is a deterministic baseline; AI is deferred.

### Phase 2 — Wannier Quality Landscape

Systematically investigate

$$
\mathcal L=\mathcal L(P,E_{\mathrm{outer}},E_{\mathrm{frozen}},N_W,\ldots),
$$

where $P$ is the projection choice, $E_{\mathrm{outer}}$ and $E_{\mathrm{frozen}}$ denote the outer and frozen energy-window bounds, and $N_W$ is the Wannier subspace dimension. The goal is to understand the construction parameter space, admissible setups, failure regions, and tradeoffs between fidelity and model complexity.

### Phase 3 — Automated Optimization

Compare grid/random search, Bayesian optimization, and other suitable algorithms for

$$
\theta^*=\arg\min_{\theta\in\Theta_{\mathrm{admissible}}}\mathcal L(\theta).
$$

Optimization should respect window and subspace constraints, use declared evaluation budgets, and retain individual validation metrics. This phase does not require an LLM.

### Phase 4 — Physics-Aware Diagnosis

Move from reporting `FAILED` to investigating why: an unsuitable projection manifold, insufficient orbital basis, poor disentanglement windows, missing ligand orbitals, symmetry inconsistency, or SOC-related issues. These are hypotheses to test, not causes identifiable from every failed run.

```text
diagnosis -> parameter modification -> rerun -> validation
```

Record the evidence for each hypothesis and whether the proposed correction improves the relevant metrics.

### Phase 5 — AI-Assisted Decision Making

After establishing a reliable physics engine and validators, investigate ML predictors, graph neural networks (GNNs), learned parameter priors, LLM-based planning/diagnosis, and scientific agents. Compare their decisions with deterministic and conventional optimization baselines. AI is a later decision layer, not the foundation of the project.

### Phase 6 — Magnetism and Spin–Orbit Coupling

Introduce more demanding benchmarks such as **bcc Fe**. Study spin polarization, SOC, magnetic Wannier models, spinor Hamiltonians, band crossings, and anomalous Hall/Berry-related quantities. This phase expands physical conventions and validation evidence; it does not claim current support for Fe or spinor calculations.

### Phase 7 — High Throughput and HPC

Extend a validated single-system workflow to Slurm/HPC execution and many-material studies:

```text
many materials -> automated DFT -> automated Wannierization
               -> validation -> dataset -> learned decision models
```

Scaling should retain failure records, provenance, and per-model validation reports, rather than count every completed job as a valid model.

## Research Questions

| Direction | Open question |
| --- | --- |
| Effective subspace discovery | Can electronic-structure information be used to infer the appropriate Wannier subspace automatically? |
| Gauge-aware comparison | How should effective Hamiltonians or subspaces be compared when gauge freedom is present? |
| Physics-aware objectives | What constitutes a good effective Hamiltonian beyond band-energy RMSE? |
| Automated diagnosis | Can common Wannierization failures be mapped to interpretable physical causes? |
| Transferability | Can experience from previously Wannierized materials improve decisions for unseen materials? |

These are potential research directions, not demonstrated findings or promises of publication.

## Current Status

**Status: Concept / pre-alpha research project.**

The project is currently in the design and baseline-validation stage. Here, baseline validation is being specified; a completed baseline is not claimed. No autonomous AI Wannierization system is claimed to exist yet.

| Category | Scope and maturity |
| --- | --- |
| Current scope | README-level scientific definition, conceptual architecture, validation philosophy, and staged research roadmap. |
| Planned capability | Deterministic Si baseline, input construction, parsing and TB reconstruction, quantitative validators, parameter studies, optimization, and diagnosis. None is claimed implemented. |
| Long-term research vision | Effective-subspace discovery, AI-assisted decisions, magnetic/SOC validation, transferable policies, and validated high-throughput HPC workflows. |

There is no claimed runnable AutoWannier package, stable API, installation procedure, supported-material list, benchmark result, performance measurement, or AI accuracy result. Si and bcc Fe are proposed benchmarks. This README is a design document, not a user manual for functioning software.

## External Physics Software

The initial integration plan centers on:

- [Quantum ESPRESSO](https://www.quantum-espresso.org/) for first-principles electronic-structure calculations, with `pw2wannier90` as the planned interface in the Si baseline.
- [Wannier90](https://wannier90.readthedocs.io/en/latest/) for Wannierization and the associated Hamiltonian output.

Other DFT backends may be considered later; no such integration is currently claimed.

**AutoWannier does not vendor or redistribute these electronic-structure packages.** They retain their own licenses, installation requirements, and citation policies. Version compatibility and environment specifications will be defined during baseline development; no automated installation scheme is provided here.

## Development and Reproducibility Philosophy

Development should prioritize explicit conventions, reproducible calculations, machine-readable outputs, provenance tracking, transparent decisions, and reproducible validation metrics.

Future run records should identify structures, pseudopotentials, software versions, input settings, energy references, sampling, and validation definitions. Each parameter change should link to its hypothesis, parent run, resulting model, and comparison report. Stochastic searches should record seeds and budgets where applicable.

Every automated decision should make it possible to answer:

```text
What changed?
Why was it changed?
Did the result improve?
Which physical metric improved?
```

Progress should proceed from a reproducible numerical baseline to validated optimization and only then to learned decisions. Negative results and unresolved failures are part of the scientific record.

## License / Citation

This repository is licensed under the [MIT License](LICENSE).

No AutoWannier paper or DOI is claimed at this stage. A formal project citation will be added when an appropriate research artifact exists. Research using external physics software should follow the citation guidance of the packages and methods actually used.
