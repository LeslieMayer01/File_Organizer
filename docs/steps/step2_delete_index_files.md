# Step 2 - Delete Index Files

This script scans all folders under `config.FOLDER_TO_ORGANIZE` and
deletes any file that starts with `00IndiceElectronicoC0`. It supports
simulation mode using `config.SIMULATE_STEP_2` and generates a report
listing deleted or detected files.

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
make run ARGS="--steps 2"
```

---

## Behavior

- If `config.SIMULATE_STEP_2 = True`, the script simulates the deletion
  and logs the affected files.
- If `config.SIMULATE_STEP_2 = False`, the script deletes the matching
  files.

Only files starting with `00IndiceElectronicoC0` are affected.

---

## Output

A report is generated in:

```bash
./reports/step_2/deleted_index_files_<timestamp>.csv
```

---

## Example Report

| TYPE      | PATH                                                      |
|-----------|-----------------------------------------------------------|
| DELETED   | /base/CARPETA/00IndiceElectronicoC0123456789012345.xlsm   |
| SIMULATED | /base/OTRA/00IndiceElectronicoC0987654321123456.xlsm      |

---

## Summary

This step helps prevent conflicts with pre-existing electronic index
files. It ensures that the system does not reuse outdated or incorrect
index templates.

---

## Script Location

```bash
src/organizer/step2_delete_index_files.py
```

---

🔗 [Back to Main Index](../index.md)
