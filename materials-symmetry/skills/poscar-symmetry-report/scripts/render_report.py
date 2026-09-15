#!/usr/bin/env python3
"""Render materials-symmetry's structured POSCAR analysis as Markdown."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path


def find_project(explicit: str | None) -> Path:
    candidates = [explicit, os.environ.get("MATSYM_PROJECT")]
    candidates += [str(parent) for parent in Path(__file__).resolve().parents]
    candidates += [str(parent) for parent in Path.cwd().resolve().parents]
    candidates.append(str(Path.cwd().resolve()))
    for candidate in candidates:
        if candidate:
            root = Path(candidate).expanduser().resolve()
            if (root / "pyproject.toml").is_file() and (
                root / "src/materials_symmetry/analysis/pipeline.py"
            ).is_file():
                return root
    raise SystemExit("Cannot locate materials-symmetry; pass --project or set MATSYM_PROJECT.")


def material_name(source: Path, result: dict) -> str:
    with source.open(encoding="utf-8", errors="replace") as handle:
        title = handle.readline().strip()
    if re.fullmatch(r"[A-Z][A-Za-z0-9()+-]{0,79}", title):
        return title
    from pymatgen.core import Composition

    formula = Composition(Counter(result["structure"]["species"])).reduced_formula
    safe = re.sub(r"[^A-Za-z0-9()+-]", "", formula)
    return safe or source.stem


def code(value: object) -> str:
    return "`" + json.dumps(value, ensure_ascii=False, separators=(",", ":")) + "`"


def value(item: object) -> str:
    return "未提供" if item is None else str(item)


def scalar(number: int | float) -> str:
    if abs(number) < 1e-12:
        return "0"
    formatted = f"{number:.8g}"
    if "e" in formatted:
        coefficient, exponent = formatted.split("e")
        return rf"{coefficient}\times 10^{{{int(exponent)}}}"
    return formatted


def matrix(items: list[list[int | float]]) -> str:
    rows = [" & ".join(scalar(item) for item in row) for row in items]
    return r"\begin{pmatrix}" + r" \\ ".join(rows) + r"\end{pmatrix}"


def vector(items: list[int | float]) -> str:
    return matrix([[item] for item in items])


def inline_vector(items: list[int | float]) -> str:
    return r"$\left(" + r",\;".join(scalar(item) for item in items) + r"\right)$"


def display(lines: list[str], expression: str) -> None:
    if lines and lines[-1]:
        lines.append("")
    lines += ["$$", expression, "$$", ""]


def table_cell(item: object) -> str:
    return str(item).replace("|", r"\|").replace("\n", " ")


def ossg_math(symbol: str | None) -> str | None:
    if not symbol or not re.fullmatch(r"[A-Za-z0-9_{} .+\-/|∞]+", symbol):
        return None
    expression = symbol.replace("∞", r"\infty").replace("|", r"\mid ")
    expression = re.sub(r"-(\d+)", lambda match: r"\overline{" + match[1] + "}", expression)
    return "$" + expression + "$"


def operation_label(label: str) -> str:
    if label == "E":
        return "$E$"
    match = re.fullmatch(r"C(\d+)", label)
    if match:
        return rf"$C_{{{match[1]}}}$"
    match = re.fullmatch(r"(\d+)-bar(?: / S(\d+))?", label)
    if match:
        barred = rf"$\bar{{{match[1]}}}$"
        return barred + (rf"（$S_{{{match[2]}}}$）" if match[2] else "")
    if label.startswith("inversion"):
        return r"$\bar{1}$（反演）"
    if label.startswith("mirror"):
        return "$m$（镜面）"
    return table_cell(label)


def operations(
    lines: list[str], title: str, group: dict | None, kind: str, lattice: list | None = None
) -> None:
    lines.append(f"#### {title}群操作")
    if group is None:
        lines.append("未分析：未提供磁矩配置。" if kind != "crystal" else "未识别。")
        lines.append("")
        return
    items = group.get("operations") or []
    lines.append(f"共 {len(items)} 个。$R$ 和 $\\mathbf{{t}}$ 作用于分数坐标。")
    if kind == "spin":
        lines.append("$S$ 是笛卡尔自旋旋转矩阵。")
    lines.append("")
    if not items:
        lines.append("当前后端未返回群操作。")
        lines.append("")
        return
    if kind == "crystal":
        from materials_symmetry.symmetry.operations import classify_operation

    for index, item in enumerate(items, 1):
        label = ""
        if kind == "crystal":
            label = classify_operation(item["real_rotation"], lattice, item["translation"])["label"]
        lines.append(f"**操作 #{index}**" + (f" · {operation_label(label)}" if label else ""))
        display(
            lines,
            rf"R_{{{index}}}={matrix(item['real_rotation'])},\qquad "
            rf"\mathbf{{t}}_{{{index}}}={vector(item['translation'])}",
        )
        if kind == "magnetic":
            lines.append(f"时间反演：{'是' if item['time_reversal'] else '否'}。")
            lines.append("")
        elif kind == "spin":
            display(lines, rf"S_{{{index}}}={matrix(item['spin_rotation'])}")


def highlight_altermagnetic_operations(lines: list[str], result: dict) -> None:
    classification = result["altermagnetic_classification"]
    if not classification:
        return
    connections = result["connecting_operations"]
    candidate = classification["candidate_altermagnet"]
    lines += ["", "### 交替磁相关操作", ""]
    if candidate is not True:
        lines.append("当前输入未通过交替磁初步判定。")
        lines.append("")
        return
    relevant = [
        item
        for item in connections
        if item["classification"]["kind"] in {"rotation", "mirror", "rotoinversion"}
    ]
    if not relevant:
        lines.append("项目给出候选判定，但没有可列举的非平凡异号自旋连接操作。")
        lines.append("")
        return
    lines.append(
        "**交替磁初步候选。**下列非平凡空间操作连接异号自旋位点；"
        "磁结构共线且补偿，纯平移与反演没有连接异号自旋位点。"
    )
    lines += [
        "",
        "| 关键操作 | 类型 | 位点映射 | 匹配自旋操作 |",
        "|:---:|:---:|:---:|:---:|",
    ]
    for item in relevant:
        actions = item.get("spin_actions") or []
        flipped = any(action.get("flips_ordered_moment") for action in actions)
        spin_status = "已验证自旋翻转" if flipped else "未验证自旋翻转"
        lines.append(
            f"| **#{item['operation_index'] + 1}** | "
            f"{operation_label(item['classification']['label'])} | "
            f"{item['source']} $\\rightarrow$ {item['target']} | {spin_status} |"
        )
    if lines[-1]:
        lines.append("")
    lines.append("操作矩阵见下文同序号群操作；判定只给出对称性候选，不代表能带劈裂已被计算。")
    lines.append("")


def render(result: dict, source: Path, config: Path | None, material: str, output: Path) -> str:
    crystal = result["crystal_space_group"]
    magnetic = result["magnetic_space_group"]
    spin = result["spin_space_group"]
    structure = result["structure"]
    source_link = f"[{source.name}](<{os.path.relpath(source, output.parent)}>)"
    config_link = (
        f"[{config.name}](<{os.path.relpath(config, output.parent)}>)" if config else "未提供"
    )
    lines = [
        f"## {material} · 对称性报告",
        "",
        f"结构：{source_link} · 磁矩：{config_link}",
        "",
        "### 群判定",
        "",
        "| 群 | 判定结果 | 状态与来源 | 操作数 |",
        "|:---:|:---:|:---:|:---:|",
        (
            f"| 普通空间群 | **{table_cell(crystal['international'])} "
            f"(No. {crystal['number']})**；点群 {table_cell(crystal['pointgroup'])}；"
            f"Hall {table_cell(crystal['hall_symbol'])} (No. {crystal['hall_number']}) "
            f"| spglib；已识别 | {len(crystal['operations'])} |"
        ),
    ]
    if magnetic:
        lines.append(
            f"| 磁空间群 | **BNS {table_cell(magnetic['bns_number'])}；"
            f"UNI {magnetic['uni_number']}**；类型 {magnetic['msg_type']} "
            f"| spglib；已识别 | {len(magnetic['operations'])} |"
        )
    elif config:
        lines.append("| 磁空间群 | 未识别 | spglib；详见警告 | 0 |")
    else:
        lines.append("| 磁空间群 | 未分析 | 未提供磁矩 | — |")
    if spin:
        identifier = spin.get("index")
        symbol = spin.get("international_symbol")
        if identifier:
            rendered_symbol = ossg_math(symbol)
            lines.append(
                f"| 定向自旋空间群 | **OSSG {table_cell(identifier)}**；"
                f"{rendered_symbol or table_cell(value(symbol))} "
                f"| {spin['status']}；FindSpinGroup 识别，spinspg 操作 "
                f"| {len(spin['operations'])} |"
            )
        else:
            lines.append(
                f"| 定向自旋空间群 | 标准群未识别 | {spin['status']} | {len(spin['operations'])} |"
            )
        lines.append("")
        if symbol:
            lines.append(f"OSSG 后端原始符号：{code(symbol)}。")
        if spin.get("spin_point_group_hm"):
            point_group = table_cell(spin["spin_point_group_hm"])
            lines.append(f"自旋点群（后端记号）：`{point_group}`。")
        if spin.get("detail"):
            lines.append(f"后端说明：{spin['detail']}")
        lines.append(
            f"识别后端：{value(spin.get('identification_backend'))}；"
            f"操作后端：{value(spin.get('operation_backend'))}。"
        )
        if spin.get("group_components"):
            components = spin["group_components"]
            g0, l0, msg = (components.get(key) or {} for key in ("G0", "L0", "MSG"))
            lines.append(
                f"群构成：$G_0$ 为 {value(g0.get('symbol'))} "
                f"(No. {value(g0.get('number'))})；"
                f"$L_0$ 为 {value(l0.get('symbol'))} "
                f"(No. {value(l0.get('number'))})；"
                f"MSG 为 {value(msg.get('symbol'))} "
                f"(BNS {value(msg.get('bns_number'))})。"
            )
        if spin.get("magnetic_phase"):
            lines.append(f"磁相（后端标签）：{spin['magnetic_phase']}。")
    else:
        lines.append("| 自旋空间群 | 未分析 | 未提供磁矩 | — |")
    lines += [
        "",
        "No. 是普通空间群编号；BNS、UNI 是磁空间群编号；OSSG 是定向自旋空间群索引。",
    ]
    if config:
        highlight_altermagnetic_operations(lines, result)
    if lines[-1]:
        lines.append("")
    lines += ["### 晶体对称性", ""]
    lines.append("晶格矩阵（行矢量，Å）：")
    display(lines, rf"A_{{\mathrm{{rows}}}}={matrix(structure['lattice'])}")
    lines.append(
        f"{len(structure['species'])} 个原子；"
        f"{len(set(crystal['equivalent_atoms']))} 个对称性不等价位点。"
    )
    lines += [
        "",
        "| 原子索引 | 元素 | 分数坐标 | 等价原子代表 | Wyckoff |",
        "|:---:|:---:|:---:|:---:|:---:|",
    ]
    for index, (species, position, equivalent, wyckoff) in enumerate(
        zip(
            structure["species"],
            structure["positions"],
            crystal["equivalent_atoms"],
            crystal["wyckoffs"],
            strict=True,
        )
    ):
        lines.append(
            f"| {index} | {species} | {inline_vector(position)} | {equivalent} | {wyckoff} |"
        )
    lines.append("")
    lines += ["### 群操作", ""]
    operations(lines, "普通空间", crystal, "crystal", structure["lattice"])
    if config:
        operations(lines, "磁空间", magnetic, "magnetic")
        operations(lines, "自旋空间", spin, "spin")
        lines += ["### 磁结构与对称性", ""]
        setting = result["magnetic_configuration"]
        if setting:
            lines.append("非零原子磁矩（笛卡尔坐标；未列出的原子磁矩为零）：")
            nonzero = [
                (index, moment)
                for index, moment in enumerate(setting["moments"])
                if any(abs(component) > 1e-12 for component in moment)
            ]
            if nonzero:
                lines += ["", "| 原子索引 | 磁矩 |", "|:---:|:---:|"]
                for index, moment in nonzero:
                    lines.append(f"| {index} | {inline_vector(moment)} |")
            else:
                lines.append("没有非零磁矩。")
            lines.append("")
            display(lines, rf"\mathbf{{M}}_{{\mathrm{{net}}}}={vector(setting['net_moment'])}")
            lines.append(
                f"共线：{'是' if setting['is_collinear'] else '否'}；"
                f"补偿：{'是' if setting['is_compensated'] else '否'}；"
                f"SOC：{'是' if setting['soc'] else '否'}。"
            )
            lines.append("")
        pairs = result["opposite_spin_pairs"]
        lines.append(f"异号自旋原子对：{len(pairs)} 对。")
        if pairs:
            lines.append(
                "位点映射："
                + "；".join(
                    f"{pair['source']}→{pair['target']} ({pair['species']})" for pair in pairs
                )
                + "。"
            )
        connections = result["connecting_operations"]
        lines.append(f"连接操作：{len(connections)} 条。")
        classification = result["altermagnetic_classification"]
        if classification:
            candidate = classification["candidate_altermagnet"]
            verdict = (
                "初步对称性条件兼容交替磁候选"
                if candidate is True
                else ("初步条件不满足" if candidate is False else "初步条件不确定")
            )
            lines.append(f"交替磁初步判定：**{verdict}**。")
            independent = classification.get("independent_validation") or {}
            lines.append(f"amcheck：{code(independent)}。")
            lines.append("")
        constraints = result["momentum_constraints"]
        lines.append(f"动量空间对称约束：{len(constraints)} 条。")
        lines.append(r"$\mathbf{k}$ 使用倒易晶格分数坐标；$R_k=R^{-T}$。")
        lines.append("")
        for index, item in enumerate(constraints, 1):
            lines.append(f"**约束 #{index}**：{operation_label(item['operation'])}。")
            display(lines, rf"R_{{k,{index}}}={matrix(item['reciprocal_rotation'])}")
        if constraints:
            display(
                lines,
                r"E_{\uparrow}(\mathbf{k})="
                r"E_{\downarrow}(R_{k,i}\mathbf{k}),\qquad "
                r"\Delta(\mathbf{k})="
                r"-\Delta(R_{k,i}\mathbf{k})",
            )
            lines.append("$i$ 为上列约束序号。")
            lines.append("")
        lines.append("")
    lines += ["### 容差与后端", "", f"容差：{code(result['tolerances'])}。"]
    if spin and spin.get("identification_tolerances"):
        lines.append(f"FindSpinGroup 内部容差：{code(spin['identification_tolerances'])}。")
    lines.append(f"后端版本：{code(result['provenance'])}。")
    warnings = result["warnings"] + (spin.get("backend_warnings", []) if spin else [])
    if warnings:
        lines.append("警告：")
        for warning in dict.fromkeys(warnings):
            lines.append(f"- {warning}")
    else:
        lines.append("警告：无。")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("poscar", type=Path, help="POSCAR path")
    parser.add_argument("--config", type=Path, help="JSON magnetic configuration")
    parser.add_argument(
        "--output", type=Path, help="Markdown output; defaults beside POSCAR with material name"
    )
    parser.add_argument("--project", help="materials-symmetry checkout")
    parser.add_argument("--symprec", type=float, default=1e-3)
    parser.add_argument("--mag-symprec", type=float, default=1e-3)
    args = parser.parse_args()
    root = find_project(args.project)
    sys.path.insert(0, str(root / "src"))
    from materials_symmetry.analysis.pipeline import analyze_material

    poscar = args.poscar.expanduser().resolve()
    config = args.config.expanduser().resolve() if args.config else None
    magnetic = json.loads(config.read_text()) if config else None
    result = analyze_material(
        poscar,
        magnetic_config=magnetic,
        options={"symprec": args.symprec, "mag_symprec": args.mag_symprec},
    )
    material = material_name(poscar, result)
    output = (
        args.output.expanduser().resolve()
        if args.output
        else poscar.with_name(material + (".md" if config else "_crystal.md"))
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render(result, poscar, config, material, output), encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
