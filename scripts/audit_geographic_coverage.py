
from pathlib import Path

import pandas as pd


PROCESSED = Path("data/processed")


def audit_geographic_coverage():
    """Audit HUD and Census coverage of Mecklenburg ZCTAs."""

    hud = pd.read_csv(
        PROCESSED / "charlotte_hud_fy2027.csv",
        dtype={"zip_code": str},
    )

    gazetteer_matches = pd.read_csv(
        PROCESSED / "hud_census_zcta_comparison.csv",
        dtype={"zip_code": str},
    )

    overlap = pd.read_csv(
        PROCESSED / "mecklenburg_zcta_overlap.csv",
        dtype={"zcta": str},
    )

    # One record per HUD ZIP identifier.
    hud_zips = hud[["zip_code"]].drop_duplicates()

    # Keep only the fields needed from the Gazetteer audit.
    gazetteer = gazetteer_matches[
        ["zip_code", "match_status"]
    ].copy()

    if gazetteer["zip_code"].duplicated().any():
        raise ValueError("Duplicate ZIPs in Gazetteer audit.")

    # Start with every ZCTA overlapping Mecklenburg.
    audit = overlap.merge(
        hud_zips.assign(in_hud=True),
        left_on="zcta",
        right_on="zip_code",
        how="left",
        validate="one_to_one",
    )

    audit["in_hud"] = audit["in_hud"].fillna(False).astype(bool)

    # Add the earlier Gazetteer match results.
    audit = audit.merge(
        gazetteer,
        on="zip_code",
        how="left",
        validate="one_to_one",
    )

    audit["in_gazetteer"] = (
        audit["match_status"] == "matched"
    )

    print("\n=== MECKLENBURG GEOGRAPHIC COVERAGE AUDIT ===")

    print("ZCTAs with positive county overlap:", len(audit))
    print("Also present in HUD:", int(audit["in_hud"].sum()))

    print(
        "Present in HUD and matched to Gazetteer:",
        int((audit["in_hud"] & audit["in_gazetteer"]).sum()),
    )

    print(
        "Present in HUD but unmatched to Gazetteer:",
        int((audit["in_hud"] & ~audit["in_gazetteer"]).sum()),
    )

    print("\n=== POLYGON ZCTAs MISSING FROM HUD ===")

    print(
        audit.loc[~audit["in_hud"], ["zcta", "pct_in_mecklenburg"]]
        .round(2)
        .to_string(index=False)
    )

    print("\n=== HUD ZIPs WITH POLYGONS BUT NO GAZETTEER MATCH ===")

    discrepancy = audit.loc[
        audit["in_hud"] & ~audit["in_gazetteer"],
        ["zcta", "pct_in_mecklenburg"],
    ]

    print(discrepancy.round(2).to_string(index=False))

    print("\n=== COVERAGE BY OVERLAP THRESHOLD ===")

    for threshold in (0, 10, 50, 90):
        subset = audit.loc[
            audit["pct_in_mecklenburg"] > threshold
        ]
        print(
            f"Greater than {threshold}%: "
            f"{len(subset)} ZCTAs, "
            f"{int(subset['in_hud'].sum())} in HUD"
        )

    output_path = PROCESSED / "geographic_coverage_audit.csv"

    audit.drop(columns=["zip_code", "match_status"]).to_csv(
        output_path,
        index=False,
    )

    print(f"\nSaved audit to: {output_path}")


if __name__ == "__main__":
    audit_geographic_coverage()
