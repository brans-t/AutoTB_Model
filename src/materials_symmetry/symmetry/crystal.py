"""Ordinary symmetry and independent tolerance scans."""

from materials_symmetry.adapters.spglib_adapter import crystal
from materials_symmetry.models.structure import Structure


def scan_symprec(structure: Structure, tolerances: list[float]) -> dict:
    """Report every requested tolerance; never select a larger one automatically."""
    rows = []
    for tolerance in tolerances:
        group = crystal(structure, tolerance)
        rows.append(
            {
                "symprec": tolerance,
                "number": group.number,
                "international": group.international,
                "operation_count": len(group.operations),
            }
        )
    return {"rows": rows, "sensitive": len({(r["number"], r["operation_count"]) for r in rows}) > 1}
