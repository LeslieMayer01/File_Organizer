# src/organizer/step5_create_C0_folders.py

"""
Step 5 - Create Internal Folder Structure.

This script searches for folders starting with
config.JUDGEMENT_ID inside config.FOLDER_TO_ORGANIZE and
performs restructuring based on folder content:

Scenario 1: Folder contains only files → Move to
/01PrimeraInstancia/C01Principal/
Scenario 2: Folder contains subfolders + files → Rename or merge
subfolders based on a keyword mapping, move top-level files into
C01Principal (resolving name collisions), and report any items
needing manual review.

All changes are logged using write_report(). Behavior depends on
config.SIMULATE_STEP_5.
"""
import os
import json
import re
from typing import Dict, List, Optional, Tuple

import config
from utils.reports import write_report


def load_keyword_mapping(json_path: str) -> Dict[str, List[str]]:
    """Load keyword-to-folder mapping from a JSON file."""
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def is_target_folder(folder_name: str) -> bool:
    """Check if a folder name starts with the judgment ID."""
    return folder_name.startswith(config.JUDGEMENT_ID[:5])


def is_file(path: str) -> bool:
    """Check if a path is a file."""
    return os.path.isfile(path)


def normalize_string(text: str) -> str:
    """Normalize a string to lowercase and remove accents/spaces."""
    return re.sub(r"[^a-z0-9]", "", text.lower())


def get_matching_key(
    name: str,
    mapping: Dict[str, List[str]],
) -> Optional[str]:
    """Get standard folder name from a given name using the mapping."""
    normalized = normalize_string(name)
    for target, keywords in mapping.items():
        for kw in keywords:
            if normalize_string(kw) in normalized:
                return target
    return None


def get_unique_name(destination: str) -> str:
    """
    Given a desired destination path (file or folder), if it exists,
    append a suffix _1, _2, ... until a unique one is found.
    Returns the unique path.
    """
    base, ext = os.path.splitext(destination)
    counter = 1
    new_dest = destination
    while os.path.exists(new_dest):
        new_dest = f"{base}_{counter}{ext}"
        counter += 1
    return new_dest


def move_all_files(
    source_folder: str,
    destination_folder: str,
    simulate: bool,
    moved_report: List[List[str]],
    error_report: List[List[str]],
) -> None:
    """
    Move all files from source_folder into destination_folder.
    If a file name collision occurs, choose a unique name.
    Appends each move ([src, dst]) to moved_report.
    Logs any unexpected errors to error_report ([path, reason]).
    """
    os.makedirs(destination_folder, exist_ok=True)
    for file_name in os.listdir(source_folder):
        source_path = os.path.join(source_folder, file_name)
        # Skip directories in this step
        if os.path.isdir(source_path):
            continue
        desired_dst = os.path.join(destination_folder, file_name)
        unique_dst = get_unique_name(desired_dst)
        moved_report.append([source_path, unique_dst])
        if not simulate:
            try:
                os.rename(source_path, unique_dst)
            except Exception as e:
                error_report.append([source_path, f"Failed to move: {e}"])


def merge_folders(
    src_folder: str,
    dst_folder: str,
    simulate: bool,
    moved_report: List[List[str]],
    merged_report: List[List[str]],
    error_report: List[List[str]],
) -> None:
    """
    Merge contents of src_folder into dst_folder.
    - For files: move and resolve name collisions.
    - For subdirectories: if a subdir with same name exists in dst,
      merge recursively; else, move or rename the subdir.
    Record each top-level merge ([src_folder, dst_folder]) in
    merged_report. Record each file move in moved_report.
    Log any errors to error_report.
    After successful merge, delete src_folder (if empty).
    """
    merged_report.append([src_folder, dst_folder])
    os.makedirs(dst_folder, exist_ok=True)
    for item in os.listdir(src_folder):
        src_path = os.path.join(src_folder, item)
        dst_path = os.path.join(dst_folder, item)
        if os.path.isdir(src_path):
            if os.path.exists(dst_path) and os.path.isdir(dst_path):
                # Recursive merge into existing subdirectory
                merge_folders(
                    src_path,
                    dst_path,
                    simulate,
                    moved_report,
                    merged_report,
                    error_report,
                )
            else:
                unique_dst = (
                    dst_path
                    if not os.path.exists(dst_path)
                    else get_unique_name(dst_path)
                )
                moved_report.append([src_path, unique_dst])
                if not simulate:
                    try:
                        os.rename(src_path, unique_dst)
                    except Exception as e:
                        error_report.append(
                            [src_path, f"Failed to move folder: {e}"]
                        )
        else:
            # File: resolve name collision
            unique_dst = (
                dst_path
                if not os.path.exists(dst_path)
                else get_unique_name(dst_path)
            )
            moved_report.append([src_path, unique_dst])
            if not simulate:
                try:
                    os.rename(src_path, unique_dst)
                except Exception as e:
                    error_report.append(
                        [src_path, f"Failed to move file: {e}"],
                    )
    # After moving contents, attempt to delete the now-empty src_folder
    if not simulate:
        try:
            os.rmdir(src_folder)
        except Exception:
            pass


