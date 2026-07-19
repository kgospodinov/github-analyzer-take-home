from unittest.mock import patch

import requests
from fastapi.testclient import TestClient

import main
from github_api import Repo


client = TestClient(main.app)


def test_returns_user_summary():
    with (
        patch("service.get_user_data", return_value={"login": "test-github-user", "followers": 42}),
        patch(
            "service.get_user_repos",
            return_value=[
                Repo(name="repo1", language="Python"),
                Repo(name="repo2", language="Python"),
                Repo(name="repo3", language="Go"),
                Repo(name="repo4", language=None),
            ],
        ),
    ):
        response = client.get("/api/user", params={"username": "test-github-user"})

    assert response.status_code == 200
    body = response.json()
    assert body["followers_count"] == 42
    assert body["most_used_language"] == "Python"
    assert set(body["technologies"]) == {"Python", "Go"}
    assert body["repos"] == [
        {"name": "repo1", "language": "Python"},
        {"name": "repo2", "language": "Python"},
        {"name": "repo3", "language": "Go"},
        {"name": "repo4", "language": None},
    ]


def test_returns_404_when_user_not_found():
    with patch("service.get_user_data", return_value=None):
        response = client.get("/api/user", params={"username": "does-not-exist"})

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_returns_429_when_github_rate_limit_exceeded():
    resp = requests.Response()
    resp.status_code = 403

    with patch("service.get_user_data", side_effect=requests.exceptions.HTTPError(response=resp)):
        response = client.get("/api/user", params={"username": "test-github-user"})

    assert response.status_code == 429
    assert response.json()["detail"] == "GitHub API rate limit exceeded. Please try again later."


def test_other_http_errors_are_not_treated_as_rate_limited():
    resp = requests.Response()
    resp.status_code = 500

    with patch("service.get_user_data", side_effect=requests.exceptions.HTTPError(response=resp)):
        error_client = TestClient(main.app, raise_server_exceptions=False)
        response = error_client.get("/api/user", params={"username": "test-github-user"})

    assert response.status_code == 500
