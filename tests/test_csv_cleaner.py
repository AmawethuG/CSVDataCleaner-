import pandas as pd
import pytest

from src.csv_cleaner import clean_data


def test_duplicate_rows_are_removed(tmp_path):
    input_file = tmp_path / "input.csv"
    output_file = tmp_path / "output.csv"

    data = {
        "case_id": [2001, 2001],
        "case_name": ["S v Mokoena", "S v Mokoena"],
        "court_level": ["Magistrates Court", "Magistrates Court"],
        "court_name": [
            "Johannesburg Magistrates Court",
            "Johannesburg Magistrates Court",
        ],
        "province": ["Gauteng", "Gauteng"],
        "city": ["Johannesburg", "Johannesburg"],
        "filing_date": ["2022-01-10", "2022-01-10"],
        "decision_date": ["2022-03-15", "2022-03-15"],
        "case_duration_days": [64, 64],
        "case_type": ["Criminal", "Criminal"],
        "charge_or_claim": ["Theft", "Theft"],
        "verdict": ["Guilty", "Guilty"],
        "fine_amount_zar": [3500, 3500],
        "settlement_amount_zar": [0, 0],
        "sentence_years": [2, 2],
        "appealed": ["Yes", "Yes"],
        "appeal_result": ["Upheld", "Upheld"],
    }

    pd.DataFrame(data).to_csv(input_file, index=False)

    clean_data(input_file, output_file)

    cleaned_df = pd.read_csv(output_file)

    assert len(cleaned_df) == 1


def test_whitespace_is_removed_from_text_columns(tmp_path):
    input_file = tmp_path / "input.csv"
    output_file = tmp_path / "output.csv"

    data = {
        "case_id": [2001],
        "case_name": ["  S v Mokoena  "],
        "court_level": [" Magistrates Court "],
        "court_name": [" Johannesburg Magistrates Court "],
        "province": [" Gauteng "],
        "city": [" Johannesburg "],
        "filing_date": ["2022-01-10"],
        "decision_date": ["2022-03-15"],
        "case_duration_days": [64],
        "case_type": [" Criminal "],
        "charge_or_claim": [" Theft "],
        "verdict": [" Guilty "],
        "fine_amount_zar": [3500],
        "settlement_amount_zar": [0],
        "sentence_years": [2],
        "appealed": [" Yes "],
        "appeal_result": [" Upheld "],
    }

    pd.DataFrame(data).to_csv(input_file, index=False)

    clean_data(input_file, output_file)

    cleaned_df = pd.read_csv(output_file)

    assert cleaned_df.loc[0, "case_name"] == "S v Mokoena"
    assert cleaned_df.loc[0, "province"] == "Gauteng"
    assert cleaned_df.loc[0, "city"] == "Johannesburg"
    assert cleaned_df.loc[0, "verdict"] == "Guilty"


def test_dates_are_converted_to_valid_dates(tmp_path):
    input_file = tmp_path / "input.csv"
    output_file = tmp_path / "output.csv"

    data = {
        "case_id": [2001],
        "case_name": ["S v Mokoena"],
        "court_level": ["Magistrates Court"],
        "court_name": ["Johannesburg Magistrates Court"],
        "province": ["Gauteng"],
        "city": ["Johannesburg"],
        "filing_date": ["2022-01-10 14:30:00"],
        "decision_date": ["2022-03-15 09:45:00"],
        "case_duration_days": [64],
        "case_type": ["Criminal"],
        "charge_or_claim": ["Theft"],
        "verdict": ["Guilty"],
        "fine_amount_zar": [3500],
        "settlement_amount_zar": [0],
        "sentence_years": [2],
        "appealed": ["Yes"],
        "appeal_result": ["Upheld"],
    }

    pd.DataFrame(data).to_csv(input_file, index=False)

    clean_data(input_file, output_file)

    cleaned_df = pd.read_csv(
        output_file,
        parse_dates=["filing_date", "decision_date"]
    )

    assert pd.api.types.is_datetime64_any_dtype(
        cleaned_df["filing_date"]
    )

    assert pd.api.types.is_datetime64_any_dtype(
        cleaned_df["decision_date"]
    )

    assert cleaned_df.loc[0, "filing_date"].date() == pd.Timestamp("2022-01-10").date()
    assert cleaned_df.loc[0, "decision_date"].date() == pd.Timestamp("2022-03-15").date()

def test_invalid_date_becomes_nat(tmp_path):
    input_file = tmp_path / "input.csv"
    output_file = tmp_path / "output.csv"

    data = {
        "case_id": [2001],
        "case_name": ["S v Mokoena"],
        "court_level": ["Magistrates Court"],
        "court_name": ["Johannesburg Magistrates Court"],
        "province": ["Gauteng"],
        "city": ["Johannesburg"],
        "filing_date": ["NOT-A-DATE"],
        "decision_date": ["2022-03-15"],
        "case_duration_days": [64],
        "case_type": ["Criminal"],
        "charge_or_claim": ["Theft"],
        "verdict": ["Guilty"],
        "fine_amount_zar": [3500],
        "settlement_amount_zar": [0],
        "sentence_years": [2],
        "appealed": ["Yes"],
        "appeal_result": ["Upheld"],
    }

    pd.DataFrame(data).to_csv(input_file, index=False)

    clean_data(input_file, output_file)

    cleaned_df = pd.read_csv(
        output_file,
        parse_dates=["filing_date", "decision_date"]
    )

    assert pd.isna(cleaned_df.loc[0, "filing_date"])
    assert cleaned_df.loc[0, "decision_date"] == pd.Timestamp("2022-03-15")

