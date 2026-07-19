# Backend

FastAPI service that proxies the GitHub API.

## Run

With [uv](https://docs.astral.sh/uv/):

```bash
uv sync
uv run uvicorn main:app --reload
```

With plain pip:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

The API is available at `http://localhost:8000`.

## Test

```bash
uv run pytest
```

Or with pip (after activating the venv above):

```bash
pip install pytest httpx
pytest
```
