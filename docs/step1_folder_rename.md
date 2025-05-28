# 🗂️ Step 1: Rename Case Folders Based on Judicial ID

This step ensures that folder names follow a standardized format that includes
the court code and case number, making them suitable for the electronic
judicial system.

## 📑 Table of Contents

- [🎯 Objective](#-objective)
- [🔍 Validation Rules](#-validation-rules)
- [✏️ Renaming Strategy](#️-renaming-strategy)
- [📝 Output Report](#-output-report)

---

## 🎯 Objective

To validate and rename case folders so that they follow a structured naming
convention required by the document management system.

---

## 🔍 Validation Rules

A folder is considered valid if:

- Its name starts with **23 digits** (court code + case number + suffix `00`).
  - Example (valid): `05380408900120230009400`
  - Example (invalid): `2023-00234 Ejecutivo Singular`

The 23-digit identifier is composed of:

- **First 12 digits:** Judicial court code.
- **Next 9 digits:** Judicial case number.
- **Last 2 digits:** Always `00` (fixed suffix).

---

## ✏️ Renaming Strategy

If the folder name does not match the required format, the following
adjustments are applied:

1. Extract the original name components: court code, case number, suffix.
2. Reconstruct the name using the correct format.
3. Remove all whitespaces and special characters.
4. Truncate the final name to a **maximum of 39 characters**.
5. If a folder with the new name already exists, generate a CSV report
and skip renaming.

📌 **Example:**

- Original name: `2023-00234 Ejecutivo Singular`
- Transformed name: `05380408900120230009400EjecutivoSingular`

If the folder includes descriptions, retain them after the identifier:

- Final format: `05380408900120230009400 EjecutivoSingular`

---

## 📝 Output Report

A CSV report is generated with the following information:

- Original folder name
- New folder name
- Full path

This report helps trace all changes and review any naming conflicts.

---

🔗 [Back to Main Index](index.md)
