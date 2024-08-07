import requests
import json
from datetime import datetime
from kubernetes import client, config

def get_node_ips():
    config.load_incluster_config() 
    v1 = client.CoreV1Api()
    nodes_list = v1.list_node()
    node_ips = [addr.address for node in nodes_list.items for addr in node.status.addresses if addr.type == 'InternalIP']
    return node_ips

def fetch_metrics_from_node(node_ip):
    metric_url = f"http://{node_ip}:9100/metrics"
    try:
        response = requests.get(metric_url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Unable to fetch metrics from {node_ip}: {e}")
        return None

def save_metrics_to_file(metrics):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"/mnt/data/node_metrics_{timestamp}.json"
    with open(output_filename, 'w') as f:
        json.dump(metrics, f, indent=4)
    print(f"Metrics saved to {output_filename}")

def main():
    node_ips = get_node_ips()
    all_node_metrics = {}
    for node_ip in node_ips:
        metrics = fetch_metrics_from_node(node_ip)
        if metrics:
            all_node_metrics[node_ip] = metrics
    save_metrics_to_file(all_node_metrics)

if __name__ == "__main__":
    main()