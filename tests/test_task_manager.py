from src.server.task_manager import TaskManager


def test_add_task():
    manager = TaskManager()

    task_id = manager.add_task(
        "hash",
        "sample.txt",
    )

    assert task_id is not None
    assert len(manager.get_tasks()) == 1


def test_get_next_task():
    manager = TaskManager()

    manager.add_task(
        "hash",
        "sample.txt",
    )

    task = manager.get_next_task()

    assert task is not None
    assert task["task_type"] == "hash"
    assert task["file_path"] == "sample.txt"
    assert task["status"] == "ASSIGNED"


def test_no_task_available():
    manager = TaskManager()

    task = manager.get_next_task()

    assert task is None