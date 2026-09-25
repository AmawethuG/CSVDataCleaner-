A Python-based data engineering project that cleans, validates, and prepares legal case data stored in CSV files.

The project demonstrates a simple data pipeline:

```text
Raw CSV Data
     ↓
Data Cleaning
     ↓
Data Validation / Tests
     ↓
Processed CSV Data
     ↓
Docker
     ↓
CI/CD Pipeline
```

---

## Project Structure

```text
CSVDataCleaner-/
│
├── data/
│   ├── raw/
│   │   └── cases.csv
│   │
│   └── processed/
│       └── cases_clean.csv
│
├── src/
│   └── csv_cleaner.py
│
├── tests/
│   └── test_csv_cleaner.py
│
├── reports/
│
├── Dockerfile
├── .dockerignore
├── Makefile
├── requirements.txt
└── README.md
```

---

## What Each File Does

### `data/raw/cases.csv`

This is the **raw input dataset**.

It contains the original legal case records before cleaning.

Example fields include:

```text
case_id
case_name
court_level
court_name
province
city
filing_date
decision_date
case_duration_days
case_type
charge_or_claim
verdict
fine_amount_zar
settlement_amount_zar
sentence_years
appealed
appeal_result
```

The raw data should remain unchanged so that the cleaning process can always be reproduced from the original source.

---

### `data/processed/cases_clean.csv`

This is the **output dataset** produced by the cleaning pipeline.

The cleaner:

* removes duplicate rows
* removes unnecessary whitespace
* converts numeric columns into numeric data types
* converts date columns into datetime values
* saves the cleaned dataset as a new CSV file

The raw dataset is not overwritten.

---

### `src/csv_cleaner.py`

This is the main **data cleaning program**.

It:

1. Reads the raw CSV file.
2. Removes duplicate records.
3. Removes extra whitespace from text columns.
4. Converts numeric columns.
5. Converts date columns.
6. Writes the cleaned data to `data/processed/cases_clean.csv`.

The main function is:

```python
clean_data(input_file, output_file)
```

This makes the cleaner reusable because it can receive different input and output files.

---

### `tests/test_csv_cleaner.py`

This file contains the **automated tests** for the data cleaning program.

The tests check whether the cleaner behaves as expected.

Examples include:

* duplicate records are removed
* whitespace is removed from text fields
* numeric values are handled correctly
* dates are handled correctly
* cleaned output is generated

The tests use temporary files so that testing does not modify the real dataset.

---

### `requirements.txt`

This file contains the Python dependencies required by the project.

For example:

```text
pandas
pytest
```

Install the dependencies with:

```bash
pip3 install -r requirements.txt
```

---

### `Makefile`

The `Makefile` provides simple commands for common project operations.

Instead of remembering long commands, you can run:

```bash
make install
make test
make run
make clean
make docker-build
```

Current Makefile targets:

```text
install       Install Python dependencies
test          Run automated tests
run           Run the data cleaning pipeline
clean         Remove generated files
docker-build  Build the Docker image
```

---

### `Dockerfile`

The `Dockerfile` defines the environment required to run the application inside Docker.

It allows the project to run consistently without depending on the Python environment installed directly on the computer.

Build the Docker image with:

```bash
docker build -t csv-data-cleaner .
```

The Makefile provides a shortcut:

```bash
make docker-build
```

---

### `.dockerignore`

This file tells Docker which files and directories should **not** be copied into the Docker build context.

This prevents unnecessary files such as:

```text
.git/
.pytest_cache/
__pycache__/
```

from being included in the Docker image.

---

### `reports/`

This directory is reserved for generated reports from the data pipeline.

For example, future versions of the project could generate:

* data quality reports
* cleaning summaries
* validation reports
* pipeline statistics

---

### `README.md`

This file documents the project.

It explains:

* what the project does
* how to install it
* how to run it
* how to test it
* how Docker is used
* how the pipeline works
* what each project file is responsible for

---

# Installation

Clone the repository:

```bash
git clone <repository-url>
```

Move into the project:

```bash
cd CSVDataCleaner-
```

Install the dependencies:

```bash
make install
```

Or manually:

```bash
pip3 install -r requirements.txt
```

---

# Running the Data Cleaner

The simplest way to run the cleaner is:

```bash
make run
```

This executes:

```bash
python3 src/csv_cleaner.py
```

The cleaner reads:

```text
data/raw/cases.csv
```

and creates:

```text
data/processed/cases_clean.csv
```

A successful run should produce output similar to:

```text
Cleaned 25 records.
Saved to data/processed/cases_clean.csv
```

---

# Running the Cleaner Manually

You can also run the Python program directly:

