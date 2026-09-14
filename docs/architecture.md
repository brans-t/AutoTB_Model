# Architecture

```text
input structure -> parser -> crystal symmetry
                              |
magnetic config --------------+
                              v
                    magnetic space group
                              |
                              v
                       spin-space group
                              |
                              v
                    opposite-spin mapping
                              |
                              v
                    conservative checks
                              |
                              v
                    momentum constraints
                              |
                              v
                         report / JSON
```

`io` owns parsing and preserves site order. `models` contains backend-independent data
classes. `adapters` is the only layer allowed to expose spglib, spinspg, FindSpinGroup,
or amcheck calling conventions. FindSpinGroup owns standard OSSG identification;
spinspg owns the explicit operation matrices used for site mapping. `symmetry` classifies
operations and computes exact periodic site mappings. `magnetism` assigns moments and evaluates explicit preliminary checks.
`analysis` orchestrates the workflow and reporting. No layer stores global mutable state.

Raw symmetry results, derived site and momentum relations, and physical interpretations
remain distinct fields in `AnalysisResult`. Backend failures become warnings or status
objects whenever a useful partial result can still be returned.
