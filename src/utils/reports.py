"""Shared utilities for writing reports in CSV format."""

import os
import csv
from datetime import datetime
from typing import List

import config


def write_report(
    step_folder: str,
    filename_prefix: str,
    header: List[str],
    rows: List[List[str]],
) -> None:
    """Write a CSV report to a timestamped file.

    Args:
        step_folder (str): Subfolder (e.g. 'step_1', 'step_2') to organize
        reports.
        filename_prefix (str): Prefix for the output file.
        header (List[str]): List of column headers.
        rows (List[List[str]]): Data to be written as CSV rows.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    step_dir = os.path.join(config.REPORTS_DIR, step_folder)
    os.makedirs(step_dir, exist_ok=True)

    report_path = os.path.join(step_dir, f"{filename_prefix}_{timestamp}.csv")
    with open(report_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)

    print(f"📄 Report saved: {report_path}")
