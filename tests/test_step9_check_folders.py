import os
import pytest
from pathlib import Path
from typing import List
from src.organizer import step9_check_folders


@pytest.mark.parametrize(
    "folder,expected",
    [
        ("05380400000000123456789", True),
        ("01PrimeraInstancia", True),
        ("C01Principal", True),
        ("2023-0001", False),
        ("Aleatorio", False),
    ],
)
def test_is_valid_folder(folder: str, expected: bool) -> None:
    assert step9_check_folders.is_valid_folder(folder) is expected


@pytest.mark.parametrize(
    "filename,expected",
    [
        ("00IndiceElectronicoC005380408900120230013800.xlsm", True),
        ("01 File.pdf", False),
    ],
)
def test_is_index_file(filename: str, expected: bool) -> None:
    assert step9_check_folders.is_index_file(filename) is expected


def test_analyze_folders_generates_reports(
    monkeypatch,
    tmp_path: Path,
) -> None:
    valid = tmp_path / "05380400000000123456789"
    valid.mkdir()
    (valid / "normal.txt").write_text("data")
    (valid / "00IndiceElectronicoC0123.xlsm").write_text("index")

    invalid = tmp_path / "Aleatorio"
    invalid.mkdir()

    reports: List[dict] = []

    def fake_report(step_folder, filename_prefix, header, rows) -> None:
        reports.append(
            {
                "prefix": filename_prefix,
                "header": header,
                "rows": rows,
            }
        )

    monkeypatch.setattr(
        "src.organizer.step9_check_folders.write_report", fake_report
    )

    step9_check_folders.analyze_folders(str(tmp_path))

    assert len(reports) == 2

    invalid_report = next(
        r for r in reports if r["prefix"] == "invalid_folders"
    )
    summary_report = next(r for r in reports if r["prefix"] == "summary")

    assert len(invalid_report["rows"]) == 1
    assert "Aleatorio" in invalid_report["rows"][0][0]

    assert summary_report["rows"][0][0] == 1
    assert summary_report["rows"][0][1] == 1
    assert summary_report["rows"][0][2] == 2
    assert summary_report["rows"][0][3] == 1


def test_analyze_folders_listdir_exception(
    monkeypatch,
    tmp_path: Path,
) -> None:
    valid = tmp_path / "05380400000000123456789"
    valid.mkdir()

    def fail_listdir(path):
        raise OSError("Simulated failure")

    monkeypatch.setattr(os, "listdir", fail_listdir)

    collected = {}

    def fake_report(step_folder, filename_prefix, header, rows):
        collected[filename_prefix] = rows

    monkeypatch.setattr(
        "src.organizer.step9_check_folders.write_report", fake_report
    )

    step9_check_folders.analyze_folders(str(tmp_path))

    assert collected["invalid_folders"] == []
    assert collected["summary"][0][0] == 1
    assert collected["summary"][0][2] == 0
