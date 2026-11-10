
from pathlib import Path

import pandas as pd
import pytest


DATA_PATH = Path("data/processed/charlotte_hud_fy2027.csv")

EXPECTED_COLUMNS = {
    "zip_code",
    "hud_area_code",
    "hud_area_name",
    "fiscal_year",
    "bedrooms",
    "monthly_safmr",
    "source",
}

HUD_AREA_CODE = "METRO16740M16740"


@pytest.fixture
def hud_data():
    """Load the processed HUD dataset for testing."""
    return pd.read_csv(
        DATA_PATH,
        dtype={"zip_code": str},
    )


def test_expected_columns(hud_data):
    """Verify the output contains the expected schema."""
    assert set(hud_data.columns) == EXPECTED_COLUMNS


def test_no_missing_values(hud_data):
    """Verify required fields have no missing values."""
    assert not hud_data[list(EXPECTED_COLUMNS)].isna().any().any()


def test_valid_zip_codes(hud_data):
    """Verify ZIP codes contain exactly five digits."""
    assert hud_data["zip_code"].str.fullmatch(r"\d{5}").all()


def test_valid_bedroom_categories(hud_data):
    """Verify bedroom categories range from 0 to 4."""
    assert set(hud_data["bedrooms"].unique()) == {0, 1, 2, 3, 4}


def test_positive_rental_benchmarks(hud_data):
    """Verify rental benchmarks are positive."""
    assert (hud_data["monthly_safmr"] > 0).all()


def test_correct_hud_area(hud_data):
    """Verify all records belong to the selected HUD area."""
    assert hud_data["hud_area_code"].eq(HUD_AREA_CODE).all()


def test_no_duplicate_records(hud_data):
    """Verify unique ZIP, year, and bedroom combinations."""
    keys = ["zip_code", "fiscal_year", "bedrooms"]
    assert not hud_data.duplicated(subset=keys).any()


def test_five_bedroom_records_per_zip(hud_data):
    """Verify every ZIP has all five bedroom categories."""
    counts = hud_data.groupby("zip_code")["bedrooms"].nunique()
    assert counts.eq(5).all()
