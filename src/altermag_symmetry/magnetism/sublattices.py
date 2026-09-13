"""Find explicit mappings between opposite-spin magnetic sites."""

from __future__ import annotations

from altermag_symmetry.models.magnetic import MagneticConfiguration
from altermag_symmetry.models.structure import Structure
from altermag_symmetry.models.symmetry import SpatialOperation
from altermag_symmetry.symmetry.operations import atom_mapping, classify_operation


def find_connections(
    structure: Structure,
    configuration: MagneticConfiguration,
    operations: list[SpatialOperation],
    tolerance: float,
) -> tuple[list[dict], list[dict]]:
    """Return unique opposite-spin pairs and every connecting spatial operation."""
    down = set(configuration.down)
    pairs: dict[tuple[int, int], dict] = {}
    connections: list[dict] = []
    for operation_index, operation in enumerate(operations):
        mapping = atom_mapping(structure, operation, tolerance)
        classification = classify_operation(
            operation.real_rotation, structure.lattice, operation.translation
        )
        for source in configuration.up:
            target = mapping[source]
            if target not in down:
                continue
            pairs[(source, target)] = {
                "source": source,
                "target": target,
                "species": structure.species[source],
            }
            connections.append(
                {
                    "operation_index": operation_index,
                    "source": source,
                    "target": target,
                    "real_rotation": operation.real_rotation,
                    "translation": operation.translation,
                    "classification": classification,
                    "exchanges_spin_sublattices": True,
                }
            )
    return list(pairs.values()), connections
