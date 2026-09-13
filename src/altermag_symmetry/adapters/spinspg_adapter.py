"""Optional spinspg adapter with backend-independent output models."""

from __future__ import annotations

import numpy as np

from altermag_symmetry.adapters.spglib_adapter import cell
from altermag_symmetry.models.structure import Structure
from altermag_symmetry.models.symmetry import SpinSpaceGroup, SpinSpaceOperation


def analyze_spin_space(
    structure: Structure,
    moments: list[list[float]],
    symprec: float,
    mag_symprec: float,
) -> SpinSpaceGroup:
    """Return spin-space operations, or a structured unavailable result."""
    try:
        import spinspg
    except ImportError:
        return SpinSpaceGroup(
            status="unavailable",
            detail="Install altermag-symmetry[spin] to enable spin-space symmetry.",
        )

    lattice, positions, numbers = cell(structure)
    try:
        spin_only, rotations, translations, spin_rotations = spinspg.get_spin_symmetry(
            lattice,
            positions,
            np.asarray(numbers),
            np.asarray(moments),
            symprec=symprec,
            mag_symprec=mag_symprec,
        )
    except Exception as exc:  # backend errors must survive in machine output
        return SpinSpaceGroup(status="failed", detail=f"spinspg: {exc}")

    operations = [
        SpinSpaceOperation(r.tolist(), t.tolist(), s.tolist())
        for r, t, s in zip(rotations, translations, spin_rotations, strict=True)
    ]
    return SpinSpaceGroup(status="ok", spin_only_group=str(spin_only), operations=operations)