def test_invalid_numeric_value_becomes_nan(tmp_path):
    input_file = tmp_path / "input.csv"
    output_file = tmp_path / "output.csv"

    data = {
        "case_id": [2001],
        "case_name": ["S v Mokoena"],
        "court_level": ["Magistrates Court"],
        "court_name": ["Johannesburg Magistrates Court"],
        "province": ["Gauteng"],
        "city": ["Johannesburg"],
        "filing_date": ["2022-01-10"],
        "decision_date": ["2022-03-15"],
        "case_duration_days": ["64"],
        "case_type": ["Criminal"],
        "charge_or_claim": ["Theft"],
        "verdict": ["Guilty"],
        "fine_amount_zar": ["NOT-A-NUMBER"],
        "settlement_amount_zar": ["0"],
        "sentence_years": ["2"],
        "appealed": ["Yes"],
        "appeal_result": ["Upheld"],
    }

    pd.DataFrame(data).to_csv(input_file, index=False)

    clean_data(input_file, output_file)

    cleaned_df = pd.read_csv(output_file)

    assert pd.isna(cleaned_df.loc[0, "fine_amount_zar"])
    assert cleaned_df.loc[0, "case_duration_days"] == 64

def test_required_columns_have_no_missing_values(tmp_path):
    input_file = tmp_path / "input.csv"
    output_file = tmp_path / "output.csv"

    data = {
        "case_id": [2001],
        "case_name": ["S v Mokoena"],
        "court_level": ["Magistrates Court"],
        "court_name": ["Johannesburg Magistrates Court"],
        "province": ["Gauteng"],
        "city": ["Johannesburg"],
        "filing_date": ["2022-01-10"],
        "decision_date": ["2022-03-15"],
        "case_duration_days": [64],
        "case_type": ["Criminal"],
        "charge_or_claim": ["Theft"],
        "verdict": ["Guilty"],
        "fine_amount_zar": [3500],
        "settlement_amount_zar": [0],
        "sentence_years": [2],
        "appealed": ["Yes"],
        "appeal_result": ["Upheld"],
    }

    pd.DataFrame(data).to_csv(input_file, index=False)

    clean_data(input_file, output_file)

    cleaned_df = pd.read_csv(output_file)

    required_columns = [
        "case_id",
        "case_name",
        "court_level",
        "court_name",
        "province",
        "filing_date",
        "decision_date",
        "case_type",
        "verdict",
    ]

    for column in required_columns:
        assert cleaned_df[column].notna().all()


def test_numeric_columns_have_numeric_dtypes(tmp_path):
    input_file = tmp_path / "input.csv"
    output_file = tmp_path / "output.csv"

    data = {
        "case_id": ["2001"],
        "case_name": ["S v Mokoena"],
        "court_level": ["Magistrates Court"],
        "court_name": ["Johannesburg Magistrates Court"],
        "province": ["Gauteng"],
        "city": ["Johannesburg"],
        "filing_date": ["2022-01-10"],
        "decision_date": ["2022-03-15"],
        "case_duration_days": ["64"],
        "case_type": ["Criminal"],
        "charge_or_claim": ["Theft"],
        "verdict": ["Guilty"],
        "fine_amount_zar": ["3500"],
        "settlement_amount_zar": ["0"],
        "sentence_years": ["2"],
        "appealed": ["Yes"],
        "appeal_result": ["Upheld"],
    }

    pd.DataFrame(data).to_csv(input_file, index=False)

    clean_data(input_file, output_file)

    cleaned_df = pd.read_csv(output_file)

    numeric_columns = [
        "case_id",
        "case_duration_days",
        "fine_amount_zar",
        "settlement_amount_zar",
        "sentence_years",
    ]

    for column in numeric_columns:
        assert pd.api.types.is_numeric_dtype(cleaned_df[column])



def test_missing_required_value_is_rejected(tmp_path):
    input_file = tmp_path / "input.csv"
    output_file = tmp_path / "output.csv"

    data = {
        "case_id": [2001],
        "case_name": [None],
        "court_level": ["Magistrates Court"],
        "court_name": ["Johannesburg Magistrates Court"],
        "province": ["Gauteng"],
        "city": ["Johannesburg"],
        "filing_date": ["2022-01-10"],
        "decision_date": ["2022-03-15"],
        "case_duration_days": [64],
        "case_type": ["Criminal"],
        "charge_or_claim": ["Theft"],
        "verdict": ["Guilty"],
        "fine_amount_zar": [3500],
        "settlement_amount_zar": [0],
        "sentence_years": [2],
        "appealed": ["Yes"],
        "appeal_result": ["Upheld"],
    }

    pd.DataFrame(data).to_csv(input_file, index=False)

    with pytest.raises(ValueError):
        clean_data(input_file, output_file)

