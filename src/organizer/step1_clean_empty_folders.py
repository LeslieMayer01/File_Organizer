# step1_clean_empty_folders.py

"""
Step 1 - Cleanup Script

This script lists and optionally deletes Excel index files and empty folders
from the specified base path. It logs the results into CSV files for auditing.
"""

import csv
import os
from datetime import datetime
from typing import List, Tuple

import config


def is_excel_file(filename: str) -> bool:
    """Check if the filename is an Excel file (.xls or .xlsx)."""
    return filename.lower().endswith((".xls", ".xlsx"))


def contains_index_keyword(name: str) -> bool:
    """Check if the filename contains the word 'indice' (case-insensitive)."""
    return "indice" in name.lower()


def generate_report_filename(base_path: str, prefix: str) -> str:
    """Generate a timestamped CSV filename."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return os.path.join(base_path, f"{prefix}_{timestamp}.csv")


def find_index_excel_files(base_path: str) -> List[str]:
    """Recursively find Excel files that contain 'indice' in the filename."""
    matches = []
    for dirpath, _, filenames in os.walk(base_path):
        for filename in filenames:
            if is_excel_file(filename) and contains_index_keyword(filename):
                matches.append(os.path.join(dirpath, filename))
    return matches


def write_csv(file_path: str, header: List[str], rows: List[List[str]]) -> None:
    """Write data to a CSV file."""
    with open(file_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)


def delete_items(base_path: str, dry_run: bool = True) -> List[Tuple[str, str]]:
    """
    Delete Excel files with 'indice' in the name and empty directories.
    Returns a list of deletions (type, path).
    """
    deleted_items = []

    for dirpath, _, filenames in os.walk(base_path, topdown=False):
        for filename in filenames:
            if is_excel_file(filename) and contains_index_keyword(filename):
                file_path = os.path.join(dirpath, filename)
                if not dry_run:
                    try:
                        os.remove(file_path)
                        print(f"✅ Deleted file: {file_path}")
                    except Exception as e:
                        print(f"❌ Failed to delete file {file_path}: {e}")
                deleted_items.append(("File", file_path))

        if not os.listdir(dirpath):
            if not dry_run:
                try:
                    os.rmdir(dirpath)
                    print(f"✅ Deleted empty folder: {dirpath}")
                except Exception as e:
                    print(f"❌ Failed to delete folder {dirpath}: {e}")
            deleted_items.append(("Folder", dirpath))

    return deleted_items


def run() -> None:
    """Execute the cleanup process and save reports."""
    print("🧹 Step 1: Cleaning empty folders and index files...")

    perform_deletions = True

    index_report_path = generate_report_filename(
        config.REPORTS_DIR, "step1_index_files"
    )
    deletion_report_path = generate_report_filename(
        config.REPORTS_DIR, "step1_deleted_items"
    )

    index_files = find_index_excel_files(config.FOLDER_TO_ORGANIZE)
    write_csv(index_report_path, ["File Path"], [[f] for f in index_files])
    print(f"ℹ️ Saved {len(index_files)} index files to {index_report_path}")

    deleted_items = delete_items(
        config.FOLDER_TO_ORGANIZE, dry_run=not perform_deletions
    )
    write_csv(
        deletion_report_path, ["Type", "Path"], [[t, p] for t, p in deleted_items]
    )
    print(f"📊 Deletion report saved to {deletion_report_path}")
