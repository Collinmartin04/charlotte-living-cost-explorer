# HUD and Census Geographic Validation

## Purpose

Evaluate how well ZIP identifiers in the FY2027 HUD Small Area Fair Market Rent dataset correspond to 2020 Census ZIP Code Tabulation Areas (ZCTAs).

This analysis supports geographic data quality assessment for the Charlotte Living Cost Explorer.

## Data Sources

- HUD FY2027 Small Area Fair Market Rents
- 2020 U.S. Census ZCTA Gazetteer

**Study scope:** Charlotte-Concord-Gastonia, NC-SC HUD Metro FMR Area.

## Methodology

1. Extracted records belonging to HUD area `METRO16740M16740`.
2. Standardized ZIP identifiers as five-character strings.
3. Reduced the normalized HUD table to unique ZIP identifiers.
4. Loaded the 2020 Census ZCTA Gazetteer.
5. Performed a left join between HUD ZIP identifiers and Census ZCTA GEOIDs.
6. Classified identifiers as matched or unmatched.
7. Compared two-bedroom rental benchmark distributions across the two groups.

## Results

| Metric | Result |
|---|---:|
| HUD ZIP identifiers | 129 |
| Matched Census ZCTAs | 85 |
| Unmatched identifiers | 44 |
| Identifier match rate | 65.9% |

### Two-Bedroom Benchmark Comparison

| Metric | Matched | Unmatched |
|---|---:|---:|
| Records | 85 | 44 |
| Mean | $1,646.82 | $1,827.50 |
| Median | $1,580 | $1,890 |
| Unique benchmark values | 64 | 7 |
| Records with $1,890 benchmark | 3 | 33 |

## Key Finding

Of the 44 unmatched HUD ZIP identifiers, 33 (75%) share a two-bedroom rental benchmark of $1,890.

In contrast, only 3 of the 85 matched identifiers (approximately 3.5%) have this same value.

This suggests that repeated benchmark values are strongly concentrated among identifiers that do not correspond to 2020 Census ZCTAs.

The underlying reason for this pattern has not yet been established.

## Limitations

- Matching five-digit identifiers does not establish equivalent geographic boundaries.
- Unmatched ZIP codes are not necessarily invalid or nonresidential.
- This analysis does not establish whether HUD used fallback estimates.
- The study area includes locations outside Charlotte city limits.
- Rental benchmarks are not current apartment asking prices.
- Statistics are unweighted by households or rental housing units.
- The Census geography and HUD fiscal year have different reference periods.

## Next Steps

- Review HUD methodology for repeated rental benchmark values.
- Obtain Census ZCTA polygon boundaries.
- Obtain Mecklenburg County and Charlotte municipal boundaries.
- Evaluate actual geographic intersections.
- Develop rules for including geographic areas in application visualizations.

## Status

Initial identifier validation complete. Spatial validation pending.