def rename_and_merge_subfolders(
    base_path: str,
    subfolder_names: List[str],
    mapping: Dict[str, List[str]],
    simulate: bool,
    moved_report: List[List[str]],
    renamed_report: List[List[str]],
    merged_report: List[List[str]],
    error_report: List[List[str]],
) -> Tuple[List[List[str]], List[List[str]]]:
    """
    Rename subfolders based on mapping. If multiple subfolders map to
    the same target name, merge their contents.

    Returns:
      - renamed_report: [[original_path, new_path]] for pure renames.
      - skipped_report: [[path, reason]] for folders without match.
    """
    skipped_report: List[List[str]] = []
    folder_to_dst: Dict[str, List[str]] = {}

    # Build mapping from each subfolder to intended standard name
    for sub in subfolder_names:
        src_path = os.path.join(base_path, sub)
        standard = get_matching_key(sub, mapping)
        if not standard:
            skipped_report.append([src_path, "Unrecognized keyword"])
            continue
        dst_path = os.path.join(base_path, standard)
        folder_to_dst.setdefault(dst_path, []).append(src_path)

    # Process each target destination
    for dst_path, src_paths in folder_to_dst.items():
        if len(src_paths) == 1:
            src = src_paths[0]
            if os.path.exists(dst_path):
                merge_folders(
                    src,
                    dst_path,
                    simulate,
                    moved_report,
                    merged_report,
                    error_report,
                )
            else:
                renamed_report.append([src, dst_path])
                if not simulate:
                    try:
                        os.rename(src, dst_path)
                    except Exception as e:
                        skipped_report.append([src, f"Rename error: {e}"])
        else:
            # Collision: merge multiple src into one dst
            first_src = src_paths[0]
            if not os.path.exists(dst_path):
                renamed_report.append([first_src, dst_path])
                if not simulate:
                    try:
                        os.rename(first_src, dst_path)
                    except Exception as e:
                        skipped_report.append(
                            [
                                first_src,
                                f"Rename error: {e}",
                            ]
                        )
            else:
                merge_folders(
                    first_src,
                    dst_path,
                    simulate,
                    moved_report,
                    merged_report,
                    error_report,
                )
            for src in src_paths[1:]:
                merge_folders(
                    src,
                    dst_path,
                    simulate,
                    moved_report,
                    merged_report,
                    error_report,
                )

    return renamed_report, skipped_report


def handle_only_files(
    folder_path: str,
    file_names: List[str],
    simulate: bool,
    moved_report: List[List[str]],
    error_report: List[List[str]],
) -> Tuple[
    List[List[str]],
    List[List[str]],
    List[List[str]],
    List[List[str]],
    List[List[str]],
]:
    """
    Scenario 1: folder contains only files.
    Moves them into 01PrimeraInstancia/C01Principal.
    """
    target = os.path.join(folder_path, "01PrimeraInstancia", "C01Principal")
    move_all_files(folder_path, target, simulate, moved_report, error_report)
    return moved_report, [], [], [], error_report


def move_files_to_new_c01(
    folder_path: str,
    file_names: List[str],
    simulate: bool,
    moved_report: List[List[str]],
    error_report: List[List[str]],
) -> None:
    """
    Creates 01PrimeraInstancia/C01Principal if needed and moves
    top-level files there, resolving name collisions.
    """
    if len(file_names) == 0:
        return
    target = os.path.join(folder_path, "01PrimeraInstancia", "C01Principal")
    os.makedirs(target, exist_ok=True)
    for name in file_names:
        src = os.path.join(folder_path, name)
        dst = os.path.join(target, name)
        unique_dst = get_unique_name(dst)
        moved_report.append([src, unique_dst])
        if not simulate:
            try:
                os.rename(src, unique_dst)
            except Exception as e:
                error_report.append([src, f"Failed to move: {e}"])


