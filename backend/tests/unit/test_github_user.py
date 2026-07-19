from github_api import Repo
from github_user import GitHubUser


def make_repo(name: str, language: str | None) -> Repo:
    return Repo(name=name, language=language)

class TestGetMostUsedLanguage:
    def test_returns_none_when_no_repos(self):
        user = GitHubUser(username="test-github-user", repos=[], followers=0)
        assert user.get_most_used_language() is None

    def test_returns_none_when_repos_is_none(self):
        user = GitHubUser(username="test-github-user", repos=None, followers=0)
        assert user.get_most_used_language() is None

    def test_returns_none_when_all_languages_are_none(self):
        repos = [make_repo("repo1", None), make_repo("repo2", None)]
        user = GitHubUser(username="test-github-user", repos=repos, followers=0)
        assert user.get_most_used_language() is None

    def test_ignores_repos_with_none_language(self):
        repos = [
            make_repo("repo1", None),
            make_repo("repo2", "Python"),
            make_repo("repo3", None),
        ]
        user = GitHubUser(username="test-github-user", repos=repos, followers=0)
        assert user.get_most_used_language() == "Python"

    def test_returns_single_language(self):
        repos = [make_repo("repo1", "Python")]
        user = GitHubUser(username="test-github-user", repos=repos, followers=0)
        assert user.get_most_used_language() == "Python"

    def test_returns_most_frequent_language(self):
        repos = [
            make_repo("repo1", "Python"),
            make_repo("repo2", "JavaScript"),
            make_repo("repo3", "Python"),
            make_repo("repo4", "Python"),
            make_repo("repo5", "JavaScript"),
        ]
        user = GitHubUser(username="test-github-user", repos=repos, followers=0)
        assert user.get_most_used_language() == "Python"

class TestGetTechnologies:
    def test_returns_empty_set_when_repos_is_none(self):
        user = GitHubUser(username="test-github-user", repos=None, followers=0)
        assert user.get_technologies() == set()

    def test_excludes_none_language(self):
        repos = [make_repo("repo1", None), make_repo("repo2", "Python")]
        user = GitHubUser(username="test-github-user", repos=repos, followers=0)
        assert user.get_technologies() == {"Python"}

    def test_deduplicates_languages(self):
        repos = [
            make_repo("repo1", "Python"),
            make_repo("repo2", "Python"),
            make_repo("repo3", "Go"),
        ]
        user = GitHubUser(username="test-github-user", repos=repos, followers=0)
        assert user.get_technologies() == {"Python", "Go"}
