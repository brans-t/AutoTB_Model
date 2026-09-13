from pathlib import Path

import pytest


@pytest.fixture
def simple_poscar(tmp_path: Path) -> Path:
    path = tmp_path / "POSCAR"
    path.write_text(
        """Two-site cubic test
1.0
2.0 0.0 0.0
0.0 2.0 0.0
0.0 0.0 2.0
Fe
2
Direct
0.0 0.0 0.0
0.5 0.5 0.5
"""
    )
    return path
