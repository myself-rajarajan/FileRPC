# Architecture: FileRPC

## High-Level Architecture

FileRPC follows a centralized orchestration model where a server manages the distribution of tasks to a pool of workers.

```text
                         FileRPC
                            |
              +-------------+-------------+
              |                           |
              v                           v
           Client                    Dashboard
              |                           |
              +-------------+-------------+
                            |
                            v
                    +---------------+
                    |   RPC Server  |
                    +-------+-------+
                            |
             +--------------+--------------+
             |              |              |
             v              v              v
        +---------+     +---------+    +---------+
        | Worker 1|     | Worker 2|    | Worker 3|
        +---------+     +---------+    +---------+
```

### Component Responsibilities

* **Client:** Submits job requests and receives results.
* **RPC Server:** Acts as the gateway and coordinator for all tasks.
* **Worker:** Performs the actual computational work on files.
* **Dashboard:** Provides a visual interface for monitoring the entire system.

## Future Architecture

As the system evolves, the RPC Server will integrate specialized components:

```text
Client
  |
  v
API / RPC Server
  |
  +---- Worker Registry: Tracks worker availability and health.
  |
  +---- Task Queue: Buffers incoming jobs.
  |
  +---- Scheduler: Determines optimal task assignment.
  |
  +---- Database: Stores persistent system state and history.
  |
  +---- Workers: Execute the distributed tasks.
  |
  +---- Dashboard: External monitoring and control interface.
```

## Architectural Rules

### Worker
The Worker is a specialized execution unit.
* **Responsibilities:** Execute assigned tasks, report progress, and heartbeat.
* **Constraints:** Worker should NOT schedule other workers, manage the global queue, or control the dashboard.

### Scheduler
The Scheduler is the decision-making engine.
* **Responsibilities:** Assign work to the most appropriate available worker.
* **Constraints:** Scheduler should NOT perform actual file processing.

### Client
The Client is the entry point.
* **Responsibilities:** Formulate and submit requests.
* **Constraints:** Client should NOT directly manage worker internals or bypass the RPC Server.

### Dashboard
The Dashboard is the observation layer.
* **Responsibilities:** Monitor status and provide control through defined interfaces.
* **Constraints:** Dashboard should NOT directly manipulate worker internals; it must interact through the Server's API.

## Separation of Concerns
FileRPC strictly enforces the separation of concerns. Communication between components must happen through well-defined RPC interfaces, ensuring that the internal implementation of one component does not leak into another.
