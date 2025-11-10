"""
Test script for multi-node simulation
Useful for testing coordinator with multiple virtual workers
"""

import threading
import time
import requests
import random

class TestWorker:
    """Simulated Android worker for testing"""
    
    def __init__(self, worker_id, coordinator_url="http://localhost:5000"):
        self.worker_id = f"test_worker_{worker_id}"
        self.coordinator_url = coordinator_url
        self.running = True
        self.jobs_completed = 0
        
    def register(self):
        """Register with coordinator"""
        data = {
            'node_id': self.worker_id,
            'resources': {
                'cpu_cores': random.randint(2, 8),
                'memory_total': 1024 * 1024 * random.randint(512, 2048),
                'battery_level': random.randint(20, 100),
                'is_charging': random.choice([True, False])
            }
        }
        
        try:
            response = requests.post(f"{self.coordinator_url}/register", json=data, timeout=5)
            print(f"✅ {self.worker_id} registered")
            return True
        except Exception as e:
            print(f"❌ {self.worker_id} registration failed: {e}")
            return False
    
    def simulate_work(self):
        """Simulate job processing"""
        while self.running:
            try:
                # Check for jobs
                response = requests.get(f"{self.coordinator_url}/get_job/{self.worker_id}", timeout=5)
                
                if response.status_code == 200:
                    job_data = response.json()
                    
                    if job_data.get('job_id'):
                        print(f"🎯 {self.worker_id} got job: {job_data['job_id']}")
                        
                        # Simulate work
                        time.sleep(random.uniform(1.0, 3.0))
                        
                        # Submit result
                        result_data = {
                            'job_id': job_data['job_id'],
                            'node_id': self.worker_id,
                            'result': f"Result from {self.worker_id}",
                            'execution_time': random.uniform(1.0, 3.0)
                        }
                        
                        requests.post(f"{self.coordinator_url}/submit_result", json=result_data, timeout=5)
                        self.jobs_completed += 1
                        print(f"✅ {self.worker_id} completed job {self.jobs_completed}")
                
            except Exception as e:
                print(f"⚠️ {self.worker_id} error: {e}")
            
            time.sleep(2)  # Check every 2 seconds
    
    def start(self):
        """Start the test worker"""
        if self.register():
            thread = threading.Thread(target=self.simulate_work)
            thread.daemon = True
            thread.start()
            return thread

def start_test_harness(num_workers=3, coordinator_url="http://localhost:5000"):
    """
    Start multiple test workers for simulation
    
    Args:
        num_workers: Number of virtual workers to create
        coordinator_url: URL of the coordinator
    """
    print(f"🚀 Starting {num_workers} test workers...")
    print(f"📡 Coordinator: {coordinator_url}")
    
    workers = []
    threads = []
    
    # Create and start workers
    for i in range(num_workers):
        worker = TestWorker(i, coordinator_url)
        thread = worker.start()
        if thread:
            workers.append(worker)
            threads.append(thread)
        time.sleep(0.5)  # Stagger startup
    
    print(f"✅ {len(workers)} test workers started")
    print("💡 Press Ctrl+C to stop test harness")
    
    try:
        # Keep main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping test harness...")
        for worker in workers:
            worker.running = False
        
        # Wait for threads to finish
        for thread in threads:
            thread.join(timeout=2)
        
        total_jobs = sum(worker.jobs_completed for worker in workers)
        print(f"📊 Total jobs completed: {total_jobs}")
        print("👋 Test harness stopped")

if __name__ == "__main__":
    # Example usage
    start_test_harness(
        num_workers=3,
        coordinator_url="http://localhost:5000"  # Change to your coordinator URL
    )
