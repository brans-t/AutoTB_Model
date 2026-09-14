"""High-level workflow joining parsing, backends and physical interpretation."""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

import numpy as np

from altermag_symmetry.adapters.amcheck_adapter import validate as validate_amcheck
from altermag_symmetry.adapters.findspingroup_adapter import identify_spin_space_group
from altermag_symmetry.adapters.spglib_adapter import crystal, magnetic
from altermag_symmetry.adapters.spinspg_adapter import analyze_spin_space
from altermag_symmetry.analysis.momentum import constraint
from altermag_symmetry.io.structure import read_structure
from altermag_symmetry.magnetism.altermagnet import classify
from altermag_symmetry.magnetism.configuration import configure
from altermag_symmetry.magnetism.sublattices import find_connections
from altermag_symmetry.models.result import AnalysisResult
from altermag_symmetry.models.structure import Structure
from altermag_symmetry.models.symmetry import SpinSpaceGroup


def _version(package: str) -> str:
    try:
        return version(package)
    except PackageNotFoundError:
        return "unavailable"


def _attach_spin_actions(result: AnalysisResult) -> None:
    """Attach matching S matrices without changing the spatial classification."""
    if not result.spin_space_group.operations:
        return
    for item in result.connecting_operations:
        r = np.asarray(item["real_rotation"])
        t = np.asarray(item["translation"])
        matching = [
            operation
            for operation in result.spin_space_group.operations
            if np.array_equal(operation.real_rotation, r)
            and np.allclose(
                (np.asarray(operation.translation) - t)
                - np.round(np.asarray(operation.translation) - t),
                0,
                atol=1e-7,
            )
        ]
        item["spin_actions"] = [
            {
                "spin_rotation": operation.spin_rotation,
                "flips_ordered_moment": operation.flips_moment(result.magnetic_configuration.axis),
            }
            for operation in matching
        ]


def analyze_spin_space_group(
    structure: Structure,
    moments: list[list[float]],
    *,
    source_name: str,
    symprec: float,
    mag_symprec: float,
    fsg_eigenvalue_tol: float = 2e-5,
    fsg_matrix_tol: float = 1e-2,
    identify_ossg: bool = True,
) -> SpinSpaceGroup:
    """Combine standardized FindSpinGroup identification with spinspg operations."""
    group = analyze_spin_space(structure, moments, symprec, mag_symprec)
    if not identify_ossg:
        return group
    identified = identify_spin_space_group(
        structure,
        moments,
        source_name=source_name,
        space_tol=symprec,
        moment_tol=mag_symprec,
        eigenvalue_tol=fsg_eigenvalue_tol,
        matrix_tol=fsg_matrix_tol,
    )
    if identified["status"] != "ok":
        if group.status == "ok":
            group.status = "partial"
        group.detail = identified.get("detail") or group.detail
        return group

    group.status = "ok"
    group.identification_backend = "findspingroup"
    group.index = identified["index"]
    group.international_symbol = identified["international_symbol"]
    group.acc_symbol = identified["acc_symbol"]
    group.spin_point_group_hm = identified["spin_point_group_hm"]
    group.spin_point_group_schoenflies = identified["spin_point_group_schoenflies"]
    group.magnetic_phase = identified["magnetic_phase"]
    group.properties = identified["properties"]
    group.group_components = identified["group_components"]
    group.identification_tolerances = identified["tolerances"]
    group.backend_warnings = identified["warnings"]
    if group.operation_backend != "spinspg":
        group.detail = group.detail or "spinspg operations are unavailable"
    return group


