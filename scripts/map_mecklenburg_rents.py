
from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd


# ============================================================
# FILE PATHS AND CONFIGURATION
# ============================================================

ZCTA_PATH = Path("data/raw/cb_2020_us_zcta520_500k.zip")
COUNTY_PATH = Path("data/raw/cb_2020_us_county_500k.zip")

HOUSING_PATH = Path(
    "data/processed/mecklenburg_housing_fy2027.csv"
)

OUTPUT_PATH = Path(
    "reports/figures/mecklenburg_2br_safmr_map.png"
)

# NAD83 / North Carolina
# A projected CRS suitable for area calculations in meters.
PROJECTED_CRS = "EPSG:32119"

# Mecklenburg County, North Carolina
STATE_FIPS = "37"
COUNTY_FIPS = "119"


# ============================================================
# MAIN FUNCTION
# ============================================================

def map_mecklenburg_rents():
    """
    Create a choropleth map of FY2027 two-bedroom HUD
    Small Area Fair Market Rent benchmarks.

    Only ZCTAs with more than 90% of their mapped area
    inside Mecklenburg County are included.

    ZCTA polygons are clipped to Mecklenburg County
    before plotting.
    """

    # --------------------------------------------------------
    # 1. LOAD DATA
    # --------------------------------------------------------

    print("\n=== LOADING DATA ===")

    zctas = gpd.read_file(ZCTA_PATH)
    counties = gpd.read_file(COUNTY_PATH)

    housing = pd.read_csv(
        HOUSING_PATH,
        dtype={"zip_code": str},
    )

    print(f"National Census ZCTAs: {len(zctas)}")
    print(f"National Census counties: {len(counties)}")
    print(f"Housing benchmark records: {len(housing)}")

    # --------------------------------------------------------
    # 2. FILTER HOUSING BENCHMARKS
    # --------------------------------------------------------

    print("\n=== FILTERING HOUSING DATA ===")

    core = housing.loc[
        (housing["bedrooms"] == 2)
        & (housing["geographic_category"] == "mostly_inside"),
        ["zip_code", "monthly_safmr"],
    ].copy()

    if core.empty:
        raise ValueError(
            "No two-bedroom benchmarks found for core ZCTAs."
        )

    if core["zip_code"].duplicated().any():
        raise ValueError(
            "Duplicate ZIP identifiers in core housing data."
        )

    if core["monthly_safmr"].isna().any():
        raise ValueError(
            "Missing rental benchmarks in core housing data."
        )

    print(f"Core ZCTAs selected: {len(core)}")
    print(
        f"Benchmark range: "
        f"${core['monthly_safmr'].min():,.0f} to "
        f"${core['monthly_safmr'].max():,.0f}"
    )

    # --------------------------------------------------------
    # 3. JOIN HOUSING DATA WITH ZCTA POLYGONS
    # --------------------------------------------------------

    print("\n=== JOINING GEOGRAPHIC DATA ===")

    mapped = zctas.merge(
        core,
        left_on="GEOID20",
        right_on="zip_code",
        how="inner",
        validate="one_to_one",
    )

    if len(mapped) != len(core):
        raise ValueError(
            "Not all core ZCTAs matched Census polygons."
        )

    if mapped.geometry.isna().any():
        raise ValueError(
            "Missing ZCTA polygon geometry."
        )

    print(f"Matched ZCTA polygons: {len(mapped)}")

    # --------------------------------------------------------
    # 4. IDENTIFY MECKLENBURG COUNTY
    # --------------------------------------------------------

    county = counties.loc[
        (counties["STATEFP"] == STATE_FIPS)
        & (counties["COUNTYFP"] == COUNTY_FIPS)
    ].copy()

    if len(county) != 1:
        raise ValueError(
            "Expected exactly one Mecklenburg County record. "
            f"Found {len(county)}."
        )

    if not county.geometry.is_valid.all():
        raise ValueError(
            "Mecklenburg County geometry is invalid."
        )

    print("Mecklenburg County identified successfully.")

    # --------------------------------------------------------
    # 5. PROJECT GEOGRAPHIC DATA
    # --------------------------------------------------------

    print("\n=== PROJECTING GEOMETRIES ===")

    mapped = mapped.to_crs(PROJECTED_CRS)
    county = county.to_crs(PROJECTED_CRS)

    print(f"Projected coordinate system: {PROJECTED_CRS}")

    # --------------------------------------------------------
    # 6. CLIP ZCTAs TO MECKLENBURG COUNTY
    # --------------------------------------------------------

    print("\n=== CLIPPING ZCTA POLYGONS ===")

    original_count = mapped["zip_code"].nunique()

    # Keep a copy of the original ZCTA geometry so we can
    # measure how much polygon area the clipping removes.
    original_area = mapped.geometry.area.sum()

    # Clip the mapped ZCTA polygons to the county boundary.
    #
    # This changes the displayed geographic shapes only.
    # It does not modify the HUD rental benchmark values.
    clipped = gpd.clip(
        mapped,
        county,
        keep_geom_type=True,
    )

    if clipped.empty:
        raise ValueError(
            "No mapped ZCTA polygons remain after clipping."
        )

    clipped_count = clipped["zip_code"].nunique()

    if clipped_count != original_count:
        raise ValueError(
            "Some ZCTAs were lost during clipping. "
            f"Before: {original_count}, after: {clipped_count}"
        )

    # Clipping may produce multiple geometry pieces for one ZCTA.
    # This is a valid geospatial result, not necessarily bad data.
    duplicate_count = clipped["zip_code"].duplicated().sum()

    print(
        f"Additional clipped geometry records: {duplicate_count}"
    )

    # Combine pieces belonging to the same ZCTA.
    clipped = clipped.dissolve(
        by="zip_code",
        aggfunc="first",
    ).reset_index()

    # Validate the resulting geographic identifiers.
    if clipped["zip_code"].duplicated().any():
        raise ValueError(
            "Duplicate ZIP identifiers remain after dissolving."
        )

    if clipped["zip_code"].nunique() != original_count:
        raise ValueError(
            "The number of unique ZCTAs changed after dissolving."
        )

    if not clipped.geometry.is_valid.all():
        raise ValueError(
            "Invalid geometry detected after clipping."
        )

    clipped_area = clipped.geometry.area.sum()

    print(f"ZCTAs before clipping: {original_count}")
    print(f"ZCTAs after clipping: {clipped_count}")

    print(
        f"Original mapped area: "
        f"{original_area:,.2f} square meters"
    )

    print(
        f"Clipped mapped area: "
        f"{clipped_area:,.2f} square meters"
    )

    print(
        f"Area removed by clipping: "
        f"{original_area - clipped_area:,.2f} square meters"
    )

    # --------------------------------------------------------
    # 7. VERIFY CLIPPED GEOMETRIES
    # --------------------------------------------------------

    print("\n=== GEOMETRY VALIDATION ===")

    county_geometry = county.geometry.iloc[0]

    # Any geometry remaining outside the county would indicate
    # that clipping did not work as intended.
    outside_area = (
        clipped.geometry
        .difference(county_geometry)
        .area
        .sum()
    )

    print(
        "Total mapped area outside county: "
        f"{outside_area:.6f} square meters"
    )

    # A tiny tolerance accounts for numerical precision.
    geometry_tolerance = 1e-6

    if outside_area > geometry_tolerance:
        raise ValueError(
            "Clipped polygons still extend outside "
            "Mecklenburg County."
        )

    print("Clipping validation passed.")

    # --------------------------------------------------------
    # 8. CREATE CHOROPLETH MAP
    # --------------------------------------------------------

    print("\n=== GENERATING CHOROPLETH MAP ===")

    fig, ax = plt.subplots(
        figsize=(10, 10),
    )

    # IMPORTANT:
    # Plot the clipped GeoDataFrame, not the original mapped
    # GeoDataFrame.
    clipped.plot(
        column="monthly_safmr",
        ax=ax,
        cmap="YlOrRd",
        vmin=core["monthly_safmr"].min(),
        vmax=core["monthly_safmr"].max(),
        legend=True,
        edgecolor="white",
        linewidth=0.7,
        legend_kwds={
            "label": "Monthly HUD SAFMR benchmark ($)",
            "shrink": 0.7,
        },
    )

    # Draw the Mecklenburg County boundary over the polygons.
    county.boundary.plot(
        ax=ax,
        color="black",
        linewidth=1.5,
        zorder=3,
    )

    ax.set_title(
        "Mecklenburg County: Two-Bedroom HUD Rental Benchmarks",
        fontsize=15,
        fontweight="bold",
        pad=18,
    )

    ax.set_axis_off()
    ax.set_aspect("equal")

    # Add an explanatory note.
    fig.text(
        0.5,
        0.04,
        "FY2027 HUD SAFMR | 2020 Census ZCTAs | "
        f"{clipped_count} areas with >90% overlap\n"
        "ZCTAs clipped to Mecklenburg County for display. "
        "Benchmarks are not apartment listing prices.",
        ha="center",
        va="center",
        fontsize=9,
    )

    fig.tight_layout(
        rect=[0, 0.075, 1, 1],
    )

    # --------------------------------------------------------
    # 9. SAVE OUTPUT
    # --------------------------------------------------------

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    fig.savefig(
        OUTPUT_PATH,
        dpi=200,
        bbox_inches="tight",
    )

    print(f"\nSaved map to: {OUTPUT_PATH}")

    plt.show()
    plt.close(fig)

    print("\n=== MAP GENERATION COMPLETE ===")


if __name__ == "__main__":
    map_mecklenburg_rents()
