# FileRPC

**FileRPC** is an open-source distributed file-processing platform built using **Python and gRPC**.

The goal of FileRPC is to allow clients to submit file-processing tasks to a central coordinator, which manages workers and distributes tasks for processing.

The system is designed around a client-server-worker architecture where file-processing operations such as hashing, PDF extraction, and image resizing can be executed by distributed worker nodes.

---

## Project Goals

FileRPC aims to provide:

* Distributed file processing
* RPC-based communication using gRPC
* Worker registration and management
* Task creation and assignment
* Worker capability management
* Task execution
* Task result submission
* Task status tracking
* Scalable worker architecture
* Support for multiple file-processing operations
* Reliable task and result management

---

## Architecture

The current architecture consists of three major components:

```text
                    +----------------+
                    |     Client     |
                    +-------+--------+
                            |
                            | gRPC
                            v
                    +----------------+
                    | FileRPC Server |
                    |  Coordinator   |
                    +-------+--------+
                            |
                 +----------+----------+
                 |                     |
                 v                     v
          Worker Management       Task Manager
                 |                     |
                 +----------+----------+
                            |
                            | Task Assignment
                            v
                    +----------------+
                    |     Worker     |
                    +-------+--------+
                            |
                            | Execute Task
                            v
                    +----------------+
                    | File Processing|
                    |     Engine     |
                    +-------+--------+
                            |
                            | Result
                            v
                    +----------------+
                    | FileRPC Server |
                    +----------------+
```

### Components

#### Client

The client communicates with the FileRPC server using gRPC.

The client will eventually be responsible for submitting file-processing tasks and retrieving task results.

#### FileRPC Server

The server acts as the central coordinator.

It manages:

* Worker registration
* Worker status
* Task management
* Task assignment
* Task results

#### Worker

Workers are processing nodes that:

1. Register with the server
2. Report their capabilities
3. Request available tasks
4. Execute tasks
5. Submit results back to the server

#### File Processing Engine

The processing engine contains the actual file-processing operations.

Current operations include:

* SHA-256 file hashing
* PDF text extraction
* Image resizing

---

## Technology Stack

| Technology       | Purpose                         |
| ---------------- | ------------------------------- |
| Python           | Main programming language       |
| gRPC             | RPC communication               |
| Protocol Buffers | Service and message definitions |
| pytest           | Testing                         |
| Git              | Version control                 |
| GitHub           | Source code hosting             |

---

## Project Structure

```text
FileRPC/
│
├── docs/
│   ├── ARCHITECTURE.md
│   ├── PROJECT.md
│   └── ROADMAP.md
│
├── proto/
│   └── filerpc.proto
│
├── src/
│   ├── client/
│   │   ├── __init__.py
│   │   └── client.py
│   │
│   ├── processing/
│   │   ├── __init__.py
│   │   ├── hashing.py
│   │   ├── pdf_extraction.py
│   │   └── resizing.py
│   │
│   ├── rpc/
│   │   ├── __init__.py
│   │   ├── filerpc_pb2.py
│   │   └── filerpc_pb2_grpc.py
│   │
│   ├── server/
│   │   ├── __init__.py
│   │   ├── server.py
│   │   ├── task_manager.py
│   │   └── worker_manager.py
│   │
│   └── worker/
│       ├── __init__.py
│       └── worker.py
│
├── tests/
│   ├── test_hashing.py
│   ├── test_pdf_extraction.py
│   ├── test_resizing.py
│   ├── test_task_manager.py
│   ├── test_worker_manager.py
│   └── test_server.py
│
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

---

## RPC Services

FileRPC currently defines two main RPC services.

### FileProcessor

The `FileProcessor` service handles file-processing operations.

Current RPC:

```text
HashFile
```

### WorkerCoordinator

The `WorkerCoordinator` service manages workers and tasks.

Current RPC methods:

```text
RegisterWorker
UpdateWorkerStatus
GetTask
SubmitTaskResult
```

---

## Current Processing Operations

### SHA-256 File Hashing

FileRPC can calculate the SHA-256 hash of a file using a buffered file-reading approach.

Example result:

```text
SHA-256:
9f8d47a33cdd02a542204b45196b0d83dceb32565077e0e692c0db634e04b2c0
```

### PDF Text Extraction

The processing engine supports extracting text from PDF files.

### Image Resizing

The processing engine supports resizing image files.

---

## Worker Lifecycle

A worker currently follows this workflow:

```text
Start Worker
     |
     v
Register Worker
     |
     v
Update Worker Status
     |
     v
