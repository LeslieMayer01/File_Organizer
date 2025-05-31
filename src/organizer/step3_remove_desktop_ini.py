"""
Step 3 - Remove desktop.ini files

This script recursively scans the directory defined in
config.FOLDER_TO_ORGANIZEand removes all `desktop.ini` files
it finds. It supports simulation mode through
config.SIMULATE_STEP_3 and generates a report using the
write_report function.
"""

import os
from typing import List, Tuple

import config
from utils.reports import write_report


def run() -> None:
    """
    Entry point for Step 3.
    Deletes all desktop.ini files under config.FOLDER_TO_ORGANIZE.
    Generates a report with the paths of the files removed or that
    would be removed.
    """
    print("🧹 Step 3: Removing desktop.ini files...")

    deleted = remove_desktop_ini_files(
        root_path=config.FOLDER_TO_ORGANIZE,
        simulate=config.SIMULATE_STEP_3,
    )

    if deleted:
        write_report(
            step_folder="step_3",
            filename_prefix="deleted_desktop_files",
            header=["Type", "Path"],
            rows=[[typ, path] for typ, path in deleted],
        )
        print("✅ Report generated.")
    else:
        print("✅ No desktop.ini files found.")


def remove_desktop_ini_files(
    root_path: str, simulate: bool
) -> List[Tuple[str, str]]:
    """
    Find and remove all desktop.ini files within the given directory tree.

    Args:
        root_path (str): Root folder to start searching.
        simulate (bool): If True, no files will actually be deleted.

    Returns:
        List[Tuple[str, str]]: List of tuples with (Type, FilePath),
        where Type is 'Simulated' or 'Deleted'.
    """
    results: List[Tuple[str, str]] = []

    for current_root, _, files in os.walk(root_path):
        for file_name in files:
            if file_name.lower() == "desktop.ini":
                file_path = os.path.join(current_root, file_name)
                if simulate:
                    results.append(("Simulated", file_path))
                else:
                    try:
                        os.remove(file_path)
                        results.append(("Deleted", file_path))
                    except Exception as error:
                        results.append(("Error", f"{file_path} ({error})"))

    return results
