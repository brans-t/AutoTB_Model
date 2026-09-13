"""Command-line interface for focused and complete analyses."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from altermag_symmetry.adapters.spglib_adapter import crystal, magnetic
from altermag_symmetry.adapters.spinspg_adapter import analyze_spin_space
from altermag_symmetry.analysis.pipeline import analyze
from altermag_symmetry.analysis.report import render
from altermag_symmetry.io.structure import read_structure
from altermag_symmetry.magnetism.configuration import configure, load_config
from altermag_symmetry.symmetry.crystal import scan_symprec
from altermag_symmetry.symmetry.operations import classify_operation


def _moments(text: str) -> list[list[float]]:
    try:
        result = [
            [float(component) for component in vector.split(",")] for vector in text.split(";")
        ]
    except ValueError as exc:
        raise argparse.ArgumentTypeError("moments must contain numbers") from exc
    if any(len(vector) != 3 for vector in result):
        raise argparse.ArgumentTypeError("use x,y,z;x,y,z for moments")
    return result


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="altermag")
    sub = parser.add_subparsers(dest="command", required=True)
    for command in ("analyze", "magnetic", "spin-group"):
        item = sub.add_parser(command)
        item.add_argument("structure")
        source = item.add_mutually_exclusive_group(required=True)
        source.add_argument("--config")
        source.add_argument("--moments", type=_moments)
        item.add_argument("--symprec", type=float, default=1e-3)
        item.add_argument("--mag-symprec", type=float, default=1e-3)
        item.add_argument("--json", dest="json_path")
    symmetry = sub.add_parser("symmetry")
    symmetry.add_argument("structure")
    symmetry.add_argument("--symprec", type=float, nargs="+", default=[1e-3])
    symmetry.add_argument("--scan-symprec", action="store_true")
    operations = sub.add_parser("operations")
    operations.add_argument("structure")
    operations.add_argument("--symprec", type=float, default=1e-3)
    return parser


def _config(args: argparse.Namespace) -> dict:
    return load_config(args.config) if args.config else {"moments": args.moments}


def main(argv: list[str] | None = None) -> int:
    """Run the CLI; user-data errors become concise parser diagnostics."""
    parser = _parser()
    args = parser.parse_args(argv)
    try:
        structure = read_structure(args.structure)
        if args.command == "symmetry":
            tolerances = args.symprec
            if args.scan_symprec and args.symprec == [1e-3]:
                tolerances = [1e-4, 1e-3, 5e-3, 1e-2, 2e-2]
            print(json.dumps(scan_symprec(structure, tolerances), indent=2))
            return 0
        if args.command == "operations":
            group = crystal(structure, args.symprec)
            payload = [
                {
                    **classify_operation(op.real_rotation, structure.lattice, op.translation),
                    "real_rotation": op.real_rotation,
                    "translation": op.translation,
                }
                for op in group.operations
            ]
            print(json.dumps(payload, indent=2))
            return 0

        config = _config(args)
        moments = configure(
            len(structure.species),
            config.get("moments", {}),
            args.mag_symprec,
            config.get("soc", False),
            config.get("neel_vector"),
        )
        if args.command == "magnetic":
            payload = magnetic(structure, moments.moments, args.symprec, args.mag_symprec).__dict__
            text = json.dumps(payload, default=lambda item: item.__dict__, indent=2)
        elif args.command == "spin-group":
            payload = analyze_spin_space(structure, moments.moments, args.symprec, args.mag_symprec)
            text = json.dumps(payload.__dict__, default=lambda item: item.__dict__, indent=2)
        else:
            result = analyze(
                args.structure,
                config.get("moments", {}),
                symprec=args.symprec,
                mag_symprec=args.mag_symprec,
                soc=config.get("soc", False),
                neel_vector=config.get("neel_vector"),
            )
            text = result.to_json()
            print(render(result))
        if args.json_path:
            Path(args.json_path).write_text(text + "\n")
        elif args.command != "analyze":
            print(text)
        return 0
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
