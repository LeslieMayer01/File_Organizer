from pathlib import Path

from organizer.step3_remove_desktop_ini import remove_desktop_ini_files


def test_remove_desktop_ini_files_real(tmp_path: Path) -> None:
    """
    It should delete only 'desktop.ini' files when simulate=False.
    """
    folder = tmp_path / "test_folder"
    folder.mkdir()

    # Create files
    desktop_file = folder / "desktop.ini"
    desktop_file.write_text("dummy")

    safe_file = folder / "not_to_delete.txt"
    safe_file.write_text("keep this")

    results = remove_desktop_ini_files(str(tmp_path), simulate=False)

    assert ("Deleted", str(desktop_file)) in results
    assert not desktop_file.exists()
    assert safe_file.exists()


def test_remove_desktop_ini_files_simulate(tmp_path: Path) -> None:
    """
    It should not delete 'desktop.ini' files when simulate=True.
    """
    folder = tmp_path / "sim_folder"
    folder.mkdir()

    # Create desktop.ini
    desktop_file = folder / "desktop.ini"
    desktop_file.write_text("dummy")

    results = remove_desktop_ini_files(str(tmp_path), simulate=True)

    assert ("Simulated", str(desktop_file)) in results
    assert desktop_file.exists()


def test_no_desktop_ini_found(tmp_path: Path) -> None:
    """
    It should return an empty list if no 'desktop.ini' files are present.
    """
    folder = tmp_path / "empty_folder"
    folder.mkdir()

    (folder / "somefile.txt").write_text("nothing to remove")

    results = remove_desktop_ini_files(str(tmp_path), simulate=False)

    assert results == []
