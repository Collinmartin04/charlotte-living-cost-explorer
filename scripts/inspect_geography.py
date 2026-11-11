
from pathlib import Path

import geopandas as gpd


RAW_DIR = Path("data/raw")

ZCTA_PATH = RAW_DIR / "cb_2020_us_zcta520_500k.zip"
COUNTY_PATH = RAW_DIR / "cb_2020_us_county_500k.zip"


def inspect_geography():
    """Inspect Census ZCTA and county boundary datasets."""

    print("\n=== LOADING ZCTA BOUNDARIES ===")

    zctas = gpd.read_file(ZCTA_PATH)

    print("Number of ZCTAs:", len(zctas))
    print("Columns:", zctas.columns.tolist())
    print("Coordinate system:", zctas.crs)

    print("\nSample records:")
    print(zctas.drop(columns="geometry").head(3).to_string(index=False))

    print("\n=== LOADING COUNTY BOUNDARIES ===")

    counties = gpd.read_file(COUNTY_PATH)

    print("Number of counties:", len(counties))
    print("Columns:", counties.columns.tolist())
    print("Coordinate system:", counties.crs)

    print("\n=== FINDING MECKLENBURG COUNTY ===")

    # Census state FIPS 37 = North Carolina
    # Census county FIPS 119 = Mecklenburg County
    mecklenburg = counties.loc[
        (counties["STATEFP"] == "37")
        & (counties["COUNTYFP"] == "119")
    ]

    if len(mecklenburg) != 1:
        raise ValueError(
            f"Expected one Mecklenburg County record, found {len(mecklenburg)}."
        )

    print(
        mecklenburg.drop(columns="geometry")
        .to_string(index=False)
    )

    print("\nMecklenburg geometry type:",
          mecklenburg.geometry.iloc[0].geom_type)

    print("Mecklenburg geometry valid:",
          mecklenburg.geometry.is_valid.iloc[0])


if __name__ == "__main__":
    inspect_geography()
