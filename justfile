set positional-arguments # Recipe arguments will be passed as positional arguments to commands. For linewise recipes, argument $0 will be the name of the recipe.
# -e Exit immediately if a command exits with a non-zero status.
# -u Treat unbound variables as an error when substituting.
# -c If set, commands are read from string. This option is used to provide commands that don't come from a file.
# -o pipefail If any command in a pipeline fails, that return code will be used as the return code of the whole pipeline.
set shell := ["bash", "-euco", "pipefail"]

JUST_DIR := justfile_directory()
KUBE_VERSION := "v1.33.1"

# List available recipes.
default: 
  @just --list --unsorted

##################################################
### Manage environment for local development
##################################################

# Create local Python venv and install dependencies with Poetry.
py-setup:
  cd {{JUST_DIR}}
  poetry config virtualenvs.in-project true # Create the Python virtual environment inside the project’s root directory.
  poetry env info -n # Print venv info.
  poetry sync # Synchronize the project’s venv with the locked packages in the poetry.lock file.
  just create-env-file

# Run the Python FastAPI server locally.
py-run-server:
  PYTHONPATH={{JUST_DIR}} poetry run fastapi dev app/main.py --reload --port 8000; \

# Create .env file based on template.
@py-create-env-file:
  cd {{JUST_DIR}} \
  && [ -z "$(ls .env)" ] && cp .env.template .env || echo ".env already exists"

# Poetry synchronize the project’s venv with the locked packages (Similar to poetry install but also removes packages not tracked in the lock file).
py-dep-sync *args="":
    poetry sync {{args}}

# Poetry update all dependencies in poetry.lock to the latest (Respecting the version constraints in the pyproject.toml) and sync venv.
py-dep-upd *args="--sync":
    poetry update {{args}}

# Poetry validate pyproject.toml and lock dependencies to the poetry.lock file (Without installing/syncing).
py-dep-lock:
    poetry check; poetry check --lock; poetry lock

# Poetry remove lock file and regenerate from pyproject.toml.
py-dep-lock-rg:
    poetry lock --regenerate

# Poetry show all dependencies in tree.
py-dep-show:
    poetry show --tree

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
