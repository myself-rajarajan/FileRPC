import grpc

from src.rpc import filerpc_pb2
from src.rpc import filerpc_pb2_grpc


def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = filerpc_pb2_grpc.FileProcessorStub(channel)

        response = stub.HashFile(
            filerpc_pb2.HashRequest(
                file_path="sample.txt"
            )
        )

        print("SHA-256:", response.sha256)


if __name__ == "__main__":
    run()