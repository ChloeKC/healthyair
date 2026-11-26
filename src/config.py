# HealthyAir - Google Cloud Storage configuration

from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()
# DATA_SOURCE = os.getenv("DATA_SOURCE", "local")

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"

RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
FEATURE_DIR = DATA_DIR / "features"

PROJECT_ID = "healthy-air-analysis"
BUCKET_NAME = "uci_air_quality_20119102"
LOCATION = "EU"

PROJECT_ID = os.getenv("PROJECT_ID")
BUCKET_NAME = os.getenv("BUCKET_NAME")
LOCATION = os.getenv("LOCATION")

DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
FEATURE_DIR = DATA_DIR / "features"

RAW_GCS_PATH = (
    "raw/uci-air-quality_20119102/v1/AirQualityUCI.csv"
)

PROCESSED_GCS_PATH = (
    "processed/v1/"
)