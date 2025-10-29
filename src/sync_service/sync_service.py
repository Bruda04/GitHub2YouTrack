# Service to synchronize GitHub issues with YouTrack tasks
from src.model.issue import Issue
from src.storage.mapping_store import MappingStore
from .change_detection import ChangeDetector
from src.model.mapper import convert_issue_to_task, convert_issue_to_dict
from src.youtrack_client.youtrack_client import YouTrackClient


class SyncService:
    def __init__(self, youtrack_client: YouTrackClient, mapping_store: MappingStore, change_detector: ChangeDetector):
        self.youtrack_client = youtrack_client
        self.mapping_store = mapping_store
        self.change_detector = change_detector

    def sync_issues(self, github_issues: list[Issue]):
        print(f"\n=== Starting sync of {len(github_issues)} GitHub issues ===\n")

        created_count = 0
        updated_count = 0
        skipped_count = 0

        for issue in github_issues:
            youtrack_id = self.mapping_store.get_youtrack_id(issue.number)
            last_synced_state = self.mapping_store.get_last_synced_state(issue.number)

            if youtrack_id:
                if self.change_detector.has_changes(issue, last_synced_state):
                    changes = self.change_detector.get_changes_summary(issue, last_synced_state)
                    print(f"\tUpdating issue: {issue.title}")
                    print(f"\tChanges: {', '.join(changes)}")

                    self._update_existing_task(issue, youtrack_id)
                    updated_count += 1
                else:
                    print(f"\tSkipping issue: {issue.title} (no changes)")
                    skipped_count += 1
            else:
                print(f"Creating new issue: {issue.title}")
                self._create_new_task(issue)
                created_count += 1

        print(f"\n=== Sync completed ===")
        print(f"Created: {created_count}, Updated: {updated_count}, Skipped: {skipped_count}")

    def sync_issue(self, issue: Issue):
        self.sync_issues([issue])

    def _create_new_task(self, issue: Issue):
        try:
            task = convert_issue_to_task(issue)
            created_task = self.youtrack_client.create_task(task)

            issue_dict = convert_issue_to_dict(issue)
            self.mapping_store.add_mapping(issue.number, created_task['id'], issue_dict)

            print(f"\tCreated YouTrack task: {created_task['id']}")
        except Exception as e:
            print(f"\tFailed to create task: {e}")

    def _update_existing_task(self, issue: Issue, youtrack_id: str):
        try:
            task = convert_issue_to_task(issue)
            self.youtrack_client.update_task(youtrack_id, task)

            issue_dict = convert_issue_to_dict(issue)
            self.mapping_store.update_synced_state(issue.number, issue_dict)

            print(f"   Updated YouTrack task: {youtrack_id}")
        except Exception as e:
            print(f"\tFailed to update task: {e}")
