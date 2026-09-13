"""Reciprocal-space actions derived from real-space operations."""

import numpy as np


def reciprocal_transform(rotation: list[list[int]]) -> list[list[float]]:
    """Return the action on fractional reciprocal coordinates: k' = R^-T k."""
    transformed = np.linalg.inv(np.asarray(rotation, float)).T
    return np.where(abs(transformed) < 1e-12, 0.0, transformed).tolist()


def constraint(rotation: list[list[int]], label: str) -> dict:
    """Express the spin-splitting constraint for an opposite-spin exchange."""
    reciprocal = reciprocal_transform(rotation)
    return {
        "operation": label,
        "reciprocal_rotation": reciprocal,
        "coordinate_basis": "fractional reciprocal lattice",
        "energy_relation": "E_up(k) = E_down(R_k k)",
        "splitting_relation": "Delta(k) = -Delta(R_k k)",
    }
