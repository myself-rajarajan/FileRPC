# Roadmap: FileRPC

This roadmap outlines the development path for the FileRPC distributed desktop file-processing platform. It represents our plan to progress from the core processing engines and RPC system to a robust, containerized distributed environment, and ultimately a polished native desktop application.

## Overall Progress

- **Completed Phases:** 4 / 9
- **Current Status:** Core single-worker gRPC coordination system is fully completed and verified in-memory.
- **Next Milestone:** Phase 5 — Task Management & Reliability.
- **Project Goal:** To deliver a native desktop application that is simple for local use and easily expandable for distributed, Docker-containerized worker clusters.

---

## Phase 1 — Project Foundation
Status: **COMPLETED**

This phase laid down the initial workspace structure, configuration, and dependencies required for the development of FileRPC.

* [x] Initialize Git repository
* [x] Set up Python virtual environment (`.venv`)
* [x] Configure basic `.gitignore`
* [x] Establish core project folder structure (`src/`, `tests/`, `docs/`, `proto/`)
* [x] Define project requirements and specs

---

## Phase 2 — Processing Engines
Status: **COMPLETED**

In this phase, we developed the core, standalone file-processing engines and verified them with comprehensive unit tests.

* [x] SHA-256 file hashing with buffered file reading
* [x] Image resizing engine
* [x] PDF text extraction engine (using pypdf)
* [x] Unit tests for all engines (`test_hashing.py`, `test_resizing.py`, `test_pdf_extraction.py`)

---

## Phase 3 — RPC Communication
Status: **COMPLETED**

This phase established the core gRPC protocol and communication contracts between the central Coordinator and the workers/clients.

* [x] Define services and messages in `proto/filerpc.proto`
* [x] Generate Python gRPC stubs and client-server bindings (`src/rpc/`)
* [x] Implement the Coordinator's basic gRPC server
* [x] Implement the Client interface for submitting basic requests
* [x] Verify basic end-to-end RPC connectivity and test correctness

---

## Phase 4 — Worker System
Status: **COMPLETED**

This phase successfully implemented and verified the basic Worker System natively, allowing workers to dynamically register, update health, request tasks from the Coordinator, execute them using the processing engines, and report results back.

* [x] Implement remote Worker logic (`src/worker/worker.py`)
* [x] Implement worker registration mechanism on the Coordinator
* [x] Implement worker heartbeat / status updates (`UpdateWorkerStatus`)
* [x] Implement task request and assignment loop (`GetTask`)
* [x] Implement worker-side execution for Hash tasks
* [x] Implement worker-side execution for Resize tasks
* [x] Implement worker-side execution for PDF extraction tasks
* [x] Implement result reporting mechanism (`SubmitTaskResult`)
* [x] Verify successful end-to-end task workflow natively (SHA-256, Resize, and PDF extraction with 3,393 characters extracted and reported successfully in-memory to the Coordinator)

---

## Phase 5 — Task Management & Reliability
Status: **NEXT**

This phase will focus on making the task queue, scheduling, and worker orchestration robust, load-aware, and fault-tolerant.

* [ ] Task status tracking (detailed lifecycle states)
* [ ] Task history log on the Coordinator
* [ ] Persistent task and result storage
* [ ] Robust task failure handling
* [ ] Task retry mechanism on timeout or failure
* [ ] Support for multiple concurrent workers
* [ ] Worker availability and active connection tracking
* [ ] Worker failure detection (stale heartbeat/disconnect)
* [ ] Worker recovery and automatic task re-assignment
* [ ] Capability-based task assignment (assigning tasks only to workers who support them)
* [ ] Load-aware scheduling and distribution

---

## Phase 6 — Docker & Distributed Deployment
Status: **PLANNED**

This phase will introduce Docker as a planned development, testing, and distributed deployment mechanism to run Coordinator and Worker components consistently across different environments without affecting normal native desktop use.

* [ ] Draft `Dockerfile` for the central Coordinator
* [ ] Draft `Dockerfile` for the lightweight Worker
* [ ] Design `docker-compose.yml` for multi-worker simulation and container orchestration
* [ ] Configure container networking rules to allow secure gRPC communication
* [ ] Test standalone Coordinator container execution
* [ ] Test standalone Worker container execution
* [ ] Verify containerized multi-worker parallel task execution
* [ ] Support dynamic Worker scaling under Docker Compose (e.g., `docker compose up --scale worker=5` planned future conceptual example)
* [ ] Establish runtime environment configuration via Docker environment variables
* [ ] Design container volume mapping and secure local/distributed file handling
* [ ] Execute distributed deployment tests on independent host machines
* [ ] Implement Docker container health checks
* [ ] Document Docker and Docker Compose deployment workflows

---

## Phase 7 — Desktop Application
Status: **PLANNED**

This phase will build the native native GUI application. The desktop UI will run directly on the host operating system (not inside a container) and communicate with the Coordinator over gRPC.

* [ ] Choose PySide6 / Qt as the native desktop GUI framework
* [ ] Design main application dashboard
* [ ] Implement file selection dialogs
* [ ] Implement task selection and configuration panels
* [ ] Implement task submission flow to the Coordinator
* [ ] Create real-time task progress and state indicators
* [ ] Display task results (e.g., text preview, resized image preview, SHA-256 hash output)
* [ ] Build worker monitoring panel (showing connected workers, health, capabilities)
* [ ] Integrate application logs panel
* [ ] Create toast/system error notifications

---

## Phase 8 — Testing & Reliability
Status: **PLANNED**

Before packaging, the entire system must undergo exhaustive system and stress testing, specifically leveraging Docker to simulate complex multi-worker failure and load states.

* [ ] End-to-end system validation tests
* [ ] Multi-worker distributed stress testing
* [ ] Docker containerized network disruption and failure testing
* [ ] Task retry validation tests under container failovers
* [ ] Large-file handling optimization and stress testing
* [ ] High-concurrency task execution testing
* [ ] Coordinator and Worker performance benchmarking
* [ ] PySide6 GUI automated/manual testing

---

## Phase 9 — Packaging & Release
Status: **PLANNED**

The final phase will package FileRPC into an easy-to-install, standalone desktop executable alongside clear deployment configurations for containerized setups.

* [ ] Build standalone desktop executable (e.g., using PyInstaller)
* [ ] Package all external library and native dependencies
* [ ] Design and implement configuration management (local configuration files)
* [ ] Create an installer/executable packager for easy distribution
* [ ] Perform clean-installation testing
* [ ] Verify seamless Windows compatibility
* [ ] Write end-user Docker deployment and configuration documentation
* [ ] Write release documentation
* [ ] Publish initial official release on GitHub
