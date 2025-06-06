# Step 7 - Organize Subfolders by Logical Group

This script searches for all folders that start with the configured
`config.JUDGEMENT_ID` and groups their internal `C0*` subfolders into
logical containers (e.g., `01PrimeraInstancia`, `02SegundaInstancia`)
based on the mapping provided in the JSON file specified by
`config.FOLDER_MAPPINGS`.

---

## Table of Contents

- [How to Run](#how-to-run)
- [Behavior](#behavior)
- [Before and After Example](#before-and-after-example)
- [Folder Mapping](#folder-mapping)
- [Output Reports](#output-reports)
- [Example Report](#example-report)
- [Summary](#summary)
- [Script Location](#script-location)

---

## How to Run

Use the Makefile command with the corresponding step:

```bash
make run ARGS="--steps 7"
```

---

## Behavior

- Finds all folders starting with `config.JUDGEMENT_ID`
- For each, checks if all children are folders beginning with `C0`
- If valid, it moves each subfolder into a parent folder based on its
  code (e.g., `C01` → `01PrimeraInstancia`)
- Uses the mapping file configured in `config.FOLDER_MAPPINGS`
- If the folder does not follow the expected structure, it is reported

---

## Before and After Example

### Input Structure

```text
/05380408900120230013800/
├── C01Principal/
├── C05Medidas/
├── C06Apelacion/
```

### Output Structure

```text
/05380408900120230013800/
├── 01PrimeraInstancia/
│   ├── C01Principal/
│   └── C05Medidas/
└── 02SegundaInstancia/
    └── C06Apelacion/
```

---

## Folder Mapping

Example contents of `config.FOLDER_MAPPINGS`:

```json
{
  "C01": "01PrimeraInstancia",
  "C05": "01PrimeraInstancia",
  "C06": "02SegundaInstancia",
  "C08": "03RecursosExtraordinarios",
  "C10": "04Ejecucion"
}
```

---

## Output Reports

Reports are saved to:

```bash
./reports/step_7/
```

- `c0_folders_moved_<timestamp>.csv`
- `c0_folders_skipped_<timestamp>.csv`

---

## Example Report

### c0_folders_moved.csv

| ORIGINAL_PATH    | NEW_PATH                            |
|------------------|-------------------------------------|
| /folder/C01alpha | /folder/01PrimeraInstancia/C01alpha |
| /folder/C06beta  | /folder/02SegundaInstancia/C06beta  |

### c0_folders_skipped.csv

| FOLDER_REQUIRES_MANUAL_REVIEW             |
|-------------------------------------------|
| /folder_with_files_and_non_c0_subfolders  |

---

## Summary

This step helps organize subfolders into logical categories, which is
crucial for downstream processing and structured indexing. It separates
folders based on their C0 prefix into standardized instances.

---

## Script Location

```bash
src/organizer/step7_subfolder_organization.py
```

---

🔗 [Back to Main Index](../index.md)
