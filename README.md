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
- [Molecule](https://molecule.readthedocs.io/en/latest/installation.html)

### How to Run Locally

You can make use of molecule scenarios to stand up containers locally, simply run:

```
molecule converge -s local
```

Review the generated deployment artifacts with:

```
% tree molecule/local/docker
molecule/local/docker
├── ca.crt
├── ca.key
└── localhost
    ├── docker-compose.yml
    ├── kafka1
    │   ├── kafka1.crt
    │   ├── kafka1.key
    │   ├── kafka1.keystore.pkcs12
    │   └── kafka1.truststore.pkcs12
    ├── kafka2
    │   ├── kafka2.crt
    │   ├── kafka2.key
    │   ├── kafka2.keystore.pkcs12
    │   └── kafka2.truststore.pkcs12
<lines omitted>
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

To destroy run:
```
molecule destroy -s local
```

### How to Run on the on your AWS EC2s

A scenario is created for convenience, but you must set these environment variables, and pull a role from Ansible Galaxy

```
export AWS_ACCESS_KEY_ID=XXXXXXX
export AWS_SECRET_ACCESS_KEY=XXxxXXX
export AWS_SUBNET_ID=subnet-12345

molecule converge -s default
```

This will create VMs and a security group with proper ports opened. Don't worry the VMs get destroyed :)

Deployment artifacts will be saved at:
```
dbove@dbove-MBP15 docker-compose-demo % tree molecule/default/docker
molecule/default/docker
├── 34.222.43.107
│   └── zookeeper1
│       ├── docker-compose.yml
│       ├── zookeeper1.crt
│       ├── zookeeper1.key
│       ├── zookeeper1.keystore.pkcs12
│       └── zookeeper1.truststore.pkcs12
<lines ommitted>
```

Review your infrastructure and connection details with:
```
cat ~/.cache/molecule/cp-docker/default/inventory/ansible_inventory.yml
# Molecule managed

---
all:
  hosts:
    zookeeper1: &id001
      ansible_connection: smart
      ansible_host: 34.222.43.107
      ansible_port: 22
      ansible_private_key_file: /Users/dbove/.cache/molecule/cp-docker/default/ssh_key
      ansible_ssh_common_args: -o UserKnownHostsFile=/dev/null -o ControlMaster=auto
        -o ControlPersist=60s -o IdentitiesOnly=yes -o StrictHostKeyChecking=no
      ansible_user: ubuntu
<lines omitted>
```

And so to connect to a host you can run:
```
ssh -i /Users/dbove/.cache/molecule/cp-docker/default/ssh_key -o StrictHostKeyChecking=no -o IdentitiesOnly=yes ubuntu@34.222.43.107
```

And finally to destroy the VMs (and save your bill) run:
```
molecule destroy -s default
```
