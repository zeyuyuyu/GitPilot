import time
import os
import logging
from collections import deque

# Configure logging
logging.basicConfig(filename='gitpilot.log', level=logging.INFO)

# Real-time performance monitoring and alerting
class PerformanceMonitor:
    def __init__(self, window_size=60, alert_threshold=0.9):
        self.window_size = window_size
        self.alert_threshold = alert_threshold
        self.response_times = deque(maxlen=window_size)
        self.last_alert_time = 0

    def track_response_time(self, response_time):
        self.response_times.append(response_time)
        if self.should_alert():
            self.send_alert()

    def should_alert(self):
        avg_response_time = sum(self.response_times) / len(self.response_times)
        if avg_response_time > self.alert_threshold * self.window_size:
            current_time = time.time()
            if current_time - self.last_alert_time > 300:  # 5 minutes
                self.last_alert_time = current_time
                return True
        return False

    def send_alert(self):
        logging.error('Performance alert: Average response time exceeds threshold.')
        # Add code to send alert (e.g., email, Slack, etc.)

# Example usage
monitor = PerformanceMonitor(window_size=60, alert_threshold=0.9)

while True:
    # Simulate processing a request
    response_time = random.uniform(0.5, 2.0)
    monitor.track_response_time(response_time)
    time.sleep(1)
