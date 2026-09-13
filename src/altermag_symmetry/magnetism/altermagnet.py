"""Conservative, explicit candidate classification."""

from altermag_symmetry.models.magnetic import (
    AltermagneticClassification,
    MagneticConfiguration,
)


def classify(
    configuration: MagneticConfiguration,
    connections: list[dict],
    independent_validation: dict | None = None,
) -> AltermagneticClassification:
    """Apply the documented preliminary criterion and record each premise."""
    kinds = {item["classification"]["kind"] for item in connections}
    translation = any(
        item["classification"]["kind"] == "identity"
        and item["classification"]["has_fractional_translation"]
        for item in connections
    )
    inversion = "inversion" in kinds
    rotation = "rotation" in kinds
    mirror = "mirror" in kinds
    rotoinversion = "rotoinversion" in kinds
    nontrivial_rotation = rotation or mirror or rotoinversion
    candidate: bool | None
    if not configuration.is_collinear or not configuration.is_compensated:
        candidate = False
    elif not connections:
        candidate = None
    else:
        candidate = bool(nontrivial_rotation and not translation and not inversion)

    collinearity = "collinear" if configuration.is_collinear else "non-collinear"
    compensation = "compensated" if configuration.is_compensated else "not compensated"
    reasoning = [
        f"magnetic configuration is {collinearity}",
        f"net magnetic moment is {compensation}",
    ]
    if connections:
        reasoning.append("opposite-spin sites are connected by: " + ", ".join(sorted(kinds)))
    else:
        reasoning.append("no opposite-spin mapping was found at the stated tolerance")
    if candidate:
        reasoning.append(
            "the preliminary spatial-symmetry criterion is compatible with altermagnetism"
        )
    elif candidate is None:
        reasoning.append("the preliminary criterion is inconclusive")
    else:
        reasoning.append("the preliminary spatial-symmetry criterion is not satisfied")

    return AltermagneticClassification(
        configuration.is_collinear,
        configuration.is_compensated,
        translation,
        inversion,
        rotation,
        mirror,
        rotoinversion,
        candidate,
        reasoning,
        independent_validation or {},
    )
