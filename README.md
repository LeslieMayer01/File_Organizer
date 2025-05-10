# 📁 File Organizer & Report Generator (Python)

This project is a collection of Python scripts that organize external folders
and files based on naming rules and generate various reports in CSV format.

## 📌 Features

- Cleans empty folders
- Renames folders and files based on rules and a dictionary
- Organizes files into structured folders (e.g., `C01_`, `C04_`)
- Generates multiple CSV reports:
  - All folder names with paths
  - Unique folder names
  - File type extensions and counts
  - Excel files with the word "indice" in the name
- Identifies empty files and files without extensions

## 🚀 Getting Started

### ✅ Prerequisites

Ensure you have the following installed:

- Python 3.8+
- pip
- Git
- (Optional) `make` to simplify setup

### 🔧 Setup

You can run the setup automatically with `make`:

```bash
make check      # Check prerequisites
make setup      # Create virtual environment and install dependencies
```

Or manually:

```bash
python -m venv venv
venv\Scripts\activate      # On Windows
source venv/bin/activate  # On Linux/macOS

pip install -r requirements.txt
pre-commit install
```

## 🧩 Usage

Run a specific script (e.g. generate the index file):

```bash
make run ARGS="--steps 1 2 3"
```

## 📂 Project Structure

```text
.
├── data/                     # Helper files with data required by the scripts
├── docs/                     # Extra documentation
├── src/                      # Source of python code
├── tests/                    # Unit tests
├── v0-1/                     # Deprecated scripts (Will be removed)
├── tests/                    # Python virtual environment
├── .gitignore                # G configurations
├── .pre-commit-config.yaml   # Linting rules
├── requirements.txt          # Python requirements
├── README.md                 # Main documentation page
└── Makefile                  # Helper commands to run the project
```

## 🧪 Development

To run linting and enforce code standards:

```bash
make lint
```

Pre-commit hooks are configured for:

- black
- flake8
- isort
- end-of-file-fixer
- trailing-whitespace

## 🙌 Contributing

Pull requests are welcome. For major changes, please open an issue first.
