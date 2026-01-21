#!/usr/bin/env python3
"""
Script to create a new app package under src/app using templates.

This script copies template files from scripts/_scratch/app_template to
src/app/<app_name> and replaces placeholders in both filenames and file contents.

Usage:
    python scripts/create_app.py myapp

Creates:
    src/app/<app_name>/... based on templates.

The script is idempotent: it won't overwrite existing files unless --force is passed.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Define important project paths
ROOT = Path(__file__).resolve().parents[1]  # repository root
SRC_APP = ROOT / "src" / "app"
TESTS_DIR = ROOT / "tests"
TEMPLATE_DIR = ROOT / "scripts" / "_scratch" / "app_template"

# Regex for validating app name (snake_case)
VALID_NAME = re.compile(r"^[a-z_][a-z0-9_]*$")


def to_class_name(name: str) -> str:
    """Convert snake_case to PascalCase for class names."""
    parts = name.split("_")
    return "".join(p.capitalize() for p in parts)


def process_template_file(
        src_path: Path, dest_path: Path, app_name: str, class_name: str, force: bool = False
):
    """
    Read a template file, replace placeholders, and write to destination.

    Args:
        src_path: Path to the template file.
        dest_path: Path to write the processed file.
        app_name: The app's snake_case name.
        class_name: The app's PascalCase class name.
        force: Overwrite existing files if True.

    Returns:
        True if file was created, False otherwise.
    """
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    if dest_path.exists() and not force:
        return False

    try:
        content = src_path.read_text(encoding="utf-8")
        content = content.replace("{{app_name}}", app_name)
        content = content.replace("{{ClassName}}", class_name)

        dest_path.write_text(content, encoding="utf-8")
        return True
    except Exception as e:
        print(f"Error processing {src_path}: {e}")
        return False


def main() -> None:
    """Parse arguments and create a new app from templates."""
    parser = argparse.ArgumentParser(description="Create a new app under src/app using templates")
    parser.add_argument("name", help="App name (snake_case). Example: my_feature")
    parser.add_argument("-f", "--force", action="store_true", help="Overwrite existing files")
    args = parser.parse_args()

    name = args.name.strip()
    if not VALID_NAME.match(name):
        parser.error(
            "App name must be snake_case: lowercase letters, digits and underscores, starting with a letter or underscore"
        )

    if not TEMPLATE_DIR.exists():
        print(f"Error: Template directory not found at {TEMPLATE_DIR}")
        sys.exit(1)

    app_dir = SRC_APP / name
    class_name = to_class_name(name)

    print(f"Creating app '{name}'...")

    created_count = 0

    # Walk through the template directory and process each file
    for src_path in TEMPLATE_DIR.rglob("*"):
        if src_path.is_dir():
            continue

        # Determine relative path from template root
        rel_path = src_path.relative_to(TEMPLATE_DIR)

        # Determine filename (remove -tpl suffix)
        file_name = rel_path.name
        if file_name.endswith("-tpl"):
            file_name = file_name[:-4]  # Remove last 4 chars (-tpl)

        # Replace placeholders in filename
        file_name = file_name.replace("{{app_name}}", name)

        # Determine destination path
        if rel_path.parts[0] == "tests":
            # Files in 'tests' folder go to tests/app/<app_name>/
            dest_rel_path = rel_path.relative_to("tests").parent / file_name
            dest_path = TESTS_DIR / "app" / name / dest_rel_path
        else:
            dest_rel_path = rel_path.parent / file_name
            dest_path = app_dir / dest_rel_path

        # Process the file
        if process_template_file(src_path, dest_path, name, class_name, args.force):
            created_count += 1

    if created_count == 0:
        print("No files created.")
    else:
        print(f"Successfully created app '{name}' with {created_count} files.")


if __name__ == "__main__":
    main()
