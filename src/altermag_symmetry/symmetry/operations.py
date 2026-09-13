"""Basis-aware point-operation classification and unambiguous periodic mappings."""

import numpy as np
from pymatgen.core import Lattice

from altermag_symmetry.models.structure import Structure
from altermag_symmetry.models.symmetry import SpatialOperation


def classify_operation(rotation: list, lattice: list, translation: list | None = None) -> dict:
    """Classify by determinant, finite order and Cartesian eigenspaces."""
    r, a = np.asarray(rotation, float), np.asarray(lattice, float).T
    q = a @ r @ np.linalg.inv(a)
    if not np.allclose(q.T @ q, np.eye(3), atol=1e-5):
        raise ValueError("Rotation is not an isometry in the supplied lattice")
    det = int(round(np.linalg.det(q)))
    order = next(
        (
            n
            for n in range(1, 13)
            if np.allclose(np.linalg.matrix_power(r, n), np.eye(3), atol=1e-6)
        ),
        None,
    )
    if order is None:
        raise ValueError("Not a finite crystallographic point operation")
    if np.allclose(r, np.eye(3)):
        kind, label = "identity", "E"
    elif np.allclose(r, -np.eye(3)):
        kind, label = "inversion", "inversion (-1)"
    elif det == 1:
        kind, label = "rotation", f"C{order}"
    elif order == 2:
        kind, label = "mirror", "mirror (m)"
    else:
        proper = -r
        n = next(
            n for n in range(1, 13) if np.allclose(np.linalg.matrix_power(proper, n), np.eye(3))
        )
        kind, label = "rotoinversion", f"{n}-bar" + (" / S4" if n == 4 else "")
    axis = None
    if kind in {"rotation", "mirror", "rotoinversion"}:
        values, vectors = np.linalg.eig(q)
        target = 1 if det == 1 else -1
        v = np.real(vectors[:, np.argmin(abs(values - target))])
        axis = (v / np.linalg.norm(v)).tolist()
    t = np.zeros(3) if translation is None else np.asarray(translation, float)
    # Accumulated translation removes origin-dependent transverse components.
    accumulated = sum(np.linalg.matrix_power(r, j) @ t for j in range(order))
    fractional = not np.allclose(t, np.round(t), atol=1e-7)
    nonsymmorphic = fractional and np.linalg.norm(accumulated) > 1e-7
    modifier = "screw" if kind == "rotation" else "glide" if kind == "mirror" else None
    return {
        "kind": kind,
        "label": label,
        "determinant": det,
        "order": order,
        "axis_cartesian": axis,
        "has_fractional_translation": fractional,
        "translation_character": modifier if nonsymmorphic else None,
        "translation_note": "Representative-dependent; not a space-group symmorphicity test",
    }


def atom_mapping(
    structure: Structure, operation: SpatialOperation, tolerance: float = 1e-3
) -> list[int]:
    """Map every site bijectively, using exact periodic distances for skew cells."""
    x = np.asarray(structure.positions)
    transformed = x @ np.asarray(operation.real_rotation).T + operation.translation
    distances = Lattice(structure.lattice).get_all_distances(transformed, x)
    mapping = []
    for i, row in enumerate(distances):
        matches = [
            j
            for j, distance in enumerate(row)
            if distance <= tolerance and structure.species[i] == structure.species[j]
        ]
        if len(matches) != 1:
            raise ValueError(f"Ambiguous or missing atom mapping for site {i}: {matches}")
        mapping.append(matches[0])
    if len(set(mapping)) != len(mapping):
        raise ValueError("Atom mapping is not bijective")
    return mapping
