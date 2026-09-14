# FileRPC

**FileRPC** is an open-source distributed desktop file-processing platform built using **Python and gRPC**.

The goal of FileRPC is to allow users to submit file-processing tasks to a central coordinator via a native desktop application, which manages workers and distributes tasks for processing.

The system is designed around a **Desktop Application -> Coordinator -> Workers** architecture, where file-processing operations such as hashing, PDF extraction, and image resizing are executed by distributed worker nodes. FileRPC is a native desktop application, NOT a web application, and does not use browsers, HTML, CSS, JavaScript, or REST APIs.

---

## Problem Statement

Single-machine file processing is heavily constrained by local hardware limitations (such as CPU, memory, and disk I/O bottlenecks). When dealing with large volumes of files or computationally heavy tasks (e.g., batch image resizing or deep text parsing), a single machine can slow down drastically, freezing the user interface and preventing other work.

Traditional solutions are typically:
1. **Web-based platforms** that require complex deployments, internet connections, and uploading sensitive local files to remote third-party servers.
2. **Command-line tools** that are difficult for non-technical users to configure, manage, and monitor.

FileRPC provides a local, privacy-focused native desktop application that can orchestrate and distribute these tasks without requiring a web browser or cloud uploads, keeping all data private and processing highly scalable.

---

## What FileRPC Does

FileRPC provides a distributed pipeline for computationally heavy file operations:
* **User-Friendly Execution:** Normal users operate a clean, native desktop application directly on their operating system without touching the command line.
* **Centralized Orchestration:** A Coordinator receives requests, schedules tasks, tracks worker availability, and logs results in-memory.
* **Scalable Workload Processing:** Multiple remote or local Workers request pending tasks, execute them in parallel, and return results.
* **Robust File Operations:** Integrated processing engines perform cryptographically secure SHA-256 hashing, high-performance image resizing, and character-level PDF extraction.

---

## Architecture

The main architecture consists of three major components:

```text
                     FileRPC Desktop Software
                              |
                              v
                    +-------------------+
                    | Desktop           |
                    | Application       |
                    | PySide6 / Qt      |
                    +---------+---------+
                              |
                              v
                    +-------------------+
                    | Coordinator       |
                    |                   |
                    | Task Manager      |
                    | Worker Manager    |
                    | Task Scheduler    |
                    | gRPC Server       |
                    +---------+---------+
                              |
                             gRPC
                              |
                +-------------+-------------+
                |             |             |
                v             v             v
           +---------+   +---------+   +---------+
           | Worker 1|   | Worker 2|   | Worker N|
           +----+----+   +----+----+   +----+----+
                |             |             |
                +-------------+-------------+
                              |
                     Processing Engines
                              |
                +-------------+-------------+
                |             |             |
              Hash          Resize        Extract
```

### Component Breakdown

#### Desktop Application (PySide6 / Qt)
The user-facing native desktop application. It eventually provides the GUI for local file selection, task configuration, real-time progress monitoring, and final output viewing. It runs natively directly on the host operating system.
*Note: Currently, a lightweight command-line client (`src/client/client.py`) is used for developer verification while the PySide6 UI is planned.*

#### Coordinator
The central internal system coordinator. It manages the task queue, registered worker status/heartbeats, and scheduling logic over a central gRPC server.

#### Workers
Standalone execution nodes that register dynamically over gRPC, periodically report active health via heartbeats, request tasks from the Coordinator, execute them, and report results back.

#### Processing Engines
Optimized Python engines for local execution:
* **SHA-256 Hashing:** Safe, chunk-based buffered file hashing.
* **Image Resizing:** Aspect-ratio-preserving resizing.
* **PDF Text Extraction:** Parsing text characters from PDF documents.

---

## Docker Integration (Planned Deployment)

To facilitate developer environment setup, multi-worker simulation, and isolated distributed deployments, **Docker** containerization is integrated into the project roadmap as a future planned capability. 

Under the planned containerized setup, the user-facing PySide6 Desktop Application continues to run natively on the host machine, while the Coordinator and a scalable pool of Workers run inside isolated Docker containers on the same or multiple machines:

```text
Host Operating System
│
├── FileRPC Desktop Application (PySide6 / Qt)
│
└── Docker Environment
        │
        ├── Coordinator Container
        │
        ├── Worker Container 1
        ├── Worker Container 2
        └── Worker Container N
```

### Docker Compose Orchestration (Planned)
In Phase 6, developers will eventually be able to spin up a fully isolated multi-worker cluster with a single command. The following is an example of the planned future deployment model:
```text
docker compose up --scale worker=5
```
This is a planned deployment capability and **is not yet implemented**. No Dockerfiles or docker-compose.yml files currently exist, and the command does not yet work. Normal users will always be able to run FileRPC natively without Docker.

---

## Technology Stack

| Technology       | Purpose                              |
| ---------------- | ------------------------------------ |
| Python           | Main programming language            |
| PySide6 / Qt     | Native Desktop GUI (Planned)         |
| gRPC             | High-performance RPC communication    |
| Protocol Buffers | Service and message definitions      |
| Docker           | Containerization & Scaling (Planned) |
| Docker Compose   | Multi-worker Orchestration (Planned) |
| Pillow           | Image processing library             |
| pypdf            | PDF processing engine               |
| pytest           | Testing framework                    |
| Git              | Version control                      |

