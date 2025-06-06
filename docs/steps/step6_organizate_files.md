# Step 6 - Organize Files Inside C0 Folders

This script standardizes the file names within each C0 subfolder
found in the project structure. It assigns each file a numeric prefix
and removes invalid characters.

Simulation mode is controlled via `config.SIMULATE_STEP_6`.

---

## Table of Contents

- [How to Run](#how-to-run)
- [Behavior](#behavior)
- [Before and After Example](#before-and-after-example)
- [Renaming Rules](#renaming-rules)
- [Output Reports](#output-reports)
- [Example Report](#example-report)
- [Summary](#summary)
- [Script Location](#script-location)

---

## How to Run

Use the Makefile command with the corresponding step:

```bash
make run ARGS="--steps 6"
```

---

## Behavior

- Looks recursively for folders matching `config.JUDGEMENT_ID`
- Searches inside subfolders starting with `C0`
- Renames all files to use a format like:
  `001 CleanedFileName.pdf`, `002 OtherName.docx`
- Keeps extensions
- Removes special characters from names
- Avoids file name conflicts

---

## Before and After Example

### Before

```text
/05380408900120230013800/
└── 01PrimeraInstancia/
    └── C01Principal/
        ├── Contestación-Juez!.pdf
        └── 1.pdf
```

### After

```text
/05380408900120230013800/
└── 01PrimeraInstancia/
    └── C01Principal/
        ├── 001 ContestacionJuez.pdf
        └── 002 1.pdf
```

---

## Renaming Rules

- File name starts with a 3-digit sequential number
- Keeps original extension
- Removes or replaces symbols (e.g., `!@#$%`)
- File names are cleaned using `normalize_filename`

---

## Output Reports

Reports are generated in:

```bash
./reports/step_6/
```

- `renamed_files_<timestamp>.csv`
- `files_requires_manual_review_<timestamp>.csv`

---

## Example Report

### renamed_files.csv

| ORIGINAL_PATH               | NEW_PATH                      |
|-----------------------------|-------------------------------|
| /C01/Contestación-Juez!.pdf | /C01/001 ContestacionJuez.pdf |
| /C01/1.pdf                  | /C01/002 1.pdf                |

### files_requires_manual_review.csv

| FILE_PATH           | ERROR_MESSAGE      |
|---------------------|--------------------|
| /C01/duplicated.pdf | File name conflict |
| /C02/fail.docx      | Rename failed      |

---

## Summary

This step ensures a predictable and consistent naming convention for
all files inside C0 folders. This is useful for sorting, indexing,
and traceability.

---

## Script Location

```bash
src/organizer/step6_organizate_files.py
```

---

🔗 [Back to Main Index](../index.md)
