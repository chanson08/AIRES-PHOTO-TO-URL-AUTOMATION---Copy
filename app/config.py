import os

from dotenv import load_dotenv

load_dotenv()

# =============================================================================
# Secrets (from environment)
# =============================================================================

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
ECOQPAY_API_KEY = os.getenv("ECOQPAY_API_KEY")

# =============================================================================
# GitHub
# =============================================================================

GITHUB_USERNAME = "kyanng"
GITHUB_REPO = "AIRES-ENVIRONMENT"
GITHUB_UPLOAD_FOLDER = "uploaded_images"
GITHUB_BRANCH = "main"

# =============================================================================
# EcoQPay
# =============================================================================

ECOQPAY_API_URL = "https://ecoqcode.sg/api/v1/generator/generate/ecoqpay"
#ECOQPAY_ENCRYPTION_KEY = "123456"

# =============================================================================
# Networking
# =============================================================================

REQUEST_TIMEOUT = 20


def validate_config() -> None:
    if not GITHUB_TOKEN:
        raise RuntimeError("Missing GITHUB_TOKEN environment variable.")

    if not ECOQPAY_API_KEY:
        raise RuntimeError("Missing ECOQPAY_API_KEY environment variable.")
