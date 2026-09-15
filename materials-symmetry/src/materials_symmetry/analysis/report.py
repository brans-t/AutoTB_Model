"""Concise terminal rendering; JSON rendering lives on the result model."""

from materials_symmetry.models.result import AnalysisResult


def render(result: AnalysisResult) -> str:
    """Render a readable summary while retaining explicit uncertainty."""
    crystal = result.crystal_space_group
    lines = [
        "Materials symmetry analysis",
        f"Crystal space group: {crystal.international} ({crystal.number}), "
        f"point group {crystal.pointgroup}",
    ]
    if result.magnetic_configuration is None:
        lines.append("Magnetic analysis: not requested (no magnetic moments supplied)")
        lines.extend(f"Warning: {warning}" for warning in result.warnings)
        return "\n".join(lines)

    magnetic = result.magnetic_space_group
    classification = result.altermagnetic_classification
    spin_group = result.spin_space_group
    assert classification is not None and spin_group is not None
    candidate = {
        True: "yes — symmetry-compatible candidate",
        False: "no under the preliminary criterion",
        None: "inconclusive",
    }[classification.candidate_altermagnet]
    lines.extend(
        [
            (
                f"Magnetic space group: UNI {magnetic.uni_number}, "
                f"BNS {magnetic.bns_number}, type {magnetic.msg_type}"
                if magnetic
                else "Magnetic space group: unresolved"
            ),
            (
                f"Oriented spin-space group: {spin_group.index}"
                if spin_group.index
                else "Oriented spin-space group: unidentified"
            ),
            (
                f"OSSG symbol: {spin_group.international_symbol}"
                if spin_group.international_symbol
                else f"Spin-space backend status: {spin_group.status}"
            ),
            f"Spin-space operations: {len(spin_group.operations)} "
            f"({spin_group.operation_backend or 'unavailable'})",
            f"Magnetic sites: {len(result.magnetic_configuration.up)} up, "
            f"{len(result.magnetic_configuration.down)} down, "
            f"{len(result.magnetic_configuration.nonmagnetic)} nonmagnetic",
            f"Opposite-spin pairs: {len(result.opposite_spin_pairs)}",
            f"Candidate altermagnet: {candidate}",
        ]
    )
    lines.extend(f"  - {reason}" for reason in classification.reasoning)
    lines.extend(f"Warning: {warning}" for warning in result.warnings)
    return "\n".join(lines)
