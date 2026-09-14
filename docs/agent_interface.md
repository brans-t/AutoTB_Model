# Agent interface

Use `analyze_material(structure_path, magnetic_config, options=None)`. The path must point
to POSCAR, CONTCAR, or an ordinary CIF. `magnetic_config` accepts `moments`, `soc`, and
`neel_vector`; moment keys are zero-based input atom indices. Options currently accept
`symprec`, `mag_symprec`, `compare_amcheck`, `identify_ossg`,
`fsg_eigenvalue_tol`, and `fsg_matrix_tol`.

The return value is a dictionary with schema version `0.2.0` and these top-level fields:

```text
structure, crystal_space_group, magnetic_configuration,
magnetic_space_group, spin_space_group, opposite_spin_pairs,
connecting_operations, altermagnetic_classification,
momentum_constraints, warnings, tolerances, provenance, schema_version
```

Invalid paths, formats, indices, vector shapes, non-finite values, or tolerances raise
`OSError` or `ValueError`. An unavailable optional backend appears as a status and a
warning. Noncollinearity, non-compensation, backend disagreement, and unresolved magnetic
symmetry are also explicit warnings.

Within `spin_space_group`, `index`, `international_symbol`, and `group_components` come
from FindSpinGroup; `operations` come from spinspg. Preserve the reported setting and
tolerance context when interpreting either source.

Agents may safely summarize group identifiers, mappings, tolerance sensitivity, raw
constraints, and the exact `reasoning` entries. They should preserve “candidate” wording,
must not turn a symmetry permission into a calculated magnitude, and must not turn an
unavailable backend into a negative scientific result.
