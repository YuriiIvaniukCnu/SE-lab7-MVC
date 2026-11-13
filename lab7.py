import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

DATE_FORMAT = "%Y-%m-%d %H:%M"


class Status(Enum):
    TODO = "ToDo"
    IN_PROGRESS = "InProgress"
    DONE = "Done"


@dataclass
class Task:
    description: str
    schedule_for: datetime
    status: Status = Status.TODO
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime = field(default_factory=datetime.now)


class TaskModel:
    def __init__(self):
        self.tasks = {}

    def create(self, description, schedule_for):
        task = Task(description, schedule_for)
        self.tasks[task.id] = task
        return task

    def get(self, task_id):
        return self.tasks[task_id]

    def get_all(self):
        return list(self.tasks.values())

    def filter_by_status(self, status):
        return [t for t in self.tasks.values() if t.status == status]

    def update(self, task_id, description, schedule_for):
        task = self.tasks[task_id]
        task.description = description
        task.schedule_for = schedule_for

    def set_status(self, task_id, status):
        if status == Status.TODO:
            raise ValueError("Статус можна змінити тільки на InProgress або Done")
        self.tasks[task_id].status = status

    def delete(self, task_id):
        del self.tasks[task_id]
