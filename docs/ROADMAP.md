# Roadmap: FileRPC

## Phase 0 — Project Definition
* [x] Project definition
* [x] Problem statement
* [x] Requirements
* [x] Architecture
* [x] MVP definition
* [x] Scope definition

## Phase 1 — Environment
* [x] Repository setup
* [x] Python environment
* [x] Dependencies
* [x] Git configuration

## Phase 2 — File Processing Engine
* [x] SHA-256 implementation
* [ ] Image resizing implementation
* [ ] PDF extraction implementation
* [x] Unit tests for engine (hashing)

## Phase 3 — Basic gRPC
* [ ] gRPC setup and basics
* [ ] Protocol Buffers definition
* [ ] Basic client implementation
* [ ] Basic server implementation
* [ ] RPC connectivity test

## Phase 4 — RPC Server
* [ ] Server internal structure
* [ ] RPC services implementation
* [ ] Server-side logic and testing

## Phase 5 — Single Worker
* [ ] Worker internal structure
* [ ] Worker executor logic
* [ ] Task execution workflow
* [ ] Worker-specific testing

## Phase 6 — Distributed Workflow
* [ ] Client-Server-Worker integration
* [ ] End-to-end distributed workflow test
* [ ] Result propagation

## Phase 7 — Multiple Workers
* [ ] Worker identification (IDs)
* [ ] Support for multiple concurrent workers
* [ ] Basic job distribution

## Phase 8 — Worker Registry
* [ ] Worker registration mechanism
* [ ] Worker status tracking
* [ ] Heartbeat implementation
* [ ] Offline worker detection

## Phase 9 — Task Queue + Scheduler
* [ ] Internal task queue
* [ ] Job state management
* [ ] Basic scheduling logic
* [ ] Job distribution optimization

## Phase 10 — Fault Tolerance
* [ ] Task timeout handling
* [ ] Retry mechanisms
* [ ] Failed job management
* [ ] Worker failure recovery logic

## Phase 11 — Database
* [ ] Database schema design
* [ ] Job persistence
* [ ] Worker state persistence
* [ ] Result storage

## Phase 12 — Dashboard
* [ ] Job monitoring interface
* [ ] Worker monitoring interface
* [ ] Job submission via UI
* [ ] Result viewing and management

## Phase 13 — Docker
* [ ] Dockerfile for all components
* [ ] Docker Compose orchestration
* [ ] Multi-worker local deployment test

## Phase 14 — Open-Source Release
* [ ] Final documentation pass
* [ ] CONTRIBUTING.md creation
* [ ] CODE_OF_CONDUCT.md creation
* [ ] SECURITY.md creation
* [ ] Usage examples
* [ ] Initial release tag