```bash
python3 src/csv_cleaner.py
```

This is useful when debugging the Python program itself.

---

# Validating the Cleaned Data

After running the cleaner, inspect the generated CSV:

```bash
head data/processed/cases_clean.csv
```

Check the number of records:

```bash
wc -l data/processed/cases_clean.csv
```

Because the CSV contains a header, the number of data records is one less than the line count.

You can also inspect the columns and data types with Python:

```bash
python3 -c "import pandas as pd; df=pd.read_csv('data/processed/cases_clean.csv'); print(df.dtypes)"
```

---

# Running Automated Tests

Run the complete test suite with:

```bash
make test
```

This executes:

```bash
python3 -m pytest
```

You can also run pytest directly:

```bash
python3 -m pytest
```

The tests verify the behaviour of the cleaning pipeline without modifying the real production dataset.

---

# Cleaning the Project

To remove generated files and temporary Python files:

```bash
make clean
```

This removes:

```text
data/processed/*
reports/*
.pytest_cache
src/__pycache__
tests/__pycache__
```

The raw dataset in:

```text
data/raw/
```

is not deleted.

---

# Docker

Docker packages the application and its dependencies into a container.

## Build the Docker Image

Run:

```bash
make docker-build
```

This is equivalent to:

```bash
docker build -t csv-data-cleaner .
```

Check that the image was created:

```bash
docker images
```

You should see:

```text
csv-data-cleaner
```

---

## Run the Docker Container

Once the image has been built:

```bash
docker run --rm csv-data-cleaner
```

The container runs the data-cleaning application in an isolated environment.

---

# Complete Local Workflow

A typical development workflow is:

```bash
make install
```

Install dependencies.

Then:

```bash
make test
```

Run the automated tests.

Then:

```bash
make run
```

Run the data cleaning pipeline.

Then validate the generated data:

```bash
head data/processed/cases_clean.csv
```

If Docker is available:

```bash
make docker-build
```

Then:

```bash
docker run --rm csv-data-cleaner
```

---

# Pipeline Workflow

The project is designed around the following pipeline:

```text
                    ┌─────────────────┐
                    │  Raw CSV Data   │
                    │  cases.csv      │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ csv_cleaner.py  │
                    │                 │
                    │ • Remove        │
                    │   duplicates    │
                    │ • Strip spaces  │
                    │ • Convert       │
                    │   numbers       │
                    │ • Convert dates │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Clean CSV Data  │
                    │ cases_clean.csv │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Automated Tests │
                    │     pytest      │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │     Docker      │
                    │                 │
                    │ Reproducible    │
                    │ environment     │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    CI / CD      │
                    │ Automated       │
                    │ pipeline        │
                    └─────────────────┘
```

---

# CI/CD Pipeline

The project can use GitLab CI/CD to automatically test the project whenever changes are pushed.

The intended pipeline is:

```text
Git Push
   ↓
CI Pipeline Starts
   ↓
Install Dependencies
   ↓
Run Tests
   ↓
Run Data Cleaner
   ↓
Build Docker Image
```

The CI/CD configuration will be stored in:

```text
.gitlab-ci.yml
```

The pipeline will use the Makefile commands instead of duplicating commands:

```bash
make install
make test
make run
make docker-build
```

This means the same commands can be used locally and inside CI.

---

# Makefile Command Reference

| Command             | Purpose                        |
| ------------------- | ------------------------------ |
| `make install`      | Install Python dependencies    |
| `make test`         | Run automated tests            |
| `make run`          | Run the data cleaning pipeline |
| `make clean`        | Remove generated files         |
| `make docker-build` | Build the Docker image         |

---

# Example Development Workflow

```bash
# 1. Get the latest code
git pull

# 2. Install dependencies
make install

# 3. Run tests
make test

# 4. Run the cleaner
make run

# 5. Inspect the output
head data/processed/cases_clean.csv

# 6. Build Docker image
make docker-build

# 7. Run the Docker container
docker run --rm csv-data-cleaner

# 8. Check Git changes
git status

# 9. Commit changes
git add .
git commit -m "feat: improve data cleaning pipeline"

# 10. Push changes
git push
```

---

# Data Engineering Concepts Demonstrated

This project demonstrates several fundamental data engineering concepts:

* CSV data ingestion
* Data cleaning
* Data transformation
* Data validation
* Automated testing
* Reproducible environments
* Docker containerisation
* Makefile automation
* CI/CD
* Version control with Git
* Pipeline automation

The project can later be extended with:

* SQL/database storage
* data quality reports
* logging
* schema validation
* larger datasets
* scheduled pipeline execution
* cloud storage
* ETL/ELT workflows
* data visualisation
* analytics dashboards