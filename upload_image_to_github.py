import os

from flask import Flask, render_template, request

import config
from ecoqpay_client import generate_ecoqpay_qr_base64
from github_client import upload_image_to_github

app = Flask(__name__)


# =============================================================================
# Routes
# =============================================================================

@app.route("/", methods=["GET", "POST"])
def index():
    ecoqpay_image_base64 = None
    error = None

    if request.method == "POST":
        try:
            config.validate_config()

            image = request.files.get("image")

            if not image or image.filename == "":
                raise ValueError("No image uploaded.")

            github_url = upload_image_to_github(image, image.filename)
            ecoqpay_image_base64 = generate_ecoqpay_qr_base64(github_url)

        except Exception as exc:
            error = str(exc)

    return render_template(
        "index.html",
        ecoqpay_image_base64=ecoqpay_image_base64,
        error=error,
    )


# =============================================================================
# Entry Point
# =============================================================================

if __name__ == "__main__":
    port = int(os.getenv("PORT", 9999))
    debug = os.getenv("FLASK_DEBUG", "False").lower() in ("1", "true", "yes")
    app.run(host="0.0.0.0", port=port, debug=debug)
