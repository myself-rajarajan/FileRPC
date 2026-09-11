import grpc

from src.rpc import filerpc_pb2
from src.rpc import filerpc_pb2_grpc
from src.processing.hashing import calculate_sha256


SERVER_ADDRESS = "localhost:50051"


def start_worker():

    worker_id = "worker-001"

    with grpc.insecure_channel(SERVER_ADDRESS) as channel:

        stub = filerpc_pb2_grpc.WorkerCoordinatorStub(channel)

        # Register worker
        response = stub.RegisterWorker(
            filerpc_pb2.RegisterWorkerRequest(
                worker_id=worker_id,
                address="localhost:50052",
                capabilities=[
                    "hash",
                    "resize",
                    "extract",
                ],
            )
        )

        registered_worker_id = response.worker_id

        print("Registration:")
        print("Success:", response.success)
        print("Worker ID:", response.worker_id)
        print("Message:", response.message)

        # Update worker status
        status_response = stub.UpdateWorkerStatus(
            filerpc_pb2.UpdateWorkerStatusRequest(
                worker_id=registered_worker_id,
                status=filerpc_pb2.WORKER_STATUS_IDLE,
            )
        )

        print("\nStatus update:")
        print("Success:", status_response.success)
        print("Message:", status_response.message)

        # Request task
        task_response = stub.GetTask(
            filerpc_pb2.GetTaskRequest(
                worker_id=registered_worker_id
            )
        )

        print("\nTask:")
        print("Has task:", task_response.has_task)

        if task_response.has_task:

            task = task_response.task

            print("Task ID:", task.task_id)
            print("Task type:", task.task_type)
            print("File path:", task.file_path)

            # Execute task
            if task.task_type == "hash":

                try:
                    result = calculate_sha256(task.file_path)

                    print("\nTask Result:")
                    print("SHA-256:", result)

                    # Submit result to server
                    result_response = stub.SubmitTaskResult(
                        filerpc_pb2.SubmitTaskResultRequest(
                            worker_id=registered_worker_id,
                            task_id=task.task_id,
                            success=True,
                            result=result,
                        )
                    )

                    print("\nResult Submission:")
                    print("Success:", result_response.success)
                    print("Message:", result_response.message)

                except Exception as e:

                    result_response = stub.SubmitTaskResult(
                        filerpc_pb2.SubmitTaskResultRequest(
                            worker_id=registered_worker_id,
                            task_id=task.task_id,
                            success=False,
                            error_message=str(e),
                        )
                    )

                    print("\nResult Submission:")
                    print("Success:", result_response.success)
                    print("Message:", result_response.message)

        else:
            print("No task available.")


if __name__ == "__main__":
    start_worker()