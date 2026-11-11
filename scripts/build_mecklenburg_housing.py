
from pathlib import Path

import pandas as pd


PROCESSED_DIR = Path("data/processed")

HUD_PATH = PROCESSED_DIR / "charlotte_hud_fy2027.csv"
OVERLAP_PATH = PROCESSED_DIR / "mecklenburg_zcta_overlap.csv"
OUTPUT_PATH = PROCESSED_DIR / "mecklenburg_housing_fy2027.csv"


def build_mecklenburg_housing():
    """Combine HUD rental benchmarks with Mecklenburg ZCTA overlap."""

    hud = pd.read_csv(
        HUD_PATH,
        dtype={"zip_code": str},
    )

    overlap = pd.read_csv(
        OVERLAP_PATH,
        dtype={"zcta": str},
    )

    # Allow a very small tolerance for floating-point precision.
    tolerance = 1e-8

    if (
        overlap["pct_in_mecklenburg"].isna().any()
        or (overlap["pct_in_mecklenburg"] < -tolerance).any()
        or (overlap["pct_in_mecklenburg"] > 100 + tolerance).any()
    ):
        raise ValueError("Invalid geographic overlap percentages.")

    # Remove tiny floating-point errors from valid percentages.
    overlap["pct_in_mecklenburg"] = (
        overlap["pct_in_mecklenburg"].clip(0, 100)
    )

    if not overlap["pct_in_mecklenburg"].between(0, 100).all():
        raise ValueError("Invalid geographic overlap percentages.")

    # Keep only HUD records with overlapping Census ZCTA polygons.
    housing = hud.merge(
        overlap[["zcta", "pct_in_mecklenburg"]],
        left_on="zip_code",
        right_on="zcta",
        how="inner",
        validate="many_to_one",
    )

    # Categorize overlap for analytical comparisons.
    housing["geographic_category"] = pd.cut(
        housing["pct_in_mecklenburg"],
        bins=[-0.001, 10, 90, 100],
        labels=[
            "small_overlap",
            "partial_overlap",
            "mostly_inside",
        ],
        include_lowest=True,
    )

    # Validate our final analytical table.
    if housing.empty:
        raise ValueError("No geographic matches were found.")

    if housing["monthly_safmr"].isna().any():
        raise ValueError("Missing rental benchmarks.")

    if housing["geographic_category"].isna().any():
        raise ValueError("Missing geographic categories.")

    if housing.duplicated(
        subset=["zip_code", "fiscal_year", "bedrooms"]
    ).any():
        raise ValueError("Duplicate housing benchmark records.")

    # Remove the redundant join identifier.
    housing = housing.drop(columns="zcta")

    housing = housing.sort_values(
        ["zip_code", "bedrooms"]
    ).reset_index(drop=True)

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    housing.to_csv(OUTPUT_PATH, index=False)

    print("\n=== MECKLENBURG HOUSING DATASET ===")
    print("Total records:", len(housing))
    print("Unique ZCTAs:", housing["zip_code"].nunique())

    print("\n=== GEOGRAPHIC COVERAGE ===")

    print(
        housing.drop_duplicates("zip_code")[
            "geographic_category"
        ].value_counts().to_string()
    )

    print("\n=== SAMPLE TWO-BEDROOM BENCHMARKS ===")

    sample = housing.loc[
        housing["bedrooms"] == 2,
        [
            "zip_code",
            "monthly_safmr",
            "pct_in_mecklenburg",
            "geographic_category",
        ],
    ]

    print(sample.head(10).to_string(index=False))

    print(f"\nSaved dataset to: {OUTPUT_PATH}")


if __name__ == "__main__":
    build_mecklenburg_housing()
