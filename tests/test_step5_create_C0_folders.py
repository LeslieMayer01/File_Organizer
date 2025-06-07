import sys
import json
from pathlib import Path
import pytest
from organizer.step5_create_C0_folders import (
    get_unique_name,
    merge_folders,
    rename_and_merge_subfolders,
    handle_only_files,
    handle_folders_and_files,
)

# Ensure src is on sys.path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


@pytest.fixture
def keywords_mapping():
    """Load the actual keywords.json mapping for folder renaming."""
    mapping_path = Path(__file__).parent.parent / "data/keywords.json"
    with open(mapping_path, "r", encoding="utf-8") as f:
        return json.load(f)


def test_get_unique_name_no_conflict(tmp_path):
    file_path = tmp_path / "file.txt"
    # File does not exist yet
    unique = get_unique_name(str(file_path))
    assert unique == str(file_path)


def test_get_unique_name_conflict(tmp_path):
    file_path = tmp_path / "file.txt"
    file_path.write_text("content")
    # Expect a new name with _1 suffix
    unique = get_unique_name(str(file_path))
    assert unique.endswith("_1.txt")
    # Create second conflict
    Path(unique).write_text("other")
    unique2 = get_unique_name(str(file_path))
    assert unique2.endswith("_2.txt")


def test_merge_folders_simple(tmp_path):
    # src has one file, dst is empty
    src = tmp_path / "src"
    dst = tmp_path / "dst"
    src.mkdir()
    dst.mkdir()
    f = src / "doc.txt"
    f.write_text("data")
    moved = []
    merged = []
    errors = []
    merge_folders(str(src), str(dst), False, moved, merged, errors)
    # After merge, src should be removed
    assert not src.exists()
    # File should be in dst
    assert (dst / "doc.txt").exists()
    # Records should be correct
    assert [str(src), str(dst)] in merged
    assert [str(f), str(dst / "doc.txt")] in moved


def test_merge_folders_conflict(tmp_path):
    # src has file 'doc.txt', dst has same file
    src = tmp_path / "src"
    dst = tmp_path / "dst"
    src.mkdir()
    dst.mkdir()
    (src / "doc.txt").write_text("one")
    (dst / "doc.txt").write_text("two")
    moved = []
    merged = []
    errors = []
    merge_folders(str(src), str(dst), False, moved, merged, errors)
    # Check that dst still has original file and new file with suffix
    names = {f.name for f in dst.iterdir()}
    assert "doc.txt" in names
    assert any(n.startswith("doc_1") for n in names)
    # src removed
    assert not src.exists()
    # Check merged report has merge entry
    assert [str(src), str(dst)] in merged
    # Confirm a file move from src is recorded
    assert any(rec[0].endswith("doc.txt") for rec in moved)


@pytest.mark.parametrize(
    "subfolder_name, expected_standard",
    [
        ("PrincipalSection", "C01Principal"),
        ("MedidaCautelarDocs", "C05MedidasCautelares"),
        ("Ejecucion2020", "C10EjecucionSentencia"),
    ],
)
def test_rename_subfolders_using_keywords(
    tmp_path, keywords_mapping, subfolder_name, expected_standard
):
    base = tmp_path / "base"
    base.mkdir()
    sub = base / subfolder_name
    sub.mkdir()
    moved = []
    renamed = []
    merged = []
    errors = []
    renamed_res, skipped = rename_and_merge_subfolders(
        str(base),
        [sub.name],
        keywords_mapping,
        False,
        moved,
        renamed,
        merged,
        errors,
    )
    new_path = base / expected_standard
    # Since simulate=False, rename occurs
    assert new_path.exists()
    assert [str(sub), str(new_path)] in renamed_res
    assert not skipped


