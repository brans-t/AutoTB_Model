"""Versioned, strictly JSON-serializable analysis results."""

import json
from dataclasses import asdict, dataclass

from .magnetic import AltermagneticClassification, MagneticConfiguration
from .structure import Structure
from .symmetry import CrystalSpaceGroup, MagneticSpaceGroup, SpinSpaceGroup


@dataclass
class AnalysisResult:
    structure: Structure
    crystal_space_group: CrystalSpaceGroup
    magnetic_configuration: MagneticConfiguration
    magnetic_space_group: MagneticSpaceGroup | None
    spin_space_group: SpinSpaceGroup
    opposite_spin_pairs: list[dict]
    connecting_operations: list[dict]
    altermagnetic_classification: AltermagneticClassification
    momentum_constraints: list[dict]
    warnings: list[str]
    tolerances: dict[str, float]
    provenance: dict[str, str]
    schema_version: str = "0.1.0"

    @property
    def crystal_symmetry(self) -> CrystalSpaceGroup:
        return self.crystal_space_group

    @property
    def altermagnetism(self) -> AltermagneticClassification:
        return self.altermagnetic_classification

    def to_dict(self) -> dict:
        """Return plain Python objects without backend representations."""
        return asdict(self)

    def to_json(self) -> str:
        """Serialize without nonstandard NaN/Infinity values."""
        return json.dumps(self.to_dict(), indent=2, allow_nan=False)
