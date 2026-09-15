"""Optional independent comparison with amcheck."""

from __future__ import annotations

import numpy as np

from materials_symmetry.models.magnetic import MagneticConfiguration
from materials_symmetry.models.structure import Structure
from materials_symmetry.models.symmetry import CrystalSpaceGroup


def validate(
    structure: Structure,
    crystal: CrystalSpaceGroup,
    configuration: MagneticConfiguration,
    tolerance: float,
) -> dict:
    """Run amcheck when installed; failures are data, rather than fatal errors."""
    try:
        from amcheck import is_altermagnet
    except ImportError:
        return {"status": "unavailable"}

    spins = ["n"] * len(structure.species)
    for index in configuration.up:
        spins[index] = "u"
    for index in configuration.down:
        spins[index] = "d"
    symops = [
        (np.asarray(operation.real_rotation), np.asarray(operation.translation))
        for operation in crystal.operations
    ]
    try:
        result = is_altermagnet(
            symops,
            np.asarray(structure.positions),
            np.asarray(crystal.equivalent_atoms),
            structure.species,
            spins,
            tol=tolerance,
            silent=True,
        )
    except Exception as exc:
        return {"status": "failed", "detail": str(exc)}
    return {"status": "ok", "candidate_altermagnet": bool(result)}
