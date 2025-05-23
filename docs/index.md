# 📚 Project Documentation: File Organizer & Report Generator

Welcome to the official documentation for the **File Organizer & Report
Generator** project. This suite of Python scripts automates the
organization of judicial case files for migration to the Electronic
Document Management System of the Superior Council of the Judiciary.

## 📑 Table of Contents

- [🧭 Purpose](#-purpose)
- [⚙️ Requirements](#️-requirements)
- [🚀 Execution Guide](#-execution-guide)
- [🔢 Process Steps](#-process-steps)
  - [Step 0: Initial Cleanup](step0_cleanup.md)
  - [Step 1: Rename Folders](step1_folder_rename.md)
  - [Step 2: Structure by Instance](step2_subfolders_structure.md)
  - [Step 3: Relocate Subfolders](step3_relocate_folders.md)
  - [Step 4: Organize Files](step4_file_organization.md)
  - [Step 5: Create Electronic Index](step5_electronic_index.md)
- [✍️ File Naming Guidelines](file_naming_guidelines.md)

---

## 🧭 Purpose

Ensure that case files comply with digital document management standards to
allow for proper migration and digital access.

## ⚙️ Requirements

- Python 3.12+
- pip
- Git
- Chocolatey (Windows only)
- Make (optional for simplified commands)

## 🚀 Execution Guide

Run the project using Make:

```bash
make check      # Validate prerequisites
make setup      # Install virtual environment and dependencies
make run ARGS="--steps 1 2 3 4 5"
```

Or run specific scripts manually from the terminal:

```bash
python src/organizer/step5_create_electronic_index.py
```

---

## 🔢 Process Steps

Each step is documented in its own file within the `docs/` folder:

- **[Step 0](step0_cleanup.md):** Remove empty folders and old index files.
- **[Step 1](step1_folder_rename.md):** Rename folders based on judicial
case IDs.
- **[Step 2](step2_subfolders_structure.md):** Create structured subfolders
by legal instance.
- **[Step 3](step3_relocate_folders.md):** Relocate `C0*` folders under their
corresponding instance.
- **[Step 4](step4_file_organization.md):** Sort and rename files inside each
subfolder.
- **[Step 5](step5_electronic_index.md):** Automatically generate the electronic
index in `.xlsm` format.

For more information, see each corresponding documentation file.

## 🧑‍💻 Development & Ownership

- [🔁 CI Pipeline](ci_pipeline.md)
- [👥 CODEOWNERS Explained](codeowners_explained.md)
