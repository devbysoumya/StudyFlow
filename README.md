# StudyFlow

A clean student study planner for organizing coursework and deadlines.

## Features
- Dashboard with total, completed, pending, and high-priority task counts
- Add tasks with subject, due date, and priority
- Mark tasks complete or reopen them
- Delete tasks
- Search by task or subject
- SQLite persistence
- JSON API at `/api/tasks`
- Health endpoint at `/health`
- Responsive UI with seeded sample tasks

## Run locally (Windows)
1. Install Python 3.10+.
2. Open PowerShell in this folder.
3. `py -m venv .venv`
4. `.\.venv\Scripts\Activate.ps1`
5. `pip install -r requirements.txt`
6. `python app.py`
7. Open `http://127.0.0.1:5000`.

No API key or external service is required.

## API
- `GET /health`
- `GET /api/tasks`

## CCA-2 pipeline extension
For the assignment, add a Dockerfile, Jenkinsfile, Docker Hub image publishing, and Kubernetes Deployment/Service manifests for Minikube.
