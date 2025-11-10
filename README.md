# AndroCompute: Distributed Mobile Compute Network

Turn Android devices into distributed compute nodes for secure, verifiable workloads across a decentralized network.

## 🚀 Features
- **Mobile-First**: Optimized for Android devices
- **Real-time Dashboard**: Live monitoring of nodes and jobs
- **Secure Execution**: Sandboxed code execution
- **Multi-Node Support**: Scale across multiple devices
- **Performance Metrics**: Execution timing and resource usage

## 🏗️ Architecture
[Coordinator Server] ← Manages nodes & schedules jobs
↓
[Android Workers] ← Execute compute jobs securely
↓
[Real-time Dashboard] ← Monitor & control interface

## 🛠️ Quick Start

### Coordinator Setup
```bash
cd coordinator
pip install -r requirements.txt
python server.py
