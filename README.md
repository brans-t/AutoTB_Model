# altermag-symmetry

Research-grade symmetry analysis for collinear antiferromagnets and altermagnetic
candidates. The current 0.2 milestone reads POSCAR, CONTCAR, and ordinary CIF files,
combines them with explicit Cartesian magnetic moments, and produces both a readable
report and versioned JSON.

## What problem does this solve?

A crystallographic space-group label alone cannot decide whether opposite-spin
sublattices permit nonrelativistic momentum-dependent spin splitting. This package keeps
ordinary space-group symmetry, magnetic space-group symmetry, and spin-space symmetry
as separate result objects, maps sites explicitly, and reports the assumptions behind a
conservative candidate classification.

## Space group vs magnetic space group vs spin space group

- A space-group operation `{R | t}` acts on positions and ignores magnetic order.
- A magnetic operation augments `{R | t}` with an optional time reversal and treats
  moments as axial vectors.
- A spin-space operation `[S || {R | t}]` allows the Cartesian spin rotation `S` to be
  independent of the spatial action.

That distinction matters because an operation can exchange two sites while a separate
spin operation maps their opposite moments. See [the theory guide](docs/theory.md).

## Why altermagnets require spin-space symmetry

For a collinear compensated structure, the code finds spatial operations that connect
up and down sites, then associates matching spin-space operations. A candidate result
means only that the implemented preliminary symmetry checks passed. It is neither a
complete proof of a particular wave form nor a band-structure calculation.

## Installation

Python 3.11 or newer is required.

```bash
python -m venv .venv
.venv/bin/pip install -e '.[all,dev]'
```

Core dependencies are NumPy, spglib, and pymatgen. FindSpinGroup identifies the standard
oriented spin-space group (OSSG), while spinspg supplies explicit `[S || {R | t}]`
operations. These and amcheck are isolated behind adapters and available through the
`findspingroup`, `spin`, `amcheck`, and `all` extras. The project is Apache-2.0 licensed.
Dependency licenses remain the terms of their respective projects; the package does not
vendor those dependencies.

## Quick start

Atom indices in configuration files are always zero-based and refer to the unmodified
input order.

```bash
altermag analyze examples/POSCAR --config examples/magnetic_config.json
altermag analyze examples/POSCAR --config examples/magnetic_config.json --json result.json
altermag analyze examples/POSCAR --moments '0,0,1;0,0,-1'
```

## CLI examples

```bash
altermag symmetry examples/POSCAR --scan-symprec
altermag symmetry examples/POSCAR --symprec 1e-3 5e-3 1e-2 2e-2
altermag magnetic examples/POSCAR --config examples/magnetic_config.json
altermag spin-group examples/POSCAR --config examples/magnetic_config.json
altermag operations examples/POSCAR
```

`spin-group` and `analyze` use FindSpinGroup by default. Pass `--no-findspingroup` for
an operations-only run. The FindSpinGroup numerical controls are exposed as
`--fsg-eigenvalue-tol` and `--fsg-matrix-tol`; their values are recorded in JSON.

The tolerance scan reports every requested result and whether the group changes. It
never silently selects a larger tolerance.

## Python API

```python
from altermag_symmetry import analyze

result = analyze(
    "POSCAR",
    magnetic_moments={0: [0, 0, 1], 1: [0, 0, -1]},
    symprec=1e-2,
)
print(result.crystal_symmetry)
print(result.magnetic_space_group)
print(result.altermagnetism)
```

Agents can call `analyze_material(path, config, options)` and receive a plain,
JSON-serializable dictionary. Its contract is documented in
[the agent interface](docs/agent_interface.md).

## Interpretation of results

The JSON separates input-derived structure data, raw backend symmetry results, explicit
site mappings, mathematical momentum constraints, and the physical interpretation. The
`spin_space_group` object records the FindSpinGroup OSSG `index`, symbol, spin point
group, group components, magnetic phase, property constraints, tolerances, and backend
warnings. Explicit operation matrices retain `operation_backend: spinspg`.
For an opposite-spin exchange, it reports
`E_up(k) = E_down(R_k k)` and `Delta(k) = -Delta(R_k k)`, with `R_k = R^-T` in
fractional reciprocal coordinates. Tolerances and package versions are recorded.

## Limitations

Version 0.2 accepts vector moments but its local classifier is collinear-only. It does
not yet support magnetic CIF, partial occupancies, SOC representation theory, little
groups, corepresentations, or band degeneracies. FindSpinGroup property fields are
symmetry permissions and polynomial classifications, not calculated response magnitudes.
A candidate result does not establish observable splitting; electronic bands and the
relevant symmetry representations must still be checked.

## Roadmap

1. Phase 1: spglib, spinspg, conservative classification, CLI, and JSON.
2. Phase 2: FindSpinGroup OSSG identification and amcheck comparison (current).
3. Phase 3: IRSSG, little spin groups, corepresentations, enforced degeneracies.
4. Phase 4: VASP PROCAR/vasprun.xml and band comparisons.
5. Phase 5: Wannier90, spin textures, and momentum-space splitting maps.
6. Phase 6: conductivity, spin conductivity, anomalous Hall, and field symmetry breaking.
7. Phase 7: hardened AI agent/skill service.

## Development

```bash
ruff check .
pytest -q
```

Tests use local synthetic structures and require no network access. Contributions should
preserve explicit tolerances, backend boundaries, and conservative physical wording.
