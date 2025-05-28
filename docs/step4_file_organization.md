# 🗃️ Step 4: Organize and Rename Files

This step organizes the documents inside each `C0*` folder by ordering
and renaming them based on defined conventions, making them easier to
read and ready for indexing.

## 📑 Table of Contents

- [🎯 Objective](#-objective)
- [🔍 File Sorting Logic](#-file-sorting-logic)
- [✏️ Renaming Rules](#️-renaming-rules)
- [📝 Output Report](#-output-report)

---

## 🎯 Objective

To organize all files in each `C0*` folder by applying:

- Sorting by number or creation date
- Filename cleanup and normalization
- Assignment of positional prefix numbers

---

## 🔍 File Sorting Logic

1. **If all files start with digits:**
   - Use prefix to sort:
     - Use 3 digits if more than 100 files
     - Otherwise, use 2 digits
2. **If not all files are numbered:**
   - Sort by file creation date (ascending)

---

## ✏️ Renaming Rules

After sorting:

1. Remove existing numeric prefix and special characters
2. Keep the file extension
3. Truncate to a maximum of **35 characters**
4. Apply new name with index number prefix:
   - `01 DocumentName.ext`
   - `02 DocumentName 01.ext` (if duplicated)

### Example

Original name:

```bash
02 2023-00094 2023-07-14 Memorial-admisión.pdf
```

Transformed:

```bash
01 Memorialadmision.pdf
```

> Duplicates are renamed as `DocumentName 01`, `DocumentName 02`, etc.

---

## 📝 Output Report

A CSV file containing:

- Original file name
- Final file name
- Folder path
- Order applied (by number or date)

---

🔗 [Back to Main Index](index.md)
