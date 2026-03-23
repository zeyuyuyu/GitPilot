import asyncio
from typing import Callable, Any, Optional, Dict
from datetime import datetime
from dataclasses import dataclass

@dataclass
class Task:
    id: str
    func: Callable
    args: tuple
    kwargs: dict
    retries: int = 0
    max_retries: int = 3
    last_error: Optional[Exception] = None
    created_at: datetime = datetime.now()

class GitPilot:
    def __init__(self):
        self.task_queue: asyncio.Queue = asyncio.Queue()
        self.results: Dict[str, Any] = {}
        self.running = False

    async def enqueue(self, task_id: str, func: Callable, *args, **kwargs) -> None:
        """Add a task to the queue"""
        task = Task(id=task_id, func=func, args=args, kwargs=kwargs)
        await self.task_queue.put(task)

    async def process_task(self, task: Task) -> None:
        """Process a single task with retry logic"""
        try:
            result = await task.func(*task.args, **task.kwargs)
            self.results[task.id] = result
        except Exception as e:
            if task.retries < task.max_retries:
                task.retries += 1
                task.last_error = e
                await self.task_queue.put(task)
            else:
                self.results[task.id] = f"Failed after {task.retries} retries: {str(e)}"

    async def worker(self) -> None:
        """Main worker loop processing tasks from queue"""
        while self.running:
            try:
                task = await self.task_queue.get()
                await self.process_task(task)
                self.task_queue.task_done()
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Worker error: {str(e)}")

    async def start(self, num_workers: int = 3) -> None:
        """Start the task processing system"""
        self.running = True
        workers = [asyncio.create_task(self.worker()) for _ in range(num_workers)]
        await asyncio.gather(*workers)

    async def stop(self) -> None:
        """Stop the task processing system"""
        self.running = False
        await self.task_queue.join()

    def get_result(self, task_id: str) -> Optional[Any]:
        """Get the result of a specific task"""
        return self.results.get(task_id)

    def get_queue_size(self) -> int:
        """Get current size of task queue"""
        return self.task_queue.qsize()

# Example usage:
'''
async def main():
    pilot = GitPilot()
    
    # Start workers
    asyncio.create_task(pilot.start(num_workers=3))
    
    # Example async task
    async def example_task(x):
        await asyncio.sleep(1)
        return x * 2
    
    # Enqueue some tasks
    await pilot.enqueue("task1", example_task, 5)
    await pilot.enqueue("task2", example_task, 10)
    
    # Wait for tasks to complete
    await asyncio.sleep(2)
    
    # Get results
    print(pilot.get_result("task1"))  # 10
    print(pilot.get_result("task2"))  # 20
    
    await pilot.stop()

if __name__ == "__main__":
    asyncio.run(main())
'''