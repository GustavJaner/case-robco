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

_These are suggested installations. Adapt paths to suit your local environment. Tested on Mac AMD._

### Initial Setup
1. Clone the repo.
2. Run `just` to list the available commands.
3. Run `just setup-local-env` to create the development environment and install dependencies for the Python FastAPI backend (BE) and the React frontend (FE).
4. Run `just mk-start` to start the minikube cluster instance.
5. Run `just mk-build-images` to build the Docker images for the BE & FE in the minikube env.
6. Run `just kubectl-apply` to apply the K8S resources to the minikube cluster (To namespace `robco`).
7. Run `just mk-update-hosts` to add the K8S Ingress host names to /etc/hosts _with sudo_.
8. Run `just mk-tunnel` to start minikube tunnel to the BE & FE ingresses.
9. Go to http://robot-dashboard.local in your browser and try adding some robots in the UI 🤖
   - http://robot-service.local/docs for FastAPI docs.

### Assumptions & Tradeoffs
- TODO

## TODO
- [x] Deploy minikube k8s cluster
- [x] Test deploy a new namespace with a deployment+pod+svc (dummy image) for the BE+FE
- [x] Deploy simple python FastAPI BE
- [x] Add simple BE routes for adding and listing robots
- [x] Deploy simple (Framework: React) FE (web UI)
- [x] Setup basic tests
- [x] Test build my own Docker image for the BE
- [x] Test initial setup
- [x] Setup some svc/ingress to locally access the BE & FE
- [ ] Add a proper SQL DB for the BE (Ensure the PATCH issue is fixed in K8S).
- [ ] Deploy Loki and add to FE.
- [ ] Deploy Prometheus and add to FE.
- [x] Write local setup instructions
- [ ] Add architecture overview diagrams (drawio)
- [ ] Add notes on assumptions and tradeoffs

### Improvements
- [ ] Add pre-commit.
- [ ] Automate with GHA.
- [ ] Use OTEL.
- [ ] Add more API endpoints. Ex. get a specific robot by id and delete (Complete CRUD).
- [ ] Add tests for the React FE.
