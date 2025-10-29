# This module provides a simple storage mechanism for maintaining mappings between GitHub issues and YouTrack tasks
import json
import os

class MappingStore:
    def __init__(self, storage_file: str = "github_youtrack_mapping.json"):
        self.storage_file = storage_file
        self.mappings = self._load_mappings()

    def _load_mappings(self) -> dict:
        if os.path.exists(self.storage_file):
            with open(self.storage_file, 'r') as f:
                return json.load(f)
        return {}

    def _save_mappings(self):
        with open(self.storage_file, 'w') as f:
            json.dump(self.mappings, f, indent=2)

    def add_mapping(self, github_issue_number: int, youtrack_task_id: str, github_issue_data: dict):
        self.mappings[str(github_issue_number)] = {
            "youtrack_id": youtrack_task_id,
            "last_synced_state": github_issue_data
        }
        self._save_mappings()

    def get_youtrack_id(self, github_issue_number: int) -> str:
        mapping = self.mappings.get(str(github_issue_number))
        return mapping["youtrack_id"] if mapping else None

    def get_last_synced_state(self, github_issue_number: int) -> dict:
        mapping = self.mappings.get(str(github_issue_number))
        return mapping["last_synced_state"] if mapping else None

    def update_synced_state(self, github_issue_number: int, github_issue_data: dict):
        if str(github_issue_number) in self.mappings:
            self.mappings[str(github_issue_number)]["last_synced_state"] = github_issue_data
            self._save_mappings()

    def get_all_mappings(self) -> dict:
        return self.mappings