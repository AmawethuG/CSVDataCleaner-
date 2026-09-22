import pandas as pd


def clean_data(input_file, output_file):
    df = pd.read_csv(input_file)

    #Remove duplicate rows
    df = df.drop_duplicates()

    #Clear out and remove extra spaces from text values
    for column in df.select_dtypes(include="object"):
        df[column

def clean_csv(input_file, cleaned_file, report_file):
    # Load CSV
    df = pd.read_csv(input_file)
    original_rows = len(df)

    # Drop duplicate rows
    df = df.drop_duplicates()
    cleaned_rows = len(df)

    # Count missing values before cleaning
    missing_before = df.isnull().sum()

    # Fill missing values
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            # Numeric column: fill NaN with mean
            df[col] = df[col].fillna(df[col].mean())
        else:
            # Try converting to numeric (if mixed types)
            df[col] = pd.to_numeric(df[col], errors='coerce')
            if pd.api.types.is_numeric_dtype(df[col]):
                df[col] = df[col].fillna(df[col].mean())
            else:
                # Non-numeric column: fill NaN with "UNKNOWN"
                df[col] = df[col].fillna("UNKNOWN")

    # Count missing values after cleaning
    missing_after = df.isnull().sum()

    # Summary statistics
    summary = df.describe(include='all')

    # Save cleaned CSV
    df.to_csv(cleaned_file, index=False)

    # Write report
    with open(report_file, "w") as f:
        f.write("CSV CLEANING REPORT\n")
        f.write("===================\n\n")
        f.write(f"Original rows: {original_rows}\n")
        f.write(f"Rows after removing duplicates: {cleaned_rows}\n")
        f.write(f"Duplicates removed: {original_rows - cleaned_rows}\n\n")
        f.write("Missing Values BEFORE Cleaning:\n")
        f.write(str(missing_before))
        f.write("\n\n")
        f.write("Missing Values AFTER Cleaning:\n")
        f.write(str(missing_after))
        f.write("\n\n")
        f.write("Summary Statistics:\n")
        f.write(str(summary))
        f.write("\n")

    print("Cleaning complete!")
    print(f"Cleaned file saved as: {cleaned_file}")
    print(f"Report saved as: {report_file}")

if __name__ == "__main__":
    clean_csv("data.csv", "cleaned_data.csv", "report.txt")