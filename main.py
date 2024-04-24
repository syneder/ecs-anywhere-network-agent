import docker
import os

docker_client = docker.from_env()
docker_none_network = docker_client.networks.get('none')
network_label = os.environ.get('AGENT_NETWORK_LABEL')

def connect_network(container, network):
    if 'none' in container.attrs['NetworkSettings']['Networks']:
        docker_none_network.disconnect(container)
        network.connect(container)

def handle_event(event):
    if 'Action' in event and event['Action'] == 'start':
        container = docker_client.containers.get(event['id'])
        container_labels = container.labels
        if network_label in container_labels:
            try:
                network = docker_client.networks.get(container_labels[network_label])
                connect_network(container, network)
            except docker.errors.NotFound:
                print((
                    '[Error] The container label %s indicates to connect to the "%s" network, ' +
                    'but this docker network does not exist on the current host.') % (network_label, network))

for event in docker_client.events(decode=True):
    handle_event(event)
