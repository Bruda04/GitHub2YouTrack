from github_client.github_client import GitHubClient
import config.config as cfg
from youtrack_client.youtrack_client import YouTrackClient
from model.mapper import convert_issues_to_tasks

if __name__ == '__main__':
    github_client = GitHubClient(cfg.GITHUB_TOKEN, cfg.GITHUB_REPOSITORY_PATH)

    issues = github_client.get_repository_issues()

    tasks = convert_issues_to_tasks(issues)

    youtrack_client = YouTrackClient(cfg.YOUTRACK_URL, cfg.YOUTRACK_TOKEN, cfg.YOUTRACK_PROJECT_SHORT_NAME)

    youtrack_client.create_tasks(tasks)