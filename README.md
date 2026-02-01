# Microservice Deployment Using Virtual Machines (VirtualBox)

## Overview
This project demonstrates the deployment of a microservice-based application using multiple virtual machines created in VirtualBox. The system is designed with separate virtual machines for frontend, backend, and testing to ensure modularity, isolation, and scalability.

---

## System Architecture

| Virtual Machine | Purpose |
|----------------|---------|
| VM1 | Frontend |
| VM2 | Backend |
| VM3 | Testing |

All virtual machines are connected through a common virtual network to allow inter-VM communication.

---

## Prerequisites
- VirtualBox
- Ubuntu ISO
- Git
- Python 3.x
- Pip (latest version)
- Node.js (for frontend, if applicable)

---

## Implementation Steps

### 1. VirtualBox and Ubuntu Setup
- VirtualBox was installed on the host system.
- Ubuntu ISO was downloaded and installed on a base virtual machine.
- System updates were applied and unused kernels were removed.
- Required packages and dependencies were installed.
- Python and Pip were installed and Pip was upgraded.
- System reboot was performed successfully.

---

### 2. Base VM Preparation
- Versions of all installed tools were verified.
- The base VM was stabilized and prepared for cloning.

---

### 3. Virtual Machine Cloning
The base virtual machine was cloned into:
- VM1 – Frontend
- VM2 – Backend
- VM3 – Testing

---

### 4. Network Configuration
- All VMs were configured on the same private network.

**Backend VM (VM2):**

---

## Backend Setup (VM2)
- Project folder was created.
- Source code was cloned from Git.
- All backend dependencies were installed.
- Uvicorn was installed.
- `localhost` references were replaced with backend VM IP.
- Backend service was started successfully.

---

## Frontend Setup (VM1)
- Frontend application was deployed.
- Backend API endpoint was configured using VM2 IP.
- Login and Signup pages were implemented.

---

## Testing Setup (VM3)
- VM3 was configured for testing.
- Backend IP was updated in `test_system.py`.
- Tests were executed to validate backend connectivity and system functionality.

---

## User Flow
1. User accesses frontend.
2. User logs in or signs up.
3. User receives contact information.
4. Clicking return ends the process.

---

## Results
- Successful deployment across multiple VMs.
- Verified communication between frontend, backend, and testing environments.

---

## Future Enhancements
- Docker and Kubernetes integration
- Load balancing
- CI/CD pipeline
- Improved security mechanisms

---

## Author
Sagnik Chandra
