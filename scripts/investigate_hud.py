
from pathlib import Path

import pandas as pd

FILE_PATH = Path("data/raw/FY27_safmrs.xlsx")
CHARLOTTE_HUD_AREA = "METRO16740M16740"

ZIP_COLUMN = "ZIP\nCode"
RENT_COLUMN = "SAFMR\n2BR"


def investigate_hud():
    """Investigate repeated two-bedroom HUD rental benchmarks."""

    df = pd.read_excel(
        FILE_PATH,
        sheet_name="SAFMRs",
        dtype={ZIP_COLUMN: str},
    )

    charlotte = df.loc[
        df["HUD Area Code"] == CHARLOTTE_HUD_AREA
    ].copy()

    charlotte[ZIP_COLUMN] = (
        charlotte[ZIP_COLUMN]
        .str.strip()
        .str.zfill(5)
    )

    print("\n=== TWO-BEDROOM BENCHMARK ANALYSIS ===")

    print(f"Total ZIP codes: {len(charlotte)}")
    print(
        f"Unique 2BR benchmark values: "
        f"{charlotte[RENT_COLUMN].nunique()}"
    )

    print("\n=== MOST FREQUENT BENCHMARKS ===")

    frequencies = (
        charlotte[RENT_COLUMN]
        .value_counts()
        .head(15)
    )

    print(frequencies.to_string())

    print("\n=== ZIP CODES WITH THE MEDIAN BENCHMARK ===")

    median_rent = charlotte[RENT_COLUMN].median()

    matching_zips = charlotte.loc[
        charlotte[RENT_COLUMN] == median_rent,
        ZIP_COLUMN,
    ]

    print(f"Median benchmark: ${median_rent:,.0f}")
    print(f"ZIP codes sharing this value: {len(matching_zips)}")
    print(matching_zips.to_list())

    print("\n=== TEN LOWEST TWO-BEDROOM BENCHMARKS ===")

    print(
        charlotte[
            [ZIP_COLUMN, RENT_COLUMN]
        ]
        .sort_values(RENT_COLUMN)
        .head(10)
        .to_string(index=False)
    )

    print("\n=== TEN HIGHEST TWO-BEDROOM BENCHMARKS ===")

    print(
        charlotte[
            [ZIP_COLUMN, RENT_COLUMN]
        ]
        .sort_values(RENT_COLUMN, ascending=False)
        .head(10)
        .to_string(index=False)
    )


if __name__ == "__main__":
    investigate_hud()
