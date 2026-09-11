import uuid


class WorkerManager:
    def __init__(self):
        self.workers = {}

    def register_worker(self, worker_id, address, capabilities):
        if not worker_id:
            worker_id = str(uuid.uuid4())

        self.workers[worker_id] = {
            "worker_id": worker_id,
            "address": address,
            "status": "IDLE",
            "capabilities": list(capabilities),
        }

        return worker_id

    def update_status(self, worker_id, status):
        if worker_id not in self.workers:
            return False

        self.workers[worker_id]["status"] = status
        return True

    def get_worker(self, worker_id):
        return self.workers.get(worker_id)

    def get_workers(self):
        return self.workers