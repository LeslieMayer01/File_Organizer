from pathlib import Path
from typing import List

import config
from utils.reports import write_report

def find_folders_missing_index(base_path: Path) -> List[List[str]]:
    """
    Recursively find folders without an index file starting with
    '00IndiceElectronicoC0'. Returns list of [folder_name, path].
    """
    missing: List[List[str]] = []
    for folder in base_path.rglob('*'):
        if not folder.is_dir():
            continue
        if not folder.name.upper().startswith('C0'):
            continue
        has_index = any(
            child.is_file() and
            child.name.startswith('00IndiceElectronicoC0')
            for child in folder.iterdir()
        )
        if not has_index:
            missing.append([folder.name, folder.as_posix()])
    return missing

def run() -> List[List[str]]:
    """
    1) Find folders missing index.
    2) Generate report using write_report.
    """
    base = Path(config.FOLDER_TO_ORGANIZE)
    invalid = find_folders_missing_index(base)

    if config.SIMULATE_STEP_10:
        print('--- SIMULATION: folders missing index ---')
        for name, path in invalid:
            print(f'{name}: {path}')
    else:
        write_report(
            step_folder='step_10',
            filename_prefix='invalid_folders',
            header=['Folder Name', 'Path'],
            rows=invalid,
        )
        print('✅ Report generated via write_report')

    return invalid