def handle_folders_and_files(
    folder_path: str,
    subfolder_names: List[str],
    file_names: List[str],
    mapping: Dict[str, List[str]],
    simulate: bool,
    moved_report: List[List[str]],
    renamed_report: List[List[str]],
    merged_report: List[List[str]],
    orphans_report: List[List[str]],
    error_report: List[List[str]],
) -> None:
    """
    Scenario 2: folder has subfolders and possibly top-level files.
    - Rename or merge subfolders.
    - Move top-level files into C01Principal.
    - If rename/merge errors occur, mark top-level files as orphans.
    """
    # Attempt to rename or merge subfolders
    renamed, skipped = rename_and_merge_subfolders(
        folder_path,
        subfolder_names,
        mapping,
        simulate,
        moved_report,
        renamed_report,
        merged_report,
        error_report,
    )
    # If any skipped (errors), treat files as needing manual review
    if skipped:
        reason = "Rename/merge issues, review manually"
        for f in file_names:
            orphans_report.append([os.path.join(folder_path, f), reason])
        return

    # After renaming/merging, ensure C01Principal exists, then move files
    subdirs_after = [
        name
        for name in os.listdir(folder_path)
        if os.path.isdir(os.path.join(folder_path, name))
    ]
    if "C01Principal" not in subdirs_after:
        move_files_to_new_c01(
            folder_path, file_names, simulate, moved_report, error_report
        )
    else:
        if len(file_names) > 0:
            c01_path = os.path.join(
                folder_path, "01PrimeraInstancia", "C01Principal"
            )
            os.makedirs(c01_path, exist_ok=True)

            for name in file_names:
                src = os.path.join(folder_path, name)
                dst = os.path.join(c01_path, name)
                unique_dst = get_unique_name(dst)
                moved_report.append([src, unique_dst])
                if not simulate:
                    try:
                        os.rename(src, unique_dst)
                    except Exception as e:
                        error_report.append([src, f"Failed to move: {e}"])


def handle_folder(
    folder_path: str,
    mapping: Dict[str, List[str]],
    simulate: bool,
) -> Tuple[
    List[List[str]],
    List[List[str]],
    List[List[str]],
    List[List[str]],
    List[List[str]],
]:
    """
    Delegates processing based on folder content.
    Returns lists: moved, renamed, merged, orphans, errors.
    """
    moved: List[List[str]] = []
    renamed: List[List[str]] = []
    merged: List[List[str]] = []
    orphans: List[List[str]] = []
    errors: List[List[str]] = []
    try:
        items = os.listdir(folder_path)
    except Exception as e:
        errors.append([folder_path, f"Cannot list directory: {e}"])
        return moved, renamed, merged, orphans, errors

    file_names = [f for f in items if is_file(os.path.join(folder_path, f))]
    folder_names = [
        f for f in items if os.path.isdir(os.path.join(folder_path, f))
    ]
    if not folder_names:
        # Only files
        _, _, _, _, _ = handle_only_files(
            folder_path, file_names, simulate, moved, errors
        )
        return moved, renamed, merged, orphans, errors

    handle_folders_and_files(
        folder_path,
        folder_names,
        file_names,
        mapping,
        simulate,
        moved,
        renamed,
        merged,
        orphans,
        errors,
    )
    return moved, renamed, merged, orphans, errors


def find_judgment_folders_recursive(base_path: str) -> List[str]:
    """Find all folders recursively starting with first 5 digits of ID."""
    folders: List[str] = []
    for root, dirs, _ in os.walk(base_path):
        for d in dirs:
            if is_target_folder(d):
                folders.append(os.path.join(root, d))
    return folders


def run() -> None:
    """Main entry point to organize internal folder structure."""
    print("\n📂 Step 5: Create Internal Folder Structure")
    print(f"📁 Folder to process: {config.FOLDER_TO_ORGANIZE}")
    print(f"🧪 Simulation mode: {config.SIMULATE_STEP_5}")
    confirm = input("❓ Do you want to continue? [y/N]: ").lower()
    if confirm != "y":
        print("🚫 Operation cancelled.")
        return

    mapping = load_keyword_mapping(config.KEYWORDS_JSON)
    target_folders = find_judgment_folders_recursive(config.FOLDER_TO_ORGANIZE)

    all_moved: List[List[str]] = []
    all_renamed: List[List[str]] = []
    all_merged: List[List[str]] = []
    all_orphans: List[List[str]] = []
    all_errors: List[List[str]] = []

    for folder in target_folders:
        moved, renamed, merged, orphans, errors = handle_folder(
            folder, mapping, simulate=config.SIMULATE_STEP_5
        )
        all_moved.extend(moved)
        all_renamed.extend(renamed)
        all_merged.extend(merged)
        all_orphans.extend(orphans)
        all_errors.extend(errors)

    # Write reports for each action
    write_report(
        step_folder="step_5",
        filename_prefix="moved_files",
        header=["From", "To"],
        rows=all_moved,
    )
    write_report(
        step_folder="step_5",
        filename_prefix="renamed_folders",
        header=["Original Path", "New Path"],
        rows=all_renamed,
    )
    write_report(
        step_folder="step_5",
        filename_prefix="merged_folders",
        header=["Source Folder", "Destination Folder"],
        rows=all_merged,
    )
    write_report(
        step_folder="step_5",
        filename_prefix="manual_review",
        header=["Path", "Reason"],
        rows=all_orphans + all_errors,
    )
