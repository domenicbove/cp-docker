## CP-Docker

A template and orchestration tool for Dockerized Confluent Platform Deployments

### Introduction

Built off of the great work in the [cp-ansible](https://github.com/confluentinc/cp-ansible) and [cp-demo](https://github.com/confluentinc/cp-demo) projects, this tool aims to bridge the gap between local docker deployments and production VM deployments. With a minimal Ansible inventory file, cp-docker will create fully customizable, ready to run docker-compose files and then handle the challenging operational logic of Confluent Platform deployments. This tool is meant for GitOps workflows.

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- For local deployments, increase your Docker Resources to 6 CPU Cores and 10 GB Memory
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)
- TODO - Run Ansible scripts in a docker container to remove this dependency

### How to Run Locally

A base inventory file is included at the root of this repo with the hosts-local.yml

```
# cat hosts-local.yml

all:
  vars:
    zookeeper_tls_enabled: true
    zookeeper_client_authentication: mtls
    zookeeper_server_authentication: mtls

zookeeper:
  hosts:
    zookeeper1:
    zookeeper2:
    zookeeper3:

kafka:
  hosts:
    kafka1:
    kafka2:
    kafka3:

schema_registry:
  hosts:
    schema-registry1:
```

In your inventory file, all containers must be included as hosts. It is also required that each container has a unique id at the end (ie zookeeper1). Next you can add supported configuration variables which describe the features you want enabled on your deployment. TODO write docs for all supported variables.

First you need to create a certificate authority cert and key
```
ansible-playbook -i hosts-local.yml create_ca.yml
```

Next, to create deployment artifacts based off of your inventory file, run:

```
ansible-playbook -i hosts-local.yml artifacts.yml
```

You can now review your deployment files in the docker directory.
```
% tree docker
docker
├── ca.crt
├── ca.key
└── localhost
    ├── docker-compose.yml
    ├── kafka1
    │   ├── kafka1.crt
    │   ├── kafka1.key
    │   ├── kafka1.keystore.pkcs12
    │   └── kafka1.truststore.pkcs12
<lines omitted>
```

Ssl files are generated for you and properly referenced in the docker-compose.yml file.

Now to deploy simply run:
```
ansible-playbook -i hosts-local.yml deploy.yml
```

And thats it!
```
% docker ps
CONTAINER ID        IMAGE                                   COMMAND                  CREATED             STATUS              PORTS                                                                NAMES
8d12aa0506e9        confluentinc/cp-schema-registry:6.0.0   "/etc/confluent/dock…"   3 seconds ago       Up 3 seconds        0.0.0.0:8081->8081/tcp                                               schema-registry1
441f054c038a        confluentinc/cp-server:6.0.0            "/etc/confluent/dock…"   5 seconds ago       Up 5 seconds        0.0.0.0:9291->9091/tcp, 0.0.0.0:9292->9092/tcp                       kafka3
9b18b815d596        confluentinc/cp-server:6.0.0            "/etc/confluent/dock…"   7 seconds ago       Up 7 seconds        0.0.0.0:9191->9091/tcp, 0.0.0.0:9192->9092/tcp                       kafka2
2b494ac5ea00        confluentinc/cp-server:6.0.0            "/etc/confluent/dock…"   9 seconds ago       Up 8 seconds        0.0.0.0:9091-9092->9091-9092/tcp                                     kafka1
6f3e232e8fc0        confluentinc/cp-zookeeper:6.0.0         "/etc/confluent/dock…"   10 seconds ago      Up 10 seconds       2888/tcp, 3888/tcp, 0.0.0.0:2185->2181/tcp, 0.0.0.0:2186->2182/tcp   zookeeper3
fd8a2a72ec54        confluentinc/cp-zookeeper:6.0.0         "/etc/confluent/dock…"   12 seconds ago      Up 11 seconds       2888/tcp, 3888/tcp, 0.0.0.0:2183->2181/tcp, 0.0.0.0:2184->2182/tcp   zookeeper2
24d7b887c41b        confluentinc/cp-zookeeper:6.0.0         "/etc/confluent/dock…"   13 seconds ago      Up 13 seconds       2888/tcp, 0.0.0.0:2181-2182->2181-2182/tcp, 3888/tcp                 zookeeper1
```

To destroy run: (TODO this could be a playbook)
```
cd docker/localhost
docker-compose down
```

### How to Run on the on your VMs

The exact same process will be used for generating deployment artifacts/ deploying the Confluent stack on VMs. The only difference is your inventory file. Here is one for an AWS deployment:

```
# cat hosts.yml

aws:
  vars:
    ansible_ssh_common_args: -o StrictHostKeyChecking=no -o IdentitiesOnly=yes
    ansible_connection: ssh
    ansible_ssh_user: centos
    ansible_become: true

    zookeeper_tls_enabled: true
    zookeeper_client_authentication: mtls
    zookeeper_server_authentication: mtls

  children:
    zookeeper:
    kafka:
    schema_registry:

zookeeper:
  hosts:
    zookeeper1:
      hostname: ip-172-31-36-37.us-west-2.compute.internal
      ansible_host: ec2-52-36-250-35.us-west-2.compute.amazonaws.com
    zookeeper2:
      hostname: ip-172-31-41-6.us-west-2.compute.internal
      ansible_host: ec2-52-12-73-131.us-west-2.compute.amazonaws.com
    zookeeper3:
      hostname: ip-172-31-42-81.us-west-2.compute.internal
      ansible_host: ec2-34-220-229-127.us-west-2.compute.amazonaws.com

kafka:
  hosts:
    kafka1:
      hostname: ip-172-31-36-37.us-west-2.compute.internal
      ansible_host: ec2-52-36-250-35.us-west-2.compute.amazonaws.com
    kafka2:
      hostname: ip-172-31-41-6.us-west-2.compute.internal
      ansible_host: ec2-52-12-73-131.us-west-2.compute.amazonaws.com
    kafka3:
      hostname: ip-172-31-42-81.us-west-2.compute.internal
      ansible_host: ec2-34-220-229-127.us-west-2.compute.amazonaws.com

schema_registry:
  hosts:
    schema_registry1:
      hostname: ip-172-31-43-94.us-west-2.compute.internal
      ansible_host: ec2-34-222-9-124.us-west-2.compute.amazonaws.com
```

For the VM based deployment, you can colocate services. In the above example zookeeper1 and kafka1 are on the same host. What is important is to make sure hostname matches the FQDN of your host itself. Right now all containers will be using the host network for VM based deployment.

TODO document the terraform
