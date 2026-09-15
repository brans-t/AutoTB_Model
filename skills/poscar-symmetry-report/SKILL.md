---
name: poscar-symmetry-report
description: Analyze a POSCAR with materials-symmetry and produce a Markdown report of crystallographic, magnetic, and spin-space groups, their operations, and symmetry implications. Use when a user provides a POSCAR path or asks for a Markdown symmetry report; magnetic results require supplied moments or a magnetic config.
---

# POSCAR symmetry report

Use the project's `materials_symmetry.analysis.pipeline.analyze_material` interface through [scripts/render_report.py](scripts/render_report.py). The helper writes a Markdown file beside the POSCAR, named for the material. Tables center their contents; small headings separate the group summary, all returned LaTeX matrix operations, equivalent sites, magnetic mappings, momentum constraints, warnings, and backend versions. When the preliminary altermagnetic classifier returns a candidate, the report highlights nontrivial operations connecting opposite-spin sites and matching spin flips.

1. Locate the POSCAR and any user-supplied magnetic configuration. A POSCAR alone has no ordered moments: report ordinary space-group symmetry only. Do not guess moments or magnetic groups. Configuration files use the project's JSON schema (`moments`, optional `soc` and `neel_vector`); atom indices are zero-based in input order.
2. Ensure the project environment exists. From the project root, `bash install.sh` creates `.venv`. Run the helper with that interpreter:

   ```bash
   MATSYM_PROJECT=/path/to/materials-symmetry /path/to/materials-symmetry/.venv/bin/python /path/to/poscar-symmetry-report/scripts/render_report.py /path/to/POSCAR
   ```

   Add `--config /path/to/magnetic_config.json` when moments are supplied. By default, a magnetic run writes `<material>.md` and a crystal-only run writes `<material>_crystal.md` beside the POSCAR; `--output` overrides the path. `--symprec` is in Å and `--mag-symprec` is in μB. `--project` can replace `MATSYM_PROJECT`. The helper also finds the project when the skill is inside the repo or the current directory is within it.
3. Read the generated Markdown and check that group status and warnings are represented faithfully. Return the report path and a concise account of the result. If the user requests the report inline, provide the Markdown content.

Preserve the reported symmetry setting and tolerances. Keep matrices and equations in LaTeX math mode, including $E_{\uparrow}$, $E_{\downarrow}$, $R_k$, and $\Delta$. Describe altermagnetism only as the project's preliminary symmetry-compatible candidate when that is what the classifier says; an individual operation alone does not prove it. An unavailable optional backend is an analysis limitation, not evidence that the symmetry is absent. Do not promote property permissions or momentum constraints into calculated observables.
