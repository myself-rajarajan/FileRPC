from src.server.server import WorkerCoordinator

def test_submit_task_result():
    coordinator = WorkerCoordinator()
    
    task = coordinator.task_manager.get_next_task()
    
    response = type(
        "Request",
        (),
        {
            "task_id": task["task_id"],
            "worker_id": "worker-001",
            "success": True,
            "result": "test-sha256-result",
            "error_message": "",
        },
    )()
    
    result = coordinator.SubmitTaskResult(response, None)
    
    assert result.success is True
    assert result.message == "Task result received successfully"
        
    saved_task = coordinator.task_manager.get_task(
        task["task_id"]
    )
    
    assert saved_task["status"] == "COMPLETED"
    assert saved_task["result"] == "test-sha256-result"