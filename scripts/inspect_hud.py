
import pandas as pd
from pathlib import Path

# Location of our downloaded HUD dataset
FILE_PATH = Path("data/raw/FY27_safmrs.xlsx")


def inspect_hud_data():
    """Inspect the structure of the HUD SAFMR dataset."""

    if not FILE_PATH.exists():
        raise FileNotFoundError(
            f"HUD dataset not found: {FILE_PATH}"
        )

    # Read only the first five rows for initial inspection
    df = pd.read_excel(
        FILE_PATH,
        sheet_name="SAFMRs",
        nrows=5
    )

    print("\n=== DATASET COLUMNS ===")
    print(df.columns.tolist())

    print("\n=== FIRST FIVE ROWS ===")
    print(df.to_string(index=False))

    print("\n=== COLUMN DATA TYPES ===")
    print(df.dtypes)


if __name__ == "__main__":
    inspect_hud_data()
