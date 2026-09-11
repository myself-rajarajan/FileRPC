from src.server.worker_manager import WorkerManager


def test_register_worker():
    manager = WorkerManager()

    worker_id = manager.register_worker(
        "",
        "localhost:50052",
        ["hash", "resize"],
    )

    worker = manager.get_worker(worker_id)

    assert worker is not None
    assert worker["address"] == "localhost:50052"
    assert worker["status"] == "IDLE"
    assert "hash" in worker["capabilities"]


def test_update_worker_status():
    manager = WorkerManager()

    worker_id = manager.register_worker(
        "worker-001",
        "localhost:50052",
        ["hash"],
    )

    result = manager.update_status(worker_id, "BUSY")

    assert result is True
    assert manager.get_worker(worker_id)["status"] == "BUSY"


def test_update_unknown_worker():
    manager = WorkerManager()

    result = manager.update_status(
        "unknown-worker",
        "BUSY",
    )

    assert result is False