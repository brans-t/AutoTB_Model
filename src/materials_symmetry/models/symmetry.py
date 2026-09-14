"""Distinct models for crystal, magnetic and spin-space operations."""

from dataclasses import dataclass, field

import numpy as np


@dataclass
class SpatialOperation:
    real_rotation: list[list[int]]
    translation: list[float]


@dataclass
class MagneticOperation(SpatialOperation):
    time_reversal: bool


@dataclass
class SpinSpaceOperation(SpatialOperation):
    spin_rotation: list[list[float]]

    def flips_moment(self, axis: list[float], tolerance: float = 1e-5) -> bool:
        """Test spin action on the Cartesian ordered-moment direction."""
        n = np.asarray(axis, float)
        return bool(np.linalg.norm(np.asarray(self.spin_rotation) @ n + n) <= tolerance)


@dataclass
class CrystalSpaceGroup:
    international: str
    number: int
    pointgroup: str
    hall_number: int
    hall_symbol: str
    equivalent_atoms: list[int]
    wyckoffs: list[str]
    operations: list[SpatialOperation]
    symprec: float


@dataclass
class MagneticSpaceGroup:
    uni_number: int
    bns_number: str
    msg_type: int
    equivalent_atoms: list[int]
    operations: list[MagneticOperation]


@dataclass
class SpinSpaceGroup:
    status: str
    spin_only_group: str | None = None
    operations: list[SpinSpaceOperation] = field(default_factory=list)
    detail: str | None = None
    identification_backend: str | None = None
    operation_backend: str | None = None
    index: str | None = None
    international_symbol: str | None = None
    acc_symbol: str | None = None
    spin_point_group_hm: str | None = None
    spin_point_group_schoenflies: str | None = None
    magnetic_phase: str | None = None
    properties: dict = field(default_factory=dict)
    group_components: dict = field(default_factory=dict)
    identification_tolerances: dict = field(default_factory=dict)
    backend_warnings: list[str] = field(default_factory=list)
