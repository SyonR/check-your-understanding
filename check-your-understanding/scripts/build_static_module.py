#!/usr/bin/env python3
"""Build an offline interactive learning module from onboarding session data."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Any


DATA_MARKER = "__MODULE_DATA_JSON__"

# The six tabs that are always required, in order.
REQUIRED_GUIDE_TABS = [
    ("setup", "Setup"),
    ("first-tasks", "First Tasks"),
    ("architecture", "Architecture"),
    ("patterns", "Patterns"),
    ("test-debug", "Test & Debug"),
    ("reference", "Reference"),
]

# The optional 7th tab: present when identity.role == "junior" or any
# relevant tech_familiarity == 0.  When present it must be last.
OPTIONAL_GUIDE_TAB = ("key-concepts", "Key Concepts")

GUIDE_FACT_CATEGORIES = ["setup", "first_tasks", "architecture", "patterns", "test_debug", "reference"]


def require_object(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    return value


def require_list(value: Any, label: str) -> list[Any]:
    if not isinstance(value, list) or not value:
        raise ValueError(f"{label} must be a non-empty array")
    return value


def validate_guide(value: Any) -> dict[str, Any]:
    guide = require_object(value, "curriculum.guide")
    tabs = require_list(guide.get("tabs"), "curriculum.guide.tabs")

    n = len(tabs)
    if n not in (len(REQUIRED_GUIDE_TABS), len(REQUIRED_GUIDE_TABS) + 1):
        raise ValueError(
            f"curriculum.guide.tabs must contain {len(REQUIRED_GUIDE_TABS)} or "
            f"{len(REQUIRED_GUIDE_TABS) + 1} tabs, got {n}"
        )

    has_optional = n == len(REQUIRED_GUIDE_TABS) + 1

    # Validate the six required tabs positionally.
    for index, (expected_id, expected_label) in enumerate(REQUIRED_GUIDE_TABS):
        tab = require_object(tabs[index], f"curriculum.guide.tabs[{index}]")
        if tab.get("id") != expected_id or tab.get("label") != expected_label:
            raise ValueError(
                f"curriculum.guide.tabs[{index}] must be {expected_id!r} / {expected_label!r}"
            )
        _validate_standard_tab_content(tab, index)

    # Validate the optional Key Concepts tab when present.
    if has_optional:
        tab = require_object(tabs[6], "curriculum.guide.tabs[6]")
        opt_id, opt_label = OPTIONAL_GUIDE_TAB
        if tab.get("id") != opt_id or tab.get("label") != opt_label:
            raise ValueError(
                f"curriculum.guide.tabs[6] must be {opt_id!r} / {opt_label!r} when a 7th tab is present"
            )
        content = tab.get("content")
        if not isinstance(content, str) or not content.strip():
            raise ValueError("curriculum.guide.tabs[6] (Key Concepts) content must be non-empty text")
        # Key Concepts holds short definitions, not bullet lists — no word/bullet cap enforced.

    return guide


def _validate_standard_tab_content(tab: dict[str, Any], index: int) -> None:
    content = tab.get("content")
    if not isinstance(content, str) or not content.strip():
        raise ValueError(f"curriculum.guide.tabs[{index}].content must be non-empty text")
    if len(content.split()) > 80:
        raise ValueError(f"curriculum.guide.tabs[{index}].content must be 80 words or fewer")
    bullet_count = sum(
        1 for line in content.splitlines() if line.lstrip().startswith(("- ", "* "))
    )
    if bullet_count > 4:
        raise ValueError(f"curriculum.guide.tabs[{index}].content must have at most four bullets")


def validate_guide_facts(value: Any) -> None:
    repo_context = require_object(value, "repo_context")
    guide_facts = require_object(repo_context.get("guide_facts"), "repo_context.guide_facts")
    for category in GUIDE_FACT_CATEGORIES:
        facts = require_list(guide_facts.get(category), f"repo_context.guide_facts.{category}")
        for index, raw_fact in enumerate(facts):
            fact = require_object(raw_fact, f"repo_context.guide_facts.{category}[{index}]")
            if not isinstance(fact.get("text"), str) or not fact["text"].strip():
                raise ValueError(f"repo_context.guide_facts.{category}[{index}].text must be non-empty")
            evidence = require_list(
                fact.get("evidence"), f"repo_context.guide_facts.{category}[{index}].evidence"
            )
            if any(not isinstance(path, str) or not path.strip() for path in evidence):
                raise ValueError(
                    f"repo_context.guide_facts.{category}[{index}].evidence must contain non-empty paths"
                )


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
    validate_guide_facts(session.get("repo_context"))
    curriculum = require_object(session.get("curriculum"), "curriculum")
    quiz = require_object(session.get("quiz"), "quiz")
    slides = require_list(curriculum.get("slides"), "curriculum.slides")
    questions = require_list(quiz.get("questions"), "quiz.questions")

    if not template_path.is_file() or not template_assets.is_dir():
        raise FileNotFoundError(f"Offline HTML template is incomplete: {template_dir}")

    guide = validate_guide(curriculum.get("guide"))
    curriculum_payload: dict[str, Any] = {"slides": slides, "guide": guide}

    payload = {
        "title": infer_title(session, slides),
        "curriculum": curriculum_payload,
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
        default="onboarding/onboarding-session.json",
        type=Path,
        help="Completed onboarding session JSON (default: ./onboarding/onboarding-session.json)",
    )
    parser.add_argument(
        "output_dir",
        nargs="?",
        default="onboarding/learning-module",
        type=Path,
        help="Output directory (default: ./onboarding/learning-module)",
    )
    args = parser.parse_args()

    output_path = build(args.session_file.resolve(), args.output_dir.resolve())
    print(f"Offline learning module written to {output_path}")
    print("Open index.html directly in a modern browser; no package manager or server is required.")


if __name__ == "__main__":
    main()
