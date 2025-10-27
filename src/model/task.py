class Task:
    def __init__(self, task_id: int, summary: str, description: str = ''):
        self.task_id = task_id
        self.summary = summary
        self.description = description
        self.custom_fields = []


    def add_custom_field(self, field_name: str, field_value: str):
        self.custom_fields.append({"name": field_name, "value": {"name": field_value}})


    def get_custom_fields(self) -> list:
        return self.custom_fields

    def __str__(self):
        return f"Task #{self.task_id}: {self.description} - Completed: {self.completed}"