import time
import schedule
from threading import Thread
from src.model.issue import Issue


class SyncScheduler:
    def __init__(self, sync_service, github_client, interval_minutes: int = 10):
        self.sync_service = sync_service
        self.github_client = github_client
        self.interval_minutes = interval_minutes
        self._scheduler_thread = None

    def _run_sync_job(self):
        print("\n\tScheduled sync triggered...")
        try:
            issues: list[Issue] = self.github_client.get_repository_issues()
            self.sync_service.sync_issues(issues)
            print("\tScheduled sync finished\n")
        except Exception as e:
            print(f"\tScheduled sync failed: {e}\n")

    def start(self):
        print(f"\tStarting scheduled sync every {self.interval_minutes} minutes")

        schedule.every(self.interval_minutes).minutes.do(self._run_sync_job)

        def _scheduler_loop():
            while True:
                schedule.run_pending()
                time.sleep(1)

        self._scheduler_thread = Thread(target=_scheduler_loop, daemon=True)
        self._scheduler_thread.start()
        print("\tScheduler thread started")

    def stop(self):
        print("\tScheduler stopped (thread will end when main process exits).")
        self._scheduler_thread = None
