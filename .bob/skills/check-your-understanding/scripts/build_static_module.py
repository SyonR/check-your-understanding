#!/usr/bin/env python3
"""Build an offline interactive learning module from onboarding session data."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Any


DATA_MARKER = "__MODULE_DATA_JSON__"


def require_object(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    return value


def require_list(value: Any, label: str) -> list[Any]:
    if not isinstance(value, list) or not value:
        raise ValueError(f"{label} must be a non-empty array")
    return value


def infer_title(session: dict[str, Any], slides: list[Any]) -> str:
    if slides and isinstance(slides[0], dict) and slides[0].get("title"):
        return str(slides[0]["title"])

    source_path = str(session.get("repo_context", {}).get("source_path", "")).replace("\\", "/")
    repo_name = source_path.rstrip("/").split("/")[-1]
    return f"{repo_name} — Developer Onboarding" if repo_name else "Developer Onboarding"


def build(session_path: Path, output_dir: Path) -> Path:
    skill_dir = Path(__file__).resolve().parent.parent
    template_dir = skill_dir / "assets" / "html-template"
    template_path = template_dir / "index.html"
    template_assets = template_dir / "assets"

    session = require_object(json.loads(session_path.read_text(encoding="utf-8")), "session")
    curriculum = require_object(session.get("curriculum"), "curriculum")
    quiz = require_object(session.get("quiz"), "quiz")
    slides = require_list(curriculum.get("slides"), "curriculum.slides")
    questions = require_list(quiz.get("questions"), "quiz.questions")

    if not template_path.is_file() or not template_assets.is_dir():
        raise FileNotFoundError(f"Offline HTML template is incomplete: {template_dir}")

    payload = {
        "title": infer_title(session, slides),
        "curriculum": {"slides": slides},
        "quiz": {
            "questions": questions,
            "pass_threshold": quiz.get("pass_threshold", 0.8),
        },
    }

    serialized = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    serialized = serialized.replace("<", "\\u003c").replace("&", "\\u0026")
    template = template_path.read_text(encoding="utf-8")
    if template.count(DATA_MARKER) != 1:
        raise ValueError(f"Template must contain exactly one {DATA_MARKER} marker")

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "index.html"
    output_path.write_text(template.replace(DATA_MARKER, serialized), encoding="utf-8")
    shutil.copytree(template_assets, output_dir / "assets", dirs_exist_ok=True)
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build a package-manager-free onboarding module that opens from the filesystem."
    )
    parser.add_argument(
        "session_file",
        nargs="?",
        default="onboarding-session.json",
        type=Path,
        help="Completed onboarding session JSON (default: ./onboarding-session.json)",
    )
    parser.add_argument(
        "output_dir",
        nargs="?",
        default="learning-module",
        type=Path,
        help="Output directory (default: ./learning-module)",
    )
    args = parser.parse_args()

    output_path = build(args.session_file.resolve(), args.output_dir.resolve())
    print(f"Offline learning module written to {output_path}")
    print("Open index.html directly in a modern browser; no package manager or server is required.")


if __name__ == "__main__":
    main()
