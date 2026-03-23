import threading

class MultiThreadedProcessor:
    def __init__(self, num_threads=4):
        self.num_threads = num_threads
        self.task_queue = []
        self.thread_pool = []
        self.lock = threading.Lock()

    def add_task(self, task):
        with self.lock:
            self.task_queue.append(task)

    def start(self):
        for _ in range(self.num_threads):
            thread = threading.Thread(target=self.worker)
            thread.daemon = True
            thread.start()
            self.thread_pool.append(thread)

        for thread in self.thread_pool:
            thread.join()

    def worker(self):
        while True:
            with self.lock:
                if not self.task_queue:
                    return
                task = self.task_queue.pop(0)

            task.process()

if __name__ == '__main__':
    processor = MultiThreadedProcessor(num_threads=8)
    processor.add_task(Task1())
    processor.add_task(Task2())
    processor.add_task(Task3())
    processor.start()
