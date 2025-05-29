"""Tests for step6_subfolder_organization.py."""

import json
import pytest
from pathlib import Path
from src.organizer.step6_subfolder_organization import (
    is_target_folder,
    is_c0_structure_only,
    load_folder_mapping,
    classify_and_move_subfolders,
    process_structure,
    has_only_c01_folder,
)
from config import JUDGEMENT_ID


@pytest.fixture
def mapping_json(tmp_path: Path) -> Path:
    data = {
        "C01": "01PrimeraInstancia",
        "C05": "01PrimeraInstancia",
        "C06": "02SegundaInstancia",
        "C08": "03RecursosExtraordinarios",
        "C10": "04Ejecucion",
    }
    path = tmp_path / "folder_mapping.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


def test_is_target_folder_true() -> None:
    assert is_target_folder(JUDGEMENT_ID + "_resto")


def test_is_target_folder_false() -> None:
    assert not is_target_folder("XYZfolder")


def test_is_c0_structure_only_true(tmp_path: Path) -> None:
    path = tmp_path / "test_folder"
    path.mkdir()
    (path / "C01test").mkdir()
    (path / "C05prueba").mkdir()
    assert is_c0_structure_only(str(path))


def test_is_c0_structure_only_false(tmp_path: Path) -> None:
    path = tmp_path / "bad_folder"
    path.mkdir()
    (path / "C01a").mkdir()
    (path / "Otra").mkdir()
    assert not is_c0_structure_only(str(path))


def test_load_folder_mapping(mapping_json: Path) -> None:
    expected = "03RecursosExtraordinarios"
    mapping = load_folder_mapping(str(mapping_json))
    assert mapping["C01"] == "01PrimeraInstancia"
    assert "C08" not in mapping or mapping["C08"] == expected


def test_classify_and_move_subfolders_simulate(tmp_path: Path) -> None:
    base = tmp_path / "123"
    base.mkdir()
    (base / "C01alpha").mkdir()
    (base / "C05beta").mkdir()

    mapping = {"C01": "01PrimeraInstancia", "C05": "01PrimeraInstancia"}
    rows = classify_and_move_subfolders(str(base), mapping, simulate=True)

    assert len(rows) == 2

    dest_paths = [Path(row[1]) for row in rows]
    expected1 = Path("01PrimeraInstancia") / "C01alpha"
    expected2 = Path("01PrimeraInstancia") / "C05beta"

    assert any(expected1.parts[-2:] == dp.parts[-2:] for dp in dest_paths)
    assert any(expected2.parts[-2:] == dp.parts[-2:] for dp in dest_paths)


def test_process_structure_valid_and_skipped(tmp_path: Path) -> None:
    valid = tmp_path / f"{JUDGEMENT_ID}_valid"
    valid.mkdir()
    (valid / "C01xx").mkdir()

    invalid = tmp_path / f"{JUDGEMENT_ID}_invalid"
    invalid.mkdir()
    (invalid / "XxOther").mkdir()

    mapping = {"C01": "01PrimeraInstancia"}

    moved, skipped = process_structure(str(tmp_path), mapping, simulate=True)

    assert len(moved) == 1
    assert len(skipped) == 1


def test_has_only_c01_folder_true(tmp_path: Path) -> None:
    """Should return True when only folder is '01PrimeraInstancia'."""
    parent = tmp_path / "target"
    parent.mkdir()
    (parent / "01PrimeraInstancia").mkdir()
    assert has_only_c01_folder(str(parent))


def test_has_only_c01_folder_false_extra_folder(tmp_path: Path) -> None:
    """Should return False when other folders exist."""
    parent = tmp_path / "target"
    parent.mkdir()
    (parent / "01PrimeraInstancia").mkdir()
    (parent / "Other").mkdir()
    assert not has_only_c01_folder(str(parent))


def test_has_only_c01_folder_false_empty(tmp_path: Path) -> None:
    """Should return False when folder is empty."""
    parent = tmp_path / "target"
    parent.mkdir()
    assert not has_only_c01_folder(str(parent))
