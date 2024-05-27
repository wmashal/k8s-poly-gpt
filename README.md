# K8s Poly GPT

## Description**

Introducing **K8s Poly GPT** your AI-powered Kubernetes copilot. Ask questions in plain language, and our GPT agent leverages NLP to understand and execute tasks within your cluster.  Harness the power of built-in tools, add your own custom tools, or even upload documentation for instant reference.  Tired of remembering complex commands?  Teach poly gpt your favorite shortcuts and streamline your Kubernetes workflow.



# Installation

## Run docker locally
- docker-compose up --build

## helm chart
- helm install k8s-poly-gpt --namespace k8s-poly-gpt --create-namespace .
- helm uninstall k8s-poly-gpt --namespace k8s-poly-gpt

## Samples

- use kubectl to get the pods in the all namespaces if there is a pod name contains the word 'poly' get its container image name and version?
- use kubectl to check if all pods in a Running state? if no who is the pod is not in the Running state ?
- use kubectl to check if all pods in a Running state? if no who is the pod is not in the Running state and what the reason ?
- use kubectl to create a configmap with name 'myconfigmap'  under the default namespace contains 'test' key with '123' value then add a volume in the as-cluster-deployment mapped with myconfigmap config map
- use kubectl to delete the volume in the as-cluster-deployment yaml mapped with configmap name 'myconfigmap'
- use kubectl to delete configmap name 'myconfigmap'

