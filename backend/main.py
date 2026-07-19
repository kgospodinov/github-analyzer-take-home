import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models.user import UserSummary
from service import fetch_github_user


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/user", response_model=UserSummary)
def get_user(username: str):
    try:
        user = fetch_github_user(username=username)
    except requests.exceptions.HTTPError as exc:
        if exc.response is not None and exc.response.status_code == 403:
            raise HTTPException(status_code=429, detail="GitHub API rate limit exceeded. Please try again later.")
        raise

    return {
        "followers_count": user.followers,
        "repos": [{"name": repo.name, "language": repo.language} for repo in user.repos],
        "most_used_language": user.get_most_used_language(),
        "technologies": user.get_technologies(),
    }
