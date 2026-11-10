
from pathlib import Path
import pandas as pd

FILE_PATH = Path("data/raw/FY27_safmrs.xlsx")
CHARLOTTE_HUD_AREA = "METRO16740M16740"

RENT_COLUMNS = [
    "SAFMR\n0BR",
    "SAFMR\n1BR",
    "SAFMR\n2BR",
    "SAFMR\n3BR",
    "SAFMR\n4BR",
]


def profile_hud_data():
    """Profile Charlotte HUD metro rental benchmark records."""

    df = pd.read_excel(
        FILE_PATH,
        sheet_name="SAFMRs",
        dtype={"ZIP\nCode": str},
    )

    charlotte = df.loc[
        df["HUD Area Code"] == CHARLOTTE_HUD_AREA
    ].copy()

    charlotte["ZIP\nCode"] = (
        charlotte["ZIP\nCode"]
        .str.strip()
        .str.zfill(5)
    )

    print("\n=== DATASET STRUCTURE ===")
    print(f"National rows: {len(df):,}")
    print(f"National columns: {len(df.columns)}")
    print(f"Charlotte metro rows: {len(charlotte):,}")
    zip_column = "ZIP\nCode"
    print(f"Charlotte unique ZIPs: {charlotte[zip_column].nunique()}")

    print("\n=== ALL COLUMN NAMES ===")
    for column in df.columns:
        print(repr(column))

    print("\n=== MISSING VALUES ===")
    print(
        charlotte[["ZIP\nCode", *RENT_COLUMNS]]
        .isna()
        .sum()
        .to_string()
    )

    print("\n=== DUPLICATE ZIP CODES ===")
    duplicates = charlotte[
        charlotte.duplicated(
            subset=["ZIP\nCode"],
            keep=False,
        )
    ]

    print(f"Duplicate rows: {len(duplicates)}")

    if not duplicates.empty:
        print(duplicates.to_string(index=False))

    print("\n=== RENTAL BENCHMARK SUMMARY ===")
    print(
        charlotte[RENT_COLUMNS]
        .describe()
        .round(2)
        .to_string()
    )

    print("\n=== INVALID RENT VALUES ===")

    for column in RENT_COLUMNS:
        invalid_count = (
            pd.to_numeric(charlotte[column], errors="coerce")
            .le(0)
            .sum()
        )

        print(f"{column!r}: {invalid_count}")

    print("\n=== ZIP CODE FORMAT ===")
    invalid_zip = ~charlotte["ZIP\nCode"].str.fullmatch(r"\d{5}")

    print(f"Invalid ZIP formats: {invalid_zip.sum()}")


if __name__ == "__main__":
    profile_hud_data()