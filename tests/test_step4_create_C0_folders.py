"""Tests for step4_create_C0_folders.py."""

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
    """Create a temporary keyword mapping file."""
    mapping = {
        "C01Principal": ["ppal", "principal"],
        "C05MedidasCautelares": ["medida", "cautelar"],
    }
    path = tmp_path / "mapping.json"
    path.write_text(json.dumps(mapping), encoding="utf-8")
    return path


def test_normalize_string() -> None:
    """Normalize string with symbols and accents."""
    assert normalize_string("Ppal !@#") == "ppal"
    assert normalize_string("  MÉDIDA ") == "mdida"


def test_is_target_folder() -> None:
    """Validate folders matching judgment prefix."""
    from config import JUDGEMENT_ID

    folder_name = JUDGEMENT_ID[:5] + "_something"
    assert is_target_folder(folder_name) is True


def test_get_matching_key_found(keyword_mapping: Path) -> None:
    """Get standard folder from a name using the mapping."""
    mapping = load_keyword_mapping(str(keyword_mapping))
    assert get_matching_key("Ppal Cuaderno", mapping) == "C01Principal"
    assert get_matching_key("Medida Extra", mapping) == "C05MedidasCautelares"


def test_get_matching_key_not_found(keyword_mapping: Path) -> None:
    """Return None for unknown folder names."""
    mapping = load_keyword_mapping(str(keyword_mapping))
    assert get_matching_key("no-match", mapping) is None


def test_move_all_files(tmp_path: Path) -> None:
    """Move files from flat folder to new folder."""
    src = tmp_path / "src"
    dst = tmp_path / "dst"
    src.mkdir()
    dst.mkdir()
    (src / "a.txt").write_text("data")

    moved = move_all_files(str(src), str(dst), simulate=False)
    assert len(moved) == 1
    assert (dst / "a.txt").exists()


def test_rename_subfolders(tmp_path: Path) -> None:
    """Rename folders using keyword mapping with no conflicts."""
    src = tmp_path / "case"
    src.mkdir()
    (src / "ppal").mkdir()
    (src / "medida prueba").mkdir()

    mapping = {
        "C01Principal": ["ppal"],
        "C05MedidasCautelares": ["medida"],
    }

    renamed, skipped = rename_subfolders(
        str(src),
        ["ppal", "medida prueba"],
        mapping,
        simulate=False,
    )

    renamed_names = [Path(new).name for _, new in renamed]
    assert "C01Principal" in renamed_names
    assert "C05MedidasCautelares" in renamed_names
    assert not skipped


def test_rename_subfolders_conflict(tmp_path: Path) -> None:
    """Skip renaming if multiple folders target the same name."""
    folder = tmp_path / "conflict"
    folder.mkdir()
    (folder / "ppal").mkdir()
    (folder / "principal").mkdir()

    mapping = {"C01Principal": ["ppal", "principal"]}

    renamed, skipped = rename_subfolders(
        str(folder),
        ["ppal", "principal"],
        mapping,
        simulate=False,
    )

    assert not renamed
    assert len(skipped) == 2


def test_handle_folder_scenario_1_only_files(tmp_path: Path) -> None:
    """Move files into 01PrimeraInstancia/C01Principal structure."""
    base = tmp_path / "folder"
    base.mkdir()
    (base / "file1.txt").write_text("ok")

    moved, renamed, orphans = handle_folder(
        str(base),
        mapping={},
        simulate=False,
    )

    target = base / "01PrimeraInstancia" / "C01Principal" / "file1.txt"
    assert target.exists()
    assert len(moved) == 1
    assert not renamed
    assert not orphans


def test_handle_folder_scenario_2_with_orphans(tmp_path: Path) -> None:
    """Handle folders with subfolders + unclassified files."""
    base = tmp_path / "case"
    base.mkdir()
    (base / "loose.pdf").write_text("info")
    (base / "ppal").mkdir()

    mapping = {"C01Principal": ["ppal"]}

    moved, renamed, orphans = handle_folder(
        str(base),
        mapping=mapping,
        simulate=False,
    )

    assert not moved
    assert renamed[0][1].endswith("C01Principal")
    assert orphans[0][0].endswith("loose.pdf")
