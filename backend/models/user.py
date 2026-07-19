from pydantic import BaseModel


class RepoOut(BaseModel):
    name: str
    language: str | None


class UserSummary(BaseModel):
    followers_count: int
    repos: list[RepoOut]
    most_used_language: str | None
    technologies: set[str]
