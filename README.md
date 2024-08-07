# Kubernetes CronJob for Collecting Node Metrics

## Overview

This project sets up a Kubernetes CronJob to periodically collect node metrics (CPU, Memory, Disk usage) and store them in files. The generated output files are stored on persistent storage to ensure they are retained across pod restarts.

Node exporter is used as the tool for collecting the metrics of the nodes and exposing it to port 9100.

## Setup
1. **Node Exporter Deployment**
   - The node exporter is deployed as Daemonset on the cluster (`nodeexporter.yaml`), so that its pods run on each node of the cluster. It runs on each node to collect their metrics and exposes them to port 9100.

2. **Python Script**
   - The script `metrics_collector.py` interacts with the Kubernetes API to get the internal IP for the nodes.
   - It then fetches metrics from `node_exporter` and saves them to a file with a timestamp.

3. **Dockerfile**
   - Build a Docker image using the `Dockerfile`:
     ```sh
     docker build -t nodemetric:latest .
     ```
   - Tag the image with the username of the Docker hub:
     ```sh
     docker tag nodemetric:latest harshvardhan1506/nodemetric:latest
     ```
   - Push the Docker image to your container registry (Docker hub):
     ```sh
     docker push harshvardhan1506/nodemetric:latest
     ```

4. **Kubernetes Deployment**
   - Create a kubernetes service account and associate secret with your service account
     ```sh
     kubectl apply -f sa.yaml
     ```
   - Grant necessary permissions to created service account, in order to access the Kubernetes API. Create a custom ClusterRole with the permission to list and get the nodes. 
     Bind this ClusterRole to the service account through ClusterRoleBinding.
     ```sh
     kubectl apply -f rbac.yaml
     ```
   - Create a Persistent Volume (PV) and Persistent Volume Claim (PVC):
     ```sh
     kubectl apply -f pv.yaml
     kubectl apply -f pvc.yaml
     ```
   - Create the cronjob that is scheduled to run job every minute. Apply the CronJob YAML manifest:
     ```sh
     kubectl apply -f cronjob.yaml
     ```

## Configuration
- **Schedule:** Modify the `schedule` field in `cronjob.yaml` to change the frequency of the CronJob.

## Assumption
- The node where the HostPath is mounted remains stable and available.
- Ensure frequent backups are taken.

## Example
- Metrics files will be created in the persistent storage, named like `node_metrics_20240804_083211.json`.
- An example of the output file is provided in `output.json`.

## Notes
- Ensure `node_exporter` is running and accessible from the pod.
- Adjust the URL in the Python script if `node_exporter` is exposed on a different endpoint.