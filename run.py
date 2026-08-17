import os

from app import create_app

app = create_app()

# =============================================================================
# Entry Point
# =============================================================================

if __name__ == "__main__":
    port = int(os.getenv("PORT", 9999))
    debug = os.getenv("FLASK_DEBUG", "False").lower() in ("1", "true", "yes")
    app.run(host="0.0.0.0", port=port, debug=debug)
