"""Unit tests for step1_delete_empty_folders.py."""

from pathlib import Path
from src.organizer import step1_delete_empty_folders as step1


def test_is_folder_empty(tmp_path: Path) -> None:
    """Test detection of empty vs non-empty folders."""
    empty = tmp_path / "empty"
    empty.mkdir()
    assert step1.is_folder_empty(str(empty)) is True

    non_empty = tmp_path / "non_empty"
    non_empty.mkdir()
    (non_empty / "file.txt").write_text("content")
    assert step1.is_folder_empty(str(non_empty)) is False


def test_find_empty_folders(tmp_path: Path) -> None:
    """Test discovery of empty folders."""
    (tmp_path / "a").mkdir()
    (tmp_path / "b").mkdir()
    (tmp_path / "b" / "c").mkdir()
    (tmp_path / "b" / "c" / "file.txt").write_text("123")
    found = step1.find_empty_folders(str(tmp_path))
    assert str(tmp_path / "a") in found


def test_delete_folders(tmp_path: Path) -> None:
    """Test real and simulated deletion of folders."""
    folder = tmp_path / "to_delete"
    folder.mkdir()
    simulated = step1.delete_folders([str(folder)], simulate=True)
    assert simulated == [("Folder", str(folder))]

    step1.delete_folders([str(folder)], simulate=False)
    assert not folder.exists()
