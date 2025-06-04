# Case: RobCo
Cloud application tech case challenge for RobCo.

## Instructions

### Requirements
1. [Python](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python) v3.13
2. [Poetry](https://python-poetry.org/docs/#installation) v2.1 (Python package and dependency manager)
```
curl -sSL https://install.python-poetry.org | POETRY_VERSION=2.1.3 python3 -
# Follow the install instructions and add Poetry to PATH if required. Verify that Poetry works:
poetry --help
```
3. [just](https://github.com/casey/just?tab=readme-ov-file#installation) v1.40.0 (Just a command runner. Inspired by _make_)
```
curl --proto '=https' --tlsv1.2 -sSf https://just.systems/install.sh | bash -s -- --to /usr/local/bin
# just should now be executable. If not: export PATH="$PATH:/usr/local/bin". Verify that just works:
just --help
```
4. [Docker](https://docs.docker.com/desktop/) v24.0.6
5. [minikube](https://minikube.sigs.k8s.io/docs/start) v1.36
6. [Helm](https://helm.sh/docs/intro/quickstart/#install-helm) v3.18.0

_These are suggested installations. Adapt paths to suit your local environment. Tested on Mac (amd64)._

### Run the App
1. Clone the repo.
2. Run `just` to list the available commands.

#### (Optional) Local Development Setup
1. Run `just setup-local-env` to create the local development environment (Installs dependencies for the Python FastAPI backend (BE) and the React frontend (FE)).
2. Run `just py-run-be` to start the Python FastAPI BE locally.
3. Run `just re-run-fe` to start the React FE locally.
4. Go to http://localhost:3000 in your browser and try adding some robots in the UI 🤖
   - http://localhost:8000/docs for FastAPI docs.

#### minikube K8S Setup
1. Run `just mk-start` to start the minikube cluster instance.
2. Run `just mk-deploy-app` to build the Docker images for the BE & FE in the minikube Docker env and apply the K8S resources to the minikube cluster (To namespace `robco` & `monitoring`).
3. Run `just mk-host-tunnel` to add the K8S Ingress host names to /etc/hosts _with sudo_ and start minikube tunnel to the BE & FE ingresses.
4. Go to http://robot-dashboard.local in your browser and try adding some robots in the UI 🤖
   - http://robot-service.local/docs for FastAPI docs.

## Architecture
![Architecture Diagram](docs/architecture.drawio.svg)

### Backend API Endpoints
| Method  | Endpoint         | Description                 |
|---------|------------------|-----------------------------|
| `GET`   | /robots          | Get all robots.             |
| `POST`  | /robots          | Create a new robot.         |
| `PATCH` | /robot/{robot_id}| Update an existing robot.   |

### Repository Structure
<details>
  <summary>Repo directory tree.</summary>

```
.
├── justfile
├── README.md
├── docs/
│   └── architecture.drawio.svg
├── k8s/
│   ├── monitoring/
│   │   ├── values-grafana.yaml
│   │   ├── values-loki.yaml
│   │   ├── values-prometheus.yaml
│   │   └── values-promtail.yaml
│   └── robco/
│       ├── namespace.yaml
│       ├── postgres-db.yaml
│       ├── robot-dashboard.yaml
│       └── robot-service.yaml
├── python-be/
│   ├── Dockerfile
│   ├── poetry.lock
│   ├── pyproject.toml
│   └── app/
│       ├── __init__.py
│       ├── config.py
│       ├── database.py
│       ├── init_db.py
│       ├── main.py
│       ├── models/
│       │   └── robot.py
│       ├── routers/
│       │   ├── __init__.py
│       │   └── v1/
│       │       ├── __init__.py
│       │       ├── health.py
│       │       └── robots.py
│       ├── schemas/
│       │   └── robot.py
│       └── tests/
│           └── v1/
│               ├── test_main.py
│               └── test_robots.py
├── react-fe/
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── package.json
│   ├── README.md
│   ├── public/
│   │   ├── index.html
│   │   └── manifest.json
│   └── src/
│       ├── api.js
│       ├── App.css
│       ├── App.js
│       ├── App.test.js
│       ├── index.css
│       ├── index.js
│       ├── reportWebVitals.js
│       └── setupTests.js
```
</details>

## Assumptions & Tradeoffs
- Assume this is a development env only (No auth, no replicas etc.)

## TODO
- [ ] Fix BE tests with DB.
- [ ] Fix standard structured logging.
- [ ] Expose a /metrics endpoint for the BE (Counter: number of robots added, Histogram or summary: request durations).
- [ ] Add logs to FE.
- [ ] Add metrics to FE.

### Improvements
- [ ] Add pre-commit.
- [ ] Automate tests, builds and proper image tagging with GHA.
- [ ] Use OTEL.
- [ ] Add more API endpoints. Ex. get a specific robot by id and delete (Complete CRUD).
- [ ] Add DB table columns for robot created and last updated.
- [ ] Add tests for the React FE.
- [ ] Structure and utilize the python .env file and config.py better.
- [ ] Add retry logic to Python FastAPI DB init with exponential backoff to avoid pod failure until DB pod is ready.
- [ ] Add proper auth for components.
- [ ] Deploy and manage K8S resources with ArgoCD.
