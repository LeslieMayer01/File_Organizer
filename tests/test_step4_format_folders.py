"""Unit tests for step4_format_folders.py."""

import pytest
from pathlib import Path
from unittest.mock import patch

from src.organizer.step4_format_folders import (
    clean_name,
    extract_new_name,
    find_folders_to_rename,
    rename_folders,
)


def test_clean_name_removes_non_alphanumeric() -> None:
    """Test that clean_name removes all non-alphanumeric characters."""
    assert clean_name("abc-123") == "abc123"
    assert clean_name("ABC_456!") == "ABC456"
    assert clean_name("no_change") == "nochange"


@pytest.mark.parametrize(
    "original,expected",
    [
        ("2023-123", "053804089001202312300"),
        ("2023-0001 test", "0538040890012023000100 test"),
        ("2023-9 !@#ABC", "0538040890012023900 ABC"),
    ],
)
def test_extract_new_name_valid_cases(monkeypatch, original, expected) -> None:
    """Test valid folder names with case number patterns."""
    monkeypatch.setattr("config.JUDGEMENT_ID", "053804089001")
    result = extract_new_name(original)
    assert result is not None
    assert result.startswith("053804089001")
    assert expected in result


def test_extract_new_name_no_match(monkeypatch) -> None:
    """Test when folder name has no case number pattern."""
    monkeypatch.setattr("config.JUDGEMENT_ID", "053804089001")
    assert extract_new_name("folder_with_no_digits") is None


def test_extract_new_name_max_length(monkeypatch) -> None:
    """Test that result is truncated at 40 characters if needed."""
    monkeypatch.setattr("config.JUDGEMENT_ID", "999999999999")
    base = "2023-1 verylongsuffixnamewithmanycharacters"
    result = extract_new_name(base)
    assert result is not None
    assert len(result) == 40
    assert result.startswith("9999999999992023100")


def test_extract_new_name_none_if_not_found() -> None:
    """Test behavior when no case number is found."""
    assert extract_new_name("random_folder") is None


def test_find_folders_to_rename(tmp_path: Path) -> None:
    """Test detection of folders that need renaming."""
    (tmp_path / "valid_2024-001").mkdir()
    (tmp_path / "053804089001202400100000").mkdir()  # already valid

    folders = find_folders_to_rename(str(tmp_path))
    assert len(folders) == 1
    assert folders[0][1] == "valid_2024-001"


def test_rename_folders_simulation(tmp_path: Path) -> None:
    """Test simulated folder renaming."""
    source = tmp_path / "2021-888 X"
    source.mkdir()

    renamed, conflicts, errors = rename_folders(
        [(str(tmp_path), "2021-888 X", "newname")], simulate=True
    )

    assert len(renamed) == 1
    assert conflicts == []
    assert errors == []
    assert source.exists()


def test_rename_folders_real(tmp_path: Path) -> None:
    """Test real folder renaming behavior."""
    old_folder = tmp_path / "2022-001 Extra"
    old_folder.mkdir()

    entries = [(str(tmp_path), "2022-001 Extra", "renamed")]
    renamed, conflicts, errors = rename_folders(entries, simulate=False)

    assert len(renamed) == 1
    assert conflicts == []
    assert errors == []
    assert not old_folder.exists()
    assert (tmp_path / "renamed").exists()


def test_rename_folders_with_conflict(tmp_path: Path) -> None:
    """Test that conflicts are correctly detected and skipped."""
    old_folder = tmp_path / "2020-003"
    old_folder.mkdir()
    conflict_folder = tmp_path / "conflict"
    conflict_folder.mkdir()

    entries = [(str(tmp_path), "2020-003", "conflict")]
    renamed, conflicts, errors = rename_folders(entries, simulate=False)

    assert renamed == []
    assert len(conflicts) == 1
    assert conflicts[0][1] == "conflict"
    assert errors == []


def test_rename_folders_with_rename_error(tmp_path) -> None:
    """Test that rename errors are caught and reported."""
    source = tmp_path / "2021-555"
    source.mkdir()
    entries = [(str(tmp_path), "2021-555", "fail")]

    with patch("os.rename", side_effect=OSError("mocked failure")):
        renamed, conflicts, errors = rename_folders(entries, simulate=False)

    assert renamed[0][0].endswith("2021-555")
    assert conflicts == []
    assert len(errors) == 1
    assert "mocked failure" in errors[0][2]
