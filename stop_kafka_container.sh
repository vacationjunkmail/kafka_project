#!/usr/bin/env bash
docker stop python-env
docker stop kafka-ui
docker stop kafka

docker compose down --remove-orphans
docker network rm kafka-net

