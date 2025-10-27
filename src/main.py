from github_client.github_client import GitHubClient
import config.config as cfg

if __name__ == '__main__':
    print(cfg.GITHUB_REPOSITORY_NAME)
    github_client = GitHubClient(cfg.GITHUB_TOKEN, cfg.GITHUB_REPOSITORY_PATH)
    repositories = github_client.get_repository_issues()
    for repo_issue in repositories:
        print(repo_issue)