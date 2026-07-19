import os
from dataclasses import dataclass

import requests


BASE_URL = "https://api.github.com"

TOKEN = os.getenv("GITHUB_TOKEN")

@dataclass(frozen=True)
class Repo:
    name: str
    language: str | None

def _headers():
    headers = {"Accept": "application/vnd.github+json"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    return headers


def _request(path: str, params: dict | None = None) -> dict | list | None:
    resp = requests.get(f"{BASE_URL}{path}", headers=_headers(), params=params)
    if resp.status_code == 404:
        return None
    resp.raise_for_status()
    return resp.json()


def _request_all_pages(path: str, params: dict | None = None) -> list | None:
    resp = requests.get(f"{BASE_URL}{path}", headers=_headers(), params=params)
    if resp.status_code == 404:
        return None
    resp.raise_for_status()
    results = resp.json()

    while "next" in resp.links:
        resp = requests.get(resp.links["next"]["url"], headers=_headers())
        resp.raise_for_status()
        results.extend(resp.json())

    return results


def get_user_data(username) -> dict | None:
    return _request(f"/users/{username}")


def get_user_repos(username) -> list[Repo] | None:
    data = _request_all_pages(f"/users/{username}/repos", params={"per_page": 10})
    if data is None:
        return None
    return [Repo(name=repo["name"], language=repo["language"]) for repo in data]

