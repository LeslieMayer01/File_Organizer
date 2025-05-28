"""Tests for step4_create_internal_folder_structure.py."""

import json
import pytest
from pathlib import Path

from src.organizer.step4_create_C0_folders import (
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
    """Create and return a temporary mapping JSON."""
    mapping = {
        "C01Principal": ["ppal", "principal"],
        "C05MedidasCautelares": ["medida", "cautelar"],
    }
    path = tmp_path / "mapping.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(mapping, f)
    return path


def test_normalize_string_cleans_text() -> None:
    """Test normalization of string with symbols and accents."""
    assert normalize_string("Ppal !@#") == "ppal"
    assert normalize_string("  MÉDIDA ") == "mdida"


def test_is_target_folder() -> None:
    """Test detection of judgment ID folders."""
    from config import JUDGEMENT_ID

    assert is_target_folder(JUDGEMENT_ID + "001")


def test_get_matching_key_found(keyword_mapping: Path) -> None:
    """Test that known folder names are resolved via mapping."""
    mapping = load_keyword_mapping(str(keyword_mapping))
    assert get_matching_key("Ppal Cuaderno", mapping) == "C01Principal"
    assert get_matching_key("Medida Extra", mapping) == "C05MedidasCautelares"


def test_get_matching_key_not_found(keyword_mapping: Path) -> None:
    """Test that unknown names return None."""
    mapping = load_keyword_mapping(str(keyword_mapping))
    assert get_matching_key("unknown-folder", mapping) is None


def test_move_all_files(tmp_path: Path) -> None:
    """Test moving files to nested folder."""
    src = tmp_path / "source"
    dst = tmp_path / "dest"
    src.mkdir()
    (src / "a.txt").write_text("data")

    moved = move_all_files(str(src), str(dst), simulate=False)
    assert (dst / "a.txt").exists()
    assert moved[0][0].endswith("a.txt")


def test_rename_subfolders(tmp_path: Path) -> None:
    """Test renaming based on keyword mapping."""
    src = tmp_path / "main"
    src.mkdir()
    (src / "ppal").mkdir()
    (src / "medida prueba").mkdir()

    mapping = {"C01Principal": ["ppal"], "C05MedidasCautelares": ["medida"]}

    renamed, skipped = rename_subfolders(
        str(src), ["ppal", "medida prueba"], mapping, simulate=False
    )

    renamed_names = [Path(pair[1]).name for pair in renamed]
    assert "C01Principal" in renamed_names
    assert "C05MedidasCautelares" in renamed_names
    assert skipped == []


def test_handle_folder_scenario_1(tmp_path: Path) -> None:
    """Test creation of structure when only files exist."""
    base = tmp_path / "folder"
    base.mkdir()
    (base / "a.txt").write_text("ok")

    moved, renamed, orphans = handle_folder(
        str(base),
        mapping={},
        simulate=False,
    )

    new_path = base / "01PrimeraInstancia" / "C01Principal" / "a.txt"
    assert new_path.exists()
    assert len(moved) == 1
    assert renamed == []
    assert orphans == []


def test_handle_folder_scenario_2(tmp_path: Path) -> None:
    """Test folder with subfolders and loose files."""
    base = tmp_path / "case_folder"
    base.mkdir()
    (base / "file.pdf").write_text("data")
    (base / "ppal").mkdir()

    mapping = {"C01Principal": ["ppal"]}

    moved, renamed, orphans = handle_folder(
        str(base),
        mapping=mapping,
        simulate=False,
    )

    assert moved == []
    assert renamed[0][1].endswith("C01Principal")
    assert orphans[0][0].endswith("file.pdf")
