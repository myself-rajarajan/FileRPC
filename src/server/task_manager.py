import uuid


class TaskManager:

    def __init__(self):
        self.tasks = []

    def add_task(
        self,
        task_type,
        file_path,
        output_path=None,
        width=None,
        height=None,
    ):
        task = {
            "task_id": str(uuid.uuid4()),
            "task_type": task_type,
            "file_path": file_path,
            "output_path": output_path,
            "width": width,
            "height": height,
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

    def get_task(self, task_id):
        for task in self.tasks:
            if task["task_id"] == task_id:
                return task

        return None

    def get_tasks(self):
        return self.tasks

