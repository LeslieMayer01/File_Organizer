# tests/test_step1_clean_empty_folders.py

from organizer.step1_clean_empty_folders import (
    contains_index_keyword,
    delete_items,
    find_index_excel_files,
    is_excel_file,
)


def test_is_excel_file():
    assert is_excel_file("file.xlsx")
    assert is_excel_file("file.xls")
    assert not is_excel_file("file.docx")


def test_contains_index_keyword():
    assert contains_index_keyword("indice.xlsx")
    assert contains_index_keyword("INDICE_test.xls")
    assert not contains_index_keyword("summary.xlsx")


def test_find_index_excel_files(tmp_path):
    folder = tmp_path / "test_dir"
    folder.mkdir()
    good_file = folder / "indice_report.xlsx"
    good_file.write_text("test")
    bad_file = folder / "summary.xls"
    bad_file.write_text("test")

    results = find_index_excel_files(str(tmp_path))
    assert len(results) == 1
    assert str(good_file) in results


def test_delete_index_files_and_empty_dirs(tmp_path):
    dir_with_file = tmp_path / "dir_with_file"
    dir_with_file.mkdir()
    index_file = dir_with_file / "indice_data.xlsx"
    index_file.write_text("content")

    empty_dir = tmp_path / "empty_dir"
    empty_dir.mkdir()

    # Dry run mode
    deleted_items = delete_items(str(tmp_path), dry_run=True)
    assert ("File", str(index_file)) in deleted_items
    assert ("Folder", str(empty_dir)) in deleted_items
    assert index_file.exists()
    assert empty_dir.exists()

    # Real deletion
    deleted_items = delete_items(str(tmp_path), dry_run=False)
    assert not index_file.exists()
    assert not empty_dir.exists()
    assert ("File", str(index_file)) in deleted_items
    assert ("Folder", str(empty_dir)) in deleted_items
