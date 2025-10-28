from .issue import Issue
from .task import Task


def convert_issue_to_task(issue: Issue) -> Task:
    task = Task(
        task_id=issue.number,
        summary=issue.title,
        description=f"{issue.body}\n\nOriginal Issue URL: {issue.url}"
    )

    # Add custom fields if available
    if issue.state:
        state_mapping = {
            "open": "To do",
            "closed": "Done"
        }

        youtrack_state = state_mapping.get(issue.state, "To do")

        task.add_custom_field(
            "State",
            {
                "$type": "StateBundleElement",
                "name": youtrack_state
            },
            field_type="StateIssueCustomField"
        )

    return task

def convert_issues_to_tasks(issues: list[Issue]) -> list[Task]:
    return [convert_issue_to_task(issue) for issue in issues]