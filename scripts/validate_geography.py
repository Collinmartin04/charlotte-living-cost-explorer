
from pathlib import Path

import pandas as pd


HUD_PATH = Path("data/processed/charlotte_hud_fy2027.csv")
CENSUS_PATH = Path("data/raw/2020_Gaz_zcta_national.txt")


def validate_geography():
    """Compare Charlotte HUD ZIP codes with Census ZCTAs."""

    # Load the processed HUD dataset.
    hud = pd.read_csv(
        HUD_PATH,
        dtype={"zip_code": str},
    )

    # Each ZIP appears five times in our HUD dataset.
    # We only need one record per ZIP for this comparison.
    hud_zips = hud[["zip_code"]].drop_duplicates()

    # Load Census Gazetteer data.
    census = pd.read_csv(
        CENSUS_PATH,
        sep="\t",
        dtype={"GEOID": str},
    )

    # Remove extra whitespace from column names.
    census.columns = census.columns.str.strip()

    # Rename the geographic identifier.
    census = census.rename(
        columns={"GEOID": "zcta"}
    )

    # Validate unique Census identifiers.
    if census["zcta"].duplicated().any():
        raise ValueError("Duplicate ZCTA identifiers found.")

    # Compare HUD ZIPs against Census ZCTAs.
    comparison = hud_zips.merge(
        census,
        how="left",
        left_on="zip_code",
        right_on="zcta",
        indicator=True,
        validate="one_to_one",
    )

    comparison["match_status"] = comparison["_merge"].map(
        {
            "both": "matched",
            "left_only": "unmatched",
            "right_only": "census_only",
        }
    ).astype(str)

    print("\n=== GEOGRAPHIC VALIDATION ===")
    print(f"HUD ZIP identifiers: {len(hud_zips)}")
    print(f"Matched ZCTAs: {(comparison['_merge'] == 'both').sum()}")
    print(
        "Unmatched HUD ZIPs: "
        f"{(comparison['_merge'] == 'left_only').sum()}"
    )

    print("\n=== UNMATCHED ZIP IDENTIFIERS ===")

    unmatched = comparison.loc[
        comparison["_merge"] == "left_only",
        "zip_code",
    ]

    print(unmatched.sort_values().to_list())

    print("\n=== SAMPLE MATCHED RECORDS ===")

    matched = comparison.loc[
        comparison["_merge"] == "both",
        ["zip_code", "ALAND_SQMI", "INTPTLAT", "INTPTLONG"],
    ]

    print(matched.head(10).to_string(index=False))

    # Save an audit-friendly comparison table.
    output_path = Path(
        "data/processed/hud_census_zcta_comparison.csv"
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    comparison.drop(columns=["_merge"]).to_csv(
        output_path,
        index=False,
    )

    print(f"\nSaved comparison to: {output_path}")


if __name__ == "__main__":
    validate_geography()
