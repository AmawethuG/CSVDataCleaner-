import pandas as pd


def clean_data(input_file, output_file):
    df = pd.read_csv(input_file)

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Remove extra spaces from text values
    for column in df.select_dtypes(include="object"):
        df[column] = df[column].str.strip()

    # Convert known numeric columns
    numeric_columns = [
        "case_id",
        "case_duration_days",
        "fine_amount_zar",
        "settlement_amount_zar",
        "sentence_years",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    # Convert dates
    df["filing_date"] = pd.to_datetime(df["filing_date"], errors="coerce")
    df["decision_date"] = pd.to_datetime(df["decision_date"], errors="coerce")

    df.to_csv(output_file, index=False)

    print(f"Cleaned {len(df)} records.")
    print(f"Saved to {output_file}")

if __name__ == "__main__":
    clean_data(
        "data/raw/cases.csv",
        "data/processed/cases_clean.csv"
    )