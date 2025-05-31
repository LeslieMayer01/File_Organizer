"""Step 5 - Create Internal Folder Structure.

This script searches for folders starting with config.JUDGEMENT_ID inside
config.FOLDER_TO_ORGANIZE and performs restructuring based on folder content:

Scenario 1: Folder contains only files → Move to
/01PrimeraInstancia/C01Principal/
Scenario 2: Folder contains subfolders + files → Rename folders based on a
keyword mapping, and report top-level files needing manual classification
and skipped folders

All changes are logged using write_report(). Behavior depends on
config.SIMULATE_STEP_5.
"""

import os
import json
import re
from typing import List, Optional, Tuple

import config
from utils.reports import write_report


def load_keyword_mapping(json_path: str) -> dict:
    """Load keyword-to-folder mapping from a JSON file."""
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def is_target_folder(folder_name: str) -> bool:
    """Check if a folder name starts with the judgment ID."""
    return folder_name.startswith(config.JUDGEMENT_ID[:5])


def is_file(path: str) -> bool:
    """Check if a path is a file."""
    return os.path.isfile(path)


def normalize_string(text: str) -> str:
    """Normalize a string to lower case and remove accents/spaces."""
    return re.sub(r"[^a-z0-9]", "", text.lower())


def get_matching_key(name: str, mapping: dict) -> Optional[str]:
    """Get standard folder name from a given name using the mapping."""
    normalized = normalize_string(name)
    for target, keywords in mapping.items():
        if any(normalize_string(k) in normalized for k in keywords):
            return target
    return None


def move_all_files(
    source_folder: str, destination_folder: str, simulate: bool
) -> List[List[str]]:
    """Move all files from source to destination."""
    os.makedirs(destination_folder, exist_ok=True)
    moved = []

    for file_name in os.listdir(source_folder):
        source_path = os.path.join(source_folder, file_name)

        # Avoid moving the folders just created (scenario 1 case)
        if os.path.isdir(source_path):
            continue

        dest_path = os.path.join(destination_folder, file_name)
        moved.append([source_path, dest_path])

        if not simulate:
            try:
                os.rename(source_path, dest_path)
            except Exception as e:
                print(f"❌ Failed to move {source_path}: {e}")

    return moved


def rename_subfolders(
    base_path: str,
    subfolder_names: List[str],
    mapping: dict,
    simulate: bool,
) -> Tuple[List[List[str]], List[List[str]], List[List[str]]]:
    """
    Attempt to rename subfolders using keyword mapping.

    Returns:
        - renamed: [from, to]
        - skipped: [path, reason] (no match)
        - conflicted: [path, reason] (name collision)
    """
    rename_plan: List[Tuple[str, str]] = []
    renamed: List[List[str]] = []
    skipped: List[List[str]] = []
    conflicted: List[List[str]] = []

    seen_targets = set()
    collision_targets = set()
    folder_to_dst: dict[str, str] = {}

    for sub in subfolder_names:
        src_path = os.path.join(base_path, sub)
        standard = get_matching_key(sub, mapping)

        if not standard:
            skipped.append([src_path, "Unrecognized keyword"])
            continue

        dst_path = os.path.join(base_path, standard)
        folder_to_dst[src_path] = dst_path

        if dst_path in seen_targets or os.path.exists(dst_path):
            collision_targets.add(dst_path)
        else:
            seen_targets.add(dst_path)
            rename_plan.append((src_path, dst_path))

    if collision_targets:
        print("⚠️ Conflict detected: skipping all renames in this folder.")

        for src_path, dst_path in folder_to_dst.items():
            if dst_path in collision_targets:
                message = (
                    "Conflict: multiple folders target "
                    f"{os.path.basename(dst_path)}"
                )
                conflicted.append([src_path, message])

        return [], skipped, conflicted

    for src, dst in rename_plan:
        renamed.append([src, dst])
        if not simulate:
            try:
                os.rename(src, dst)
            except Exception as error:
                skipped.append([src, f"Rename error: {error}"])

    return renamed, skipped, conflicted


def handle_folder(
    folder_path: str,
    mapping: dict,
    simulate: bool,
) -> Tuple[List[List[str]], List[List[str]], List[List[str]], List[List[str]]]:
    """Delegates processing based on folder content."""
    items = os.listdir(folder_path)
    file_names = [f for f in items if is_file(os.path.join(folder_path, f))]
    folder_names = [
        f for f in items if os.path.isdir(os.path.join(folder_path, f))
    ]

    if not folder_names:
        moved, renamed, orphans = handle_only_files(
            folder_path, file_names, simulate
        )
        return moved, renamed, orphans, []

    return handle_folders_and_files(
        folder_path, folder_names, file_names, mapping, simulate
    )


