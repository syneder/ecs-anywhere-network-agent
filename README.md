# ECS Anywhere Network Agent

**ECS Anywhere Network Agent** is a simple agent for ECS Anywhere that automatically
connects a container to the custom network specified in the container labels after
the container is started.

## Introduction
**ECS Anywhere Network Agent** monitors the start of containers using Docker events,
selects containers that are not yet connected to any network (the specified network is
none), searches them for a label with the name of the target network, and connects the
specified network to the container.

**Limitation**:
- connecting multiple networks is not supported
- custom network must exist on the host
- container must be connected to network none before starting

> Custom networks can be created either before the agent starts or while the agent is
> running. However, if the agent detects a container that, according to its labels, needs
> to connect to a network that does not yet exist, it will throw an error and connect the
> network to container only after network has been created and the container has been
> restarted.

## Easy Installation
To start the **ECS Anywhere Network Agent** on the Docker host, run the command:
```
docker run -d --restart=unless-stopped -v /var/run/docker.sock:/var/run/docker.sock \
  -e CONTAINER_NETWORK_LABEL=ecs.network ghcr.io/syneder/ecs-anywhere-network-agent:latest
```

> If you start the **ECS Anywhere Network Agent** on a Docker host using the preceding
> command, Amazon ECS Anywhere will not manage the running **ECS Anywhere Network Agent**
> container. **ECS Anywhere Network Agent** container not managed by Amazon ECS Anywhere
> cannot forward logs to Amazon CloudWatch.

After starting the agent, all containers that are started with the `ecs.network` label
will automatically connect to the network specified in this label. To use a different
label name instead of `ecs.network`, set a different label name in the `CONTAINER_NETWORK_LABEL` 
environment variable when starting the **ECS Anywhere Network Agent**.

An example of starting a container with a label that contains a `custom_network` network
to automatically connect that network to the container after it starts:
```
docker run -it --net=none --label ecs.network=custom_network nginx:latest
```

## Installation using Amazon ECS Console
To run **ECS Anywhere Network Agent** on Amazon ECS Anywhere hosts using Amazon ECS Console,
you must first create a task definition. Below is the task definition in JSON format to use
the latest version of **ECS Anywhere Network Agent**. After creating a task definition, run
it as a service in ECS cluster with external instances.

> For **ECS Anywhere Network Agent** to work properly, it must be running on each
> instance, but no more than one per instance. To do this, when creating ECS service,
> select the service scheduler strategy (service type) as DAEMON.

```JSON
{
    "family": "ecs-anywhere-network-agent",
    "containerDefinitions": [
        {
            "name": "container",
            "image": "ghcr.io/syneder/ecs-anywhere-network-agent:latest",
            "environment": [
                {
                    "name": "CONTAINER_NETWORK_LABEL",
                    "value": "ecs.network"
                }
            ],
            "mountPoints": [
                {
                    "sourceVolume": "docker",
                    "containerPath": "/var/run/docker.sock"
                }
            ]
        }
    ],
    "networkMode": "none",
    "volumes": [
        {
            "name": "docker",
            "host": {
                "sourcePath": "/var/run/docker.sock"
            }
        }
    ],
    "cpu": "128",
    "memory": "32"
}
```
