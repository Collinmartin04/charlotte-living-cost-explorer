# Charlotte Living Cost Explorer

**A data-driven project exploring housing costs, commuting expenses, and the estimated total cost of living in Charlotte, North Carolina.**

> 🚧 **Project Status: In Development**
>
> This project is actively being developed. The initial HUD housing data pipeline and automated validation tests are complete. Geographic validation, additional data integration, exploratory analysis, and the interactive application are planned or in progress.

## Overview

When comparing apartments, monthly rent is often the primary consideration. However, commuting expenses, parking, utilities, and other recurring costs can significantly affect the total cost of living.

Charlotte Living Cost Explorer aims to help individuals relocating to or within the Charlotte area make more informed housing decisions by combining publicly available housing data with customizable cost estimates.

The project also serves as an end-to-end data analytics and software engineering case study, emphasizing data quality, reproducibility, geographic analysis, and transparent assumptions.

## Project Objectives

The application is being designed to:

- Explore rental benchmarks across Charlotte-area ZIP codes.
- Compare housing options using user-provided rental prices.
- Estimate monthly commuting expenses based on distance, fuel economy, commute frequency, and transportation costs.
- Calculate and visualize estimated total monthly living expenses.
- Integrate geographic and neighborhood-level data.
- Provide interactive maps and housing cost comparisons.
- Clearly distinguish published benchmarks from actual apartment prices and user-provided estimates.

These features represent the planned application and are not all implemented.

## Current Progress

### Completed

- [x] Initialize Git repository and publish project to GitHub.
- [x] Acquire HUD FY2027 Small Area Fair Market Rent data.
- [x] Explore the structure of the national HUD dataset.
- [x] Identify Charlotte-Concord-Gastonia HUD Metro FMR Area records.
- [x] Profile missing values, duplicate identifiers, and rental benchmark distributions.
- [x] Investigate repeated ZIP-level rental benchmarks.
- [x] Transform housing benchmarks into a normalized analytical dataset.
- [x] Implement eight automated data quality tests using Pytest.

### In Progress / Planned

- [ ] Validate HUD ZIP codes against Census geographic identifiers.
- [ ] Integrate Census ACS demographic and housing data.
- [ ] Evaluate Zillow rental trend coverage and usage restrictions.
- [ ] Conduct exploratory analysis of Charlotte-area housing benchmarks.
- [ ] Design a PostgreSQL database.
- [ ] Implement a FastAPI backend.
- [ ] Build an interactive React and TypeScript frontend.
- [ ] Implement customizable commute and total monthly cost calculations.
- [ ] Integrate geographic visualizations and neighborhood insights.
- [ ] Add automated data refreshes and CI/CD.
- [ ] Deploy the application publicly.

## Data Sources

### HUD Small Area Fair Market Rents

**Status: Initial ingestion and transformation complete**

The project currently uses the FY2027 HUD Small Area Fair Market Rent dataset.

The initial analysis identified:

| Metric | Result |
|---|---:|
| National dataset records | 51,871 |
| Charlotte HUD Metro FMR Area ZIP records | 129 |
| Bedroom categories | 5 |
| Processed analytical records | 645 |
| Automated validation tests | 8 passing |

The processed dataset contains ZIP identifiers, HUD geographic identifiers, fiscal year, bedroom count, and monthly rental benchmarks.

**Important:** HUD Fair Market Rents are government rental benchmarks, not live apartment listings or observed asking prices.

The initial geographic filter represents the Charlotte-Concord-Gastonia, NC-SC HUD Metro FMR Area, not exclusively the City of Charlotte or Mecklenburg County.

