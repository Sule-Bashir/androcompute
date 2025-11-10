from flask import Flask, jsonify, request, render_template_string
import time
import os

app = Flask(__name__)

# Storage
nodes = {}
jobs = {}
job_id_counter = 1
job_results = {}

DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>AndroCompute Dashboard</title>
    <style>
        body { font-family: Arial; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1000px; margin: 0 auto; }
        .header { background: #4CAF50; color: white; padding: 20px; border-radius: 10px; }
        .node { background: #e0e0e0; padding: 10px; margin: 5px; border-radius: 5px; }
        .job { background: #e0f0ff; padding: 10px; margin: 5px; border-radius: 5px; }
        .result { background: #f0ffe0; padding: 10px; margin: 5px; border-radius: 5px; }
        button { background: #4CAF50; color: white; padding: 10px; border: none; border-radius: 5px; cursor: pointer; margin: 5px; }
        .completed { background: #d4edda; }
        .assigned { background: #fff3cd; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🖥️ AndroCompute Dashboard</h1>
            <p>Coordinator URL: {{ url }}</p>
            <p>📊 System Status: <strong>{{ "ACTIVE" if nodes else "IDLE" }}</strong></p>
        </div>
        
        <h2>📱 Connected Android Nodes ({{ nodes|length }})</h2>
        <div id="nodes">
            {% for node_id, node_data in nodes.items() %}
            <div class="node">
                📱 <strong>{{ node_id }}</strong><br>
                Status: <span style="color: green;">{{ node_data.status }}</span><br>
                Battery: {{ node_data.resources.battery_level }}%<br>
                Cores: {{ node_data.resources.cpu_cores }}<br>
                Last Seen: {{ "%.1f"|format(time.time() - node_data.last_seen) }}s ago
            </div>
            {% else %}
            <p>No nodes connected yet...</p>
            {% endfor %}
        </div>
        
        <h2>📋 Job Control</h2>
        <div>
            <button onclick="submitJob('hash_file')">🔐 Hash File Job</button>
            <button onclick="submitJob('calculate_pi')">π Calculate Pi</button>
            <button onclick="submitJob('process_data')">📊 Process Data</button>
            <button onclick="clearCompletedJobs()">🗑️ Clear Completed</button>
        </div>
        
        <h2>📊 Active Jobs ({{ jobs|length }})</h2>
        <div id="jobs">
            {% for job_id, job_data in jobs.items() %}
            <div class="job {{ 'completed' if job_data.status == 'completed' else 'assigned' }}">
                🆔 <strong>{{ job_id }}</strong><br>
                Type: {{ job_data.type }}<br>
                Status: <strong>{{ job_data.status }}</strong><br>
                Assigned: {{ job_data.assigned_to }}<br>
                Submitted: {{ "%.1f"|format(time.time() - job_data.submitted_at) }}s ago
            </div>
            {% else %}
            <p>No active jobs...</p>
            {% endfor %}
        </div>
        
        <h2>📈 Job Results ({{ job_results|length }})</h2>
        <div id="results">
            {% for job_id, result in job_results.items() %}
            <div class="result">
                ✅ <strong>{{ job_id }}</strong><br>
                Result: <code>{{ result.result }}</code><br>
                Node: {{ result.node_id }}<br>
                Time: {{ "%.3f"|format(result.execution_time) }}s<br>
                Completed: {{ "%.1f"|format(time.time() - result.completed_at) }}s ago
            </div>
            {% else %}
            <p>No results yet...</p>
            {% endfor %}
        </div>
    </div>
    
    <script>
        function submitJob(jobType) {
            fetch('/submit_job', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({type: jobType})
            })
            .then(response => response.json())
            .then(data => {
                if (data.job_id) {
                    alert('✅ Job submitted: ' + data.job_id + ' to ' + data.assigned_to);
                } else {
                    alert('❌ Job submission failed: ' + data.error);
                }
                setTimeout(() => location.reload(), 1000);
            })
            .catch(error => {
                alert('❌ Error: ' + error);
            });
        }
        
        function clearCompletedJobs() {
            if (confirm('Clear all completed jobs and results?')) {
                fetch('/clear_completed', {method: 'POST'})
                .then(() => location.reload());
            }
        }
        
        // Auto-refresh every 3 seconds
        setInterval(() => location.reload(), 3000);
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return "🚀 AndroCompute Coordinator Running!<br><a href='/dashboard'>Dashboard</a>"

@app.route('/register', methods=['POST'])
def register_node():
    data = request.json
    node_id = data.get('node_id')
    nodes[node_id] = {
        'resources': data.get('resources', {}),
        'status': 'online',
        'last_seen': time.time()
    }
    print(f"📱 Node registered: {node_id}")
    return jsonify({'status': 'registered', 'node_id': node_id})

@app.route('/nodes')
def get_nodes():
    return jsonify(nodes)

@app.route('/dashboard')
def dashboard():
    return render_template_string(DASHBOARD_HTML, nodes=nodes, jobs=jobs, job_results=job_results, url=request.url_root, time=time)

@app.route('/submit_job', methods=['POST'])
def submit_job():
    global job_id_counter
    data = request.json
    job_type = data.get('type', 'compute')
    job_id = f"job_{job_id_counter}"
    job_id_counter += 1
    
    job_definitions = {
        'hash_file': {
            'code': "import hashlib; result = hashlib.md5(b'androcompute').hexdigest()",
            'description': 'Calculate MD5 hash of sample data'
        },
        'calculate_pi': {
            'code': "import math; result = str(math.pi)[:10]",
            'description': 'Calculate Pi to 10 digits'
        },
        'process_data': {
            'code': "result = sum(i*i for i in range(1000))",
            'description': 'Process numerical data'
        }
    }
    
    if nodes:
        # Assign to newest active node (most recent last_seen)
        active_nodes = {node_id: data for node_id, data in nodes.items() 
                       if time.time() - data.get('last_seen', 0) < 30}  # Nodes active in last 30 seconds
        
        if active_nodes:
            # Get the newest active node
            newest_node = max(active_nodes.keys(), key=lambda x: active_nodes[x].get('last_seen', 0))
            job_data = job_definitions.get(job_type, job_definitions['hash_file'])
            
            jobs[job_id] = {
                'type': job_type,
                'status': 'assigned',
                'assigned_to': newest_node,
                'code': job_data['code'],
                'description': job_data['description'],
                'submitted_at': time.time()
            }
            
            print(f"📋 Job {job_id} assigned to {newest_node}")
            return jsonify({
                'job_id': job_id, 
                'assigned_to': newest_node, 
                'status': 'submitted',
                'description': job_data['description']
            })
        else:
            return jsonify({'error': 'No active nodes available'}), 400
    return jsonify({'error': 'No nodes available'}), 400

@app.route('/get_job/<node_id>')
def get_job(node_id):
    # Update node's last seen time
    if node_id in nodes:
        nodes[node_id]['last_seen'] = time.time()
    
    # Find assigned jobs for this node
    for job_id, job_data in jobs.items():
        if job_data['assigned_to'] == node_id and job_data['status'] == 'assigned':
            jobs[job_id]['status'] = 'executing'
            print(f"🎯 Job {job_id} sent to {node_id}")
            return jsonify({
                'job_id': job_id,
                'code': job_data['code'],
                'type': job_data['type'],
                'description': job_data.get('description', '')
            })
    
    return jsonify({'job_id': None})

@app.route('/submit_result', methods=['POST'])
def submit_result():
    data = request.json
    job_id = data.get('job_id')
    node_id = data.get('node_id')
    result = data.get('result')
    execution_time = data.get('execution_time')
    
    if job_id in jobs:
        jobs[job_id]['status'] = 'completed'
        job_results[job_id] = {
            'result': result,
            'node_id': node_id,
            'execution_time': execution_time,
            'completed_at': time.time()
        }
        
        print(f"✅ Result received for {job_id} from {node_id}: {result}")
        return jsonify({'status': 'result_accepted', 'job_id': job_id})
    
    return jsonify({'error': 'Job not found'}), 404

@app.route('/job_status/<job_id>')
def job_status(job_id):
    return jsonify(jobs.get(job_id, {}))

@app.route('/results')
def get_results():
    return jsonify(job_results)

@app.route('/clear_completed', methods=['POST'])
def clear_completed():
    # Remove completed jobs and old results
    global jobs, job_results
    
    # Keep only assigned/executing jobs
    jobs = {job_id: job_data for job_id, job_data in jobs.items() 
            if job_data['status'] in ['assigned', 'executing']}
    
    # Keep only recent results (last 10)
    all_results = list(job_results.items())
    if len(all_results) > 10:
        job_results = dict(all_results[-10:])
    
    return jsonify({'status': 'cleared', 'jobs_remaining': len(jobs)})

@app.route('/cleanup_nodes', methods=['POST'])
def cleanup_nodes():
    # Remove inactive nodes (not seen in 2 minutes)
    global nodes
    current_time = time.time()
    inactive_nodes = [node_id for node_id, node_data in nodes.items() 
                     if current_time - node_data.get('last_seen', 0) > 120]
    
    for node_id in inactive_nodes:
        del nodes[node_id]
    
    return jsonify({'status': 'cleaned', 'inactive_removed': len(inactive_nodes)})

if __name__ == '__main__':
    app.run(debug=True)
