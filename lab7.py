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


class TaskView:
    def show_menu(self):
        print("\n1. Створити задачу\n"
              "2. Змінити статус\n"
              "3. Видалити задачу\n"
              "4. Змінити задачу\n"
              "5. Всі задачі\n"
              "6. Фільтр за статусом\n"
              "7. Задача за id\n"
              "0. Вихід")

    def show_tasks(self, tasks):
        print(f"{'id':<36} | {'description':<20} | {'created_at':<16} | {'schedule_for':<16} | status")
        for t in tasks:
            print(f"{str(t.id):<36} | {t.description:<20} | {t.created_at:{DATE_FORMAT}} | "
                  f"{t.schedule_for:{DATE_FORMAT}} | {t.status.value}")

    def show_message(self, message):
        print(message)

    def ask(self, prompt):
        return input(prompt)


class TaskController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def ask_id(self):
        return uuid.UUID(self.view.ask("id: "))

    def ask_date(self):
        return datetime.strptime(self.view.ask("Дата (РРРР-ММ-ДД ГГ:ХХ): "), DATE_FORMAT)

    def run(self):
        while True:
            self.view.show_menu()
            choice = self.view.ask("Ваш вибір: ")
            if choice == "0":
                break
            try:
                if choice == "1":
                    task = self.model.create(self.view.ask("Опис: "), self.ask_date())
                    self.view.show_message(f"Створено задачу {task.id}")
                elif choice == "2":
                    task_id = self.ask_id()
                    self.model.set_status(task_id, Status(self.view.ask("Статус (InProgress/Done): ")))
                elif choice == "3":
                    self.model.delete(self.ask_id())
                elif choice == "4":
                    task_id = self.ask_id()
                    self.model.update(task_id, self.view.ask("Новий опис: "), self.ask_date())
                elif choice == "5":
                    self.view.show_tasks(self.model.get_all())
                elif choice == "6":
                    status = Status(self.view.ask("Статус (ToDo/InProgress/Done): "))
                    self.view.show_tasks(self.model.filter_by_status(status))
                elif choice == "7":
                    self.view.show_tasks([self.model.get(self.ask_id())])
                else:
                    self.view.show_message("Невідома команда")
            except (ValueError, KeyError):
                self.view.show_message("Помилка: невірні дані або задачу не знайдено")


if __name__ == '__main__':
    TaskController(TaskModel(), TaskView()).run()
