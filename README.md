# Ansible & Simple Web App Deployment with Docker

This project provides an introduction to **Ansible**, an open-source automation platform, and guides you through installing Ansible and deploying a simple Flask-based web application using Docker on macOS.

Prepared by: **Siddharth Chitikesi (2022BCD0021)**  
Date: **March 27, 2025**

---

## What is Ansible?

Ansible is an open-source automation platform developed by Red Hat, designed to simplify IT automation, configuration management, application deployment, orchestration, and task automation. It uses **playbooks** written in YAML to define desired system states and follows an **agentless architecture**, requiring no additional software on target machines. Ansible leverages SSH for Linux and WinRM for Windows for secure, efficient communication.

### Key Features
- **Agentless**: No agents needed on managed nodes.
- **Simple YAML Syntax**: Human-readable playbooks.
- **Idempotency**: Tasks apply only when necessary, avoiding unintended changes.
- **Scalability**: Manages thousands of servers effortlessly.
- **Extensibility**: Supports custom modules and integrations.
- **Multi-Platform Support**: Works on Linux, Windows, and more.

### Why Choose Ansible?
- **Developers**: Easy setup, no extra configurations.
- **IT Administrators**: Automates repetitive tasks (e.g., deployments, updates).
- **DevOps Engineers**: Integrates with CI/CD pipelines (e.g., Jenkins, GitLab).
- **Enterprises**: Red Hat Ansible Automation Platform adds enterprise features like RBAC and dashboards.

---

## Ansible vs. Jenkins vs. Kubernetes

| Tool         | Purpose                          | Agentless | Ease of Use                  | Best Use Case                |
|--------------|----------------------------------|-----------|------------------------------|------------------------------|
| **Ansible**  | Infrastructure automation       | Yes       | Simple YAML scripts          | Infrastructure management    |
| **Jenkins**  | CI/CD automation                | No        | Plugin-based UI              | Build/test/deploy pipelines  |
| **Kubernetes** | Container orchestration       | No        | Complex but powerful         | Managing containerized apps  |

---

## Prerequisites

- **Operating System**: macOS (this guide is macOS-specific; see document for Ubuntu/Debian steps)
- **Python**: 3.8 or later (3.11 recommended)
- **pip**: Python package manager
- **Homebrew**: macOS package manager
- **Docker**: Container runtime
- **Ansible**: Automation tool
- **Internet Access**: For downloading dependencies

---

## Installation on macOS

### Step 1: Install Homebrew (if not installed)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Step 2: Install Docker
```bash
brew install --cask docker
```
- Open Docker Desktop from Applications and ensure it’s running.

### Step 3: Install Ansible
```bash
brew install ansible
```

### Step 4: Verify Installation
```bash
docker --version
ansible --version
```

---

## Basic Ansible Configuration

### Step 1: Create an Inventory File
```bash
mkdir -p ~/ansible_project
cd ~/ansible_project
echo -e "[local]\nlocalhost ansible_connection=local" > inventory
```

### Step 2: Test Ansible Connection
```bash
ansible all -i inventory -m ping
```
- Expected output: A "pong" response confirming Ansible is working.

### Step 3: Run a Sample Playbook
1. Create `hello.yml`:
   ```bash
   echo -e "- hosts: local\n  tasks:\n    - name: Print a message\n      debug:\n        msg: 'Hello, Ansible is working!'" > hello.yml
   ```
2. Execute:
   ```bash
   ansible-playbook -i inventory hello.yml
   ```

---

## Deploying a Simple Web App with Ansible and Docker

This section guides you through deploying a Flask-based web app that displays a personal message using Ansible and Docker.

### Project Overview
- **App**: A Python Flask web server displaying "Hello, I am Siddharth Chitikesi, Roll No: BCD21, this is my simple web app deployed with Ansible and Docker!"
- **Tools**: Ansible for automation, Docker for containerization.
- **Access**: Available at `http://localhost:8080`.

### Steps

#### Step 1: Create Project Structure
```bash
mkdir -p ~/ansible_docker_project
cd ~/ansible_docker_project
```

#### Step 2: Create the Flask Application
Create `app.py`:
```bash
nano app.py
```
Add:
```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, I am Siddharth Chitikesi, Roll No: BCD21, this is my simple web app deployed with Ansible and Docker!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```
Save and exit.

#### Step 3: Create a Dockerfile
Create `Dockerfile`:
```bash
nano Dockerfile
```
Add:
```dockerfile
# Use Python official image
FROM python:3.11

# Set working directory
WORKDIR /app

# Copy files to container
COPY app.py /app/

# Install Flask
RUN pip install Flask requests

# Expose port 5000
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
```
Save and exit.

#### Step 4: Create Docker Compose File
Create `docker-compose.yml`:
```bash
nano docker-compose.yml
```
Add:
```yaml
services:
  web:
    build: .
    ports:
      - "8080:5000"
```
Save and exit.  
*Note*: The `version` field is obsolete in modern Docker Compose and can be omitted.

#### Step 5: Create Ansible Inventory
```bash
mkdir -p ~/ansible_inventory
cd ~/ansible_inventory
nano inventory
```
Add:
```ini
[local]
localhost ansible_connection=local ansible_python_interpreter=/opt/homebrew/bin/python3
```
- Adjust `ansible_python_interpreter` to your Python path (find with `which python3`).
Save and exit.

#### Step 6: Create Ansible Playbook
Create `deploy.yml`:
```bash
nano deploy.yml
```
Add:
```yaml
- hosts: local
  tasks:
    - name: Ensure Docker is running
      shell: open -a Docker || echo "Docker is already running"
    - name: Build and start Docker Compose services
      command: docker compose up -d --build
      args:
        chdir: ~/ansible_docker_project
    - name: Print success message
      debug:
        msg: "Web app deployed! Access it at http://localhost:8080"
```
- Use `docker compose` for Docker Compose v2 (bundled with Docker Desktop) or `docker-compose` for v1.
Save and exit.

#### Step 7: Run the Playbook
```bash
cd ~/ansible_inventory
ansible-playbook -i inventory deploy.yml
```
- Ensure Docker Desktop is running before executing.

#### Step 8: Verify the Application
- Open a browser and visit `http://localhost:8080`.
- Expected output: "Hello, I am Siddharth Chitikesi, Roll No: BCD21, this is my simple web app deployed with Ansible and Docker!"
- Check running containers:
  ```bash
  docker ps
  ```

#### Step 9: Stop the Application (Optional)
```bash
cd ~/ansible_docker_project
docker compose down
```

---

## Troubleshooting

- **Docker Credentials Error**: Log in to Docker Hub (`docker login`) or ensure anonymous pulls work (`docker pull python:3.11`).
- **Permission Issues**: Avoid `sudo` unless necessary; ensure Docker Desktop is running.
- **Port Conflict**: If `8080` is in use, modify `docker-compose.yml` (e.g., `"8081:5000"`) and update the playbook message.
- **Verbose Output**: Run `ansible-playbook -i inventory deploy.yml -vvv` for detailed logs.

---

## Files
- `~/ansible_docker_project/app.py`: Flask application.
- `~/ansible_docker_project/Dockerfile`: Docker image definition.
- `~/ansible_docker_project/docker-compose.yml`: Docker Compose configuration.
- `~/ansible_inventory/inventory`: Ansible inventory.
- `~/ansible_inventory/deploy.yml`: Ansible deployment playbook.

---

## Acknowledgments
This guide is based on the work of Siddharth Chitikesi (2022BCD0021) and adapted for clarity and reproducibility.

--- 

Feel free to save this as `README.md` in your project directory! Let me know if you’d like adjustments.