Request Task
     |
     v
Receive Task
     |
     v
Execute Task
     |
     v
Submit Result
     |
     v
Task Completed
```

---

## Task Lifecycle

Tasks currently follow this lifecycle:

```text
PENDING
   |
   v
ASSIGNED
   |
   v
COMPLETED
```

If a task fails:

```text
PENDING
   |
   v
ASSIGNED
   |
   v
FAILED
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/myself-rajarajan/FileRPC.git
cd FileRPC
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Tests

Run the complete test suite:

```bash
python -m pytest -q
```

Current test result:

```text
23 passed, 9 subtests passed
```

---

## Running the Server

Start the FileRPC server:

```bash
python -m src.server.server
```

The server runs on:

```text
localhost:50051
```

---

## Running the Worker

In another terminal:

```bash
python -m src.worker.worker
```

The worker connects to the FileRPC server, registers itself, requests a task, executes the task, and submits the result.

---

## Development Roadmap

### Completed

* Project initialization
* File-processing engine
* SHA-256 hashing
* PDF extraction
* Image resizing
* gRPC infrastructure
* Protocol Buffer definitions
* FileProcessor RPC
* WorkerCoordinator RPC
* Worker registration
* Worker status management
* Task management
* Task assignment
* Worker task execution
* Task result submission
* Task completion tracking
* Unit and integration-level testing

### Planned

* Dynamic task submission API
* Improved worker status lifecycle
* Multiple worker support
* Worker capability-based task assignment
* Worker selection and load balancing
* Distributed file transfer
* Task IDs and job tracking
* Retry mechanism
* Failure handling
* CLI interface
* Integration testing
* Improved documentation
* Production deployment

---

# Project Progress Log

This section records the development progress of FileRPC. New progress will be added here as the project evolves.

## September 2026

### Phase 1 — Project Initialization

* [x] Created FileRPC project repository.
* [x] Created initial project structure.
* [x] Added project documentation.
* [x] Added `.gitignore`.
* [x] Added project license.

### Phase 2 — File Processing Engine

* [x] Implemented SHA-256 file hashing.
* [x] Added buffered file reading for hashing.
* [x] Implemented PDF text extraction.
* [x] Implemented image resizing.
* [x] Added unit tests for processing components.

### Phase 3 — RPC Infrastructure

* [x] Installed `grpcio`.
* [x] Installed `grpcio-tools`.
* [x] Created `proto/filerpc.proto`.
* [x] Generated Python gRPC files.
* [x] Implemented `FileProcessor` service.
* [x] Implemented `HashFile` RPC.
* [x] Created the FileRPC server.
* [x] Created the FileRPC client.
* [x] Verified RPC-based SHA-256 hashing.

### Phase 4 — Worker Management

* [x] Implemented `WorkerManager`.
* [x] Added worker registration.
* [x] Added worker IDs.
* [x] Added worker addresses.
* [x] Added worker capabilities.
* [x] Added worker status management.
* [x] Added worker manager tests.

### Phase 5 — Task Management

* [x] Implemented `TaskManager`.
* [x] Added task creation.
* [x] Added task IDs.
* [x] Added task queue.
* [x] Added task assignment.
* [x] Added task lookup by task ID.
* [x] Added task manager tests.

### Phase 6 — Worker Coordination

* [x] Implemented `WorkerCoordinator`.
* [x] Implemented worker registration through RPC.
* [x] Implemented worker status updates through RPC.
* [x] Implemented task requesting through RPC.
* [x] Implemented worker-side task execution.
* [x] Verified SHA-256 task execution by the worker.

### Phase 7 — Task Result Submission

* [x] Added `SubmitTaskResult` RPC.
* [x] Implemented successful result submission.
* [x] Implemented failed task result reporting.
* [x] Updated task status to `COMPLETED`.
* [x] Stored task results.
* [x] Added server tests for result submission.
* [x] Verified the complete worker-to-server result flow.

### Current Test Status

```text
23 passed, 9 subtests passed
```

### Current Working Flow

```text
Worker Registration
        |
        v
Worker Status Update
        |
        v
Request Task
        |
        v
Receive Task
        |
        v
Execute SHA-256
        |
        v
Submit Task Result
        |
        v
Server Stores Result
        |
        v
Task Status = COMPLETED
```

### Current Development Status

**Core RPC communication, worker management, task management, task execution, and task result submission are implemented and tested.**

**Next development milestone:** Replace the temporary hard-coded task with a proper task submission API that allows clients to dynamically create file-processing tasks.
