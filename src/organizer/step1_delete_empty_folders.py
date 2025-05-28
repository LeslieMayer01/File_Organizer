"""
Module: step1_delete_empty_folders.py

This script identifies and deletes empty folders inside a given base
directory. The behavior is controlled by a simulation flag in the config
file, and all operations (real or simulated) are logged into a timestamped
CSV report.
"""

import os
from typing import List, Tuple

import config
from utils.reports import write_report


def is_folder_empty(folder_path: str) -> bool:
    """Check whether a folder is empty.

    Args:
        folder_path (str): Path to the folder.

    Returns:
        bool: True if empty, False otherwise.
    """
    return not os.listdir(folder_path)


def find_empty_folders(base_path: str) -> List[str]:
    """Recursively find all empty folders within the given base path.

    Args:
        base_path (str): Path to start searching from.

    Returns:
        List[str]: List of empty folder paths.
    """
    empty_folders = []
    for dirpath, _, _ in os.walk(base_path, topdown=False):
        if not os.listdir(dirpath):
            empty_folders.append(dirpath)
    return empty_folders


def delete_folders(
    folder_paths: List[str], simulate: bool = True
) -> List[Tuple[str, str]]:
    """Delete folders from the list, or simulate the deletion.

    Args:
        folder_paths (List[str]): List of folder paths to delete.
        simulate (bool): If True, don't actually delete.

    Returns:
        List[Tuple[str, str]]: List of deleted (or simulated) folder entries.
    """
    deleted = []
    for folder in folder_paths:
        if simulate:
            deleted.append(("Folder", folder))
        else:
            try:
                os.rmdir(folder)
                print(f"✅ Deleted: {folder}")
                deleted.append(("Folder", folder))
            except Exception as e:
                print(f"❌ Error deleting {folder}: {e}")
    return deleted


def run() -> None:
    """Run the deletion process for empty folders.

    This function checks simulation flags, asks for user confirmation,
    and processes deletions accordingly.
    """
    print("\n🧹 Step 1: Delete Empty Folders")
    print(f"📁 Folder to process: {config.FOLDER_TO_ORGANIZE}")
    print(f"🧪 Simulation mode: {config.SIMULATE_STEP_1}")

    confirm = input("❓ Do you want to continue? [y/N]: ")
    if confirm.strip().lower() != "y":
        print("🚫 Operation cancelled by user.")
        return

    empty_folders = find_empty_folders(config.FOLDER_TO_ORGANIZE)
    deleted = delete_folders(empty_folders, simulate=config.SIMULATE_STEP_1)
    write_report(
        step_folder="step_1",
        filename_prefix="deleted_empty_folders",
        header=["Type", "Path"],
        rows=[[typ, path] for typ, path in deleted],
    )
