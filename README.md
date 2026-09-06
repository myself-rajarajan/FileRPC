# FileRPC

An open-source distributed file-processing platform powered by Remote Procedure Call (RPC).

## Overview

FileRPC is a distributed system designed to handle file-processing tasks across multiple independent worker nodes. By leveraging RPC (Remote Procedure Call), the system allows clients to submit jobs to a central server, which then orchestrates the execution of these tasks on available workers. This architecture enables horizontal scaling and efficient management of resource-intensive file operations.

### Why FileRPC?

Processing large volumes of files or performing computationally expensive operations (like image resizing or PDF extraction) can be a bottleneck on a single machine. FileRPC solves this by distributing the workload, allowing for parallel processing and improved throughput.

### The Role of RPC

RPC serves as the communication backbone, enabling seamless interaction between the Client, the RPC Server, and the Workers as if they were local function calls, while they may actually reside on different machines.

## Problem Statement

As file-processing requirements grow, single-node solutions often face performance degradation, lack of fault tolerance, and limited scalability. Manually managing a fleet of scripts across different servers is error-prone and inefficient. FileRPC provides a structured, automated, and scalable platform to handle these challenges by decoupling the task submission from its execution.

## Goals

* **Practical RPC Implementation:** Demonstrate a robust gRPC-based communication layer.
* **Distributed Processing:** Enable tasks to run across a network of workers.
* **Multiple Worker Nodes:** Support dynamic registration and management of workers.
* **Worker Management:** Monitor health and status of all active workers.
* **Task Scheduling:** Efficiently distribute jobs based on worker availability.
* **Fault Tolerance:** Detect and recover from worker or task failures.
* **Job Monitoring:** Provide visibility into the lifecycle and history of all jobs.
* **Open-source/Self-hosted Deployment:** Ensure the system is easy to deploy and maintain.

## Initial Processing Tasks

### SHA-256 File Hashing
* **Input:** file
* **Output:** SHA-256 hash

### Image Resizing
* **Input:** image + dimensions
* **Output:** resized image

### PDF Text Extraction
* **Input:** PDF
* **Output:** extracted text

## High-Level Architecture

```text
Client
   |
   | RPC
   v
RPC Server
   |
   +-------- Worker 1
   |
   +-------- Worker 2
   |
   +-------- Worker 3
```

The Client submits requests to the RPC Server. The Server manages the task lifecycle and delegates the actual processing to one of the available Workers.

## Core Components

* **Client:** The interface through which users or other systems submit file-processing jobs.
* **RPC Server:** The central orchestrator that receives jobs, manages workers, and returns results.
* **Worker:** Independent nodes that perform the actual file-processing tasks (hashing, resizing, etc.).
* **Worker Registry:** A component within the server that tracks active workers and their health.
* **Task Queue:** Holds incoming jobs before they are assigned to workers.
* **Scheduler:** Logic that determines which worker should receive which task.
* **Fault Tolerance:** Mechanisms for retrying failed jobs and detecting offline workers.
* **Database:** Persists job history, worker status, and system configuration.
* **Dashboard:** A web-based interface for monitoring and managing the system.

## Development Strategy

FileRPC is developed using strict compartmentalization. We implement one phase at a time, ensuring each phase is fully tested and verified before moving to the next. This incremental approach ensures stability and clear progress.

## Design Principles

* **Modularity:** Each component has a clearly defined responsibility.
* **Separation of Concerns:** Decoupling submission, orchestration, and execution.
* **Incremental Development:** Building the system step-by-step through defined phases.
* **Fault Tolerance:** Designing for failure at every level.
* **Extensibility:** Making it easy to add new file-processing operations.
* **Open Source:** Maintaining a clean, well-documented, and accessible codebase.

## Planned Technology Stack

| Component            | Technology       |
| -------------------- | ---------------- |
| Programming Language | Python           |
| RPC                  | gRPC             |
| Interface Definition | Protocol Buffers |
| Database             | PostgreSQL       |
| Task Queue           | Redis            |
| Frontend             | React            |
| API Layer            | FastAPI          |
| Containerization     | Docker           |
| Version Control      | Git              |

*Note: These are planned technologies and may be adjusted later if technically justified.*

## Project Status

**Current Phase: Phase 0 — Project Definition**

## Roadmap

1. Phase 0 — Project Definition
2. Phase 1 — Environment
3. Phase 2 — File Processing Engine
4. Phase 3 — Basic gRPC
5. Phase 4 — RPC Server
6. Phase 5 — Single Worker
7. Phase 6 — Distributed Workflow
8. Phase 7 — Multiple Workers
9. Phase 8 — Worker Registry
10. Phase 9 — Task Queue + Scheduler
11. Phase 10 — Fault Tolerance
12. Phase 11 — Database
13. Phase 12 — Dashboard
14. Phase 13 — Docker
15. Phase 14 — Open-Source Release
