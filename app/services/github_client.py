import base64

import requests
from werkzeug.utils import secure_filename

from .. import config

# =============================================================================
# GitHub Upload
# =============================================================================

def upload_image_to_github(image_file, filename: str) -> str:
    safe_filename = secure_filename(filename)

    if not safe_filename:
        raise ValueError("Invalid filename.")

    repo_path = f"{config.GITHUB_UPLOAD_FOLDER}/{safe_filename}"

    api_url = (
        f"https://api.github.com/repos/"
        f"{config.GITHUB_USERNAME}/{config.GITHUB_REPO}/contents/{repo_path}"
    )

    encoded_content = base64.b64encode(image_file.read()).decode("utf-8")

    headers = {
        "Authorization": f"Bearer {config.GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    check_response = requests.get(
        api_url,
        headers=headers,
        timeout=config.REQUEST_TIMEOUT,
    )

    file_sha = None

    if check_response.status_code == 200:
        file_sha = check_response.json().get("sha")
    elif check_response.status_code != 404:
        raise RuntimeError(
            f"GitHub check error {check_response.status_code}: "
            f"{check_response.text}"
        )

    payload = {
        "message": f"Upload {safe_filename}",
        "content": encoded_content,
        "branch": config.GITHUB_BRANCH,
    }

    if file_sha:
        payload["sha"] = file_sha

    upload_response = requests.put(
        api_url,
        json=payload,
        headers=headers,
        timeout=config.REQUEST_TIMEOUT,
    )

    if upload_response.status_code not in (200, 201):
        raise RuntimeError(
            f"GitHub upload error {upload_response.status_code}: "
            f"{upload_response.text}"
        )

    return (
        f"https://raw.githubusercontent.com/"
        f"{config.GITHUB_USERNAME}/{config.GITHUB_REPO}/"
        f"{config.GITHUB_BRANCH}/{repo_path}"
    )
