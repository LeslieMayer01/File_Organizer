"""
Module: step2_delete_index_files.py

This script finds and deletes Excel files that contain the keyword
'indice' in their filenames, inside a specified folder. All changes
(or simulations) are reported in CSV files.
"""

import os
from typing import List, Tuple

import config
from utils.reports import write_report


def is_excel_file(filename: str) -> bool:
    """Check if the given filename corresponds to an Excel file.

    Args:
        filename (str): Name of the file to check.

    Returns:
        bool: True if file is .xls, .xlsx or .xlsm.
    """
    return filename.lower().endswith((".xls", ".xlsx", ".xlsm"))


def contains_index_keyword(name: str) -> bool:
    """Check whether the filename contains the keyword 'indice'.

    Args:
        name (str): The filename to inspect.

    Returns:
        bool: True if the keyword is found.
    """
    return "indice" in name.lower()


def find_index_files(base_path: str) -> List[str]:
    """Recursively search for Excel files containing 'indice' in the name.

    Args:
        base_path (str): The root folder to scan.

    Returns:
        List[str]: List of matching file paths.
    """
    matches = []
    for dirpath, _, filenames in os.walk(base_path):
        for filename in filenames:
            if is_excel_file(filename) and contains_index_keyword(filename):
                matches.append(os.path.join(dirpath, filename))
    return matches


def delete_files(
    file_paths: List[str],
    simulate: bool = True,
) -> List[Tuple[str, str]]:
    """Delete files listed or simulate deletion.

    Args:
        file_paths (List[str]): List of file paths.
        simulate (bool): Whether to simulate or perform the operation.

    Returns:
        List[Tuple[str, str]]: Deleted (or simulated) file entries.
    """
    deleted = []
    for file in file_paths:
        if simulate:
            deleted.append(("File", file))
        else:
            try:
                os.remove(file)
                print(f"✅ Deleted: {file}")
                deleted.append(("File", file))
            except Exception as e:
                print(f"❌ Error deleting {file}: {e}")
    return deleted


def run() -> None:
    """Main execution method for Step 2.

    Prompts user to confirm execution. Then finds, optionally deletes,
    and logs all index-related Excel files found.
    """
    print("\n🧹 Step 2: Delete Index Files")
    print(f"📁 Folder to process: {config.FOLDER_TO_ORGANIZE}")
    print(f"🧪 Simulation mode: {config.SIMULATE_STEP_2}")

    confirm = input("❓ Do you want to continue? [y/N]: ")
    if confirm.strip().lower() != "y":
        print("🚫 Operation cancelled by user.")
        return

    index_files = find_index_files(config.FOLDER_TO_ORGANIZE)
    deleted = delete_files(index_files, simulate=config.SIMULATE_STEP_2)
    write_report(
        step_folder="step_2",
        filename_prefix="deleted_index_files",
        header=["Type", "Path"],
        rows=[[typ, path] for typ, path in deleted],
    )
