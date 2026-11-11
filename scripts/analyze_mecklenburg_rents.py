
from pathlib import Path

import pandas as pd


DATA_PATH = Path(
    "data/processed/mecklenburg_housing_fy2027.csv"
)


def analyze_mecklenburg_rents():
    """Explore two-bedroom rental benchmarks in Mecklenburg County."""

    housing = pd.read_csv(
        DATA_PATH,
        dtype={"zip_code": str},
    )

    # Focus on geographic areas mostly inside Mecklenburg.
    core = housing.loc[
        (housing["geographic_category"] == "mostly_inside")
        & (housing["bedrooms"] == 2)
    ].copy()

    if core.empty:
        raise ValueError("No two-bedroom records found.")

    print("\n=== MECKLENBURG TWO-BEDROOM SAFMR ANALYSIS ===")

    print("ZCTAs analyzed:", core["zip_code"].nunique())

    print("\n=== SUMMARY STATISTICS ===")

    print(
        core["monthly_safmr"]
        .describe()
        .round(2)
        .to_string()
    )

    print("\n=== 10 HIGHEST BENCHMARKS ===")

    highest = core.nlargest(
        10, "monthly_safmr"
    )[["zip_code", "monthly_safmr"]]

    print(highest.to_string(index=False))

    print("\n=== 10 LOWEST BENCHMARKS ===")

    lowest = core.nsmallest(
        10, "monthly_safmr"
    )[["zip_code", "monthly_safmr"]]

    print(lowest.to_string(index=False))

    print("\n=== RENTAL BENCHMARK FREQUENCIES ===")

    frequencies = (
        core["monthly_safmr"]
        .value_counts()
        .sort_index()
    )

    print(frequencies.to_string())

    print("\n=== DATA QUALITY CHECK ===")

    print("Missing benchmarks:", core["monthly_safmr"].isna().sum())
    print("Duplicate ZCTAs:", core["zip_code"].duplicated().sum())


if __name__ == "__main__":
    analyze_mecklenburg_rents()
