# Step 8 - Create Electronic Index

This script generates an electronic index in Excel format (`.xlsm`)
for each folder that starts with the configured `config.JUDGEMENT_ID`.

The output file is named using the format:
`00IndiceElectronicoC0{23_digit_code}.xlsm`

---

## Table of Contents

- [How to Run](#how-to-run)
- [Behavior](#behavior)
- [Generated Structure](#generated-structure)
- [Output Files](#output-files)
- [Example Output](#example-output)
- [Summary](#summary)
- [Script Location](#script-location)

---

## How to Run

Use the Makefile command with the corresponding step:

```bash
make run ARGS="--steps 8"
```

---

## Behavior

- Searches for folders starting with `config.JUDGEMENT_ID`
- Extracts a 23-digit identifier from each folder name
- Creates an Excel file in the same folder named:
  `00IndiceElectronicoC0{identifier}.xlsm`
- Uses a macro-enabled template (`.xlsm`) provided in the project

---

## Generated Structure

If input is:

```text
/05380408900120230013800/
```

After execution:

```text
/05380408900120230013800/
└── 00IndiceElectronicoC005380408900120230013800.xlsm
```

---

## Output Files

All index files are saved in their respective folder.

No report file is generated in this step, since the output is the
Excel file itself. Any errors during generation will raise an
exception and should be handled by the orchestrator.

---

## Example Output

| SHEET      | COLUMNS                                         |
|------------|-------------------------------------------------|
| IndexSheet | Index Number, Folder Code, File Name, Date, ... |

The content depends on the files found and may include macros or
validation checks.

---

## Summary

This step generates the official electronic index for each case
folder, ensuring a standardized and verifiable format for
institutional archiving or transfer.

---

## Script Location

```bash
src/organizer/step8_create_electronic_index.py
```

---

🔗 [Back to Main Index](../index.md)
