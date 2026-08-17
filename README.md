# EcoQPay Generator

A small Flask app: upload an image, it gets pushed to GitHub, and the
resulting raw URL is turned into an EcoQPay QR code.

## Project layout

| File | Responsibility |
|---|---|
| `upload_image_to_github.py` | Flask app + route (entry point, used by `Procfile`) |
| `config.py` | environment variables, constants, `validate_config()` |
| `github_client.py` | uploads the image to a GitHub repo |
| `ecoqpay_client.py` | generates the EcoQPay QR code from a URL |
| `templates/index.html` | the upload form / result page |

## Environment variables

Copy `.env.example` to `.env` and fill in the values:

```bash
cp .env.example .env
```

| Variable | Required | Description |
|---|---|---|
| `GITHUB_TOKEN` | yes | GitHub personal access token with `repo` scope (or fine-grained "Contents: Read and write") on the target repo. Create one at [github.com/settings/tokens](https://github.com/settings/tokens). |
| `ECOQPAY_API_KEY` | yes | API key from EcoQPay/EcoQCode for `https://ecoqcode.sg/api/v1/generator/generate/ecoqpay`. |
| `PORT` | no | Port the app listens on when run locally. Defaults to `9999`. Hosts like Railway set this automatically. |
| `FLASK_DEBUG` | no | Set to `true`/`1`/`yes` to enable Flask debug mode locally. Defaults to off — leave it off in production. |

The GitHub repo/branch/folder the image gets uploaded to are set as
constants in `config.py` (`GITHUB_USERNAME`, `GITHUB_REPO`,
`GITHUB_UPLOAD_FOLDER`, `GITHUB_BRANCH`), not env vars — edit those
directly if you're pointing at a different repo.

## Running locally

```bash
pip install -r requirements.txt
python upload_image_to_github.py
```

Then open `http://localhost:9999`.

## Deploying

The app is set up for Railway (or any host that runs a `Procfile`):

```
web: gunicorn -w 4 upload_image_to_github:app
```

Set `GITHUB_TOKEN` and `ECOQPAY_API_KEY` as environment variables on the
host — everything else (`PORT`, build/start command) is auto-detected.
