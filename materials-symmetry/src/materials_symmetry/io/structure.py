"""Parse structural files without changing site order or standardizing cells."""

from pathlib import Path

from pymatgen.core import Structure as PmgStructure

from materials_symmetry.models.structure import Structure


def read_structure(path: str | Path) -> Structure:
    """Read POSCAR, CONTCAR or ordinary CIF; moments are supplied separately."""
    path = Path(path)
    if path.suffix.lower() == ".mcif":
        raise ValueError("Magnetic CIF is not supported yet")
    if path.suffix.lower() == ".cif":
        from pymatgen.io.cif import CifParser

        if "_space_group_symop_magn" in path.read_text().lower():
            raise ValueError("Magnetic CIF requires a future adapter")
        structures = CifParser(str(path)).parse_structures(primitive=False)
        if len(structures) != 1:
            raise ValueError("CIF must contain exactly one structure")
        raw = structures[0]
    else:
        from pymatgen.io.vasp.inputs import Poscar

        raw = Poscar.from_file(str(path), check_for_potcar=False).structure
    return from_pymatgen(raw)


def from_pymatgen(raw: PmgStructure) -> Structure:
    """Detach from pymatgen and reject partial or mixed occupancies."""
    if not raw.is_ordered:
        raise ValueError("Partial occupancies/disordered sites are unsupported")
    return Structure(
        raw.lattice.matrix.tolist(), raw.frac_coords.tolist(), [str(site.specie) for site in raw]
    )
