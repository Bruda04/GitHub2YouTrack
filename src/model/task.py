# Task model representing a task in YouTrack

class Task:
    def __init__(self,
                 task_id: int,
                 summary: str,
                 description: str = '',
                 ):
        self.task_id = task_id
        self.summary = summary
        self.description = description
        self.custom_fields = []

    def add_custom_field(self, field_name: str, field_value, field_type: str = None):
        field_entry = {
            "name": field_name,
            "value": field_value
        }

        if field_type:
            field_entry["$type"] = field_type

        self.custom_fields.append(field_entry)


    def get_custom_fields(self) -> list:
        return self.custom_fields

    def __str__(self):
        return f"Task #{self.task_id}: {self.summary}"