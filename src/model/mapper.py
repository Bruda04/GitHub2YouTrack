from .issue import Issue
from .task import Task


def convert_issue_to_task(issue: Issue) -> Task:
    task = Task(
        task_id=issue.number,
        summary=issue.title,
        description=f"{issue.description}\n\nOriginal Issue URL: {issue.url}"
    )
    return task

def convert_issues_to_tasks(issues: list[Issue]) -> list[Task]:
    return [convert_issue_to_task(issue) for issue in issues]