def test_rename_and_merge_subfolders_collision(tmp_path, keywords_mapping):
    base = tmp_path / "base"
    base.mkdir()
    # Create two subfolders matching 'acumulacion'
    sub1 = base / "Acumulacion1"
    sub2 = base / "ACUMULACION2"
    sub1.mkdir()
    sub2.mkdir()
    dst = base / "C03AcumulacionProcesos"
    # Pre-create dst to force merge
    dst.mkdir()
    moved = []
    renamed = []
    merged = []
    errors = []
    renamed_res, skipped = rename_and_merge_subfolders(
        str(base),
        [sub1.name, sub2.name],
        keywords_mapping,
        False,
        moved,
        renamed,
        merged,
        errors,
    )
    # Both subfolders should be merged into dst
    assert [str(sub1), str(dst)] in merged
    assert [str(sub2), str(dst)] in merged
    assert not skipped
    assert dst.exists()


def test_rename_and_merge_subfolders_unrecognized(tmp_path, keywords_mapping):
    base = tmp_path / "base"
    base.mkdir()
    sub = base / "UnknownFolder"
    sub.mkdir()
    moved = []
    renamed = []
    merged = []
    errors = []
    renamed_res, skipped = rename_and_merge_subfolders(
        str(base),
        [sub.name],
        keywords_mapping,
        False,
        moved,
        renamed,
        merged,
        errors,
    )
    assert skipped
    assert [str(sub), "Unrecognized keyword"] in skipped


def test_handle_only_files(tmp_path):
    folder = tmp_path / "onlyfiles"
    folder.mkdir()
    for name in ("a.txt", "b.txt"):
        (folder / name).write_text("x")
    moved = []
    errors = []
    res_moved, _, _, _, _ = handle_only_files(
        str(folder), ["a.txt", "b.txt"], False, moved, errors
    )
    dest = folder / "01PrimeraInstancia" / "C01Principal"
    for name in ("a.txt", "b.txt"):
        assert (dest / name).exists()
    for rec in res_moved:
        assert rec[0].startswith(str(folder))
        assert rec[1].startswith(str(dest))


def test_handle_folders_and_files_success(tmp_path, keywords_mapping):
    folder = tmp_path / "mixed"
    folder.mkdir()
    sub = folder / "RecursoFolder"
    sub.mkdir()
    # Keyword 'Recurso' maps to 'C08Recurso'
    f = folder / "file1.txt"
    f.write_text("data")
    moved = []
    renamed = []
    merged = []
    orphans = []
    errors = []
    handle_folders_and_files(
        str(folder),
        [sub.name],
        [f.name],
        keywords_mapping,
        False,
        moved,
        renamed,
        merged,
        orphans,
        errors,
    )
    # Renamed subfolder to C08Recurso
    assert (folder / "C08Recurso").exists()
    dest = folder / "01PrimeraInstancia" / "C01Principal"
    assert (dest / "file1.txt").exists()
    assert not orphans
    assert not errors


def test_handle_folders_without_files_success(tmp_path, keywords_mapping):
    folder = tmp_path / "mixed"
    folder.mkdir()
    sub = folder / "RecursoFolder"
    sub.mkdir()
    moved = []
    renamed = []
    merged = []
    orphans = []
    errors = []
    handle_folders_and_files(
        str(folder),
        [sub.name],
        [],
        keywords_mapping,
        False,
        moved,
        renamed,
        merged,
        orphans,
        errors,
    )
    # Renamed subfolder to C08Recurso
    assert (folder / "C08Recurso").exists()
    dest = folder / "01PrimeraInstancia" / "C01Principal"
    assert not dest.exists()
    assert not orphans
    assert not errors


def test_handle_folders_and_files_unrecognized(tmp_path, keywords_mapping):
    folder = tmp_path / "mixed2"
    folder.mkdir()
    sub = folder / "SomeRandom"
    sub.mkdir()
    f = folder / "file2.txt"
    f.write_text("data")
    moved = []
    renamed = []
    merged = []
    orphans = []
    errors = []
    handle_folders_and_files(
        str(folder),
        [sub.name],
        [f.name],
        keywords_mapping,
        False,
        moved,
        renamed,
        merged,
        orphans,
        errors,
    )
    assert orphans
    assert orphans[0][0].endswith("file2.txt")
    dest = folder / "01PrimeraInstancia" / "C01Principal"
    assert not dest.exists()
