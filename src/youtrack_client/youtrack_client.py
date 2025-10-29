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

        created_task=response.json()

        if task.tags and created_task['id']:
            self._add_tags_to_issue(created_task['id'], task.tags)

        return created_task


    def update_task(self, task_id: str, task: Task) -> dict:
        payload = {
            "summary": task.summary,
            "description": task.description,
            "customFields": task.get_custom_fields()
        }
        response = requests.post(f"{self.base_url}/issues/{task_id}", headers=self.headers, json=payload)
        response.raise_for_status()

        self._add_tags_to_issue(task_id, task.tags)

        return response.json()

    def create_tasks(self, tasks: list[Task]):
        for task in tasks:
            try:
                created_task = self.create_task(task)
                print(f"Created YouTrack task: {created_task['id']}")
            except requests.HTTPError as e:
                print(f"Failed to create task '{task.summary}': {e}")

    def _add_tags_to_issue(self, issue_id: str, tag_names: list[str]):
        current_tags = self._get_issue_tags(issue_id)
        current_tag_names = {tag["name"] for tag in current_tags}

        desired_tag_names = set(tag_names) if tag_names else set()
        tags_to_add = desired_tag_names - current_tag_names
        tags_to_remove = current_tag_names - desired_tag_names

        for tag in current_tags:
            if tag["name"] in tags_to_remove:
                self._remove_tag_from_issue(issue_id, tag["id"])

        if tags_to_add:
            existing_tags = self._get_existing_tags()

            for tag_name in tags_to_add:
                tag_data = existing_tags.get(tag_name)

                if not tag_data:
                    try:
                        created_tag = self._create_tag(tag_name)
                        tag_data = created_tag
                        existing_tags[tag_name] = tag_data
                    except Exception as e:
                        print(f"\tFailed to create tag '{tag_name}': {e}")
                        continue

                try:
                    response = requests.post(
                        f"{self.base_url}/issues/{issue_id}/tags",
                        headers=self.headers,
                        json=tag_data
                    )
                    response.raise_for_status()
                except Exception as e:
                    print(f"\tFailed to add tag '{tag_name}' to issue: {e}")

    def _get_issue_tags(self, issue_id: str) -> list[dict]:
        url = f"{self.base_url}/issues/{issue_id}/tags?fields=id,name"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"\tFailed to get tags for issue {issue_id}: {e}")
            return []

    def _remove_tag_from_issue(self, issue_id: str, tag_id: str):
        try:
            response = requests.delete(
                f"{self.base_url}/issues/{issue_id}/tags/{tag_id}",
                headers=self.headers
            )
            response.raise_for_status()
        except Exception as e:
            print(f"\tFailed to remove tag {tag_id} from issue: {e}")


    def _get_existing_tags(self) -> dict[str, dict]:
        url = f"{self.base_url}/issueTags?fields=id,name"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        tags = response.json()
        return {tag["name"]: {"id": tag["id"], "name": tag["name"]}
                for tag in tags if "name" in tag and "id" in tag}

    def _create_tag(self, tag_name: str) -> dict:
        payload = {"name": tag_name}
        response = requests.post(f"{self.base_url}/issueTags", headers=self.headers, json=payload)
        response.raise_for_status()
        created_tag = response.json()
        print(f"\tCreated missing tag: {tag_name}")
        return {"id": created_tag["id"], "name": tag_name}

    def delete_task(self, task_id: str):
        try:
            url = f"{self.base_url}/issues/{task_id}"
            response = requests.delete(url, headers=self.headers)
            response.raise_for_status()
        except Exception as e:
            print(f"\tFailed to delete task {task_id}: {e}")
