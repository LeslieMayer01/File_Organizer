# Step 9 - Check Folder Naming Validity

This script validates all folders within the path defined in
`config.FOLDER_TO_ORGANIZE` to ensure their names start with a valid
23-digit identifier based on the value of `config.JUDGEMENT_ID`.

It flags folders that do not conform to the naming convention and
generates a report with the full list.

---

## Table of Contents

- [How to Run](#how-to-run)
- [Behavior](#behavior)
- [Valid Format](#valid-format)
- [Example Folder Validation](#example-folder-validation)
- [Output Report](#output-report)
- [Example Report](#example-report)
- [Summary](#summary)
- [Script Location](#script-location)

---

## How to Run

Use the Makefile command with the corresponding step:

```bash
make run ARGS="--steps 9"
```

---

## Behavior

- Recursively scans folders under `config.FOLDER_TO_ORGANIZE`
- A folder is considered valid if it starts with:
  `{config.JUDGEMENT_ID}` + 11 digits (total 23 digits)
- All invalid folders are listed in the output report

---

## Valid Format

Example:

```text
JUDGEMENT_ID: 053804089001
Valid folder: 05380408900120230013800 Contestacion
```

---

## Example Folder Validation

### Valid

```text
/05380408900120230013800 Contestacion
```

### Invalid

```text
/2023-00138 Folder A
/Contestacion No ID
```

---

## Output Report

The report is generated at:

```bash
./reports/step_9/invalid_folders_<timestamp>.csv
```

---

## Example Report

| INVALID_FOLDER_PATH       | REASON             |
|---------------------------|--------------------|
| /base/2023-00138 Folder A | Invalid prefix     |
| /base/RandomFolder        | Missing ID pattern |

---

## Summary

This step ensures that all folders follow a strict naming convention
required for consistent file organization, tracking, and automated
processing.

---

## Script Location

```bash
src/organizer/step9_check_folders.py
```

---

🔗 [Back to Main Index](../index.md)
