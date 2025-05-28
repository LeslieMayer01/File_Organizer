# 📑 Step 5: Create Electronic Index

This step generates the official electronic index file (`.xlsm`) for each
procedural subfolder (e.g., `C01Principal`). The index follows strict
guidelines for file metadata required by the judicial electronic system.

## 📑 Table of Contents

- [🎯 Objective](#-objective)
- [📁 Target Folders](#-target-folders)
- [📄 Excel Template Rules](#-excel-template-rules)
- [📋 Data Included](#-data-included)
- [🧪 Validations](#-validations)
- [📝 Output File](#-output-file)

---

## 🎯 Objective

Generate an Excel macro-enabled file that lists all documents in each
`C0*` folder, including metadata such as:

- Document name
- Creation date
- Page count
- Format
- File size

---

## 📁 Target Folders

This step applies to folders that:

- Start with `C0` (e.g., `C01Principal`, `C02Incidentes`)
- Are located inside instance folders (e.g., `01PrimeraInstancia`)

The file will be created only if:

- The folder is not empty
- All files pass validation checks (see below)

---

## 📄 Excel Template Rules

- A copy of `FormatoIndiceElectronico.xlsm` is used as the base
- File is renamed as:

```bash
00IndiceElectronicoC0{index_number}.xlsm
```

### Excel Fields Populated

| Cell | Content                            |
|------|-------------------------------------|
| B5   | Case number (Radicado)             |
| B6   | Defendant                           |
| B7   | Plaintiff                           |
| B9   | Folder name (e.g., C01Principal)   |
| J6   | Folder count (`1`)                 |

Each row from A to J will contain:

1. Document name
2. Creation date
3. Creation date (again)
4. File prefix (first two digits of name)
5. Page count
6. Sheet start page
7. Sheet end page
8. File format
9. File size
10. Value `"ELECTRÓNICO"`

---

## 📋 Data Included

Data per document is extracted using:

- PyMuPDF or PyPDF2 (for PDFs)
- `python-docx` (for DOCX)
- File system metadata (creation date, size)

---

## 🧪 Validations

Before generating the index:

- PDF readability (not encrypted/corrupt)
- Excel/Word file validity
- No zero-byte files
- All file names start with a 2-digit numeric prefix

If any issue is detected, the folder is skipped and logged.

---

## 📝 Output File

- One `.xlsm` file per `C0*` folder
- Filename: `00IndiceElectronicoC0{index_number}.xlsm`
- Location: inside the same `C0*` folder
- An optional CSV report is generated for skipped folders (non-compliant)

---

🔗 [Back to Main Index](index.md)
