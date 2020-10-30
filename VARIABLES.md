# docker_compose

Below are the supported variables for the role confluent.docker_compose

***

### docker_compose_version

Docker Compose Version

Default:  '3.4'

***

### hostname

Hostname within the container. Set to VM FQDN for Prod Deployment

Default:  "{{inventory_hostname}}"

***

### ansible_host

Hostname/IP for ansible connection for orchestrating deployment.

Default:  localhost

***

### output_dir

Directory to save deployment artifacts. Recommended to choose a git repo for GitOps

Default:  "{{playbook_dir}}/docker/{{ansible_host}}/{{inventory_hostname}}"

***

### zookeeper_tls_enabled

Boolean to Configure TLS Encryption on Zookeeper Client Port

Default:  false

***

### zookeeper_client_authentication

Authentication mode for Zookeeper Clients. Options: ['none', 'mtls', 'digest']

Default:  none

***

### zookeeper_server_authentication

Authentication mode for Zookeeper Servers. Options: ['none', 'mtls', 'digest']

Default:  none

***

### zookeeper_client_port

Zookeeper Client Port on Host (not in container)

Default:  "{{ zookeeper_container_client_port + port_map_adjustment|int * 2 }}"

***

### zookeeper_secure_client_port

Zookeeper Secure Client Port on Host (not in container)

Default:  "{{ zookeeper_container_secure_client_port + port_map_adjustment|int * 2}}"

***

### zookeeper_peer_port

Zookeeper Peer Ports, will not be port mapped on local deployments

Default:  2888

***

### zookeeper_leader_port

Zookeeper Peer Ports, will not be port mapped on local deployments

Default:  3888

***

### zookeeper_container_overrides

Zookeeper container spec overrides

Default:  {}

***

### zookeeper_data_volume_mount_path

Zookeeper data volume mount path on host

Default:  "/var/lib/{{ inventory_hostname }}/data"

***

### zookeeper_log_volume_mount_path

Zookeeper transactional log volume mount path on host

Default:  "/var/lib/{{ inventory_hostname }}/log"

***

### kafka_tls_enabled

Boolean to configure TLS Encryption on all of Kafka's listeners and rest endpoints

Default:  true

***

### kafka_listener_authentication

Authentication mode for all of Kafka's listeners

Default:  mtls

***

### kafka_listeners_override

Kafka listener overwrites. Take precedence of ours. Should container subdictionary like { "client": {"name": "CLIENT", "port": 9093, "tls_enabled": true, "authentication": "none", "advertised_hostname": "kafka1.example.com" } }

Default:  {}

***

### kafka_inter_broker_listener_name

Name of listener dict which represents the interbroker listener. Discouraged from customizing this.

Default:  broker

***

### kafka_internal_replication_factor

Replication Factor for internal topics. Defaults to the minimum of the number of brokers and 3

Default:  "{{ [ groups['kafka'] | default(['localhost']) | length, 3 ] | min }}"

***

### kafka_container_overrides

Zookeeper container spec overrides

Default:  {}

***

### kafka_data_volume_mount_path

Kafka data volume mount path on host

Default:  "/var/lib/{{ inventory_hostname }}/data"

***

### schema_registry_ssl_enabled

Boolean to configure TLS Encryption on Schema Registry's Rest Endpoint

Default:  true

***

### schema_registry_authentication

Authentication mode for Schema Registry's Rest Endpoint. Options: ['none', 'mtls', 'basic']

Default:  none

***

### schema_registry_port

Schema Registry's Port

Default:  8081

***

### schema_registry_kafka_listener_name

Name of listener dict which represents the kafka listener for Schema Registry to connect to. Discouraged from customizing this.

Default:  internal

***

### schema_registry_container_overrides

Schema Registry container spec overrides

Default:  {}

***

# ssl

Below are the supported variables for the role confluent.ssl

***

