import base64
import secrets

import requests

import config

# =============================================================================
# EcoQPay QR Generation
# =============================================================================

def generate_encryption_key() -> str:
    """
    Generate a random 6-digit encryption key.
    First digit is 1-9 to avoid leading zero.
    """
    return str(secrets.randbelow(900000) + 100000)


def generate_ecoqpay_qr_base64(github_url: str) -> str:
    headers = {
        "API-KEY": config.ECOQPAY_API_KEY,
        "Content-Type": "application/json",
    }

    encryption_key = generate_encryption_key()

    payload = {
        "link1": github_url,
        "link2": "",
        "link3": "",
        "encryption-key": encryption_key,
    }

    response = requests.post(
        config.ECOQPAY_API_URL,
        json=payload,
        headers=headers,
        timeout=config.REQUEST_TIMEOUT,
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"EcoQPay error {response.status_code}: {response.text}"
        )

    return base64.b64encode(response.content).decode("utf-8")
