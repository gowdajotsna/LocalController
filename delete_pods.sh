#!/bin/bash

# Script to delete all pods in specified namespaces

# Specify the namespaces
NAMESPACES=("node1-namespace" "node2-namespace" "default")

# Loop through each namespace
for NAMESPACE in "${NAMESPACES[@]}"
do
    echo "Deleting all pods in the $NAMESPACE namespace..."

    # Get all pod names in the current namespace
    PODS=$(kubectl get pods -n $NAMESPACE -o custom-columns=:metadata.name)

    # Loop through and delete each pod in the current namespace
    for POD in $PODS
    do
        kubectl delete pod $POD -n $NAMESPACE --force --grace-period=0
        echo "Deleted pod $POD in namespace $NAMESPACE"
    done

    echo "All pods in the $NAMESPACE namespace have been deleted."
done

echo "Pod deletion complete for all specified namespaces."
