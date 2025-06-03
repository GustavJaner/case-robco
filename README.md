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
2. Run `just mk-build-images` to build the Docker images for the BE & FE in the minikube Docker env.
3. Run `just mk-apply-resources` to apply the K8S resources to the minikube cluster (To namespace `robco`).
4. Run `just mk-update-hosts` to add the K8S Ingress host names to /etc/hosts _with sudo_.
5. Run `just mk-tunnel` to start minikube tunnel to the BE & FE ingresses.
6. Go to http://robot-dashboard.local in your browser and try adding some robots in the UI 🤖
   - http://robot-service.local/docs for FastAPI docs.

## Assumptions & Tradeoffs
- TODO

## TODO
- [ ] Add a proper SQL DB for the BE (Ensure the PATCH issue is fixed in K8S).
- [ ] Deploy Loki and add logs to FE.
- [ ] Fix standard structured logging.
- [ ] Deploy Prometheus and add metrics to FE.
- [ ] Add architecture overview diagrams (drawio).
- [ ] Add notes on assumptions and tradeoffs

### Improvements
- [ ] Add pre-commit.
- [ ] Automate with GHA.
- [ ] Use OTEL.
- [ ] Add more API endpoints. Ex. get a specific robot by id and delete (Complete CRUD).
- [ ] Add tests for the React FE.
