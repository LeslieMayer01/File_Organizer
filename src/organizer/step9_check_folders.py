"""Step 9 - Check folder naming conventions and summarize structure.

This script traverses a directory recursively and identifies folders
that do not start with an approved prefix. It generates:

- A report of invalid folder names for manual review.
- A summary report:
  - Valid vs invalid folder count
  - File count in valid folders
  - File count starting with '00IndiceElectronicoC0'
"""

import os
from typing import List

import config
from utils.reports import write_report


VALID_PREFIXES = (
    "05380",
    "01Primera",
    "01Unica",
    "C0",
    "02Segunda",
    "03Recursos",
    "04Ejecucion",
)


def is_valid_folder(folder_name: str) -> bool:
    """Return True if the folder starts with a valid prefix."""
    return folder_name.startswith(VALID_PREFIXES)


def is_index_file(file_name: str) -> bool:
    """Return True if the file starts with 00IndiceElectronicoC0."""
    return file_name.startswith("00IndiceElectronicoC0")


def analyze_folders(root_path: str) -> None:
    """
    Analyze folder structure, collect invalid folders and summary stats.

    Args:
        root_path: The directory to traverse.
    """
    invalid_folders: List[List[str]] = []

    valid_folder_count = 0
    invalid_folder_count = 0
    valid_folder_file_total = 0
    index_file_total = 0

    for current_root, dirs, _ in os.walk(root_path):
        for folder in dirs:
            full_path = os.path.join(current_root, folder)

            if is_valid_folder(folder):
                valid_folder_count += 1

                try:
                    contents = os.listdir(full_path)
                except Exception:
                    continue

                for file_name in contents:
                    file_path = os.path.join(full_path, file_name)
                    if os.path.isfile(file_path):
                        valid_folder_file_total += 1
                        if is_index_file(file_name):
                            index_file_total += 1
            else:
                invalid_folder_count += 1
                invalid_folders.append([folder, full_path])

    write_report(
        step_folder="step_9",
        filename_prefix="invalid_folders",
        header=["Folder Name", "Path"],
        rows=invalid_folders,
    )

    write_report(
        step_folder="step_9",
        filename_prefix="summary",
        header=[
            "Valid Folders",
            "Invalid Folders",
            "Files in Valid Folders",
            "00IndiceElectronicoC0 Files",
        ],
        rows=[
            [
                valid_folder_count,
                invalid_folder_count,
                valid_folder_file_total,
                index_file_total,
            ]
        ],
    )


def run() -> None:
    """Main entry point for Step 9."""
    print("✏️ Step 9: Check Folders...")
    print(f"📁 Folder to process: {config.FOLDER_TO_ORGANIZE}")
    print(f"🧪 Simulation mode: {config.SIMULATE_STEP_9}")

    confirm = input("❓ Do you want to continue? [y/N]: ")
    if confirm.strip().lower() != "y":
        print("🚫 Operation cancelled by user.")
        return

    analyze_folders(config.FOLDER_TO_ORGANIZE)
    print("✅ Reports generated in 'step_9' folder.")
