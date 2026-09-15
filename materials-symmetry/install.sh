#!/usr/bin/env bash
set -euo pipefail

project_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
python_cmd="${PYTHON:-python3}"

if ! command -v "$python_cmd" >/dev/null 2>&1; then
    echo "Python 3.11 or newer is required (set PYTHON to its executable)." >&2
    exit 1
fi

if ! "$python_cmd" -c 'import sys; sys.exit(sys.version_info < (3, 11))'; then
    echo "Python 3.11 or newer is required." >&2
    exit 1
fi

cd "$project_dir"
"$python_cmd" -m venv .venv
.venv/bin/python -m pip install -e '.[all,dev]'
.venv/bin/python -c 'import spglib, spinspg, findspingroup, amcheck, materials_symmetry'
.venv/bin/matsym --help >/dev/null

echo "Installation complete. Activate with: source .venv/bin/activate"
