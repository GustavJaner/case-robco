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
3. [just](https://github.com/casey/just?tab=readme-ov-file#installation) (Just a command runner. Inspired by _make_)
```
curl --proto '=https' --tlsv1.2 -sSf https://just.systems/install.sh | bash -s -- --to /usr/local/bin
# just should now be executable. If not: export PATH="$PATH:/usr/local/bin". Verify that just works:
just --help
```
4. [Docker](https://docs.docker.com/desktop/) v24.0.6
5. [minikube](https://minikube.sigs.k8s.io/docs/start) v1.36

_These are suggested installations; adapt paths to suit your local environment._

### Initial Setup
1. Clone the repo.
2. Run `just setup-env` to create the development environment and install dependencies. This should provision the minikube cluster and the deployments running there, or should this be in another command?


    Clone the repository.
    Run just setup-env to create the development environment and install dependencies. This will also create a .env file in the root directory.
    Adjust environment variables in .env, if necessary.
    Run just to see available commands and options, including how to start the FastAPI server for local development.
    Run just run-server to launch the application, and verify it’s working by visiting http://127.0.0.1:8000/docs.
    The endpoints are secured using basic authentication.
        The default username is username and the password is password.
        The credentials can be adjusted in the .env file.

Quality Assurance
For quality assurance, a couple of tools are set up already. To install pre-commit run just pc i. To run pre-commit hooks for all files use just pc a.

### Contributing
Test locally, then commit. Pre-commit tests are run locally.

## Notes
- What is Uvicorn? Uvicorn is a lightning-fast ASGI (Asynchronous Server Gateway Interface) server implementation, using uvloop and httptools.
Purpose: It’s primarily used to run asynchronous web applications and frameworks that are compatible with the ASGI specification, such as FastAPI.
- What is Pydantic? Pydantic is a Python library that uses type annotations to validate data and manage configurations. It enforces type hints at runtime and provides user-friendly errors when data is invalid.
Key Features: a) Data Validation


### Assumptions & Tradeoffs
- todo:)

## TODO
- [x] Deploy minikube k8s cluster
- [x] Test deploy a new namespace with a deployment+pod+svc (dummy image) for the BE+FE
- [x] Deploy simple python FastAPI BE
- [x] Add simple BE routes for adding and listing robots
- [x] Deploy simple (Framework: React) FE (web UI)
- [x] Setup basic tests
- [ ] Test build my own Docker image for the BE
- [ ] Test initial setup
- [ ] Setup some svc/ingress to locally access the BE & FE
- [ ] Deploy Loki
- [ ] Deploy Prometheus
- [ ] Write local setup instructions
- [ ] Add architecture overview diagrams (drawio)
- [ ] Add notes on assumptions and tradeoffs

Q: how to manage the deployments to minikube? Terraform(not so infra heavy project apart from the minikube cluster itself..), ArgoCD?

### Improvements
- [ ] Manage minikube k8s cluster creation and destruction with terraform?
- [ ] Add pre-commit
- [ ] Automate with GHA
- [ ] Use OTEL? Standards for logs and metrics, then the logs/metrics backends can be changed later. 
- [ ] Add more API endpoints. Ex. get a specific robot by id and delete (Complete CRUD).
