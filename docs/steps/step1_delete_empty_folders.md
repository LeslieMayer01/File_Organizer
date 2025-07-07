# Step 1 - Delete Empty Folders

This script scans the folder defined in `config.FOLDER_TO_ORGANIZE` and
removes all empty folders it finds recursively. It supports simulation
mode using `config.SIMULATE_STEP_1` and generates a CSV report listing
all folders it deleted or would have deleted.

---

## Table of Contents

- [How to Run](#how-to-run)
- [Behavior](#behavior)
- [Output](#output)
- [Example Report](#example-report)
- [Summary](#summary)
- [Script Location](#script-location)

---

## How to Run

Use the Makefile command with the corresponding step:

```bash
make run ARGS="--steps 1"
```

---

## Behavior

- If `config.SIMULATE_STEP_1 = True`, the script performs a dry run and
  only reports what would be deleted.
- If `config.SIMULATE_STEP_1 = False`, it deletes empty folders and logs
  them.

---

## Output

A report is generated in:

```bash
./reports/step_1/deleted_empty_folders_<timestamp>.csv
```

---

## Example Report

| TYPE      | PATH                                        |
|-----------|---------------------------------------------|
| SIMULATED | /base/folder/empty_subfolder                |
| DELETED   | /base/folder/another_empty_folder           |

---

## Summary

This step is useful to clean up unnecessary empty folders before further
processing. It ensures a more consistent folder structure for later
steps.

---

## Script Location

```bash
src/organizer/step1_delete_empty_folders.py
```

---

🔗 [Back to Main Index](../index.md)
