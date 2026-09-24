import subprocess


def run_pipeline():
    print("Starting data pipeline...")

    print("\n1. Cleaning data...")
    subprocess.run(["python3", "src/csv_cleaner.py"], check=True)

    print("\n2. Validating data...")
    result = subprocess.run(
        ["python3", "src/validator.py"],
        check=False
    )

    if result.returncode != 0:
        print("\nPipeline failed during validation.")
        return

    print("\nPipeline completed successfully.")


if __name__ == "__main__":
    run_pipeline()