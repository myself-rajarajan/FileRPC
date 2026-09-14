# System Architecture: FileRPC

## High-Level Architecture Overview

**FileRPC** is a distributed desktop software and file-processing system designed for robust, local-first file processing. The architecture is explicitly non-web and does not use any browser-based frameworks, HTML/CSS, REST APIs, or frontend-backend web servers. 

Instead, the system follows a clear, topology: **Desktop Application -> Coordinator -> Workers**.

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

To support seamless distributed scaling, environment isolation, and multi-worker testing, FileRPC includes a planned containerized model. When deployed in this manner, the Coordinator and Workers run within a **Docker Environment**, while the user-facing Desktop Application remains a native host OS component.

```text
                 Host Machine
                      |
          +-----------+-----------+
          |                       |
          v                       v
   Desktop Application      Docker Environment
      PySide6 / Qt                 |
                                   |
                     +-------------+-------------+
                     |                           |
                     v                           v
              Coordinator                  Worker Containers
              Container              +------+-----+------+
                                     |      |     |      |
                                   W1     W2    W3    WN
```

---

## Core System Components

### 1. Desktop Application (PySide6 / Qt)
The **Desktop Application** is the user-facing native graphical interface (GUI). It runs natively directly on the host operating system (not inside a Docker container) to guarantee proper access to local filesystem dialogues and standard desktop window controls.
* **Responsibilities:**
  * Displays a dashboard showing overall system status, active tasks, and connected workers.
  * Allows users to select files from their local filesystem.
  * Provides task configuration options (e.g., target dimensions for resizing).
  * Submits tasks directly to the **Coordinator** over gRPC.
  * Renders progress indicators, completion states, and processed results directly without command-line input.
* **Technology:** PySide6 / Qt (Planned, Phase 7). Currently, a command-line client (`src/client/client.py`) is used for development verification.

### 2. Coordinator
The **Coordinator** is an internal system component responsible for orchestration, scheduling, and health monitoring. It runs a high-performance gRPC server to manage workers and tasks.
* **Responsibilities:**
  * **Worker Manager:** Handles worker registration, tracks worker metadata (IDs, addresses, capabilities), and monitors heartbeat health status.
  * **Task Manager:** Creates and queues tasks in-memory, moving them through their lifecycle.
  * **Task Scheduler:** Matches pending tasks with eligible, idle workers.
  * Receives processing results and records them in-memory.
* **Implementation Status:** *IMPLEMENTED* (`src/server/server.py`, `task_manager.py`, `worker_manager.py`). Dynamic scheduling, persistent storage, and complex failure recovery are planned for Phase 5. Containerization is planned for Phase 6.

### 3. Workers
**Workers** are lightweight, standalone execution processes that perform the actual computational work.
* **Responsibilities:**
  * Register dynamically with the Coordinator at startup.
  * Send periodic heartbeat updates to signal active health.
  * Request tasks from the Coordinator.
  * Execute file-processing tasks using specialized local engines.
  * Return task results and execution status back to the Coordinator.
* **Implementation Status:** *IMPLEMENTED* (`src/worker/worker.py`). Currently supports single-worker registration, heartbeat, task execution, and result submission. Containerization is planned for Phase 6.

### 4. Processing Engines
Built-in, optimized Python modules for specific file operations.
* **SHA-256 Hashing:** Safe, buffered file reading to avoid memory bottlenecks.
* **Image Resizing:** Aspect-ratio-preserving resizing using Pillow.
* **PDF Extraction:** Accurate extraction of text characters using pypdf.
* **Implementation Status:** *IMPLEMENTED* (`src/processing/`).

### 5. Docker (Planned - Phase 6)
An optional, planned infrastructure capability to simplify development, testing, and scaling.
* **Responsibilities:**
  * **Containerize Coordinator:** Create a standardized Coordinator Container running the central gRPC server.
  * **Containerize Workers:** Create standardized Worker Containers executing tasks in completely isolated dependency environments.
  * **Orchestration:** Use Docker Compose to launch and scale a local cluster of workers on demand.
* **Implementation Status:** *PLANNED* (Phase 6). No Dockerfiles or configurations exist yet in the codebase.

---

## Deployment Modes

FileRPC is designed to support both local desktop operation and distributed containerized orchestration.

### 1. Local Mode (Standard Desktop Software)
All components run natively on the user's local operating system. Ideal for normal users who do not need multi-machine clusters.
```text
Desktop Application
       |
       v
  Coordinator
       |
       +---- Worker
```

