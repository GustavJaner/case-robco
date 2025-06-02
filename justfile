set positional-arguments # Recipe arguments will be passed as positional arguments to commands. For linewise recipes, argument $0 will be the name of the recipe.
# -e Exit immediately if a command exits with a non-zero status.
# -u Treat unbound variables as an error when substituting.
# -c If set, commands are read from string. This option is used to provide commands that don't come from a file.
# -o pipefail If any command in a pipeline fails, that return code will be used as the return code of the whole pipeline.
set shell := ["bash", "-euco", "pipefail"]

JUST_DIR := justfile_directory() # Just root directory.
PY_BE_DIR := JUST_DIR + "/python-be" # Python backend directory.
KUBE_VERSION := "v1.33.1"
IMAGE := "robco-robotics-platform" # Same as the ECR repo name.
TAG := env_var_or_default("TAG", "latest")

# List available recipes.
default:
  @just --list --unsorted

##################################################
### Manage environment for local development
##################################################

# Set up Python BE and React FE for local development.
setup-local-env:
  cd {{PY_BE_DIR}} && \
  poetry config virtualenvs.in-project true && \
  poetry env info -n && \
  poetry sync && \
  just py-create-env-file
  cd "{{JUST_DIR}}/react-fe" && \
  npm install

# Python run the FastAPI server locally.
py-run-be:
  cd {{PY_BE_DIR}} && PYTHONPATH={{PY_BE_DIR}} \
  poetry run fastapi dev app/main.py --reload --port 8000

# Create .env file based on template.
@py-create-env-file:
  cd {{PY_BE_DIR}} && \
  [ ! -f .env ] && cp .env.template .env || echo ".env already exists"

# Poetry synchronize the project’s venv with the locked packages.
py-dep-sync *args="":
  cd {{PY_BE_DIR}} && \
  poetry sync {{args}} # sync is similar to poetry install but also removes packages from venv not tracked in the lock file.

# Poetry update all dependencies in poetry.lock to the latest and sync venv.
py-dep-upd *args="--sync":
  cd {{PY_BE_DIR}} && \
  poetry update {{args}} # Update lock file while respecting the version constraints in the pyproject.toml.

# Poetry validate pyproject.toml and lock dependencies to the poetry.lock file.
py-dep-lock:
  cd {{PY_BE_DIR}} && \
  poetry check; poetry check --lock; poetry lock # Lock dependencies Without syncing venv.

# Poetry remove lock file and regenerate from pyproject.toml.
py-dep-lock-rg:
  cd {{PY_BE_DIR}} && \
  poetry lock --regenerate

# Poetry show all dependencies in tree.
py-dep-show:
  cd {{PY_BE_DIR}} && \
  poetry show --tree

# Run tests for the Python FastAPI BE.
py-test path="app/tests":
  cd {{PY_BE_DIR}} && PYTHONPATH={{PY_BE_DIR}} \
  poetry run pytest -r A -vs {{path}} --color=yes

# Run tests for the Python FastAPI BE and generate coverage report.
py-test-cov path="app/tests":
  cd {{PY_BE_DIR}} && PYTHONPATH={{PY_BE_DIR}} \
  poetry run coverage run --omit="*/test*,*/.venv/*,*__init__.py" -m pytest -r A -vs {{path}} && \
  poetry run coverage report -m && \
  poetry run coverage html --skip-empty

# Run pip-audit (Python dependency vulnerability scanner).
py-audit:
  cd {{PY_BE_DIR}} && PYTHONPATH={{PY_BE_DIR}} \
  poetry run pip-audit

# npm install the React FE dependencies.
re-npm-install:
  cd "{{JUST_DIR}}/react-fe" && \
  npm install

# npm start the React FE development server locally.
re-run-fe:
  cd "{{JUST_DIR}}/react-fe" && \
  npm start

# npm test the React FE.
re-test:
  cd "{{JUST_DIR}}/react-fe" && \
  npm test

# Note that the development build is not optimized. To create a production build, use npm run build.

# Clean up the local development environment.
clean-up: mk-cleanup

##################################################
### Manage minikube cluster
##################################################

# minkube start cluster instance.
mk-start kube_version=KUBE_VERSION:
  minikube start --kubernetes-version={{kube_version}}
  docker ps
  kubectl cluster-info

# minikube pause cluster (Without impacting deployed applications).
mk-pause:
  minikube pause

# minikube unpause cluster.
mk-unpause:
  minikube unpause

# minikube stop and delete cluster.
mk-cleanup:
  minikube stop
  minikube delete

##################################################
### Manage kubernetes resources
##################################################

# Apply the kubernetes resources defined in the manifests directory.
kubectl-apply:
  kubectl apply -f k8s/robco/manifest.yaml
  kubectl -n robco get all

# Forward the service port to localhost. Then visit http://localhost:8080 in your browser.
kubectl-port-forward:
  kubectl -n robco port-forward svc/robot-service 8080:8080

# Delete the kubernetes resources defined in the manifests directory.
kubectl-delete:
  kubectl delete -f k8s/robco/manifest.yaml
