"""Moment assignment uses zero-based indices and Cartesian vectors in mu_B."""

import json
from collections.abc import Mapping, Sequence
from pathlib import Path

import numpy as np

from materials_symmetry.models.magnetic import MagneticConfiguration


def load_config(path: str | Path) -> dict:
    """Load JSON and reject duplicate keys, including duplicate atom indices."""

    def unique(pairs: list) -> dict:
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"Duplicate configuration key: {key}")
            result[key] = value
        return result

    return json.loads(Path(path).read_text(), object_pairs_hook=unique)


def configure(
    n_atoms: int,
    moments: Mapping | Sequence,
    tolerance: float = 1e-5,
    soc: bool = False,
    neel_vector: Sequence | None = None,
) -> MagneticConfiguration:
    """Assign sparse moments (unlisted sites are zero), then evaluate collinearity."""
    if not np.isfinite(tolerance) or tolerance <= 0:
        raise ValueError("Magnetic tolerance must be finite and positive")
    if not isinstance(soc, bool):
        raise ValueError("soc must be a boolean")
    if isinstance(moments, Mapping):
        m = np.zeros((n_atoms, 3))
        seen = set()
        for key, value in moments.items():
            if isinstance(key, bool) or str(key) != str(int(key)):
                raise ValueError(f"Invalid zero-based atom index: {key}")
            i = int(key)
            if i in seen or not 0 <= i < n_atoms:
                raise ValueError(f"Duplicate or out-of-range atom index: {key}")
            seen.add(i)
            if np.asarray(value).shape != (3,):
                raise ValueError("Each magnetic moment must be a 3D vector")
            m[i] = value
    else:
        m = np.asarray(moments, float)
    if m.shape != (n_atoms, 3) or not np.isfinite(m).all():
        raise ValueError("Moments must be finite with shape (number of atoms,3)")
    norms = np.linalg.norm(m, axis=1)
    active = np.flatnonzero(norms > tolerance)
    axis = np.array(
        neel_vector if neel_vector is not None else (m[active[0]] if len(active) else [0, 0, 1]),
        dtype=float,
        copy=True,
    )
    if axis.shape != (3,) or not np.isfinite(axis).all() or np.linalg.norm(axis) == 0:
        raise ValueError("Neel vector must be finite and nonzero with three components")
    axis /= np.linalg.norm(axis)
    projections = m @ axis
    collinear = bool(np.all(np.linalg.norm(m - projections[:, None] * axis, axis=1) <= tolerance))
    net = m.sum(axis=0)
    return MagneticConfiguration(
        m.tolist(),
        axis.tolist(),
        np.flatnonzero(projections > tolerance).tolist(),
        np.flatnonzero(projections < -tolerance).tolist(),
        np.flatnonzero(norms <= tolerance).tolist(),
        net.tolist(),
        collinear,
        bool(len(active) > 0 and np.linalg.norm(net) <= tolerance),
        soc,
    )
