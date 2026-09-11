import uuid


class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, task_type, file_path):
        task = {
            "task_id": str(uuid.uuid4()),
            "task_type": task_type,
            "file_path": file_path,
            "status": "PENDING",
        }

        self.tasks.append(task)

        return task["task_id"]

    def get_next_task(self):
        for task in self.tasks:
            if task["status"] == "PENDING":
                task["status"] = "ASSIGNED"
                return task

        return None

    def get_tasks(self):
        return self.tasks