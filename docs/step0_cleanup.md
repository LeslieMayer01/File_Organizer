# 🧹 Step 0: Cleanup of Empty Folders and Obsolete Index Files

This step prepares the working directory by removing unnecessary content that
may interfere with the file organization process. It focuses on detecting and
deleting empty folders and outdated index files.

## 📑 Table of Contents

- [🎯 Objective](#-objective)
- [📝 File Identification Criteria](#-file-identification-criteria)
- [⚙️ Execution Description](#️-execution-description)
- [📁 Expected Outputs](#-expected-outputs)
- [💡 Notes and Considerations](#-notes-and-considerations)

---

## 🎯 Objective

To perform an initial cleanup of the root directory by removing:

- Empty folders.
- Excel files containing the word `indice` (case-insensitive), which are
considered outdated index files.

This ensures that only relevant and updated content is processed in
subsequent steps.

---

## 📝 File Identification Criteria

A file will be considered an obsolete index file if:

- It has the `.xlsx` or `.xlsm` extension.
- The filename contains the substring `indice` in any letter case (e.g.,
`Indice`, `índice`, `INDICE`).

Empty folders are identified as directories with no files or subdirectories
inside.

---

## ⚙️ Execution Description

The cleanup script performs the following operations:

1. Recursively traverses the specified root directory.
2. Generates a CSV report listing:
   - All Excel files that match the `indice` keyword.
   - All detected empty folders.
3. Deletes:
   - All matching index files.
   - All empty folders.

The process logs and reports all actions taken.

---

## 📁 Expected Outputs

- A CSV report containing:
  - Names and full paths of deleted files.
  - Paths of deleted folders.
- A clean directory structure ready for file renaming and reorganization in
Step 1.

---

## 💡 Notes and Considerations

- The detection is case-insensitive and locale-aware.
- It is recommended to back up the original folder before running the cleanup
step.
- No changes are made to files outside the specified conditions.

---

🔗 [Back to Main Index](index.md)
