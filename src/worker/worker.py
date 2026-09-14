import sys
import time
import threading

import grpc

from src.rpc import filerpc_pb2
from src.rpc import filerpc_pb2_grpc

from src.processing.hashing import calculate_sha256
from src.processing.pdf_extraction import extract_text_from_pdf
from src.processing.resizing import resize_image


class FileRPCWorker:

    def __init__(self, worker_id, server_address="localhost:50051"):
        self.worker_id = worker_id
        self.server_address = server_address

        self.address = "localhost"

        self.capabilities = [
            "hash",
            "resize",
            "extract",
        ]

        self.status = filerpc_pb2.WORKER_STATUS_IDLE

        self.channel = None
        self.stub = None

        self.running = False
        self.heartbeat_thread = None

    def connect(self):
        print(
            f"Connecting to FileRPC server at "
            f"{self.server_address}..."
        )

        self.channel = grpc.insecure_channel(
            self.server_address
        )

        self.stub = filerpc_pb2_grpc.WorkerCoordinatorStub(
            self.channel
        )

        print("Connected to FileRPC server.")

    def register(self):
        print(f"Registering worker: {self.worker_id}")

        request = filerpc_pb2.RegisterWorkerRequest(
            worker_id=self.worker_id,
            address=self.address,
            capabilities=self.capabilities,
        )

        response = self.stub.RegisterWorker(request)

        if response.success:
            self.worker_id = response.worker_id

            print("Worker registered successfully.")
            print(f"Worker ID: {self.worker_id}")
            print(f"Message: {response.message}")

            return True

        print("Worker registration failed.")
        print(f"Message: {response.message}")

        return False

    def send_heartbeat(self):
        try:
            request = filerpc_pb2.HeartbeatRequest(
                worker_id=self.worker_id,
                status=self.status,
            )

            response = self.stub.Heartbeat(request)

            if response.success:
                print(
                    f"[Heartbeat] {self.worker_id}: "
                    f"{response.message}"
                )
            else:
                print(
                    f"[Heartbeat] Failed: "
                    f"{response.message}"
                )

        except grpc.RpcError as e:
            print(
                f"[Heartbeat] Connection error: {e}"
            )

    def heartbeat_loop(self):
        while self.running:
            self.send_heartbeat()
            time.sleep(5)

    def start_heartbeat(self):
        self.running = True

        self.heartbeat_thread = threading.Thread(
            target=self.heartbeat_loop,
            daemon=True,
        )

        self.heartbeat_thread.start()

        print("Heartbeat started.")

    def get_task(self):
        request = filerpc_pb2.GetTaskRequest(
            worker_id=self.worker_id
        )

        response = self.stub.GetTask(request)

        if response.has_task:
            print("\nTask received:")
            print(f"Task ID: {response.task.task_id}")
            print(f"Task Type: {response.task.task_type}")
            print(f"File: {response.task.file_path}")

            return response.task

        print("\nNo task available.")

        return None
    
    def execute_task(self, task):
        print("\nExecuting task...")

        try:
            if task.task_type == "hash":
                result = calculate_sha256(
                    task.file_path
                )

                print("Hash task completed.")
                print(f"SHA-256: {result}")

                return True, result

            if task.task_type == "extract":
                result = extract_text_from_pdf(
                    task.file_path
                )

                print("PDF extraction completed.")
                print(
                    f"Extracted characters: {len(result)}"
                )

                return True, result

            if task.task_type == "resize":
                if not task.output_path:
                    raise ValueError(
                        "Output path is required for resize."
                    )

                if task.width <= 0 or task.height <= 0:
                    raise ValueError(
                        "Width and height must be positive."
                    )

                resize_image(
                    task.file_path,
                    task.output_path,
                    (task.width, task.height),
                )

                result = (
                    f"Image resized successfully: "
                    f"{task.output_path}"
                )

                print("Resize task completed.")
                print(f"Output: {task.output_path}")

                return True, result

            raise ValueError(
                f"Unsupported task type: {task.task_type}"
            )

        except Exception as e:
            print(f"Task failed: {e}")

            return False, str(e)
        
    def submit_task_result(self, task, success, result):
        request = filerpc_pb2.SubmitTaskResultRequest(
            worker_id=self.worker_id,
            task_id=task.task_id,
            success=success,
            result=result if success else "",
            error_message="" if success else result,
    )

        response = self.stub.SubmitTaskResult(request)

        if response.success:
            print(
                f"Result reported successfully: "
                f"{response.message}"
            )
        else:
            print(
                f"Result reporting failed: "
                f"{response.message}"
            )
        
    def stop(self):
        self.running = False

        if self.heartbeat_thread:
            self.heartbeat_thread.join(timeout=2)

        if self.channel:
            self.channel.close()

        print("Worker stopped.")

    def start(self):
        print("=" * 40)
        print("FileRPC Worker")
        print("=" * 40)

        self.connect()

        if not self.register():
            self.stop()
            return

        print(
            f"Capabilities: "
            f"{', '.join(self.capabilities)}"
        )

        print("Status: IDLE")
        print("Worker started successfully.")

        self.start_heartbeat()

        task = self.get_task()

        if task:
            success, result = self.execute_task(task)
            self.submit_task_result(
                task,
                success,
                result,
            )

        try:
            while True:
                time.sleep(1)

        except KeyboardInterrupt:
            print("\nStopping worker...")

        finally:
            self.stop()


def main():

    worker_id = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "worker-001"
    )

    worker = FileRPCWorker(worker_id)

    worker.start()


if __name__ == "__main__":
    main()