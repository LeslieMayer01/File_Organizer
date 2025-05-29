"""Tests for refactored step5_organizate_files.py."""

import os
from pathlib import Path
from collections import defaultdict
from src.organizer.step5_organizate_files import (
    normalize_filename,
    build_final_name,
    process_directory,
    sort_files,
    rename_file,
)


def test_normalize_filename_cleaning() -> None:
    assert normalize_filename("123_Archivo-#Extraño!") == "ArchivoExtrao"
    assert normalize_filename("!@#$%^&*()") == ""


def test_build_final_name_with_counter() -> None:
    name = build_final_name(1, "Documento", ".pdf", 2)
    assert name == "01Documento02.pdf"


def test_build_final_name_no_counter() -> None:
    name = build_final_name(1, "Documento", ".pdf", 0)
    assert name == "01Documento.pdf"


def test_sort_files_by_mtime(tmp_path: Path) -> None:
    f1 = tmp_path / "xB.txt"
    f2 = tmp_path / "xA.txt"
    f1.write_text("1")
    f2.write_text("2")
    os.utime(f1, (1, 1))
    os.utime(f2, (2, 2))

    sorted_files = sort_files(["xB.txt", "xA.txt"], str(tmp_path))
    assert sorted_files == ["xB.txt", "xA.txt"]


def test_rename_file_success(tmp_path: Path) -> None:
    file = tmp_path / "Alpha File!.txt"
    file.write_text("data")

    renamed, error = rename_file(
        index=1,
        file="Alpha File!.txt",
        used=defaultdict(int),
        root=str(tmp_path),
        simulate=True,
    )
    assert renamed[1] != ""
    assert error == []


def test_rename_file_error(tmp_path: Path, monkeypatch) -> None:
    file = tmp_path / "fail.txt"
    file.write_text("x")

    def fail_rename(_, __):
        raise OSError("fail")

    monkeypatch.setattr(
        "src.organizer.step5_organizate_files.os.rename",
        fail_rename,
    )

    renamed, error = rename_file(
        index=1,
        file="fail.txt",
        used=defaultdict(int),
        root=str(tmp_path),
        simulate=False,
    )
    assert renamed == []
    assert "fail" in error[2]


def test_process_directory_reports(tmp_path: Path) -> None:
    (tmp_path / "doc1.txt").write_text("a")
    (tmp_path / "doc2.txt").write_text("b")

    renamed, errors = process_directory(str(tmp_path), simulate=True)
    assert len(renamed) == 2
    assert not errors
