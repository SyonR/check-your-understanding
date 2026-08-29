#!/usr/bin/env python3
"""Copy the skill-owned Slidev shell into a session output directory."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


def install(output_dir: Path) -> list[Path]:
    skill_dir = Path(__file__).resolve().parent.parent
    template_dir = skill_dir / "assets" / "slidev-template"
    if not template_dir.is_dir():
        raise FileNotFoundError(f"Slidev template not found: {template_dir}")

    output_dir.mkdir(parents=True, exist_ok=True)
    installed: list[Path] = []
    for source in sorted(template_dir.rglob("*")):
        if not source.is_file():
            continue
        relative_path = source.relative_to(template_dir)
        destination = output_dir / relative_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        installed.append(relative_path)
    return installed


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Install the reusable check-your-understanding Slidev template."
    )
    parser.add_argument(
        "output_dir",
        nargs="?",
        default="slidev",
        type=Path,
        help="Slidev output directory (default: ./slidev)",
    )
    args = parser.parse_args()

    installed = install(args.output_dir.resolve())
    print(f"Installed {len(installed)} template files into {args.output_dir.resolve()}")


if __name__ == "__main__":
    main()
