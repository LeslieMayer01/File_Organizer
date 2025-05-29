"""Step 6 - Organize C0 folders into their logical instance containers."""

import os
import json
from typing import List, Dict, Tuple

import config
from utils.reports import write_report


def is_target_folder(name: str) -> bool:
    """Check if folder starts with the configured JUDGEMENT_ID."""
    return name.startswith(config.JUDGEMENT_ID)


def get_all_judgment_folders(base_path: str) -> List[str]:
    """Recursively find all folders starting with JUDGEMENT_ID."""
    matches = []
    for root, dirs, _ in os.walk(base_path):
        for d in dirs:
            if is_target_folder(d):
                full = os.path.join(root, d)
                if os.path.isdir(full):
                    matches.append(full)
    return matches


def is_c0_structure_only(path: str) -> bool:
    """Check if all subfolders in the path start with 'C0'."""
    children = os.listdir(path)
    return all(
        os.path.isdir(os.path.join(path, child))
        and child.upper().startswith("C0")
        for child in children
    )


def load_folder_mapping(json_path: str) -> Dict[str, str]:
    """Load folder mappings from JSON file."""
    with open(json_path, encoding="utf-8") as f:
        return json.load(f)


def has_only_c01_folder(path: str) -> bool:
    """
    Check if the folder only contains a single
    '01PrimeraInstancia' folder.
    """
    children = [
        child
        for child in os.listdir(path)
        if os.path.isdir(os.path.join(path, child))
    ]
    return len(children) == 1 and children[0] == "01PrimeraInstancia"


def classify_and_move_subfolders(
    folder_path: str, mapping: Dict[str, str], simulate: bool
) -> List[List[str]]:
    """Move subfolders into logical containers using the mapping."""
    rows = []
    for name in os.listdir(folder_path):
        src = os.path.join(folder_path, name)

        if not os.path.isdir(src) or not name.upper().startswith("C0"):
            continue

        prefix = name[:3].upper()
        instance = mapping.get(prefix)

        if not instance:
            continue  # skip unknown C0 codes

        dest_dir = os.path.join(folder_path, instance)
        dest_path = os.path.join(dest_dir, name)
        rows.append([src, dest_path])

        if not simulate:
            os.makedirs(dest_dir, exist_ok=True)
            try:
                os.rename(src, dest_path)
            except Exception as e:
                print(f"❌ Failed to move {src}: {e}")
    return rows


def process_structure(
    base_path: str, mapping: Dict[str, str], simulate: bool
) -> Tuple[List[List[str]], List[List[str]]]:
    """Process valid folders and report skipped ones."""
    moved: List[List[str]] = []
    skipped: List[List[str]] = []

    targets = get_all_judgment_folders(base_path)
    for folder in targets:
        if is_c0_structure_only(folder) or has_only_c01_folder(folder):
            rows = classify_and_move_subfolders(folder, mapping, simulate)
            moved.extend(rows)
        else:
            skipped.append([folder])

    return moved, skipped


def run() -> None:
    """Run Step 6."""
    print("🗂️ Step 6: Reorganize C0 folders...")
    print(f"📁 Base path: {config.FOLDER_TO_ORGANIZE}")
    print(f"🧪 Simulate: {config.SIMULATE_STEP_6}")

    confirm = input("❓ Proceed with Step 6? [y/N]: ")
    if confirm.strip().lower() != "y":
        print("❌ Cancelled.")
        return

    folder_mapping = load_folder_mapping(config.FOLDER_MAPPINGS)

    moved, skipped = process_structure(
        config.FOLDER_TO_ORGANIZE, folder_mapping, config.SIMULATE_STEP_6
    )

    if moved:
        write_report(
            step_folder="step_6",
            filename_prefix="c0_folders_moved",
            header=["ORIGINAL_PATH", "NEW_PATH"],
            rows=moved,
        )

    if skipped:
        write_report(
            step_folder="step_6",
            filename_prefix="folders_skipped",
            header=["FOLDER_REQUIRES_MANUAL_REVIEW"],
            rows=skipped,
        )
