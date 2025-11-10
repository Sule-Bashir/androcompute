import requests
import time
import psutil
import os
import math
import hashlib

COORDINATOR_URL = "https://sulebashir.pythonanywhere.com"

class AndroidWorker:
    def __init__(self, coordinator_url):
        self.coordinator_url = coordinator_url
        self.node_id = f"android_{os.urandom(4).hex()}"
        self.running = True

    def get_system_info(self):
        try:
            battery = psutil.sensors_battery()
            return {
                'cpu_cores': psutil.cpu_count(),
                'memory_total': psutil.virtual_memory().total,
                'battery_level': battery.percent if battery else 100,
                'is_charging': battery.power_plugged if battery else True,
            }
        except:
            return {'cpu_cores': 4, 'battery_level': 100, 'is_charging': True}

    def register(self):
        resources = self.get_system_info()
        data = {
            'node_id': self.node_id,
            'resources': resources
        }

        try:
            response = requests.post(f"{self.coordinator_url}/register", json=data, timeout=10)
            print(f"✅ Registered as: {self.node_id}")
            return True
        except Exception as e:
            print(f"❌ Registration failed: {e}")
            return False

    def execute_job(self, code):
        try:
            start_time = time.time()
            
            # FIXED: Use a safer execution environment with pre-imported modules
            safe_globals = {
                'math': math,
                'hashlib': hashlib,
                'result': None
            }
            
            # Remove import statements and execute the main logic
            clean_code = code
            if 'import hashlib' in code:
                clean_code = code.replace('import hashlib; ', '')
            if 'import math' in code:
                clean_code = clean_code.replace('import math; ', '')
            
            exec(clean_code, safe_globals)
            result = safe_globals.get('result', 'No result produced')
            
            execution_time = time.time() - start_time
            return {'success': True, 'result': result, 'execution_time': execution_time}
            
        except Exception as e:
            return {'success': False, 'error': str(e), 'execution_time': 0}

    def check_for_jobs(self):
        try:
            print(f"🔍 Checking jobs at: /get_job/{self.node_id}")
            response = requests.get(f"{self.coordinator_url}/get_job/{self.node_id}", timeout=10)
            print(f"📡 Response status: {response.status_code}")

            if response.status_code == 200:
                job_data = response.json()
                
                if job_data.get('job_id'):
                    print(f"🎯 GOT JOB: {job_data['job_id']} ({job_data['type']})")
                    result = self.execute_job(job_data['code'])

                    if result['success']:
                        print(f"✅ Job completed: {result['result']} (in {result['execution_time']:.3f}s)")
                        
                        # Submit result
                        result_data = {
                            'job_id': job_data['job_id'],
                            'node_id': self.node_id,
                            'result': result['result'],
                            'execution_time': result['execution_time']
                        }

                        submit_response = requests.post(
                            f"{self.coordinator_url}/submit_result",
                            json=result_data,
                            timeout=10
                        )
                        print(f"📤 Result submitted: {submit_response.status_code}")
                        return True
                    else:
                        print(f"❌ Job failed: {result['error']}")
                        # Mark as failed to clear the job
                        result_data = {
                            'job_id': job_data['job_id'],
                            'node_id': self.node_id,
                            'result': f"ERROR: {result['error']}",
                            'execution_time': result['execution_time']
                        }
                        requests.post(f"{self.coordinator_url}/submit_result", json=result_data, timeout=5)
                else:
                    print("📭 No job available")
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                
        except Exception as e:
            print(f"⚠️ Job check error: {e}")
            
        return False

    def start(self):
        print("🚀 Starting Android Worker...")
        print(f"📡 Coordinator: {self.coordinator_url}")

        if self.register():
            print("🔄 Worker running. Checking for jobs every 5 seconds...")
            print("💡 Press Ctrl+C to stop")
            job_count = 0
            try:
                while self.running:
                    if self.check_for_jobs():
                        job_count += 1
                        print(f"📊 Total jobs completed: {job_count}")
                    time.sleep(5)
            except KeyboardInterrupt:
                print("\n🛑 Worker stopped by user")
        else:
            print("💥 Failed to start worker.")

if __name__ == "__main__":
    worker = AndroidWorker(COORDINATOR_URL)
    worker.start()
