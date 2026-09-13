"""Concise terminal rendering; JSON rendering lives on the result model."""

from altermag_symmetry.models.result import AnalysisResult


def render(result: AnalysisResult) -> str:
    """Render a readable summary while retaining explicit uncertainty."""
    crystal = result.crystal_space_group
    magnetic = result.magnetic_space_group
    classification = result.altermagnetic_classification
    candidate = {
        True: "yes — symmetry-compatible candidate",
        False: "no under the preliminary criterion",
        None: "inconclusive",
    }[classification.candidate_altermagnet]
    lines = [
        "Altermagnetic symmetry analysis",
        f"Crystal space group: {crystal.international} ({crystal.number}), "
        f"point group {crystal.pointgroup}",
        (
            f"Magnetic space group: UNI {magnetic.uni_number}, "
            f"BNS {magnetic.bns_number}, type {magnetic.msg_type}"
            if magnetic
            else "Magnetic space group: unresolved"
        ),
        f"Spin-space group: {result.spin_space_group.status} "
        f"({len(result.spin_space_group.operations)} operations)",
        f"Magnetic sites: {len(result.magnetic_configuration.up)} up, "
        f"{len(result.magnetic_configuration.down)} down, "
        f"{len(result.magnetic_configuration.nonmagnetic)} nonmagnetic",
        f"Opposite-spin pairs: {len(result.opposite_spin_pairs)}",
        f"Candidate altermagnet: {candidate}",
    ]
    lines.extend(f"  - {reason}" for reason in classification.reasoning)
    lines.extend(f"Warning: {warning}" for warning in result.warnings)
    return "\n".join(lines)
