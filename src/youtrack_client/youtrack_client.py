# YouTrack Client to interact with YouTrack API for creating and updating tasks.
import requests
from src.model.task import Task

class YouTrackClient:
    def __init__(self, youtrack_url: str, youtrack_token: str, project_short_name: str):
        self.base_url = f"{youtrack_url}/api"
        self.headers = {
            "Authorization": f"Bearer {youtrack_token}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        self.project_short_name = project_short_name

    def create_task(self, task: Task) -> dict:
        payload = {
            "project": {"shortName": self.project_short_name},
            "summary": task.summary,
            "description": task.description,
            "customFields": task.get_custom_fields()
        }
        response = requests.post(f"{self.base_url}/issues", headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()


    def update_task(self, task_id: str, task: Task) -> dict:
        payload = {
            "summary": task.summary,
            "description": task.description,
            "customFields": task.get_custom_fields()
        }
        response = requests.post(f"{self.base_url}/issues/{task_id}", headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()

    def create_tasks(self, tasks):
        for task in tasks:
            try:
                created_task = self.create_task(task)
                print(f"Created YouTrack task: {created_task['id']}")
            except requests.HTTPError as e:
                print(f"Failed to create task '{task.summary}': {e}")