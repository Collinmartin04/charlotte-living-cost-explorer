
from pathlib import Path

import pandas as pd
import pytest


DATA_PATH = Path(
    "data/processed/mecklenburg_housing_fy2027.csv"
)


@pytest.fixture(scope="module")
def housing():
    """Load the geographically enriched housing dataset."""
    assert DATA_PATH.exists(), "Run build_mecklenburg_housing.py first."
    return pd.read_csv(DATA_PATH, dtype={"zip_code": str})


def test_required_columns(housing):
    required = {
        "zip_code",
        "fiscal_year",
        "bedrooms",
        "monthly_safmr",
        "pct_in_mecklenburg",
        "geographic_category",
    }

    assert required.issubset(housing.columns)


def test_no_missing_values(housing):
    required = [
        "zip_code",
        "fiscal_year",
        "bedrooms",
        "monthly_safmr",
        "pct_in_mecklenburg",
        "geographic_category",
    ]

    assert not housing[required].isna().any().any()


def test_unique_benchmark_records(housing):
    assert not housing.duplicated(
        subset=["zip_code", "fiscal_year", "bedrooms"]
    ).any()


def test_valid_geographic_percentages(housing):
    assert housing["pct_in_mecklenburg"].between(0, 100).all()


def test_valid_geographic_categories(housing):
    expected = {
        "small_overlap",
        "partial_overlap",
        "mostly_inside",
    }

    assert set(housing["geographic_category"]).issubset(expected)


def test_five_bedroom_categories_per_zcta(housing):
    counts = housing.groupby("zip_code")["bedrooms"].nunique()

    assert (counts == 5).all()
    assert set(housing["bedrooms"]) == {0, 1, 2, 3, 4}


def test_positive_rental_benchmarks(housing):
    assert (housing["monthly_safmr"] > 0).all()


def test_geographic_classification_consistency(housing):
    for _, row in housing.iterrows():
        percentage = row["pct_in_mecklenburg"]
        category = row["geographic_category"]

        if percentage <= 10:
            assert category == "small_overlap"
        elif percentage <= 90:
            assert category == "partial_overlap"
        else:
            assert category == "mostly_inside"
