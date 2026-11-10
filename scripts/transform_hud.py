
from pathlib import Path

import pandas as pd


RAW_PATH = Path("data/raw/FY27_safmrs.xlsx")
OUTPUT_PATH = Path("data/processed/charlotte_hud_fy2027.csv")

HUD_AREA_CODE = "METRO16740M16740"
ZIP_COLUMN = "ZIP\nCode"

BEDROOM_COLUMNS = {
    "SAFMR\n0BR": 0,
    "SAFMR\n1BR": 1,
    "SAFMR\n2BR": 2,
    "SAFMR\n3BR": 3,
    "SAFMR\n4BR": 4,
}


def transform_hud_data():
    """Transform Charlotte HUD SAFMR data into long format."""

    df = pd.read_excel(
        RAW_PATH,
        sheet_name="SAFMRs",
        dtype={ZIP_COLUMN: str},
    )

    # Filter to the exact Charlotte HUD metro area.
    charlotte = df.loc[
        df["HUD Area Code"] == HUD_AREA_CODE
    ].copy()

    # Standardize ZIP identifiers.
    charlotte["zip_code"] = (
        charlotte[ZIP_COLUMN]
        .str.strip()
        .str.zfill(5)
    )

    # Convert bedroom columns into long format.
    long_df = charlotte.melt(
        id_vars=[
            "zip_code",
            "HUD Area Code",
            "HUD Fair Market Rent Area Name",
        ],
        value_vars=list(BEDROOM_COLUMNS),
        var_name="bedroom_source",
        value_name="monthly_safmr",
    )

    # Convert HUD bedroom labels into integers.
    long_df["bedrooms"] = (
        long_df["bedroom_source"]
        .map(BEDROOM_COLUMNS)
    )

    # Rename metadata columns.
    long_df = long_df.rename(
        columns={
            "HUD Area Code": "hud_area_code",
            "HUD Fair Market Rent Area Name": "hud_area_name",
        }
    )

    # Add source metadata.
    long_df["fiscal_year"] = 2027
    long_df["source"] = "HUD SAFMR"

    # Keep a clean, consistent column order.
    columns = [
        "zip_code",
        "hud_area_code",
        "hud_area_name",
        "fiscal_year",
        "bedrooms",
        "monthly_safmr",
        "source",
    ]

    long_df = long_df[columns]

    # Sort for readability and reproducibility.
    long_df = long_df.sort_values(
        ["zip_code", "bedrooms"]
    ).reset_index(drop=True)

    # Validate the result before saving.
    assert len(long_df) == len(charlotte) * 5
    assert not long_df["monthly_safmr"].isna().any()
    assert (long_df["monthly_safmr"] > 0).all()
    assert not long_df.duplicated(
        ["zip_code", "fiscal_year", "bedrooms"]
    ).any()

    # Save the processed dataset.
    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    long_df.to_csv(
        OUTPUT_PATH,
        index=False,
    )

    print("\n=== TRANSFORMATION COMPLETE ===")
    print(f"Source ZIP records: {len(charlotte):,}")
    print(f"Processed rows: {len(long_df):,}")
    print(f"Output: {OUTPUT_PATH}")

    print("\n=== SAMPLE RECORDS ===")
    print(long_df.head(10).to_string(index=False))


if __name__ == "__main__":
    transform_hud_data()
