
# Monitoring Application Performance  with Opensearch

## Install minikube or docker-desktop


- Install Docker: https://docs.docker.com/engine/install/ubuntu/
- Post install: https://docs.docker.com/engine/install/linux-postinstall/
- Install kubectl: https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/#install-using-native-package-management
- Pimp up kubectl: https://spacelift.io/blog/kubectl-auto-completion
- Install minikube: https://minikube.sigs.k8s.io/docs/start/?arch=%2Flinux%2Fx86-64%2Fstable%2Fbinary+download
        

## Deploy Opensearch
#### Install Helm: https://helm.sh/docs/intro/install/
#### Install OS using Helm: https://opensearch.org/docs/latest/install-and-configure/install-opensearch/helm/
 
        helm upgrade --values=values.yaml dev-cluster opensearch/opensearch

Test domain:

    kubectl exec -it opensearch-cluster-master-0 -- /bin/bash
    curl -XGET https://localhost:9200 -u '$os_user:$os_pass' --insecure

    

#### Connect to applications 
Add a service configuration.

[//]: # (error: cannot expose a StatefulSet.apps)

    kubectl port-forward pod/opensearch-cluster-master-0 9200

    kubectl port-forward deployment/dev-opensearch-dashboards 5601

    curl --resolve "domain.example:80:$( minikube ip )" -i  https://localhost:9200 

https://kubernetes.io/docs/tasks/access-application-cluster/service-access-application-cluster/




## Install OpenSearch Dashboards

https://opensearch.org/docs/latest/install-and-configure/install-dashboards/index/

## Deploy Sample app to kubernetes

    ## Add PyActuator
    ## Add Otel to Minkube
    ## Add Data-prepper to Minkube



## Sending data to opensearch