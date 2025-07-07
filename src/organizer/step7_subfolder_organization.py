"""Step 7 - Organize C0 folders into their logical instance containers."""

import os
import json
import shutil
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


def load_folder_mapping(json_path: str) -> Dict[str, str]:
    """Load folder mappings from JSON file."""
    with open(json_path, encoding="utf-8") as f:
        return json.load(f)


def classify_and_move_subfolders(
    folder_path: str, mapping: Dict[str, str], simulate: bool
) -> List[List[str]]:
    """Move or merge C0 subfolders into logical containers using the mapping."""
    rows: List[List[str]] = []
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

        if simulate:
            continue

        os.makedirs(dest_dir, exist_ok=True)

        if not os.path.exists(dest_path):
            # simple move if target doesn't exist
            try:
                os.rename(src, dest_path)
            except Exception as e:
                print(f"❌ Failed to move {src} → {dest_path}: {e}")
        else:
            # merge contents into existing dest_path folder
            for item in os.listdir(src):
                item_src = os.path.join(src, item)
                try:
                    shutil.move(item_src, dest_path)
                except Exception as e:
                    print(
                        f"❌ Failed to merge {item_src} into {dest_path}: {e}"
                    )
            # remove the now-empty source folder
            try:
                os.rmdir(src)
            except Exception as e:
                print(f"❌ Failed to remove empty folder {src}: {e}")

    return rows


def is_valid_c0_structure(path: str) -> bool:
    """
    Devuelve True si se cumple alguna de las dos condiciones:
      1. Todas las subcarpetas empiezan con 'C0'.
      2. Todas empiezan con 'C0' y exactamente una se llama:
         '01PrimeraInstancia', '02SegundaInstancia',
         '03RecursosExtraordinarios' o '04Ejecucion'.
    """
    subdirs = [
        d
        for d in os.listdir(path)
        if os.path.isdir(os.path.join(path, d))
    ]
    if not subdirs:
        return False

    # 1) Todas con prefijo C0
    if all(d.upper().startswith("C0") for d in subdirs):
        return True

    # 2) Todas C0 salvo una excepción única
    exceptions = {
        "01primerainstancia",
        "02segundainstancia",
        "03recursosextraordinarios",
        "04ejecucion",
    }
    exc_count = sum(1 for d in subdirs if d.lower() in exceptions)
    if exc_count == 1 and all(
        d.upper().startswith("C0") or d.lower() in exceptions
        for d in subdirs
    ):
        return True

    return False


def process_structure(
    base_path: str, mapping: Dict[str, str], simulate: bool
) -> Tuple[List[List[str]], List[List[str]]]:
    """Process valid folders and report skipped ones."""
    moved: List[List[str]] = []
    skipped: List[List[str]] = []
    targets = get_all_judgment_folders(base_path)

    for folder in targets:
        if is_valid_c0_structure(folder):
            print(folder)
            moved.extend(classify_and_move_subfolders(folder, mapping, simulate))
        else:
            skipped.append([folder])

    return moved, skipped


def run() -> None:
    """Run Step 7."""
    print("🗂️ Step 7: Reorganize C0 folders...")
    print(f"📁 Base path: {config.FOLDER_TO_ORGANIZE}")
    print(f"🧪 Simulate: {config.SIMULATE_STEP_7}")

    confirm = input("❓ Proceed with Step 7? [y/N]: ")
    if confirm.strip().lower() != "y":
        print("❌ Cancelled.")
        return

    folder_mapping = load_folder_mapping(config.FOLDER_MAPPINGS)

    moved, skipped = process_structure(
        config.FOLDER_TO_ORGANIZE, folder_mapping, config.SIMULATE_STEP_7
    )

    if moved:
        write_report(
            step_folder="step_7",
            filename_prefix="c0_folders_moved",
            header=["ORIGINAL_PATH", "NEW_PATH"],
            rows=moved,
        )

    if skipped:
        write_report(
            step_folder="step_7",
            filename_prefix="folders_skipped",
            header=["FOLDER_REQUIRES_MANUAL_REVIEW"],
            rows=skipped,
        )
