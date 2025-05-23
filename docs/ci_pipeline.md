# 🔁 Continuous Integration (CI) Pipeline

This document explains the CI pipeline configured in `.github/workflows/ci.yml`
for the **File Organizer & Report Generator** project. The pipeline ensures
code quality, formatting, and correctness across all pull requests and
pushes to `main`.

## 📑 Table of Contents

- [⚙️ Overview](#️-overview)
- [Jobs Defined](#jobs-defined)
  - [Pre-commit Hooks](#pre-commit-hooks)
  - [Unit Tests](#unit-tests)
  - [YAML Validation](#yaml-validation)
  - [Security Audit](#security-audit)
- [🚀 Trigger Conditions](#-trigger-conditions)
- [🔍 Notes](#-notes)

---

## ⚙️ Overview

The CI pipeline uses **GitHub Actions** and is defined in the file:

```bash
.github/workflows/ci.yml
```

Its purpose is to maintain:

- Clean and consistent code formatting
- Functional correctness via testing
- Valid configuration files
- Secure dependencies

---

## Jobs Defined

### Pre-commit Hooks

Runs all pre-configured `pre-commit` checks:

- `black`
- `flake8`
- `isort`
- `trailing-whitespace`
- `end-of-file-fixer`

These checks ensure clean formatting and prevent bad commits from being pushed.

---

### Unit Tests

Runs `pytest` on the `tests/` directory:

- Validates all test cases pass
- Measures test coverage using `pytest-cov`
- Reports missing lines visually

```bash
pytest tests/ --cov=src --cov-report=term-missing
```

---

### YAML Validation

Uses `yamllint` to validate all `.yml` and `.yaml` files across the repo:

- Ensures proper indentation
- Detects syntax issues
- Enforces good practices for CI and configuration files

---

### Security Audit

Uses [`pip-audit`](https://pypi.org/project/pip-audit/) to scan
`requirements.txt`:

- Identifies known vulnerabilities in dependencies
- Recommends safe versions

```bash
pip-audit
```

---

## 🚀 Trigger Conditions

The CI pipeline is triggered on:

```yaml
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
```

This ensures all changes merged into `main` are validated beforehand.

---

## 🔍 Notes

- Python 3.12 is the required version for compatibility.
- All dependencies are installed from `requirements.txt`.
- Each job runs independently in a clean environment (`ubuntu-latest`).

---

🔗 [Back to Main Index](index.md)
