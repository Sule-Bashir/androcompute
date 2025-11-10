# AndroCompute Architecture

## System Overview
AndroCompute is a distributed computing platform that leverages Android devices as worker nodes for parallel processing.

## Components

### Coordinator Server
- **Flask-based web server** with REST API
- **Job queue management** and distribution
- **Real-time dashboard** for monitoring
- **Node registration** and health tracking
- **Result aggregation** and storage

### Android Worker Nodes
- **Lightweight Python client** running on Termux
- **Resource monitoring** (CPU, battery, memory)
- **Secure job execution** in sandboxed environment
- **Automatic reconnection** and fault tolerance

## Workflow
1. **Registration**: Android devices register with coordinator
2. **Job Submission**: Users submit jobs via dashboard/API
3. **Distribution**: Coordinator assigns jobs to available nodes
4. **Execution**: Workers process jobs and return results
5. **Aggregation**: Coordinator collects and displays results

## Data Flow
User → Coordinator API → Job Queue → Android Workers → Results → Dashboard

## Security Features
- Code execution in isolated environment
- Resource usage limits
- Input validation and sanitization
- Secure communication via HTTPS
