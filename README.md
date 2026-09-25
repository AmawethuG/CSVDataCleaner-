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

