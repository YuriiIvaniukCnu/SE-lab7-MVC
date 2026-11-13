import unittest
from datetime import datetime
from unittest.mock import patch

from lab7 import Status, TaskModel, TaskView, TaskController

DATE = datetime(2026, 12, 1, 10, 0)


class TestTaskModel(unittest.TestCase):
    def setUp(self):
        self.model = TaskModel()
        self.task = self.model.create("Купити хліб", DATE)

    def test_create(self):
        self.assertEqual(self.task.status, Status.TODO)
        self.assertEqual(self.task.schedule_for, DATE)
        self.assertEqual(self.model.get_all(), [self.task])
    def test_get(self):
        self.assertEqual(self.model.get(self.task.id), self.task)
    def test_get_missing(self):
        with self.assertRaises(KeyError):
            self.model.get("abc")
    def test_update(self):
        self.model.update(self.task.id, "Купити молоко", datetime(2027, 1, 1))
        self.assertEqual(self.task.description, "Купити молоко")
        self.assertEqual(self.task.schedule_for, datetime(2027, 1, 1))
    def test_set_status(self):
        self.model.set_status(self.task.id, Status.DONE)
        self.assertEqual(self.task.status, Status.DONE)
    def test_set_status_todo(self):
        with self.assertRaises(ValueError):
            self.model.set_status(self.task.id, Status.TODO)
    def test_filter(self):
        other = self.model.create("Прибрати", DATE)
        self.model.set_status(other.id, Status.IN_PROGRESS)
        self.assertEqual(self.model.filter_by_status(Status.IN_PROGRESS), [other])
        self.assertEqual(self.model.filter_by_status(Status.TODO), [self.task])
    def test_delete(self):
        self.model.delete(self.task.id)
        self.assertEqual(self.model.get_all(), [])


@patch("builtins.print")
class TestTaskController(unittest.TestCase):
    def setUp(self):
        self.model = TaskModel()
        self.controller = TaskController(self.model, TaskView())

    def run_with(self, *inputs):
        with patch("builtins.input", side_effect=[*inputs, "0"]):
            self.controller.run()

    def test_create(self, _):
        self.run_with("1", "Купити хліб", "2026-12-01 10:00")
        task = self.model.get_all()[0]
        self.assertEqual(task.description, "Купити хліб")
        self.assertEqual(task.schedule_for, DATE)
    def test_wrong_date(self, mock_print):
        self.run_with("1", "Купити хліб", "завтра")
        self.assertEqual(self.model.get_all(), [])
        mock_print.assert_any_call("Помилка: невірні дані або задачу не знайдено")
    def test_status(self, _):
        task = self.model.create("Купити хліб", DATE)
        self.run_with("2", str(task.id), "InProgress")
        self.assertEqual(task.status, Status.IN_PROGRESS)
    def test_delete(self, _):
        task = self.model.create("Купити хліб", DATE)
        self.run_with("3", str(task.id))
        self.assertEqual(self.model.get_all(), [])
    def test_update(self, _):
        task = self.model.create("Купити хліб", DATE)
        self.run_with("4", str(task.id), "Купити молоко", "2027-01-01 09:00")
        self.assertEqual(task.description, "Купити молоко")
    def test_show(self, mock_print):
        task = self.model.create("Купити хліб", DATE)
        self.run_with("5", "6", "ToDo", "7", str(task.id))
        printed = " ".join(str(call) for call in mock_print.call_args_list)
        self.assertEqual(printed.count("Купити хліб"), 3)
    def test_wrong_id(self, mock_print):
        self.run_with("7", "123")
        mock_print.assert_any_call("Помилка: невірні дані або задачу не знайдено")
    def test_unknown_command(self, mock_print):
        self.run_with("9")
        mock_print.assert_any_call("Невідома команда")


if __name__ == '__main__':
    unittest.main()
