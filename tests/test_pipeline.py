import json

import numpy as np

from altermag_symmetry import analyze, analyze_material
from altermag_symmetry.analysis.momentum import reciprocal_transform


def test_reciprocal_action_is_inverse_transpose():
    rotation = [[0, -1, 0], [1, 0, 0], [0, 0, 1]]
    assert np.allclose(reciprocal_transform(rotation), rotation)


def test_complete_analysis_and_strict_json(simple_poscar):
    result = analyze(simple_poscar, {0: [0, 0, 1], 1: [0, 0, -1]})
    payload = json.loads(result.to_json())
    assert payload["crystal_space_group"]["number"] == 229
    assert payload["magnetic_space_group"]["uni_number"] > 0
    assert payload["spin_space_group"]["status"] == "ok"
    assert payload["opposite_spin_pairs"] == [{"source": 0, "target": 1, "species": "Fe"}]
    assert any(item["spin_actions"] for item in payload["connecting_operations"])
    assert any(
        action["flips_ordered_moment"]
        for item in payload["connecting_operations"]
        for action in item["spin_actions"]
    )
    assert payload["tolerances"]["symprec_angstrom"] == 1e-3


def test_agent_api_is_plain_dictionary(simple_poscar):
    payload = analyze_material(str(simple_poscar), {"moments": {"0": [0, 0, 1], "1": [0, 0, -1]}})
    json.dumps(payload, allow_nan=False)
    assert payload["schema_version"] == "0.1.0"
