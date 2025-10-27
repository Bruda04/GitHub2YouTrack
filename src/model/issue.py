class Issue:
    def __init__(self, number: int, title: str, url: str, status: str, description: str = ""):
        self.id = number
        self.number = number
        self.title = title
        self.url = url
        self.status = status
        self.description = description

    def __str__(self):
        return f"Issue #{self.number}: {self.title} - {self.url}"