def handle_only_files(
    folder_path: str,
    file_names: List[str],
    simulate: bool,
) -> Tuple[List[List[str]], List[List[str]], List[List[str]]]:
    """
    Scenario 1: folder contains only files.
    Moves them into 01PrimeraInstancia/C01Principal.
    """
    target = os.path.join(folder_path, "01PrimeraInstancia", "C01Principal")
    moved = move_all_files(folder_path, target, simulate)
    return moved, [], []


def handle_folders_and_files(
    folder_path: str,
    subfolder_names: List[str],
    file_names: List[str],
    mapping: dict,
    simulate: bool,
) -> Tuple[List[List[str]], List[List[str]], List[List[str]], List[List[str]]]:
    """
    Scenario 2: folder has subfolders and possibly files.
    Returns:
        - moved files
        - renamed folders
        - orphans with reason
        - rename errors with reason
    """
    renamed, skipped, conflicted = rename_subfolders(
        folder_path, subfolder_names, mapping, simulate
    )

    rename_errors = skipped + conflicted

    if rename_errors:
        existing_folders = [
            name
            for name in os.listdir(folder_path)
            if os.path.isdir(os.path.join(folder_path, name))
        ]

        reason = (
            "C01Principal exists. Files not moved automatically."
            if "C01Principal" in existing_folders
            else "Rename failed, review manually"
        )

        orphans = [[os.path.join(folder_path, f), reason] for f in file_names]
        return [], renamed, orphans, rename_errors

    # Verifica si ya existe una subcarpeta llamada C01Principal
    subdirs = [
        name
        for name in os.listdir(folder_path)
        if os.path.isdir(os.path.join(folder_path, name))
    ]

    if "C01Principal" not in subdirs:
        moved = move_files_to_new_c01(folder_path, file_names, simulate)
        return moved, renamed, [], []

    orphans = [
        [
            os.path.join(folder_path, f),
            "C01Principal exists. Files not moved automatically.",
        ]
        for f in file_names
    ]

    return [], renamed, orphans, []


def move_files_to_new_c01(
    folder_path: str,
    file_names: List[str],
    simulate: bool,
) -> List[List[str]]:
    """
    Creates 01PrimeraInstancia/C01Principal if needed and moves files there.

    Returns a list of [src, dst] moves (even if simulated).
    """
    target = os.path.join(folder_path, "01PrimeraInstancia", "C01Principal")
    os.makedirs(target, exist_ok=True)

    results: List[List[str]] = []
    for name in file_names:
        src = os.path.join(folder_path, name)
        dst = os.path.join(target, name)
        results.append([src, dst])

        if not simulate:
            try:
                os.rename(src, dst)
            except Exception as error:
                results[-1][1] = f"Error: {error}"

    return results


def find_judgment_folders_recursive(base_path: str) -> List[str]:
    """Find all folders recursively starting with the first 5 digits of ID."""
    folders = []
    for root, dirs, _ in os.walk(base_path):
        for d in dirs:
            if is_target_folder(d):
                folders.append(os.path.join(root, d))
    return folders


def run() -> None:
    """Main entry point to organize internal folder structure."""
    print("\n📂 Step 5: Create Internal Folder Structure")
    print(f"📁 Folder to process: {config.FOLDER_TO_ORGANIZE}")
    print(f"🧪 Simulation mode: {config.SIMULATE_STEP_5}")
    confirm = input("❓ Do you want to continue? [y/N]: ").lower()
    if confirm != "y":
        print("🚫 Operation cancelled.")
        return

    mapping = load_keyword_mapping(config.KEYWORDS_JSON)
    target_folders = find_judgment_folders_recursive(config.FOLDER_TO_ORGANIZE)
    all_moved = []
    all_renamed = []
    all_orphans = []
    all_rename_issues = []

    for folder in target_folders:
        moved, renamed, orphans, rename_issues = handle_folder(
            folder, mapping, simulate=config.SIMULATE_STEP_5
        )
        all_moved.extend(moved)
        all_renamed.extend(renamed)
        all_orphans.extend(orphans)
        all_rename_issues.extend(rename_issues)

    write_report(
        step_folder="step_5",
        filename_prefix="moved_files",
        header=["From", "To"],
        rows=all_moved,
    )

    write_report(
        step_folder="step_5",
        filename_prefix="skipped_folder_renames",
        header=["Folder Path", "Reason"],
        rows=all_rename_issues,
    )

    write_report(
        step_folder="step_5",
        filename_prefix="renamed_folders",
        header=["Original Name", "New Name"],
        rows=all_renamed,
    )

    write_report(
        step_folder="step_5",
        filename_prefix="manual_review_files",
        header=["Unclassified File Path", "Reason"],
        rows=all_orphans,
    )
