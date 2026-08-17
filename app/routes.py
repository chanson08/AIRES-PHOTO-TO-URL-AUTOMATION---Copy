from flask import Blueprint, render_template, request

from . import config
from .services.ecoqpay_client import generate_ecoqpay_qr_base64
from .services.github_client import upload_image_to_github

main_bp = Blueprint("main", __name__)


# =============================================================================
# Routes
# =============================================================================

@main_bp.route("/", methods=["GET", "POST"])
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
