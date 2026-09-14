"""Magnetic configuration and explicit preliminary checks."""

from dataclasses import dataclass, field


@dataclass
class MagneticConfiguration:
    moments: list[list[float]]
    axis: list[float]
    up: list[int]
    down: list[int]
    nonmagnetic: list[int]
    net_moment: list[float]
    is_collinear: bool
    is_compensated: bool
    soc: bool = False


@dataclass
class AltermagneticClassification:
    is_collinear: bool
    is_compensated: bool
    opposite_spin_related_by_translation: bool
    opposite_spin_related_by_inversion: bool
    opposite_spin_related_by_rotation: bool
    opposite_spin_related_by_mirror: bool
    opposite_spin_related_by_rotoinversion: bool
    candidate_altermagnet: bool | None
    reasoning: list[str]
    independent_validation: dict = field(default_factory=dict)
