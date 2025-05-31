"""Tests for step5_create_C0_folders.py."""

import json
from pathlib import Path
import pytest

from src.organizer.step5_create_C0_folders import (
    normalize_string,
    is_target_folder,
    get_matching_key,
    move_all_files,
    rename_subfolders,
    handle_folder,
    load_keyword_mapping,
)


@pytest.fixture
def keyword_mapping(tmp_path: Path) -> Path:
    mapping = {
        "C01Principal": ["ppal", "principal"],
        "C05MedidasCautelares": ["medida", "cautelar"],
    }
    path = tmp_path / "mapping.json"
    path.write_text(json.dumps(mapping), encoding="utf-8")
    return path


def test_normalize_string() -> None:
    assert normalize_string("Ppal !@#") == "ppal"
    assert normalize_string("  MÉDIDA ") == "mdida"


def test_is_target_folder() -> None:
    from config import JUDGEMENT_ID

    folder_name = JUDGEMENT_ID[:5] + "_ABC"
    assert is_target_folder(folder_name) is True


def test_get_matching_key_found(keyword_mapping: Path) -> None:
    mapping = load_keyword_mapping(str(keyword_mapping))
    assert get_matching_key("Ppal Cuaderno", mapping) == "C01Principal"
    assert get_matching_key("Medida Extra", mapping) == "C05MedidasCautelares"


def test_get_matching_key_not_found(keyword_mapping: Path) -> None:
    mapping = load_keyword_mapping(str(keyword_mapping))
    assert get_matching_key("no-match", mapping) is None


def test_move_all_files(tmp_path: Path) -> None:
    src = tmp_path / "src"
    dst = tmp_path / "dst"
    src.mkdir()
    dst.mkdir()
    (src / "a.txt").write_text("data")

    moved = move_all_files(str(src), str(dst), simulate=False)
    assert len(moved) == 1
    assert (dst / "a.txt").exists()


def test_rename_subfolders_success(tmp_path: Path) -> None:
    base = tmp_path / "case"
    base.mkdir()
    (base / "ppal").mkdir()
    (base / "medida prueba").mkdir()

    mapping = {
        "C01Principal": ["ppal"],
        "C05MedidasCautelares": ["medida"],
    }

    renamed, skipped, conflicted = rename_subfolders(
        str(base), ["ppal", "medida prueba"], mapping, simulate=False
    )

    renamed_names = [Path(new).name for _, new in renamed]
    assert "C01Principal" in renamed_names
    assert "C05MedidasCautelares" in renamed_names
    assert not skipped
    assert not conflicted


def test_rename_subfolders_conflict(tmp_path: Path) -> None:
    base = tmp_path / "conflict"
    base.mkdir()
    (base / "ppal").mkdir()
    (base / "principal").mkdir()

    mapping = {"C01Principal": ["ppal", "principal"]}

    renamed, skipped, conflicted = rename_subfolders(
        str(base), ["ppal", "principal"], mapping, simulate=False
    )

    conflict_paths = [Path(row[0]).name for row in conflicted]
    assert not renamed
    assert not skipped
    assert len(conflicted) == 2
    assert "Conflict" in conflicted[0][1]
    assert "ppal" in conflict_paths
    assert "principal" in conflict_paths


def test_rename_subfolders_unrecognized(tmp_path: Path) -> None:
    base = tmp_path / "unmapped"
    base.mkdir()
    (base / "misc").mkdir()

    mapping = {"C01Principal": ["ppal"]}

    renamed, skipped, conflicted = rename_subfolders(
        str(base), ["misc"], mapping, simulate=True
    )

    assert not renamed
    assert not conflicted
    assert skipped[0][1] == "Unrecognized keyword"


def test_handle_folder_only_files(tmp_path: Path) -> None:
    base = tmp_path / "folder"
    base.mkdir()
    (base / "file1.txt").write_text("ok")

    moved, renamed, orphans, rename_issues = handle_folder(
        str(base), mapping={}, simulate=False
    )

    target = base / "01PrimeraInstancia" / "C01Principal" / "file1.txt"
    assert target.exists()
    assert len(moved) == 1
    assert not renamed
    assert not orphans
    assert not rename_issues


def test_handle_folder_conflict_and_files(tmp_path: Path) -> None:
    base = tmp_path / "case"
    base.mkdir()
    (base / "ppal").mkdir()
    (base / "principal").mkdir()
    (base / "extra.txt").write_text("info")

    mapping = {"C01Principal": ["ppal", "principal"]}

    moved, renamed, orphans, rename_issues = handle_folder(
        str(base), mapping, simulate=False
    )

    paths = [Path(row[0]).name for row in rename_issues]

    assert not moved
    assert not renamed
    assert len(orphans) == 1
    assert len(rename_issues) == 2
    assert "Conflict" in rename_issues[0][1]
    assert "ppal" in paths
    assert "principal" in paths


def test_handle_folder_existing_c01(tmp_path: Path) -> None:
    base = tmp_path / "case"
    base.mkdir()

    # Subcarpetas: una que será reconocida y otra que ya existe como destino
    (base / "misc").mkdir()
    (base / "C01Principal").mkdir()

    # Archivo suelto
    (base / "extra.txt").write_text("a")

    # mapping que lleva 'misc' → 'C01Principal' (conflicto)
    mapping = {"C01Principal": ["misc"]}

    moved, renamed, orphans, issues = handle_folder(
        str(base), mapping, simulate=False
    )

    paths = [Path(row[0]).name for row in issues]
    assert not moved
    assert not renamed
    assert len(orphans) == 1
    assert orphans[0][1].startswith("C01Principal exists")
    assert len(issues) == 2
    assert "misc" in paths
    assert "C01Principal" in paths


def test_handle_folder_without_c01_renamed(tmp_path: Path) -> None:
    base = tmp_path / "case"
    base.mkdir()
    (base / "medida").mkdir()
    (base / "extra.txt").write_text("a")

    mapping = {
        "C05MedidasCautelares": ["medida"],
    }

    moved, renamed, orphans, issues = handle_folder(
        str(base), mapping, simulate=False
    )

    target = base / "01PrimeraInstancia" / "C01Principal" / "extra.txt"
    assert target.exists()
    assert len(renamed) == 1
    assert len(moved) == 1
    assert not orphans
    assert not issues
