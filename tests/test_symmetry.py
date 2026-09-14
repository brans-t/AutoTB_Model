import numpy as np

from materials_symmetry.io.structure import read_structure
from materials_symmetry.models.structure import Structure
from materials_symmetry.models.symmetry import SpatialOperation
from materials_symmetry.symmetry.crystal import scan_symprec
from materials_symmetry.symmetry.operations import atom_mapping, classify_operation


def test_tolerance_scan_returns_each_requested_value(simple_poscar):
    result = scan_symprec(read_structure(simple_poscar), [1e-4, 1e-3, 1e-2])
    assert [row["symprec"] for row in result["rows"]] == [1e-4, 1e-3, 1e-2]
    assert all(row["number"] == 229 for row in result["rows"])


def test_s4_classification():
    rotation = [[0, 1, 0], [-1, 0, 0], [0, 0, -1]]
    result = classify_operation(rotation, np.eye(3).tolist())
    assert result["kind"] == "rotoinversion"
    assert result["order"] == 4
    assert "S4" in result["label"]


def test_periodic_atom_mapping_in_skew_cell():
    structure = Structure(
        [[2, 0, 0], [0.5, 2, 0], [0, 0, 2]],
        [[0, 0, 0], [0.5, 0.5, 0.5]],
        ["Fe", "Fe"],
    )
    operation = SpatialOperation(np.eye(3, dtype=int).tolist(), [0.5, 0.5, 0.5])
    assert atom_mapping(structure, operation, 1e-5) == [1, 0]
