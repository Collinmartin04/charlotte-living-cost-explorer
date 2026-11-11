
from pathlib import Path

import geopandas as gpd
import pandas as pd


RAW_DIR = Path("data/raw")
OUTPUT_DIR = Path("data/processed")

ZCTA_PATH = RAW_DIR / "cb_2020_us_zcta520_500k.zip"
COUNTY_PATH = RAW_DIR / "cb_2020_us_county_500k.zip"

# NAD83 / North Carolina (meters)
PROJECTED_CRS = "EPSG:32119"


def analyze_zcta_overlap():
    """Measure ZCTA land overlap with Mecklenburg County."""

    print("\n=== LOADING GEOGRAPHIC DATA ===")

    zctas = gpd.read_file(ZCTA_PATH)
    counties = gpd.read_file(COUNTY_PATH)

    mecklenburg = counties.loc[
        (counties["STATEFP"] == "37")
        & (counties["COUNTYFP"] == "119")
    ]

    if len(mecklenburg) != 1:
        raise ValueError("Expected exactly one Mecklenburg County.")

    # Transform both datasets into a projected coordinate system.
    zctas = zctas.to_crs(PROJECTED_CRS)
    mecklenburg = mecklenburg.to_crs(PROJECTED_CRS)

    # Select ZCTAs that have a spatial relationship
    # with Mecklenburg County.
    candidates = zctas.loc[
        zctas.intersects(mecklenburg.geometry.iloc[0])
    ].copy()

    print("Intersecting ZCTA candidates:", len(candidates))

    # Compute intersection geometry with Mecklenburg County.
    county_geometry = mecklenburg.geometry.iloc[0]

    candidates["overlap_area_sqm"] = (
        candidates.geometry.intersection(county_geometry).area
    )

    # Calculate the full ZCTA polygon area.
    candidates["zcta_area_sqm"] = candidates.geometry.area

    # Require a positive area overlap.
    candidates = candidates.loc[
        (candidates["overlap_area_sqm"] > 0)
        & (candidates["zcta_area_sqm"] > 0)
    ].copy()

    # Percentage of each ZCTA's mapped polygon area
    # that falls within Mecklenburg County.
    candidates["pct_in_mecklenburg"] = (
        candidates["overlap_area_sqm"]
        / candidates["zcta_area_sqm"]
        * 100
    )

    result = candidates[
        ["GEOID20", "overlap_area_sqm", "zcta_area_sqm",
         "pct_in_mecklenburg"]
    ].rename(columns={"GEOID20": "zcta"})

    result = result.sort_values(
        "pct_in_mecklenburg",
        ascending=False,
    )

    print("\n=== SPATIAL OVERLAP SUMMARY ===")
    print("ZCTAs with positive overlap:", len(result))

    print("\nZCTAs mostly inside Mecklenburg (>= 90%):")
    print((result["pct_in_mecklenburg"] >= 90).sum())

    print("\nZCTAs partially inside Mecklenburg (10% to <90%):")
    print(
        (
            (result["pct_in_mecklenburg"] >= 10)
            & (result["pct_in_mecklenburg"] < 90)
        ).sum()
    )

    print("\nZCTAs with small overlap (<10%):")
    print((result["pct_in_mecklenburg"] < 10).sum())

    print("\n=== ALL OVERLAPPING ZCTAs ===")
    print(result.round(2).to_string(index=False))

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    output_path = OUTPUT_DIR / "mecklenburg_zcta_overlap.csv"

    result.to_csv(output_path, index=False)

    print(f"\nSaved results to: {output_path}")


if __name__ == "__main__":
    analyze_zcta_overlap()
