# Hackathon Submission Guide

## Project: AndroCompute
**Distributed Computing Platform Using Android Devices**

## 🎯 Problem Statement
Leverage idle computing power of Android devices to create a distributed computing network for parallel processing tasks.

## ✨ Features Implemented

### Core Features
✅ **Distributed Job Execution** - Parallel processing across multiple devices  
✅ **Real-time Dashboard** - Web interface for monitoring and control  
✅ **Android Worker Nodes** - Lightweight clients for job execution  
✅ **Resource Monitoring** - Battery, CPU, and memory tracking  
✅ **Secure Execution** - Sandboxed code execution environment  

### Technical Features
✅ **RESTful API** - Standardized communication protocol  
✅ **Fault Tolerance** - Automatic reconnection and recovery  
✅ **Scalable Architecture** - Support for multiple concurrent workers  
✅ **Cross-platform** - Works on any Android device with Termux  

## 🏗️ System Architecture

### Components
1. **Coordinator Server** (Flask + Python)
   - Job distribution and management
   - Real-time dashboard
   - Node registration and health monitoring

2. **Android Worker** (Python + Termux)
   - Job execution engine
   - Resource monitoring
   - Result submission

### Workflow
