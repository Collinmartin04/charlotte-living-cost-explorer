
from pathlib import Path
import hashlib
import requests

# Official HUD FY2027 Small Area Fair Market Rents
HUD_URL = (
    "https://www.huduser.gov/portal/datasets/"
    "fmr/fmr2027/FY27_safmrs.xlsx"
)

OUTPUT_PATH = Path("data/raw/FY27_safmrs.xlsx")


def download_hud_data():
    """Download the HUD rental benchmark dataset."""

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    print("Downloading HUD rental data...")

    response = requests.get(HUD_URL, timeout=60)
    response.raise_for_status()

    
    print(f"HTTP Status: {response.status_code}")
    print(f"Final URL: {response.url}")
    print(f"Content-Type: {response.headers.get('Content-Type')}")
    print(f"Response size: {len(response.content):,} bytes")
    print(f"First 200 bytes: {response.content[:200]!r}")


    if not response.content.startswith(b"PK"):
        raise ValueError(
            "The response does not appear to be an Excel file."
        )

    OUTPUT_PATH.write_bytes(response.content)

    checksum = hashlib.sha256(
        response.content
    ).hexdigest()

    print("Download complete!")
    print(f"File: {OUTPUT_PATH}")
    print(f"Size: {len(response.content):,} bytes")
    print(f"SHA-256: {checksum}")


if __name__ == "__main__":
    download_hud_data()
