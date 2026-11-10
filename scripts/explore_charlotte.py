
import pandas as pd
from pathlib import Path

FILE_PATH = Path("data/raw/FY27_safmrs.xlsx")


def explore_charlotte():
    """Explore Charlotte-related records in the HUD dataset."""

    # Load the complete worksheet.
    # ZIP codes must remain strings.
    df = pd.read_excel(
        FILE_PATH,
        sheet_name="SAFMRs",
        dtype={"ZIP\nCode": str}
    )

    print("\n=== NATIONAL DATASET ===")
    print(f"Total rows: {len(df):,}")
    print(f"Total columns: {len(df.columns)}")

    # Search HUD area names for Charlotte.
    charlotte = df[
        df["HUD Fair Market Rent Area Name"]
        .str.contains(
            "Charlotte",
            case=False,
            na=False
        )
    ].copy()

    print("\n=== CHARLOTTE-RELATED RECORDS ===")
    print(f"Matching rows: {len(charlotte):,}")

    print("\n=== HUD AREA NAMES ===")
    print(
        charlotte["HUD Fair Market Rent Area Name"]
        .value_counts()
        .to_string()
    )

    print("\n=== HUD AREA CODES ===")
    print(
        charlotte["HUD Area Code"]
        .value_counts()
        .to_string()
    )

    print("\n=== SAMPLE CHARLOTTE RECORDS ===")

    columns = [
        "ZIP\nCode",
        "HUD Area Code",
        "HUD Fair Market Rent Area Name",
        "SAFMR\n1BR",
        "SAFMR\n2BR",
    ]

    print(
        charlotte[columns]
        .head(10)
        .to_string(index=False)
    )


if __name__ == "__main__":
    explore_charlotte()
