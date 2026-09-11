from concurrent import futures

import grpc

from src.rpc import filerpc_pb2
from src.rpc import filerpc_pb2_grpc
from src.processing.hashing import calculate_sha256
from src.server.worker_manager import WorkerManager
from src.server.task_manager import TaskManager


class FileProcessor(filerpc_pb2_grpc.FileProcessorServicer):

    def HashFile(self, request, context):
        try:
            result = calculate_sha256(request.file_path)

            return filerpc_pb2.HashResponse(
                sha256=result
            )

        except Exception as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(str(e))
            return filerpc_pb2.HashResponse()


class WorkerCoordinator(
    filerpc_pb2_grpc.WorkerCoordinatorServicer
):

    def __init__(self):
        self.worker_manager = WorkerManager()
        self.task_manager = TaskManager()

        self.task_manager.add_task(
            "hash",
            "sample.txt",
        )

    def RegisterWorker(self, request, context):
        worker_id = self.worker_manager.register_worker(
            request.worker_id,
            request.address,
            request.capabilities,
        )

        return filerpc_pb2.RegisterWorkerResponse(
            success=True,
            worker_id=worker_id,
            message="Worker registered successfully",
        )

    def UpdateWorkerStatus(self, request, context):
        success = self.worker_manager.update_status(
            request.worker_id,
            request.status,
        )

        if success:
            return filerpc_pb2.UpdateWorkerStatusResponse(
                success=True,
                message="Worker status updated successfully",
            )

        return filerpc_pb2.UpdateWorkerStatusResponse(
            success=False,
            message="Worker not found",
        )

    def GetTask(self, request, context):
        task = self.task_manager.get_next_task()

        if task is None:
            return filerpc_pb2.GetTaskResponse(
                has_task=False
            )

        return filerpc_pb2.GetTaskResponse(
            has_task=True,
            task=filerpc_pb2.Task(
                task_id=task["task_id"],
                task_type=task["task_type"],
                file_path=task["file_path"],
            ),
        )

    def SubmitTaskResult(self, request, context):
        task = None

        for item in self.task_manager.get_tasks():
            if item["task_id"] == request.task_id:
                task = item
                break

        if task is None:
            return filerpc_pb2.SubmitTaskResultResponse(
                success=False,
                message="Task not found",
            )

        if request.success:
            task["status"] = "COMPLETED"
            task["result"] = request.result

            return filerpc_pb2.SubmitTaskResultResponse(
                success=True,
                message="Task result received successfully",
            )

        task["status"] = "FAILED"
        task["result"] = request.error_message

        return filerpc_pb2.SubmitTaskResultResponse(
            success=True,
            message="Task failure recorded",
        )


def serve():

    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10)
    )

    filerpc_pb2_grpc.add_FileProcessorServicer_to_server(
        FileProcessor(),
        server
    )

    filerpc_pb2_grpc.add_WorkerCoordinatorServicer_to_server(
        WorkerCoordinator(),
        server
    )

    server.add_insecure_port("[::]:50051")

    server.start()

    print("FileRPC server started on port 50051")

    server.wait_for_termination()


if __name__ == "__main__":
    serve()