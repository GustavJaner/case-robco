set positional-arguments # Recipe arguments will be passed as positional arguments to commands. For linewise recipes, argument $0 will be the name of the recipe.
# -e Exit immediately if a command exits with a non-zero status.
# -u Treat unbound variables as an error when substituting.
# -c If set, commands are read from string. This option is used to provide commands that don't come from a file.
# -o pipefail If any command in a pipeline fails, that return code will be used as the return code of the whole pipeline.
set shell := ["bash", "-euco", "pipefail"]

JUST_DIR := justfile_directory() # Just root directory.
PY_BE_DIR := JUST_DIR + "/python-be" # Python FastAPI backend directory.
RE_FE_DIR := JUST_DIR + "/react-fe" # React frontend directory.

KUBE_VERSION := "v1.33.1"
REGISTRY := "robco"
IMAGE_BE := "robot-service"
IMAGE_FE := "robot-dashboard"
TAG := env_var_or_default("TAG", "latest")

# List available recipes.
default:
  @just --list --unsorted

##################################################
### Manage environment for local development
##################################################

# Set up Python BE and React FE for local development.
setup-local-env:
  # Create DB and user (If not exist).
  psql postgres -c "CREATE USER robotuser WITH PASSWORD 'password';"
  psql postgres -c "CREATE DATABASE robotdb OWNER robotuser;"
  psql postgres -c "GRANT ALL PRIVILEGES ON DATABASE robotdb TO robotuser;"
  # Install Python BE dependencies and create .env file.
  cd {{PY_BE_DIR}} && \
  poetry config virtualenvs.in-project true && \
  poetry env info -n && \
  poetry sync && \
  just py-create-env-file
  # Install React FE dependencies.
  cd {{RE_FE_DIR}} && \
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
  cd {{RE_FE_DIR}} && \
  npm install

# npm start the React FE development server locally.
re-run-fe:
  cd {{RE_FE_DIR}} && \
  npm start

# npm test the React FE.
re-test:
  cd {{RE_FE_DIR}} && \
  npm test

# Cleanup local development environment.
cleanup-local-env:
  psql postgres -c "DROP DATABASE IF EXISTS robotdb;"
  psql postgres -c "DROP USER IF EXISTS robotuser;"

##################################################
### Manage minikube cluster
##################################################

# minkube start the cluster instance.
mk-start kube_version=KUBE_VERSION:
  minikube start --kubernetes-version={{kube_version}}
  minikube addons enable ingress
  minikube addons enable ingress-dns
  docker ps
  kubectl cluster-info

# minikube build BE & FE images and apply K8S resources to the minikube cluster.
mk-deploy-app:
  just mk-build-images
  just mk-apply-resources

# Docker build  BE & FE images in the minikube Docker env.
mk-build-images:
  eval $(minikube docker-env) && \
  just docker-build-be && \
  just docker-build-fe && \
  docker images

# minikube list the images available in the minikube Docker env.
mk-list-images:
  minikube image list

# minikube apply the kubernetes resources defined in the manifests directory.
mk-apply-resources:
  minikube kubectl -- apply -f k8s/robco/manifest.yaml
  minikube kubectl -- -n robco get all

# minikube delete the kubernetes resources defined in the manifests directory.
mk-delete-resources:
  minikube kubectl -- delete -f k8s/robco/manifest.yaml

# Update /etc/hosts (sudo) and start minikube tunnel to the BE & FE ingresses.
mk-host-tunnel:
  just mk-update-hosts
  just mk-tunnel

# Update /etc/hosts with the BE & FE K8S ingress hostnames (Uses sudo).
mk-update-hosts:
  sudo sed -i '' '/robot-dashboard.local/d' /etc/hosts
  sudo sed -i '' '/robot-service.local/d' /etc/hosts
  echo "127.0.0.1 robot-dashboard.local robot-service.local" | sudo tee -a /etc/hosts

# minikube start tunnel to the BE & FE ingresses.
mk-tunnel:
  minikube tunnel

# minikube create a tunnel to the FE service via NodePort.
mk-tunnel-fe:
  minikube service -n robco robot-dashboard - url

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

# Forward the BE service port to localhost.
kubectl-port-forward-be:
  kubectl -n robco port-forward svc/robot-service 8000:8000

# Forward the FE service port to localhost.
kubectl-port-forward-fe:
  kubectl -n robco port-forward svc/robot-dashboard 3000:3000

##################################################
### Manage Docker resources
##################################################

# Docker build the BE image.
docker-build-be tag=TAG:
	DOCKER_BUILDKIT=1 docker build -t {{REGISTRY}}/{{IMAGE_BE}}:{{tag}} -f {{PY_BE_DIR}}/Dockerfile {{PY_BE_DIR}}

# Docker build the FE image.
docker-build-fe tag=TAG:
	DOCKER_BUILDKIT=1 docker build -t {{REGISTRY}}/{{IMAGE_FE}}:{{tag}} -f {{RE_FE_DIR}}/Dockerfile {{RE_FE_DIR}}

# Docker list images.
docker-images *args="":
	docker images {{args}}

# Docker run BE container locally.
docker-run tag=TAG:
	docker run -d -p 8000:80 {{REGISTRY}}/{{IMAGE_BE}}:{{tag}}

# Docker remove all stopped local Docker containers.
docker-rmc:
  docker rm -f $(docker ps -aq)

# Docker remove all local Docker images.
docker-rmi:
  docker rmi -f $(docker images -a)
