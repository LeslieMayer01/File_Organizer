# 🏛️ Step 2: Structure Subfolders by Instance

This step ensures that each case folder is divided into standardized subfolders
based on the judicial instance (e.g., First Instance, Second Instance,
Execution). It also identifies and renames thematic subfolders.

## 📑 Table of Contents

- [🎯 Objective](#-objective)
- [📁 Folder Structure](#-folder-structure)
- [⚙️ Process Description](#️-process-description)
- [🧠 Subfolder Detection Logic](#-subfolder-detection-logic)
- [📝 Output Reports](#-output-reports)

---

## 🎯 Objective

Create and standardize subfolders within each case file to separate
procedural stages and related topics, enhancing clarity and navigability.

---

## 📁 Folder Structure

Each case folder may contain the following structure:

```text
<Case Folder>/
├── 01PrimeraInstancia/ (or 01UnicaInstancia/)
│   ├── C01Principal/
│   ├── C02Incidentes/
│   ├── C03AcumulacionProcesos/
│   ├── C04DepositosJudiciales/
│   └── C05MedidasCautelares/
```

- `01PrimeraInstancia` / `01UnicaInstancia`: Primary procedural folder
- `C0*`: Subfolders by topic, labeled with standardized codes

---

## ⚙️ Process Description

1. Traverse each case folder using the first 5 digits of the court's radicado.
2. If `01PrimeraInstancia` or `01UnicaInstancia` does not exist,
create `01PrimeraInstancia`.
3. Detect and rename thematic subfolders using pattern matching.
4. If no `C0*` folder exists and only files are present, create `C01Principal`.

---

## 🧠 Subfolder Detection Logic

Using keyword detection, rename folders as follows:

| Keyword Group            | New Folder Name           |
|--------------------------|---------------------------|
| principal, ppal, unico   | C01Principal              |
| incidente, incidentes    | C02Incidentes             |
| acumulacion              | C03AcumulacionProcesos    |
| deposito, titulo, DJ04   | C04DepositosJudiciales    |
| medida cautelar, M.C     | C05MedidasCautelares      |

> Keywords are matched case-insensitively and may be refined using the folder
> names report.

---

## 📝 Output Reports

- **Renamed folders report** with:
  - Original name
  - New name
  - Full path
- **Created folders report** for new `01PrimeraInstancia` and `C01Principal`
folders

---

🔗 [Back to Main Index](index.md)
