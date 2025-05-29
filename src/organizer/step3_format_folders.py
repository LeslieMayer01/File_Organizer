"""
Module: step3_format_folders.py

This script renames folders in a specified directory so that they follow
an expected naming convention: 23 digits derived from a process number
pattern. It logs all rename actions and conflicts in timestamped CSV reports.
The behavior is controlled by a simulation flag (SIMULATE_STEP_3).
"""

import os
import re
from typing import Optional, List

import config
from utils.reports import write_report


def clean_name(name: str) -> str:
    """Remove all non-alphanumeric characters from a string.

    Args:
        name (str): Input string.

    Returns:
        str: Cleaned string with only alphanumerics.
    """
    return re.sub(r"[^A-Za-z0-9]", "", name)


def extract_new_name(original: str) -> Optional[str]:
    """Generate a 23-digit folder name based on process number in the name.

    Args:
        original (str): Original folder name.

    Returns:
        Optional[str]: Formatted name or None if pattern not found.
    """
    match = re.search(r"(\d{4}-\d+)", original)
    if not match:
        return None

    number = match.group(1).replace("-", "")

    suffix = clean_name(original.replace(match.group(1), "").strip())
    new_name = f"{config.JUDGEMENT_ID}{number}00"

    if suffix:
        new_name += f" {suffix}"

    return new_name[:40]


def find_folders_to_rename(base_path: str) -> List[tuple[str, str, str]]:
    """Identify folders to rename and generate their new names.

    Args:
        base_path (str): Base directory to search.

    Returns:
        List[tuple[str, str, str]]: (parent_path, original_name, new_name)
    """
    folders = []
    for dirpath, dirnames, _ in os.walk(base_path):
        for name in dirnames:
            if re.fullmatch(r"\d{23}", name):
                continue

            new_name = extract_new_name(name)
            if new_name:
                folders.append((dirpath, name, new_name))
    return folders


def rename_folders(
    entries: List[tuple[str, str, str]], simulate: bool
) -> tuple[List[List[str]], List[List[str]], List[List[str]]]:
    """Rename or simulate renaming of folders.

    Returns:
        Tuple of:
        - renamed: successful renames
        - conflicts: target path already exists
        - errors: unexpected errors during rename
    """
    renamed = []
    conflicts = []
    errors = []

    for dirpath, old_name, new_name in entries:
        old_path = os.path.join(dirpath, old_name)
        new_path = os.path.join(dirpath, new_name)

        if os.path.exists(new_path):
            conflicts.append([old_path, new_name])
            continue

        renamed.append([old_path, old_name, new_name])

        if simulate:
            print(f"ℹ️ (Simulated) Rename: {old_name} -> {new_name}")
        else:
            try:
                os.rename(old_path, new_path)
                print(f"✅ Renamed: {old_name} -> {new_name}")
            except Exception as e:
                print(f"❌ Failed to rename {old_path} -> {new_name}: {e}")
                errors.append([old_path, new_name, str(e)])

    return renamed, conflicts, errors


def run() -> None:
    """Run the folder renaming process, respecting simulation flag."""
    print("\n🗂️ Step 3: Format Folder Names")
    print(f"📁 Folder to process: {config.FOLDER_TO_ORGANIZE}")
    print(f"🧪 Simulation mode: {config.SIMULATE_STEP_3}")

    confirm = input("❓ Do you want to continue? [y/N]: ")
    if confirm.strip().lower() != "y":
        print("🚫 Operation cancelled by user.")
        return

    entries = find_folders_to_rename(config.FOLDER_TO_ORGANIZE)
    try:
        renamed, conflicts, errors = rename_folders(
            entries,
            simulate=config.SIMULATE_STEP_3,
        )
    except Exception as e:
        print(f"❌ Error while executing step 3: {e}")
        renamed, conflicts, errors = [], [], [["general", "run()", str(e)]]

    write_report(
        step_folder="step_3",
        filename_prefix="formatted_folders",
        header=["Path", "Original Name", "New Name"],
        rows=renamed,
    )

    write_report(
        step_folder="step_3",
        filename_prefix="conflicts",
        header=["Path", "Conflicting Name"],
        rows=conflicts,
    )

    if errors:
        write_report(
            step_folder="step_3",
            filename_prefix="rename_errors",
            header=["Path", "Target Name", "Error"],
            rows=errors,
        )
