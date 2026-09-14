# Project Specification: FileRPC

## 1. Project Purpose
**FileRPC** is a high-performance, distributed desktop software and file-processing system designed for local and remote file-processing tasks. Rather than relying on resource-intensive web stacks, FileRPC is built as a native desktop application backed by a powerful gRPC-based Coordinator and specialized Worker architecture. 

It enables users to run heavy file operations—such as cryptographic hashing, image resizing, and PDF extraction—efficiently by distributing the workload either locally across CPU cores, remotely across dedicated worker machines, or within containerized environments using Docker.

---

## 2. Problem Statement
Single-machine file processing is heavily constrained by local hardware limitations (such as CPU, memory, and disk I/O bottlenecks). When dealing with large volumes of files or computationally heavy tasks (e.g., batch image resizing or deep text parsing), a single machine can slow down drastically, freezing the user interface and preventing other work. 

Furthermore, traditional solutions are either:
1. **Web-based platforms** that require complex deployments, cloud subscriptions, constant internet connection, and uploading sensitive local files to remote third-party servers.
2. **Command-line tools** that are difficult for non-technical users to configure, manage, and monitor.

There is a distinct need for a local, privacy-focused native desktop application that can orchestrate and distribute these tasks without requiring a web browser, HTML/CSS/JavaScript frontends, or external cloud-hosted servers.

---

## 3. Proposed Solution
FileRPC provides a native desktop software application designed with a **Desktop Application -> Coordinator -> Workers** architecture:

1. **Desktop Application (PySide6 / Qt):** A clean, modern, and intuitive native GUI running directly on the host operating system. Users can easily select files, configure processing options, submit tasks, and monitor task progress and results without ever needing to use the command line.
2. **Coordinator:** An internal system component responsible for receiving task submissions, managing worker registration and heartbeats, scheduling tasks to suitable workers, and tracking task states in-memory.
3. **Workers:** Lightweight execution nodes that register with the Coordinator, listen for assigned tasks, request tasks from the Coordinator, run them using optimized native processing engines, and report results back.

For local use, the Desktop GUI, Coordinator, and Worker can run seamlessly on the same machine. For advanced or heavy-duty use, the Workers can run on separate machines over a network, communicating over gRPC.

To facilitate developer onboarding, multi-worker simulation, and isolated distributed deployments, **Docker** containerization is integrated into the roadmap as a planned, optional deployment mechanism.

---

## 4. Objectives
* **User-Friendly Desktop Experience:** Deliver a native PySide6/Qt interface that hides the complexity of distributed systems behind a clean GUI.
* **Efficient gRPC Communication:** Utilize high-performance gRPC and Protocol Buffers for fast, low-latency communication and data transfer.
* **Scalable Worker Model:** Support easy scaling from a single local worker to multiple remote workers.
* **Optional Docker Integration (Planned):** Use Docker and Docker Compose to containerize Coordinator and Worker processes, allowing developers to simulate multi-worker clusters and scale workers with a single command.
* **Capability & Load-Aware Scheduling (Planned):** Assign tasks dynamically based on worker availability, system load, and worker capabilities.
* **Fault Tolerance & Reliability (Planned):** Detect worker dropouts, retry failed tasks, and manage task lifecycles securely.
* **Privacy & Local-First Design:** Keep data local and secure. Files are processed within the user's controlled infrastructure without mandatory cloud uploads.

---

## 5. Architectural Components

The overall architecture of FileRPC is defined as:

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

### Component Responsibilities

#### Desktop Application (PySide6 / Qt)
* Native user-facing GUI running on the Host Operating System (no browser, HTML, CSS, or REST required; does not run inside a Docker container).
* Allows intuitive file selection and processing configurations.
* Handles task submission to the Coordinator over gRPC.
* Renders real-time progress indicators, worker health dashboard, and task history.
* Displays processed results directly to the user.

#### Coordinator
* Central orchestrator of the system.
* Integrates the **Task Manager** (creating, queueing, and tracking tasks in-memory) and **Worker Manager** (registration, health monitoring via heartbeats).
* Directs task assignment using a **Task Scheduler**.
* Listens on a central gRPC server to communicate with Workers.
* Keeps track of results in-memory. Persistent result storage is not yet implemented.

#### Workers
* Standalone execution nodes.
* Register themselves with the Coordinator and periodically send heartbeats.
* Listen for, request, and execute tasks using core Processing Engines.
* Return final task output and status back to the Coordinator via gRPC.
* *Planned Containerization:* Can be containerized as Worker Containers to easily scale and simulate distributed processing.

