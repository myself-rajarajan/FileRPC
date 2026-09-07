from concurrent import futures

import grpc

from src.rpc import filerpc_pb2
from src.rpc import filerpc_pb2_grpc
from src.processing.hashing import calculate_sha256


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


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    filerpc_pb2_grpc.add_FileProcessorServicer_to_server(
        FileProcessor(),
        server
    )

    server.add_insecure_port("[::]:50051")

    server.start()

    print("FileRPC server started on port 50051")

    server.wait_for_termination()


if __name__ == "__main__":
    serve()