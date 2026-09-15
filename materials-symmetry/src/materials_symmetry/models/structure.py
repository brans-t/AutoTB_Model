"""Backend-independent structure representation; lattice vectors are rows."""

from dataclasses import dataclass

import numpy as np


@dataclass
class Structure:
    lattice: list[list[float]]
    positions: list[list[float]]
    species: list[str]

    def __post_init__(self) -> None:
        a, x = np.asarray(self.lattice, float), np.asarray(self.positions, float)
        if a.shape != (3, 3) or not np.isfinite(a).all() or abs(np.linalg.det(a)) < 1e-12:
            raise ValueError("Lattice must be finite and nonsingular, shape (3,3)")
        if x.shape != (len(self.species), 3) or not len(x) or not np.isfinite(x).all():
            raise ValueError("Positions must be finite, shape (number of atoms,3)")
        if not all(isinstance(s, str) and s for s in self.species):
            raise ValueError("Species must be nonempty strings")
        self.lattice = a.tolist()
        self.positions = (x % 1).tolist()
