from fastapi import HTTPException

from github_api import get_user_data, get_user_repos
from github_user import GitHubUser


def fetch_github_user(username: str) -> GitHubUser:
    user_data = get_user_data(username)
    if user_data is None:
        raise HTTPException(status_code=404, detail="User not found")

    user_repos = get_user_repos(username=user_data["login"])

    return GitHubUser(username=user_data["login"], repos=user_repos, followers=user_data["followers"])
