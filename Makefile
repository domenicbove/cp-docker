current_dir = $(shell pwd)

define molecule_docker_exec 
docker run \
-it --rm \
-v "/var/run/docker.sock:/var/run/docker.sock" \
-v "$(current_dir):/hacking" \
-w "/hacking" \
--entrypoint="" \
localhost/molecule:latest
endef

build:
	docker build . -t localhost/molecule:latest 

shell: build
	$(molecule_docker_exec) /bin/sh

run_local: build
	$(molecule_docker_exec) molecule converge -s local

destroy_local: build
	$(molecule_docker_exec) molecule destroy -s local