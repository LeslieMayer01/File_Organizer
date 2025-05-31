"""Step 6 - Organize and rename files inside C0 folders."""

import os
import re
from collections import defaultdict
from typing import List, Tuple, DefaultDict

import config
from utils.reports import write_report


def normalize_filename(name: str) -> str:
    """Clean file name by removing special characters and limiting length."""
    name = re.sub(r"^[^a-zA-Z]*", "", name)
    name = re.sub(r"[^a-zA-Z0-9]", "", name)
    return name[:36]


def build_final_name(
    index: int,
    base_name: str,
    extension: str,
    counter: int,
) -> str:
    """Build the final file name with leading index and optional counter."""
    clean_name = f"{base_name}{counter:02d}" if counter > 0 else base_name
    return f"{index:02d}{clean_name}{extension}"


def should_process(file: str) -> bool:
    """Return True if file is eligible for processing."""
    return not file.lower().startswith("xcontrol")


def sort_files(files: List[str], root: str) -> List[str]:
    """Sort files based on naming or modification date."""
    all_numeric = all(re.match(r"^\d+", f) for f in files)

    if all_numeric:
        key_len = 3 if len(files) > 100 else 2
        return sorted(files, key=lambda x: x[:key_len], reverse=True)

    return sorted(files, key=lambda x: os.path.getmtime(os.path.join(root, x)))


def rename_file(
    index: int, file: str, used: defaultdict, root: str, simulate: bool
) -> Tuple[List[str], List[str]]:
    """Attempt to rename a file and return result or error row."""
    old_path = os.path.join(root, file)
    base, ext = os.path.splitext(file)
    clean = normalize_filename(base)
    count = used[clean]
    new_name = build_final_name(index, clean, ext, count)
    new_path = os.path.join(root, new_name)
    used[clean] += 1

    if simulate:
        return (
            [file, new_name, old_path, new_path, "SIMULATED", str(index)],
            [],
        )

    try:
        os.rename(old_path, new_path)
        return (
            [file, new_name, old_path, new_path, "RENAMED", str(index)],
            [],
        )
    except Exception as e:
        return (
            [],
            [file, old_path, str(e)],
        )


def process_directory(
    path: str, simulate: bool
) -> Tuple[List[List[str]], List[List[str]]]:
    """Rename and sort files in each subfolder of the given directory."""
    success_rows = []
    error_rows = []

    for root, _, files in os.walk(path):
        valid_files = [f for f in files if should_process(f)]
        if not valid_files:
            continue

        sorted_files = sort_files(valid_files, root)
        used_names: DefaultDict[str, int] = defaultdict(int)

        for i, file in enumerate(sorted_files, 1):
            renamed, error = rename_file(i, file, used_names, root, simulate)
            if renamed:
                success_rows.append(renamed)
            if error:
                error_rows.append(error)

    return success_rows, error_rows


def run() -> None:
    """Run Step 5: organize and rename files in C0 folders."""
    print("✏️ Step 6: Organize files in C0 folders...")
    print(f"📁 Folder to process: {config.FOLDER_TO_ORGANIZE}")
    print(f"🧪 Simulation mode: {config.SIMULATE_STEP_6}")

    confirm = input("❓ Do you want to continue? [y/N]: ")
    if confirm.strip().lower() != "y":
        print("🚫 Operation cancelled by user.")
        return

    renamed, errors = process_directory(
        config.FOLDER_TO_ORGANIZE, config.SIMULATE_STEP_6
    )

    if renamed:
        write_report(
            step_folder="step_6",
            filename_prefix="organized_files",
            header=[
                "OLD_NAME",
                "NEW_NAME",
                "OLD_PATH",
                "NEW_PATH",
                "STATUS",
                "ORDER",
            ],
            rows=renamed,
        )

    if errors:
        write_report(
            step_folder="step_6",
            filename_prefix="manual_review_files",
            header=["FILENAME", "PATH", "ERROR"],
            rows=errors,
        )
