from github_api import Repo


class GitHubUser:
    def __init__(self, username: str, repos: list[Repo] | None, followers: int):
        self._username = username
        self._followers = followers
        if repos is None:
            repos = []
        self._repos = repos

    @property
    def username(self) -> str:
        return self._username

    @property
    def followers(self) -> int:
        return self._followers

    @property
    def repos(self) -> list[Repo]:
        return self._repos

    def get_most_used_language(self) -> str | None:
        repo_count = {}
        for repo in self.repos:
            if repo.language is None:
                continue

            if repo.language not in repo_count:
                repo_count[repo.language] = 0

            repo_count[repo.language] += 1

        most_used = None
        biggest_count = 0
        for language, count in repo_count.items():
            if count > biggest_count:
                biggest_count = count
                most_used = language

        return most_used

    def get_technologies(self) -> set[str]:
        return {repo.language for repo in self.repos if repo.language is not None}


