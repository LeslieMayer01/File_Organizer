# Step 5 - Create C0 Folder Structure

This script analyzes folders whose names begin with the
`config.JUDGEMENT_ID` and restructures them to standardize their
internal layout. It supports different scenarios depending on the
contents of each folder.

---

## Table of Contents

- [How to Run](#how-to-run)
- [Scenarios](#scenarios)
- [Behavior](#behavior)
- [Before and After Example](#before-and-after-example)
- [Output Reports](#output-reports)
- [Example Report](#example-report)
- [Summary](#summary)
- [Script Location](#script-location)

---

## How to Run

Use the Makefile command with the corresponding step:

```bash
make run ARGS="--steps 5"
```

---

## Scenarios

The script supports the following scenarios:

### Scenario 1: Folder contains only files

All files are moved into the following structure:

```bash
01PrimeraInstancia/C01Principal/
```

### Scenario 2: Folder contains subfolders and files

- Files outside folders are reported for manual review
- Each subfolder is renamed based on keyword mapping to match the
  standardized C0 structure (e.g. "Ppal" → "C01Principal")

---

## Behavior

- Subfolders are renamed if their name contains known keywords
- A mapping is used to match keywords with canonical folder names
- Unrecognized subfolders or skipped files are logged for review
- Simulation mode is controlled with `config.SIMULATE_STEP_5`

---

## Before and After Example

### Input Folder

```text
/05380408900120230013800 Contestacion/
├── prueba.doc
├── medida cautelar/
└── ppal/
```

### Output Folder

```text
/05380408900120230013800 Contestacion/
├── 01PrimeraInstancia/
│   ├── C01Principal/         ← from "ppal"
│   └── C05MedidasCautelares/ ← from "medida cautelar"
```

---

## Output Reports

Reports are generated in:

```bash
./reports/step_5/
```

- `renamed_subfolders_<timestamp>.csv`
- `skipped_subfolders_<timestamp>.csv`
- `files_requires_manual_review_<timestamp>.csv`

---

## Example Report

### renamed_subfolders.csv

| ORIGINAL_FOLDER         | NEW_FOLDER             |
|-------------------------|------------------------|
| /folder/ppal            | /folder/C01Principal   |
| /folder/medida cautelar | /folder/C05Medidas...  |

### files_requires_manual_review.csv

| FILE_PATH                        |
|----------------------------------|
| /folder/some_loose_document.docx |

---

## Summary

This step ensures that folder contents are organized under a common C0
hierarchy. It makes subsequent indexing and document identification
easier by enforcing consistent structure.

---

## Script Location

```bash
src/organizer/step5_create_C0_folders.py
```

---

🔗 [Back to Main Index](../index.md)
