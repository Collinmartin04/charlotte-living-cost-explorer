
from pathlib import Path

import pandas as pd

DATA_PATH = Path(
    "data/processed/hud_census_zcta_comparison.csv"
)

HUD_PATH = Path(
    "data/processed/charlotte_hud_fy2027.csv"
)


def analyze_matches():
    """Compare rental benchmarks by geographic match status."""

    geography = pd.read_csv(
        DATA_PATH,
        dtype={"zip_code": str},
    )

    hud = pd.read_csv(
        HUD_PATH,
        dtype={"zip_code": str},
    )

    # Focus on two-bedroom benchmarks for now.
    two_bedroom = hud.loc[
        hud["bedrooms"] == 2,
        ["zip_code", "monthly_safmr"],
    ].copy()

    # Attach geographic match status.
    analysis = two_bedroom.merge(
        geography[["zip_code", "match_status"]],
        on="zip_code",
        how="left",
        validate="one_to_one",
    )

    if analysis["match_status"].isna().any():
        raise ValueError("Some ZIPs have no match status.")

    print("\n=== BENCHMARKS BY MATCH STATUS ===")

    summary = analysis.groupby("match_status")[
        "monthly_safmr"
    ].agg(["count", "mean", "median", "min", "max", "nunique"])

    print(summary.round(2).to_string())

    print("\n=== REPEATED $1,890 BENCHMARK ===")

    repeated = analysis.loc[
        analysis["monthly_safmr"] == 1890
    ]

    print(
        repeated["match_status"]
        .value_counts()
        .to_string()
    )

    print("\n=== MATCHED VS UNMATCHED ZIP COUNTS ===")

    print(
        analysis["match_status"]
        .value_counts()
        .to_string()
    )


if __name__ == "__main__":
    analyze_matches()
