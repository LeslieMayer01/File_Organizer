# Step 4 - Format Folder Names

This script renames folders that start with a process number in the
format `YYYY-XXXX` and appends the `config.JUDGEMENT_ID` to build a
standardized 23-digit prefix. It also preserves any suffix text.

The script runs under `config.SIMULATE_STEP_4` and generates reports
of renamed folders and folders that could not be renamed.

---

## Table of Contents

- [How to Run](#how-to-run)
- [Behavior](#behavior)
- [Input Format Example](#input-format-example)
- [Output Format Example](#output-format-example)
- [Output Reports](#output-reports)
- [Example Report](#example-report)
- [Summary](#summary)
- [Script Location](#script-location)

---

## How to Run

Use the Makefile command with the corresponding step:

```bash
make run ARGS="--steps 4"
```

---

## Behavior

- Matches folders that contain a process number like `2023-00138`
- Converts this to: `{JUDGEMENT_ID}20230013800`
- If suffix exists, it's appended and cleaned (e.g., "Contestación")

Folders that fail the format or already have a valid name are skipped.

---

## Input Format Example

Before formatting:

```text
2023-00138 Contestación Albeiro
2023-9 !@#ABC
```

---

## Output Format Example

After formatting:

```text
05380408900120230013800 ContestacionAlbeiro
053804089001202300900 ABC
```

---

## Output Reports

The script generates two reports in:

```bash
./reports/step_4/
```

- `renamed_folders_<timestamp>.csv`
- `folders_requires_manual_review_<timestamp>.csv`

---

## Example Report

### renamed_folders.csv

| ORIGINAL_FOLDER                       | NEW_FOLDER                          |
|---------------------------------------|-------------------------------------|
| /base/2023-00138 Contestación Albeiro | /base/0520230013800 Contestacion... |
| /base/2023-9 !@#ABC                   | /base/05202300900 ABC               |

### folders_requires_manual_review.csv

| FOLDER                       | REASON          |
|------------------------------|-----------------|
| /base/INCORRECT_FOLDER_NAME  | Invalid format  |
| /base/2023-001 Contestación# | Failed renaming |

---

## Summary

This step ensures uniform folder naming for easier indexing and
searching. It is essential for maintaining structure before building
internal hierarchy.

---

## Script Location

```bash
src/organizer/step4_format_folders.py
```

---

🔗 [Back to Main Index](../index.md)
