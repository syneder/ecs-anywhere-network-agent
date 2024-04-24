import docker
import os

docker_client = docker.from_env()
docker_network = docker_client.networks.get('none')
container_label = os.environ.get('AGENT_NETWORK_CONTAINER_LABEL')

def connect_network(container, network):
    if 'none' in container.attrs['NetworkSettings']['Networks']:
        docker_network.disconnect(container)
        network.connect(container)

def connect(container):
    if container_label in container.labels:
        try:
            network = container.labels[container_label]
            connect_network(container, docker_client.networks.get(network))
        except docker.errors.NotFound:
            print((
                '[Error] The container label "%s" indicates to connect to the "%s" network, ' +
                'but this docker network does not exist on the current host.') % (container_label, network))

for container in docker_client.containers.list():
    connect(container)

for event in docker_client.events(decode=True):
    if 'Action' in event and event['Action'] == 'start':
        connect(docker_client.containers.get(event['id']))
