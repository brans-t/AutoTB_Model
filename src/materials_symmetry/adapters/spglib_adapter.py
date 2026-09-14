"""All spglib calls and tuple conventions are confined to this adapter."""

import numpy as np
import spglib

from materials_symmetry.models.structure import Structure
from materials_symmetry.models.symmetry import (
    CrystalSpaceGroup,
    MagneticOperation,
    MagneticSpaceGroup,
    SpatialOperation,
)


def cell(structure: Structure) -> tuple:
    """Stable integer species identifiers, preserving oxidation-state labels."""
    labels = {s: i + 1 for i, s in enumerate(sorted(set(structure.species)))}
    return (
        np.asarray(structure.lattice),
        np.asarray(structure.positions),
        [labels[s] for s in structure.species],
    )


def crystal(structure: Structure, symprec: float) -> CrystalSpaceGroup:
    """Find ordinary crystallographic symmetry at an explicit length tolerance."""
    if not np.isfinite(symprec) or symprec <= 0:
        raise ValueError("symprec must be finite and positive")
    d = spglib.get_symmetry_dataset(cell(structure), symprec=symprec)
    if d is None:
        raise ValueError("Crystallographic symmetry could not be identified")
    return CrystalSpaceGroup(
        d.international,
        int(d.number),
        d.pointgroup,
        int(d.hall_number),
        d.hall,
        d.equivalent_atoms.tolist(),
        list(d.wyckoffs),
        [SpatialOperation(r.tolist(), t.tolist()) for r, t in zip(d.rotations, d.translations)],
        symprec,
    )


def magnetic(
    structure: Structure, moments: list, symprec: float, mag_symprec: float
) -> MagneticSpaceGroup:
    """Use Cartesian rank-one AXIAL moments, including optional time reversal."""
    d = spglib.get_magnetic_symmetry_dataset(
        (*cell(structure), np.asarray(moments)),
        is_axial=True,
        symprec=symprec,
        mag_symprec=mag_symprec,
    )
    if d is None:
        raise ValueError("Magnetic symmetry could not be identified")
    kind = spglib.get_magnetic_spacegroup_type(int(d.uni_number))
    return MagneticSpaceGroup(
        int(d.uni_number),
        kind.bns_number,
        int(d.msg_type),
        d.equivalent_atoms.tolist(),
        [
            MagneticOperation(r.tolist(), t.tolist(), bool(tr))
            for r, t, tr in zip(d.rotations, d.translations, d.time_reversals)
        ],
    )
