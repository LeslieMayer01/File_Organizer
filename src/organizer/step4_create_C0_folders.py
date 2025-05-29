"""Step 4 - Create Internal Folder Structure.

This script searches for folders starting with config.JUDGEMENT_ID inside
config.FOLDER_TO_ORGANIZE and performs restructuring based on folder content:

Scenario 1: Folder contains only files → Move to
/01PrimeraInstancia/C01Principal/
Scenario 2: Folder contains subfolders + files → Rename folders based on a
keyword mapping, and report top-level files needing manual classification
and skipped folders

All changes are logged using write_report(). Behavior depends on
config.SIMULATE_STEP_4.
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
    base_path: str, subfolder_names: List[str], mapping: dict, simulate: bool
) -> Tuple[List[List[str]], List[List[str]]]:
    """Rename subfolders using a keyword mapping with conflict prevention.

    If multiple folders map to the same destination name, none will be renamed.

    Args:
        base_path (str): Parent folder path.
        subfolder_names (List[str]): List of current subfolder names.
        mapping (dict): Keyword mapping to standardized folder names.
        simulate (bool): If True, do not apply changes.

    Returns:
        Tuple:
            - List of successfully renamed folders.
            - List of skipped folders due to unknown match or conflict.
    """
    rename_plan: List[Tuple[str, str]] = []
    skipped: List[List[str]] = []

    seen_targets = set()
    collision_detected = False

    for sub in subfolder_names:
        src_path = os.path.join(base_path, sub)
        standard = get_matching_key(sub, mapping)

        if not standard:
            skipped.append([src_path])
            continue

        dst_path = os.path.join(base_path, standard)

        if dst_path in seen_targets:
            collision_detected = True
            skipped.append([src_path])
        else:
            seen_targets.add(dst_path)
            rename_plan.append((src_path, dst_path))

    if collision_detected:
        print("⚠️ Conflict detected: skipping all renames in this folder.")
        return [], skipped + [[src for src, _ in rename_plan]]

    renamed: List[List[str]] = []
    for src, dst in rename_plan:
        renamed.append([src, dst])
        if not simulate:
            try:
                os.rename(src, dst)
            except Exception as e:
                print(f"❌ Failed to rename {src} → {dst}: {e}")
                skipped.append([src])

    return renamed, skipped


def handle_folder(
    folder_path: str, mapping: dict, simulate: bool
) -> Tuple[List[List[str]], List[List[str]], List[List[str]]]:
    """Process one folder and restructure contents."""
    # ⚠️ Evalúa estado ANTES de crear nuevas carpetas
    items = os.listdir(folder_path)
    file_paths = [f for f in items if is_file(os.path.join(folder_path, f))]
    folder_names = [
        f
        for f in items
        if os.path.isdir(
            os.path.join(folder_path, f),
        )
    ]

    moved_files: List[List[str]] = []
    renamed_folders: List[List[str]] = []
    orphaned_files: List[List[str]] = []

    is_solo_files = len(folder_names) == 0

    if is_solo_files:
        # ✅ Escenario 1: solo archivos — crear destino y mover
        target_path = os.path.join(
            folder_path,
            "01PrimeraInstancia",
            "C01Principal",
        )

        moved_files = move_all_files(
            folder_path,
            target_path,
            simulate=simulate,
        )
    else:
        # ✅ Escenario 2: carpetas y posiblemente archivos
        renamed_folders, _ = rename_subfolders(
            folder_path, folder_names, mapping, simulate
        )

        for f in file_paths:
            full_path = os.path.join(folder_path, f)
            orphaned_files.append([full_path])

    return moved_files, renamed_folders, orphaned_files


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
    print("\n📂 Step 4: Create Internal Folder Structure")
    print(f"📁 Folder to process: {config.FOLDER_TO_ORGANIZE}")
    print(f"🧪 Simulation mode: {config.SIMULATE_STEP_4}")
    confirm = input("❓ Do you want to continue? [y/N]: ").lower()
    if confirm != "y":
        print("🚫 Operation cancelled.")
        return

    mapping = load_keyword_mapping(config.KEYWORDS_JSON)
    target_folders = find_judgment_folders_recursive(config.FOLDER_TO_ORGANIZE)
    all_moved = []
    all_renamed = []
    all_orphans = []

    for folder in target_folders:
        moved, renamed, orphans = handle_folder(
            folder, mapping, simulate=config.SIMULATE_STEP_4
        )
        all_moved.extend(moved)
        all_renamed.extend(renamed)
        all_orphans.extend(orphans)

    write_report(
        step_folder="step_4",
        filename_prefix="moved_files",
        header=["From", "To"],
        rows=all_moved,
    )

    write_report(
        step_folder="step_4",
        filename_prefix="renamed_folders",
        header=["Original Name", "New Name"],
        rows=all_renamed,
    )

    write_report(
        step_folder="step_4",
        filename_prefix="manual_review_files",
        header=["Unclassified File Path"],
        rows=all_orphans,
    )
