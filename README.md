# 📁 File Organizer & Report Generator (Python)

This project is a modular set of Python scripts designed to clean, format,
organize, and standardize folders of legal case files. It also produces
CSV and Excel reports for traceability and institutional archiving.

---

## 🧭 Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Setup](#setup)
- [Usage](#usage)
- [Docker Workflow](#docker-workflow)
- [Development](#development)
- [Documentation](#documentation)
- [Project Structure](#project-structure)
- [Contributing](#contributing)

---

## Features

- Deletes empty folders and index files
- Cleans `desktop.ini` system files
- Formats folder names to a 23-digit identifier + suffix
- Creates structured folders like `C01Principal`, `C05MedidasCautelares`
- Groups files under `01PrimeraInstancia`, `02SegundaInstancia`, etc.
- Generates `.xlsm` electronic index files
- Detects folders with naming issues and produces reports

---

## Requirements

- Python 3.12+
- pip
- Git
- Docker (for isolated execution)
- make

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/your/repo.git
cd repo
```

### 2. Configure `.env`

```bash
cp .env-example .env
```

Define `FOLDER_TO_ORGANIZE`, simulation flags, and paths to resources.

### 3. Run environment checks and Docker image build

```bash
make check-all
make docker-build
```

---

## Usage

### ▶ Run specific step(s)

```bash
make docker-run ARGS="--steps 1"
```

You can combine multiple steps:

```bash
make docker-run ARGS="--steps 1 2 3"
```

Each step generates reports under:

```bash
reports/step_<n>/
```

---

## Docker Workflow

All scripts run inside a container using:

```bash
make docker-run ARGS="--steps 4"
```

The folder defined in `.env` as `FOLDER_TO_ORGANIZE` is mounted at `/data`
inside the container. All reports are mounted to `/app/reports`.

You can rebuild or clean the image:

```bash
make docker-build
make docker-clean
```

---

## Development

Run tests and validations locally:

```bash
make lint        # Ruff linter
make test        # Run all unit tests
make typecheck   # mypy static type check
make coverage    # Show test coverage
make format      # Auto-format with ruff
```

To run a step outside Docker:

```bash
make run-step-4
```

---

## Documentation

All scripts are documented in Markdown format in `docs/steps/`. The main
index is located at:

```text
docs/index.md
```

Each step has:

- Description and goal
- Folder structure before/after
- Sample reports
- How to run and simulate

You can validate docs with:

```bash
make docs-validate
```

---

## Project Structure

```text
.
├── Makefile                 # Main Makefile
├── makefiles/               # Sub-makefiles (docker, dev, docs, steps)
├── src/                     # Python scripts (step1 to step9)
├── tests/                   # Unit tests
├── reports/                 # Generated output
├── docs/
│   ├── index.md             # Documentation index
│   ├── steps/               # Step-by-step documentation
│   ├── references/          # Guidelines and conventions
│   └── assets/              # Images, diagrams
├── .env                     # Environment variables
├── requirements.txt         # Dependencies
└── README.md
```

---

## Contributing

Pull requests are welcome. For significant changes, please open an issue
first and describe your proposal.

---

ℹ️ Created with 💻 and 🧠 by Jorge and Leslie
