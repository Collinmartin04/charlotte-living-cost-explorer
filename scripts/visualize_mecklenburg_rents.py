
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


DATA_PATH = Path("data/processed/mecklenburg_housing_fy2027.csv")
OUTPUT_DIR = Path("reports/figures")


def visualize_mecklenburg_rents():
    """Visualize FY2027 two-bedroom SAFMR benchmarks."""

    housing = pd.read_csv(
        DATA_PATH,
        dtype={"zip_code": str},
    )

    core = housing.loc[
        (housing["geographic_category"] == "mostly_inside")
        & (housing["bedrooms"] == 2)
    ].copy()

    if core.empty:
        raise ValueError("No records available for visualization.")

    if core["monthly_safmr"].isna().any():
        raise ValueError("Missing rental benchmarks.")

    rents = core["monthly_safmr"]

    mean_rent = rents.mean()
    median_rent = rents.median()

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.hist(
        rents,
        bins=10,
        edgecolor="white",
        linewidth=1.2,
    )

    ax.axvline(
        mean_rent,
        linestyle="--",
        linewidth=2,
        label=f"Mean: ${mean_rent:,.0f}",
    )

    ax.axvline(
        median_rent,
        linestyle=":",
        linewidth=2,
        label=f"Median: ${median_rent:,.0f}",
    )

    ax.set_title(
        "Mecklenburg County Area: Two-Bedroom HUD Rent Benchmarks",
        fontsize=15,
        fontweight="bold",
        pad=16,
    )

    ax.set_xlabel("Monthly HUD SAFMR benchmark ($)")
    ax.set_ylabel("Number of ZCTAs")
    ax.legend()

    ax.grid(axis="y", alpha=0.2)
    ax.set_axisbelow(True)

    fig.text(
        0.5,
        0.01,
        "FY2027 HUD SAFMR | 33 ZCTAs with >90% mapped area in Mecklenburg County\n"
        "Benchmarks are not observed apartment listing prices.",
        ha="center",
        fontsize=9,
    )

    fig.tight_layout(rect=[0, 0.075, 1, 1])

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    output_path = OUTPUT_DIR / "mecklenburg_2br_safmr_histogram.png"

    fig.savefig(
        output_path,
        dpi=200,
        bbox_inches="tight",
    )

    plt.show()
    plt.close(fig)

    print(f"\nSaved visualization to: {output_path}")


if __name__ == "__main__":
    visualize_mecklenburg_rents()
