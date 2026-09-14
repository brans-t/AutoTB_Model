import numpy as np
import pytest

from materials_symmetry.io.structure import read_structure
from materials_symmetry.magnetism.configuration import configure


def test_poscar_preserves_site_order(simple_poscar):
    structure = read_structure(simple_poscar)
    assert structure.species == ["Fe", "Fe"]
    assert structure.positions == [[0.0, 0.0, 0.0], [0.5, 0.5, 0.5]]


def test_sparse_moment_assignment_and_compensation():
    config = configure(3, {0: [0, 0, 2], 2: [0, 0, -2]})
    assert config.up == [0]
    assert config.down == [2]
    assert config.nonmagnetic == [1]
    assert config.is_collinear and config.is_compensated
    assert np.allclose(config.net_moment, 0)


def test_wrong_moment_count_is_explicit():
    with pytest.raises(ValueError, match="number of atoms"):
        configure(2, [[0, 0, 1]])


def test_noncollinear_is_detected():
    config = configure(2, [[1, 0, 0], [0, 1, 0]])
    assert not config.is_collinear
    assert not config.is_compensated
