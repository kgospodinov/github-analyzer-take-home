from unittest.mock import Mock, patch

from github_api import Repo, get_user_data, get_user_repos


def make_response(status_code=200, json_data=None, links=None):
    resp = Mock()
    resp.status_code = status_code
    resp.json.return_value = json_data
    resp.links = links or {}
    return resp


class TestGetUserData:
    def test_returns_user_data_on_success(self):
        with patch("github_api.requests.get", return_value=make_response(200, {"login": "test-github-user"})):
            result = get_user_data("test-github-user")

        assert result == {"login": "test-github-user"}

    def test_returns_none_when_user_not_found(self):
        with patch("github_api.requests.get", return_value=make_response(404)):
            result = get_user_data("does-not-exist")

        assert result is None


class TestGetUserRepos:
    def test_returns_repos_from_a_single_page(self):
        response = make_response(200, [{"name": "repo1", "language": "Python"}])

        with patch("github_api.requests.get", return_value=response) as mock_get:
            result = get_user_repos("test-github-user")

        assert result == [Repo(name="repo1", language="Python")]
        mock_get.assert_called_once()

    def test_follows_pagination_until_there_is_no_next_link(self):
        page1 = make_response(
            200,
            [{"name": "repo1", "language": "Python"}],
            links={"next": {"url": "https://api.github.com/users/test-github-user/repos?page=2"}},
        )
        page2 = make_response(
            200,
            [{"name": "repo2", "language": "Go"}],
            links={"next": {"url": "https://api.github.com/users/test-github-user/repos?page=3"}},
        )
        page3 = make_response(200, [{"name": "repo3", "language": None}])

        with patch("github_api.requests.get", side_effect=[page1, page2, page3]) as mock_get:
            result = get_user_repos("test-github-user")

        assert result == [
            Repo(name="repo1", language="Python"),
            Repo(name="repo2", language="Go"),
            Repo(name="repo3", language=None),
        ]
        assert mock_get.call_count == 3
        assert mock_get.call_args_list[1].args[0] == page1.links["next"]["url"]
        assert mock_get.call_args_list[2].args[0] == page2.links["next"]["url"]

    def test_returns_none_when_user_not_found(self):
        with patch("github_api.requests.get", return_value=make_response(404)):
            result = get_user_repos("does-not-exist")

        assert result is None
