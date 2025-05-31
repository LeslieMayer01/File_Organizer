"""Tests for step9_check_folders.py."""

from pathlib import Path
import shutil

import pytest

from src.organizer.step9_check_folders import (
    is_valid_folder,
    is_index_file,
)


@pytest.mark.parametrize(
    "folder_name,expected",
    [
        ("C01Principal", True),
        ("01PrimeraInstancia", True),
        ("02SegundaInstancia", True),
        ("03RecursosExtraordinarios", True),
        ("Z01Incorrecta", False),
        ("random", False),
    ],
)
def test_is_valid_folder(folder_name: str, expected: bool) -> None:
    assert is_valid_folder(folder_name) is expected


@pytest.mark.parametrize(
    "file_name,expected",
    [
        ("00IndiceElectronicoC0123.xlsm", True),
        ("00IndiceElectronicoC0999.doc", True),
        ("IndiceElectronicoC0123.xlsm", False),
        ("Z01Documento.pdf", False),
    ],
)
def test_is_index_file(file_name: str, expected: bool) -> None:
    assert is_index_file(file_name) is expected


def test_analyze_folders_all_valid(tmp_path: Path, monkeypatch) -> None:
    """Should count valid folders and index files correctly."""
    from src.organizer import step9_check_folders

    monkeypatch.setattr(
        step9_check_folders.config, "FOLDER_TO_ORGANIZE", str(tmp_path)
    )

    valid = tmp_path / "C01Folder"
    valid.mkdir()
    (valid / "doc1.pdf").write_text("ok")
    (valid / "doc2.docx").write_text("ok")
    (valid / "00IndiceElectronicoC0123.xlsm").write_text("index")

    step9_check_folders.analyze_folders(str(tmp_path))

    report_folder = tmp_path.parent / "reports" / "step_9"
    assert (report_folder / "summary.csv").exists()
    assert (report_folder / "invalid_folders.csv").exists()

    summary = (report_folder / "summary.csv").read_text()
    assert "1,0,3,1" in summary


def test_analyze_folders_all_invalid(tmp_path: Path, monkeypatch) -> None:
    """Should list all folders as invalid and skip file analysis."""
    from src.organizer import step9_check_folders

    monkeypatch.setattr(
        step9_check_folders.config, "FOLDER_TO_ORGANIZE", str(tmp_path)
    )

    invalid = tmp_path / "Z99Otra"
    invalid.mkdir()
    (invalid / "file.pdf").write_text("x")

    step9_check_folders.analyze_folders(str(tmp_path))

    report = tmp_path.parent / "reports" / "step_9" / "invalid_folders.csv"
    assert report.exists()
    content = report.read_text()
    assert "Z99Otra" in content


def test_analyze_folders_mixed_structure(tmp_path: Path, monkeypatch) -> None:
    """Should count valid and invalid folders together."""
    from src.organizer import step9_check_folders

    monkeypatch.setattr(
        step9_check_folders.config, "FOLDER_TO_ORGANIZE", str(tmp_path)
    )

    valid = tmp_path / "C01Data"
    valid.mkdir()
    (valid / "00IndiceElectronicoC0555.xlsm").write_text("ok")

    invalid = tmp_path / "Random"
    invalid.mkdir()
    (invalid / "file.doc").write_text("x")

    step9_check_folders.analyze_folders(str(tmp_path))

    summary = (
        tmp_path.parent / "reports" / "step_9" / "summary.csv"
    ).read_text()
    assert "1,1,1,1" in summary


def test_analyze_folders_handles_unreadable_folder(
    tmp_path: Path, monkeypatch
) -> None:
    """Should skip folders that raise exception on listdir()."""
    from src.organizer import step9_check_folders

    monkeypatch.setattr(
        step9_check_folders.config, "FOLDER_TO_ORGANIZE", str(tmp_path)
    )

    valid = tmp_path / "C01Protected"
    valid.mkdir()
    (valid / "file.txt").write_text("ok")

    # Simulate unreadable folder by deleting it after making it
    shutil.rmtree(valid)

    step9_check_folders.analyze_folders(str(tmp_path))

    # Should still produce a valid summary
    report = tmp_path.parent / "reports" / "step_9" / "summary.csv"
    assert report.exists()
