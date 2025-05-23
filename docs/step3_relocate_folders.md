# 📂 Step 3: Relocate Subfolders Inside Case Instances

This step ensures that all `C0*` subfolders are moved under their corresponding
instance folder (e.g., `01PrimeraInstancia`) and that standalone files are
properly stored.

## 📑 Table of Contents

- [🎯 Objective](#-objective)
- [📁 Expected Structure](#-expected-structure)
- [⚙️ Process Description](#️-process-description)
- [📤 File Reallocation Logic](#-file-reallocation-logic)
- [📝 Output Report](#-output-report)

---

## 🎯 Objective

To maintain consistency in the folder structure by relocating topic-based
folders and documents to the correct procedural instance subfolder.

---

## 📁 Expected Structure

Before relocation:

```text
<Case Folder>/
├── 01PrimeraInstancia/
├── C01Principal/
├── C05MedidasCautelares/
├── archivo1.jpg
├── subsanacion/
```

After relocation:

```text
<Case Folder>/
├── 01PrimeraInstancia/
│   ├── C01Principal/
│   │   └── archivo1.jpg
│   ├── C05MedidasCautelares/
├── subsanacion/
```

---

## ⚙️ Process Description

1. Traverse all folders that start with the first 5 digits of the
court code (e.g., `05380`).
2. If a folder named `01PrimeraInstancia` exists:
   - Move all `C0*` folders into it.
   - Move loose files (e.g., `.jpg`, `.pdf`) into
   `01PrimeraInstancia/C01Principal/`.

---

## 📤 File Reallocation Logic

- All files located in the root of the case folder and not inside a
`C0*` or `01*` subfolder will be relocated to:
  - `01PrimeraInstancia/C01Principal/`

This guarantees all procedural documents are organized by instance and topic.

---

## 📝 Output Report

- A CSV file summarizing:
  - Moved folders and files
  - Their source and destination paths

---

🔗 [Back to Main Index](index.md)
