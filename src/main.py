# Main entry point for the GitHub to YouTrack synchronization application
import time
from src.github_client.github_client import GitHubClient
from src.sync_service.change_detection import ChangeDetector
from src.sync_service.sync_scheduler import SyncScheduler
from src.youtrack_client.youtrack_client import YouTrackClient
from src.storage.mapping_store import MappingStore
from src.sync_service.sync_service import SyncService
from src.config import config as cfg

def main():
    print("\tStarting GitHub -> YouTrack")

    print("Initializing clients...")
    github_client = GitHubClient(cfg.GITHUB_TOKEN, cfg.GITHUB_REPOSITORY_PATH)
    youtrack_client = YouTrackClient(cfg.YOUTRACK_URL, cfg.YOUTRACK_TOKEN, cfg.YOUTRACK_PROJECT_SHORT_NAME)
    mapping_store = MappingStore()
    change_detector = ChangeDetector()
    sync_service = SyncService(youtrack_client, mapping_store, change_detector)

    print("\nFetching GitHub issues...")
    github_issues = github_client.get_repository_issues()
    print(f"Found {len(github_issues)} issues in GitHub.\n")

    if github_issues:
        sync_service.sync_issues(github_issues)
    else:
        print("No issues to sync - repository is empty or token permissions missing.")

    print("\nStarting scheduler...")
    scheduler = SyncScheduler(sync_service, github_client, cfg.SYNC_INTERVAL_MINUTES)
    scheduler.start()


    while True:
        time.sleep(60)

if __name__ == "__main__":
    main()
