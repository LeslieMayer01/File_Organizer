"""Unit tests for step2_delete_index_files.py."""

from pathlib import Path
from src.organizer import step2_delete_index_files as step2


def test_is_excel_file() -> None:
    """Test detection of valid Excel extensions."""
    assert step2.is_excel_file("file.xls")
    assert step2.is_excel_file("file.XLSX")
    assert step2.is_excel_file("file.xlsm")
    assert step2.is_excel_file("file.XLSM")
    assert not step2.is_excel_file("file.txt")


def test_contains_index_keyword() -> None:
    """Test detection of the 'indice' keyword in filenames."""
    assert step2.contains_index_keyword("Indice_2024.xls")
    assert step2.contains_index_keyword("00IndiceElectronicoC01.xlsm")
    assert not step2.contains_index_keyword("Resumen.xlsx")


def test_find_index_files(tmp_path: Path) -> None:
    """Test that only index Excel files are found."""
    file1 = tmp_path / "indice_A.xlsm"
    file2 = tmp_path / "not_index.docx"
    file1.write_text("data")
    file2.write_text("data")
    found = step2.find_index_files(str(tmp_path))
    assert str(file1) in found
    assert str(file2) not in found


def test_delete_files(tmp_path: Path) -> None:
    """Test simulated and real file deletion."""
    file = tmp_path / "test.xls"
    file.write_text("data")
    simulated = step2.delete_files([str(file)], simulate=True)
    assert simulated == [("File", str(file))]

    step2.delete_files([str(file)], simulate=False)
    assert not file.exists()
