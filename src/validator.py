import pandas as pd


def validate_data(input_file):
    df = pd.read_csv(input_file)

    errors = []

    # Check for missing case IDs
    if df["case_id"].isnull().any():
        errors.append("Some case IDs are missing.")

    # Check for duplicate case IDs
    if df["case_id"].duplicated().any():
        errors.append("Duplicate case IDs found.")

    # Check for negative values
    if (df["case_duration_days"] < 0).any():
        errors.append("Negative case duration found.")

    if (df["fine_amount_zar"] < 0).any():
        errors.append("Negative fine amount found.")

    if (df["settlement_amount_zar"] < 0).any():
        errors.append("Negative settlement amount found.")

    # Convert dates for validation
    df["filing_date"] = pd.to_datetime(df["filing_date"], errors="coerce")
    df["decision_date"] = pd.to_datetime(df["decision_date"], errors="coerce")

    # Check date order
    if (df["filing_date"] > df["decision_date"]).any():
        errors.append("Some filing dates occur after decision dates.")

    # Check appealed values
    valid_appealed_values = {"Yes", "No"}

    invalid_appealed = set(df["appealed"].dropna()) - valid_appealed_values

    if invalid_appealed:
        errors.append(
            f"Invalid appealed values found: {invalid_appealed}"
        )

    return errors


def main():
    input_file = "data/processed/cases_clean.csv"

    errors = validate_data(input_file)

    if errors:
        print("Data validation failed:")

        for error in errors:
            print(f"- {error}")

    else:
        print("Data validation passed.")


if __name__ == "__main__":
    main()