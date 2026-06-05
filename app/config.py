import os
from pathlib import Path

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Branding configuration
BRAND_LOGO_PATH = os.getenv("BRAND_LOGO_PATH", str(BASE_DIR / "assets" / "logo.jpeg"))
BRAND_PRIMARY_COLOR = os.getenv("BRAND_PRIMARY_COLOR", "#0A0F24")  # Dark navy
BRAND_ACCENT_COLOR = os.getenv("BRAND_ACCENT_COLOR", "#1E90FF")   # Accent blue

# API keys for stock image services (optional)
UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY", "0zRhV_q030C0jwmxXd8lxwDKOJCAcAjQ_RaBLaeKuvY")
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "iviQcdanD1awyVelWUa5ksBKhvfVkPtOGPrvkMrLvpbJkacbNJ7nDJ30")

# Output configuration
OUTPUT_ROOT = os.getenv("OUTPUT_ROOT", str(BASE_DIR / "output_batches"))

# Ensure output directory exists
Path(OUTPUT_ROOT).mkdir(parents=True, exist_ok=True)
