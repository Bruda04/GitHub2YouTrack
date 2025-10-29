# This module provides functionality to detect changes between the current state of an issue
from src.model.issue import Issue

class ChangeDetector:
    @staticmethod
    def has_changes(current_issue: Issue, last_synced_state: dict) -> bool:
        if not last_synced_state:
            return True

        changes = (
                current_issue.title != last_synced_state.get('title') or
                current_issue.body != last_synced_state.get('body') or
                current_issue.state != last_synced_state.get('state') or
                set(current_issue.labels or []) != set(last_synced_state.get('labels', [])) or
                set(current_issue.assignees or []) != set(last_synced_state.get('assignees', []))
        )

        return changes

    @staticmethod
    def get_changes_summary(current_issue: Issue, last_synced_state: dict) -> list[str]:
        changes = []

        if current_issue.title != last_synced_state.get('title'):
            changes.append(f"Title: '{last_synced_state.get('title')}' -> '{current_issue.title}'")

        if current_issue.body != last_synced_state.get('body'):
            changes.append("Description updated")

        if current_issue.state != last_synced_state.get('state'):
            changes.append(f"State: '{last_synced_state.get('state')}' -> '{current_issue.state}'")

        old_labels = set(last_synced_state.get('labels', []))
        new_labels = set(current_issue.labels or [])
        if old_labels != new_labels:
            added = new_labels - old_labels
            removed = old_labels - new_labels
            if added:
                changes.append(f"Labels added: {', '.join(added)}")
            if removed:
                changes.append(f"Labels removed: {', '.join(removed)}")

        old_assignees = set(last_synced_state.get('assignees', []))
        new_assignees = set(current_issue.assignees or [])
        if old_assignees != new_assignees:
            added = new_assignees - old_assignees
            removed = old_assignees - new_assignees
            if added:
                changes.append(f"Assignees added: {', '.join(added)}")
            if removed:
                changes.append(f"Assignees removed: {', '.join(removed)}")

        return changes