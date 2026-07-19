# GitHub Analyzer

This is my solution to the HedgeServe take-home task. It's a small mono repo: a Python/FastAPI backend and an Angular frontend that let you search a GitHub username and see their follower count, repos, most-used language, and all technologies used across their repos.

### Structure

```
github-analyzer/
|
|-----backend/
|    |----main.py          # FastAPI app / API routes
|    |----github_api.py    # GitHub REST API client
|    |----github_user.py   # GitHubUser domain class
|    |----requirements.txt
|
|-----frontend/
|    |----src/             # Angular app
```

### Setup

#### Backend

Run from the `backend/` folder.

```commandline
pip install -r requirements.txt
uvicorn main:app --reload
```

#### Frontend

Run from the `frontend/` folder.

```commandline
npm install
ng serve
```

### Docker

Run both services with Docker Compose from the repo root:

```commandline
docker compose up
```

The backend is available at `http://localhost:8000` and the frontend at `http://localhost:4200`.
