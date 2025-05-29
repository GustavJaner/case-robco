set positional-arguments # Recipe arguments will be passed as positional arguments to commands. For linewise recipes, argument $0 will be the name of the recipe.
# -e Exit immediately if a command exits with a non-zero status.
# -u Treat unbound variables as an error when substituting.
# -c If set, commands are read from string. This option is used to provide commands that don't come from a file.
# -o pipefail If any command in a pipeline fails, that return code will be used as the return code of the whole pipeline.
set shell := ["bash", "-euco", "pipefail"]

KUBE_VERSION := "v1.33.1"

# List available recipes.
default: 
  @just --list --unsorted

foo:
  @echo "fooooo"
  echo "foox2"

@bar:
  echo "barrrr"
  echo "barrrr2"

posargs a b:
  echo $0
  echo $1
  echo $2


setup-env: minikube-start

clean-up: minikube-cleanup

##################################################
### Manage minikube cluster
##################################################

# Start the minkube cluster.
minikube-start kube_version=KUBE_VERSION:
  minikube start --kubernetes-version={{kube_version}}
  docker ps
  kubectl cluster-info

#minikube service hello-minikube


# Stop and delete the minikube cluster.
minikube-cleanup:
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