---

## Project Structure

This represents the actual current repository structure. No Dockerfiles or docker-compose configurations are created yet.

```text
FileRPC/
├── proto/
│   └── filerpc.proto
├── src/
│   ├── client/
│   │   ├── __init__.py
│   │   └── client.py
│   ├── processing/
│   │   ├── hashing.py
│   │   ├── pdf_extraction.py
│   │   └── resizing.py
│   ├── rpc/
│   │   ├── __init__.py
│   │   ├── filerpc_pb2.py
│   │   └── filerpc_pb2_grpc.py
│   ├── server/
│   │   ├── __init__.py
│   │   ├── server.py
│   │   ├── task_manager.py
│   │   └── worker_manager.py
│   └── worker/
│       ├── __init__.py
│       └── worker.py
├── tests/
│   ├── test_hashing.py
│   ├── test_pdf_extraction.py
│   ├── test_resizing.py
│   ├── test_server.py
│   ├── test_task_manager.py
│   └── test_worker_manager.py
├── requirements.txt
├── README.md
├── LICENSE
├── docs/
│   ├── ARCHITECTURE.md
│   ├── PROJECT.md
│   └── ROADMAP.md
└── .gitignore
```
*(Planned future files include `Dockerfile` and `docker-compose.yml` which will be added in Phase 6).*

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

---

## Running the Server (Coordinator)

Start the FileRPC Coordinator server:

```bash
python -m src.server.server
```

The Coordinator runs on:
```text
localhost:50051
```

---

## Running the Worker

In another terminal, start the worker:

```bash
python -m src.worker.worker
```

The worker connects to the Coordinator, registers itself, requests tasks from the Coordinator, and reports results.

---

## Development Roadmap

### Completed Phases
* **Phase 1 — Project Foundation:** Setup project workspace, folder structures, dependencies, git, and specifications.
* **Phase 2 — Processing Engines:** Implemented hashing, resizing, and PDF extraction libraries alongside complete unit tests.
* **Phase 3 — RPC Communication:** Defined and generated gRPC Protocol Buffer stubs, implementing central server connections and client calls.
* **Phase 4 — Worker System:** Implemented remote worker registration, heartbeat tracking, dynamic task requests, and task results submission. Successfully tested Hash, Resize, and PDF extraction tasks end-to-end.

### Planned Phases
* **Phase 5 — Task Management & Reliability (Next Milestone):** Detailed task status tracking, persistent storage, failures, retries, multiple worker handling, capability/load-aware scheduling.
* **Phase 6 — Docker & Distributed Deployment:** Drafting `Dockerfile` for Coordinator and Worker, designing `docker-compose.yml` for multi-worker scaling, network setup, and environment config.
* **Phase 7 — Desktop Application:** Developing the native PySide6/Qt desktop dashboard and UI configuration.
* **Phase 8 — Testing & Reliability:** Stress testing, failure testing, multi-worker containerized simulation, GUI testing.
* **Phase 9 — Packaging & Release:** Building standalone Windows executables with PyInstaller, configurations, and GitHub release tags.

---

# Current Project Progress

This section records the exact current development progress of FileRPC.

## Current Project Status

- **Phase 1 — Project Foundation:** **COMPLETED**
- **Phase 2 — Processing Engines:** **COMPLETED**
- **Phase 3 — RPC Communication:** **COMPLETED**
- **Phase 4 — Worker System:** **COMPLETED**
- **Phase 5 — Task Management & Reliability:** **NEXT** (Immediate Next Phase)
- **Phase 6 — Docker & Distributed Deployment:** **PLANNED** (Not Started)
- **Phase 7 — Desktop Application:** **PLANNED** (Not Started)
- **Phase 8 — Testing & Reliability:** **PLANNED** (Not Started)
- **Phase 9 — Packaging & Release:** **PLANNED** (Not Started)

*Note: Docker integration and PySide6 Desktop GUI are planned capabilities, and no Dockerfiles, Docker Compose configurations, or GUI code have been created yet.*

### Key Achievements in Phase 4
Phase 4 successfully implemented and verified the basic Worker System.
* Tested with **Hash Tasks**, **Resize Tasks**, and **PDF Extraction Tasks**.
* Validated `SubmitTaskResult` RPC call.
* The task result is successfully reported to the Coordinator and updated in-memory to `COMPLETED`. Full persistent task and result storage is not yet implemented and is planned for Phase 5.
* Multiple-worker management, retries, failure recovery, capability scheduling, and load-aware scheduling remain Phase 5 work.
* Latest successful PDF extraction test:
  * **Task Type:** extract
  * **File:** input.pdf
  * **Extracted Characters:** 3,393
  * **Result State:** Reported successfully to the Coordinator.

### Current Test Status
All tests are running and passing successfully.

### Current Working Flow
```text
Worker Registration
        |
        v
Worker Status Update (Heartbeat)
        |
        v
Request Task
        |
        v
Receive Task (Hash, Resize, Extract)
        |
        v
Execute Processing Engine
        |
        v
Submit Task Result (SubmitTaskResult)
        |
        v
Coordinator Receives Result (Status -> COMPLETED In-Memory)
```
