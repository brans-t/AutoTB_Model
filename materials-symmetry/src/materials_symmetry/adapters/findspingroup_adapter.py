"""Optional standard OSSG identification through FindSpinGroup."""

from __future__ import annotations

import warnings

from materials_symmetry.models.structure import Structure


def identify_spin_space_group(
    structure: Structure,
    moments: list[list[float]],
    *,
    source_name: str,
    space_tol: float,
    moment_tol: float,
    eigenvalue_tol: float = 2e-5,
    matrix_tol: float = 1e-2,
) -> dict:
    """Identify the standardized OSSG from in-memory Cartesian moments."""
    try:
        from findspingroup import find_spin_group_basic_from_data
    except ImportError:
        return {
            "status": "unavailable",
            "detail": "Install materials-symmetry[findspingroup] for OSSG identification.",
        }

    try:
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            raw = find_spin_group_basic_from_data(
                source_name=source_name,
                lattice_factors=structure.lattice,
                positions=structure.positions,
                elements=structure.species,
                occupancies=[1.0] * len(structure.species),
                moments=moments,
                input_spin_setting="cartesian",
                space_tol=space_tol,
                mtol=moment_tol,
                meigtol=eigenvalue_tol,
                matrix_tol=matrix_tol,
            )
    except Exception as exc:  # preserve third-party diagnostics in the result
        return {"status": "failed", "detail": f"FindSpinGroup: {exc}"}

    return {
        "status": "ok",
        "index": raw.get("index"),
        "international_symbol": raw.get("ossg_symbol_linear"),
        "acc_symbol": raw.get("acc_symbol"),
        "spin_point_group_hm": raw.get("spin_space_point_group_hm"),
        "spin_point_group_schoenflies": raw.get("spin_space_point_group_schoenflies"),
        "magnetic_phase": raw.get("magnetic_phase"),
        "properties": raw.get("properties") or {},
        "group_components": {
            "G0": {"number": raw.get("g0_number"), "symbol": raw.get("g0_symbol")},
            "L0": {"number": raw.get("l0_number"), "symbol": raw.get("l0_symbol")},
            "MSG": {
                "bns_number": raw.get("msg_bns_number"),
                "symbol": raw.get("msg_symbol"),
                "type": raw.get("msg_type"),
            },
        },
        "tolerances": raw.get("tolerances") or {},
        "warnings": list(
            dict.fromkeys(f"{item.category.__name__}: {item.message}" for item in caught)
        ),
    }
