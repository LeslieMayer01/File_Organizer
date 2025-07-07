# 📚 File Organizer - Documentation Index

Welcome to the documentation for the File Organizer and Report Generator
project. This tool is designed to streamline the preparation of digital
case files and ensure structured, traceable folder hierarchies.

---

## 🧭 Table of Contents

- [Steps Overview](#steps-overview)
- [Reference Guides](#reference-guides)
- [Assets](#assets)

---

## Steps Overview

Each step represents a sequential transformation applied to the input
folders.

- [Step 1 - Delete Empty Folders](steps/step1_delete_empty_folders.md)
- [Step 2 - Delete Index Files](steps/step2_delete_index_files.md)
- [Step 3 - Remove desktop.ini](steps/step3_remove_desktop_ini.md)
- [Step 4 - Format Folder Names](steps/step4_format_folders.md)
- [Step 5 - Create C0 Folders](steps/step5_create_C0_folders.md)
- [Step 6 - Organize Files in C0 Folders](steps/step6_organizate_files.md)
- [Step 7 - Subfolder Organization](steps/step7_subfolder_organization.md)
- [Step 8 - Create Electronic Index](steps/step8_create_electronic_index.md)
- [Step 9 - Check Folder Naming](steps/step9_check_folders.md)

---

## Reference Guides

- [CI Pipeline Overview](references/ci_pipeline.md)
- [Codeowners Explained](references/codeowners_explained.md)
- [File Naming Guidelines](references/file_naming_guidelines.md)

---

## Assets

- [Folder Structure Diagram](assets/folder_structure.jpg)

---

Feel free to explore each step in detail and use the Makefile commands
to run them individually or in sequence.

```bash
make run ARGS="--steps <number>"
```

---