### 2. Docker Multi-Worker Mode (Development & Multi-Worker Testing)
The PySide6 Desktop Application runs natively on the host machine, while the Coordinator and a scalable pool of Workers run inside isolated Docker containers on the same machine:
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
        ├── Worker Container 3
        └── Worker Container N
```
This is a planned future development environment conceptually initialized via:
```text
# Launch Coordinator and 5 parallel Worker containers (Planned conceptual example)
docker compose up --scale worker=5
```
This is a planned capability and does not currently work. It will enable developers to test multi-worker concurrency, failure recovery, and load-balancing scheduling locally.

### 3. Distributed Mode (Production Cluster)
In a production deployment, Workers run on different machines and communicate with the Coordinator over gRPC. Docker can optionally be used to deploy the Coordinator and Workers on these target nodes to guarantee environment reproducibility.

```text
                        Coordinator Machine
                                 │
                               gRPC
                                 │
           ┌─────────────────────┴─────────────────────┐
           ▼                                           ▼
    Worker Machine A                            Worker Machine B
   (Worker Container)                          (Worker Container)
```

---

## Communication Flow & Protocols

The Coordinator and Workers communicate via high-performance **gRPC** and **Protocol Buffers** defined in `proto/filerpc.proto`.

### 1. Worker Registration
When a worker starts, it invokes the `RegisterWorker` RPC method on the Coordinator.
* **Payload:** Contains unique worker ID, worker network address, and a list of capabilities (e.g., `["hash", "resize", "extract"]`).
* **Coordinator Action:** Validates the worker, stores its details in the Worker Registry, and marks the worker as `ONLINE`.

### 2. Heartbeat & Status Updates
Once registered, the worker periodically calls `UpdateWorkerStatus` to report its health and status (e.g., `IDLE`, `BUSY`, or `OFFLINE`).
* **Purpose:** Allows the Coordinator to track worker availability and detect dropped/failed worker nodes. If a worker fails to send a heartbeat within a specific timeout, the Coordinator will classify it as offline.

### 3. Task Assignment
Workers retrieve work via a pull-based model using the `GetTask` RPC.
* **Payload:** The worker requests work by passing its worker ID.
* **Coordinator Action:** The Task Scheduler checks the queue for a `PENDING` task that matches the requesting worker's capabilities. If found, the Coordinator updates the task state to `ASSIGNED` and returns the task payload to the worker.

### 4. Task Execution
Upon receiving a task, the worker triggers the appropriate **Processing Engine**:
* **Hash:** Computes a SHA-256 hash using a buffered, chunk-based approach.
* **Resize:** Opens the target image, performs aspect-ratio-preserving resizing, and writes the output.
* **Extract:** Parses the PDF document, extracts characters, and compiles them.

### 5. Result Reporting
After processing, the worker calls the `SubmitTaskResult` RPC.
* **Payload:** Contains the task ID, execution status (success/failure), and the resulting data (such as the hash string, extracted characters, or paths to the processed file).
* **Coordinator Action:** The Task Manager records the result and updates the task state to `COMPLETED` (or `FAILED`) in-memory. Persistent result storage is not yet implemented and is planned for Phase 5.

---

## Task Lifecycle (Implemented & Planned)

Tasks transition through a defined lifecycle to ensure processing integrity.

### Current Implemented Lifecycle (In-Memory)
The basic lifecycle is fully implemented and verified in-memory:
```text
  PENDING (Task created in Coordinator queue)
     │
     ▼
  ASSIGNED (Coordinator schedules and delivers task to Worker)
     │
     ▼
  COMPLETED (Worker successfully processes file and reports result to Coordinator)
```

In the event of an outright processing failure:
```text
  PENDING ──► ASSIGNED ──► FAILED (Worker reports processing error to Coordinator)
```

### Planned Lifecycle (Phase 5 Task Management & Reliability)
To support robust fault tolerance, Phase 5 will introduce retry states, timeouts, and tracking:
* **RETRY State:** If a task fails or a worker disconnects mid-task, the Coordinator will increment a retry counter. If the maximum retry count is not exceeded, the task reverts to `PENDING` to be picked up by another worker.
* **TIMEOUT Handling:** If an `ASSIGNED` task does not receive a result within a specific timeout limit, it will be automatically revoked and marked for retry.
* **Security & Authentication:** Secure TLS encryption and worker/client authentication methods are planned as future improvements.
