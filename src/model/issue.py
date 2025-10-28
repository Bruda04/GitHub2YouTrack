class Issue:
    def __init__(self,
                 number: int,
                 title: str,
                 url: str,
                 state: str,
                 body: str = "",
                 assignees: list[str] = None,
                 labels: list[str] = None,
                 user: str = ""):
        self.id = number
        self.number = number
        self.title = title
        self.url = url
        self.state = state
        self.body = body
        self.assignees = assignees
        self.labels = labels
        self.user = user

    def __str__(self):
        return f"Issue #{self.number}: {self.title} - {self.url}"