Source: [HUD Fair Market Rent Datasets](https://www.huduser.gov/portal/datasets/fmr.html)

### Planned Data Sources

| Source | Intended Use | Status |
|---|---|---|
| U.S. Census ACS | Demographic, housing, and income indicators | Planned |
| Census geographic files | ZIP/ZCTA validation and geographic boundaries | Planned |
| Zillow Research | Rental market trend analysis | Under evaluation |
| Charlotte-Mecklenburg Quality of Life Explorer | Neighborhood indicators | Planned |
| Charlotte Area Transit System | Transit routes and accessibility | Planned |
| Routing provider | Estimated commute distances and travel times | Under evaluation |

Each source will be evaluated for geographic coverage, update frequency, methodology, licensing, and data quality before integration.

## Technology Stack

### Currently Used

- **Python:** Data ingestion, exploration, and transformation
- **Pandas:** Data cleaning and analytical processing
- **OpenPyXL:** Excel data processing
- **Requests:** HTTP-based data acquisition
- **Pytest:** Automated data validation
- **Git and GitHub:** Version control and project documentation

### Planned

- **PostgreSQL:** Relational data storage and analytical queries
- **FastAPI:** Backend APIs
- **React and TypeScript:** Interactive user interface
- **Tailwind CSS:** Frontend styling
- **MapLibre or Leaflet:** Geographic visualizations
- **Docker:** Application containerization
- **GitHub Actions:** Automated testing and CI/CD

The technology stack may evolve as requirements and data availability are validated.

## Current Data Pipeline

The existing workflow follows these steps:

1. Acquire the national HUD FY2027 SAFMR workbook.
2. Inspect its structure and available geographic identifiers.
3. Filter records using the Charlotte HUD metropolitan area code.
4. Profile missing values, duplicates, and rental benchmark distributions.
5. Convert bedroom-specific columns into long-format records.
6. Save the processed analytical dataset.
7. Validate the output using automated tests.

The resulting table supports analysis by ZIP code, bedroom count, and fiscal year.

## Running the Current Project

**Requirements:** Python 3.12 or a compatible Python 3 environment.

Clone the repository:

```bash
git clone https://github.com/Collinmartin04/charlotte-living-cost-explorer.git
cd charlotte-living-cost-explorer
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the environment on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the current dependencies:

```bash
python -m pip install pandas openpyxl requests pytest
```

### Obtain the HUD Dataset

Download the FY2027 Small Area Fair Market Rents Excel workbook from the [HUD FMR data portal](https://www.huduser.gov/portal/datasets/fmr.html).

Save the workbook as:

```text
data/raw/FY27_safmrs.xlsx
```

The original workbook is excluded from version control.

The automated download script is included in the repository, but the HUD endpoint has returned an unexpected HTTP response during development. Manual acquisition is currently the verified workflow.

### Transform the Dataset

```bash
python scripts/transform_hud.py
```

This generates:

```text
data/processed/charlotte_hud_fy2027.csv
```

### Run Automated Tests

```bash
python -m pytest -v
```

The current test suite checks the processed dataset's schema, required values, ZIP format, bedroom categories, rental benchmarks, geographic identifiers, and uniqueness.

The tests require the processed dataset to exist locally.

## Data Quality and Limitations

This project prioritizes reproducible analysis and responsible interpretation.

Current considerations include:

- HUD SAFMRs are rental benchmarks, not actual available apartment prices.
- HUD metropolitan areas do not correspond exactly to municipal boundaries.
- USPS ZIP codes and Census ZIP Code Tabulation Areas are not interchangeable.
- Some ZIP identifiers may not represent conventional residential neighborhoods.
- Repeated rental benchmark values require careful interpretation.
- Summary statistics calculated across ZIP codes are not necessarily representative of households or available rental units.
- The current validation tests establish basic structural integrity but do not yet verify complete geographic coverage or all source-to-output relationships.
- Commute and total living cost estimates will depend on user assumptions and routing data limitations.

These limitations will be documented and addressed as development progresses.

## Development Roadmap

**Phase 1: Data Feasibility and Exploration**

Validate source datasets, establish geographic coverage, create reproducible transformations, and conduct exploratory analysis.

**Phase 2: Cost Comparison MVP**

Implement customizable housing and commuting cost calculations with transparent assumptions.

**Phase 3: Database and Backend**

Design PostgreSQL tables and build documented FastAPI endpoints.

**Phase 4: Interactive Application**

Develop the React frontend, interactive visualizations, maps, and neighborhood comparisons.

**Phase 5: Production Deployment**

Deploy the application, automate tests and supported data refreshes, and publish technical documentation and a project case study.

## Project Motivation

Charlotte Living Cost Explorer is being developed to address a practical question: *How much does living in a particular location actually cost beyond the advertised rent?*

The project combines my interests in data science, analytics, and software engineering with the goal of building a useful, transparent tool for people making housing decisions.

Development is ongoing, with progress tracked through GitHub commits and project documentation.

---

**Status:** Active development. The public-facing application is not yet available.