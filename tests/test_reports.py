"""Unit tests for the shared reports utility module."""

import csv
from pathlib import Path
from typing import List
from utils.reports import write_report
import config


def test_write_report_creates_csv(tmp_path: Path, monkeypatch) -> None:
    """Test that the write_report function generates a valid CSV file."""
    monkeypatch.setattr(config, "REPORTS_DIR", str(tmp_path))
    rows: List[List[str]] = [["File", "/path/to/file.xls"]]

    write_report(
        step_folder="step_test",
        filename_prefix="unit_test",
        header=["Type", "Path"],
        rows=rows,
    )

    report_dir = tmp_path / "step_test"
    report_files = list(report_dir.glob("unit_test_*.csv"))
    assert len(report_files) == 1

    with open(report_files[0], encoding="utf-8") as f:
        reader = csv.reader(f)
        lines = list(reader)
        assert lines[0] == ["Type", "Path"]
        assert lines[1] == ["File", "/path/to/file.xls"]