#### Processing Engines
* Built-in, optimized Python modules for specific file operations.
* Currently supports:
  * **SHA-256 Hashing:** Safe, buffered file reading.
  * **Image Resizing:** Precision image resizing.
  * **PDF Extraction:** Accurate extraction of textual characters.

---

## 6. Deployment Modes (Planned)

FileRPC is designed to support three distinct deployment modes to balance simple native use with advanced distributed clustering.

### Mode A: Local Mode (Standard Desktop Software)
All components run natively on the user's local operating system. Ideal for normal users who do not need multi-machine clusters.
```text
Desktop Application
       |
       v
  Coordinator
       |
       +---- Worker
```

### Mode B: Docker Multi-Worker Mode (Development & Multi-Worker Testing)
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
        └── Worker Container N
```
*Benefits of Docker here:*
* Simulates distributed execution on a single physical machine.
* Allows developers to scale workers effortlessly.
* Isolates environments and eliminates the need to install dependencies on worker machines during testing.

### Mode C: Distributed Mode (Production Cluster)
The Coordinator and Workers run on separate machines over a network, communicating over gRPC. Docker can optionally be used to deploy the Coordinator and Workers on these target nodes to guarantee environment reproducibility.

```text
                        Coordinator Machine
                                 |
                                gRPC
                                 |
           +---------------------+---------------------+
           |                     |                     |
           v                     v                     v
    Worker Machine A      Worker Machine B      Worker Machine C
```

---

## 7. Processing Operations & Tech Stack

### Implemented File Operations
* **SHA-256 Hashing:** Core Python `hashlib` with buffered reading.
* **PDF Text Extraction:** Parsing text elements using pypdf.
* **Image Resizing:** Aspect-ratio-preserving resizing using Pillow.

### Technology Stack
* **Language:** Python
* **GUI Framework:** PySide6 / Qt (Planned native frontend)
* **RPC Communication:** gRPC (via `grpcio` and `grpcio-tools`)
* **Serialization:** Protocol Buffers (`proto/filerpc.proto`)
* **Containerization:** Docker & Docker Compose (Planned for Coordinator and Workers)
* **Testing:** pytest
* **Version Control:** Git

---

## 8. Development Phases & Current Status

The development of FileRPC is structured into 9 distinct phases:

1. **Phase 1 — Project Foundation:** **COMPLETED**. Established the repo, environment, structure, and specification.
2. **Phase 2 — Processing Engines:** **COMPLETED**. Implemented hashing, resizing, and PDF extraction engines with full unit tests.
3. **Phase 3 — RPC Communication:** **COMPLETED**. Configured Protobuf definitions and generated gRPC bindings. Verified basic Coordinator-Client-Worker RPC connectivity.
4. **Phase 4 — Worker System:** **COMPLETED**. Basic Worker System successfully implemented and verified end-to-end natively. Created remote Worker implementation, including registration, heartbeats, task requesting, task execution, and result submission. Verified with PDF extraction task returning 3,393 characters successfully. Task status is updated to `COMPLETED` in-memory. Persistent storage is not yet implemented.
5. **Phase 5 — Task Management & Reliability:** **NEXT** *(Immediate milestone, not started)*. Focuses on task history, persistent storage, failures, retries, multiple worker tracking, load-aware scheduling, capability-based task assignment, and worker recovery.
6. **Phase 6 — Docker & Distributed Deployment:** **PLANNED**. Draft Dockerfiles for Coordinator and Workers, design Docker Compose multi-worker scaling configurations, and set up isolated distributed deployment environments.
7. **Phase 7 — Desktop Application:** **PLANNED**. Building the native PySide6 desktop GUI and dashboard.
8. **Phase 8 — Testing & Reliability:** **PLANNED**. System stress testing, failure testing, multi-worker containerized simulation, and GUI testing.
9. **Phase 9 — Packaging & Release:** **PLANNED**. Building standalone desktop executables and configuration installers alongside containerized setup scripts.

---

## 9. Success Criteria (MVP & Release)
* **MVP Success:** Successfully process real files (Hash, Resize, and Extract) over gRPC using remote workers. (**Status: Achieved in Phase 4!**)
* **Docker Success:** Orchestrate and scale a multi-worker cluster using a single Docker Compose configuration with independent volume maps and flawless container networks.
* **Desktop Success:** Run a standalone, native desktop application that allows end-to-end task queueing, execution, monitoring, and result rendering without command-line interaction.
* **Reliability Success:** Zero task losses under simulated worker failures, with automatic task reassignment and successful retries.