def analyze_structure(
    structure: Structure,
    magnetic_moments: dict | list,
    *,
    symprec: float = 1e-3,
    mag_symprec: float = 1e-3,
    soc: bool = False,
    neel_vector: list[float] | None = None,
    compare_amcheck: bool = True,
    source_name: str = "<in-memory>",
    fsg_eigenvalue_tol: float = 2e-5,
    fsg_matrix_tol: float = 1e-2,
    identify_ossg: bool = True,
) -> AnalysisResult:
    """Analyze an already parsed structure while preserving its atom indexing."""
    configuration = configure(
        len(structure.species), magnetic_moments, mag_symprec, soc, neel_vector
    )
    crystal_group = crystal(structure, symprec)
    warnings: list[str] = []
    try:
        magnetic_group = magnetic(structure, configuration.moments, symprec, mag_symprec)
    except ValueError as exc:
        magnetic_group = None
        warnings.append(str(exc))
    spin_group = analyze_spin_space_group(
        structure,
        configuration.moments,
        source_name=source_name,
        symprec=symprec,
        mag_symprec=mag_symprec,
        fsg_eigenvalue_tol=fsg_eigenvalue_tol,
        fsg_matrix_tol=fsg_matrix_tol,
        identify_ossg=identify_ossg,
    )
    if spin_group.status not in {"ok", "partial"}:
        warnings.append(spin_group.detail or "Spin-space symmetry unavailable")
    elif identify_ossg and spin_group.index is None:
        warnings.append(spin_group.detail or "Standard OSSG identification is unavailable")

    pairs, connections = find_connections(
        structure, configuration, crystal_group.operations, symprec
    )
    independent = (
        validate_amcheck(structure, crystal_group, configuration, symprec)
        if compare_amcheck
        else {"status": "not_requested"}
    )
    classification = classify(configuration, connections, independent)
    momentum = [
        constraint(item["real_rotation"], item["classification"]["label"]) for item in connections
    ]
    if not configuration.is_collinear:
        warnings.append("The version 0.1 classifier supports collinear moments only.")
    if not configuration.is_compensated:
        warnings.append("The supplied magnetic configuration is not compensated.")
    if independent.get("status") == "ok" and (
        independent["candidate_altermagnet"] != classification.candidate_altermagnet
    ):
        warnings.append("The preliminary classifier disagrees with amcheck.")
    if spin_group.magnetic_phase:
        fsg_candidate = "Altermagnet" in spin_group.magnetic_phase
        if fsg_candidate != classification.candidate_altermagnet:
            warnings.append("The preliminary classifier disagrees with FindSpinGroup.")
    fsg_msg = spin_group.group_components.get("MSG", {})
    if magnetic_group and fsg_msg.get("bns_number") not in {None, magnetic_group.bns_number}:
        warnings.append("spglib and FindSpinGroup report different BNS magnetic groups.")

    result = AnalysisResult(
        structure,
        crystal_group,
        configuration,
        magnetic_group,
        spin_group,
        pairs,
        connections,
        classification,
        momentum,
        warnings,
        {
            "symprec_angstrom": symprec,
            "mag_symprec_mu_B": mag_symprec,
            "findspingroup_eigenvalue_tol": fsg_eigenvalue_tol,
            "findspingroup_matrix_tol": fsg_matrix_tol,
        },
        {
            "altermag_symmetry": _version("altermag-symmetry"),
            "spglib": _version("spglib"),
            "spinspg": _version("spinspg"),
            "findspingroup": _version("findspingroup"),
            "amcheck": _version("amcheck"),
        },
    )
    _attach_spin_actions(result)
    return result


def analyze(
    structure_path: str | Path,
    magnetic_moments: dict | list,
    *,
    symprec: float = 1e-3,
    mag_symprec: float = 1e-3,
    soc: bool = False,
    neel_vector: list[float] | None = None,
    compare_amcheck: bool = True,
    fsg_eigenvalue_tol: float = 2e-5,
    fsg_matrix_tol: float = 1e-2,
    identify_ossg: bool = True,
) -> AnalysisResult:
    """Read and analyze POSCAR, CONTCAR, or ordinary CIF input."""
    return analyze_structure(
        read_structure(structure_path),
        magnetic_moments,
        symprec=symprec,
        mag_symprec=mag_symprec,
        soc=soc,
        neel_vector=neel_vector,
        compare_amcheck=compare_amcheck,
        source_name=str(structure_path),
        fsg_eigenvalue_tol=fsg_eigenvalue_tol,
        fsg_matrix_tol=fsg_matrix_tol,
        identify_ossg=identify_ossg,
    )


def analyze_material(
    structure_path: str,
    magnetic_config: dict,
    options: dict | None = None,
) -> dict:
    """Stable agent-facing API returning only JSON-serializable values."""
    options = dict(options or {})
    allowed = {
        "symprec",
        "mag_symprec",
        "compare_amcheck",
        "fsg_eigenvalue_tol",
        "fsg_matrix_tol",
        "identify_ossg",
    }
    unknown = set(options) - allowed
    if unknown:
        raise ValueError(f"Unknown analysis options: {sorted(unknown)}")
    result = analyze(
        structure_path,
        magnetic_config.get("moments", {}),
        soc=magnetic_config.get("soc", False),
        neel_vector=magnetic_config.get("neel_vector"),
        **options,
    )
    return result.to_dict()
