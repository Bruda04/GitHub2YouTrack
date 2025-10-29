# This module defines a GitHubClient class that interacts with the GitHub API to fetch issues from a specified repository
from typing import List
from github import Auth
from github import Github
from src.model.issue import Issue

class GitHubClient:
    def __init__(self, token: str, repository_name: str):
        self.repository_name = repository_name
        auth = Auth.Token(token)
        self.client = Github(auth=auth)
        self.repository = self.client.get_repo(self.repository_name)

    def get_repository_issues(self) -> List[Issue]:
        issues_list = []
        try:
            issues = self.repository.get_issues(state="all")
            for issue in issues:
                entity = Issue(
                    number=issue.number,
                    title=issue.title,
                    url=issue.html_url,
                    state=issue.state,
                    body=issue.body,
                    assignees=[assignee.login for assignee in issue.assignees],
                    labels=[label.name for label in issue.labels],
                    user=issue.user.login if issue.user else ""
                )
                issues_list.append(entity)

        except Exception as e:
            print(f"An error occurred: {e}")
        return issues_list