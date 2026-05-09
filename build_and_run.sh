#!/usr/bin/env bash
set -euo pipefail

NETWORK="kafka-net"
build=0
CURRENT_DIR=$(pwd)

if [[ "$CURRENT_DIR" == *"kafka_project"* ]]; then
  echo "You are inside the kakfa_project - stopping script"
  echo "This should be run from kafka_live. cd to that directory"
  exit 1
fi

# Check if network exists
if docker network ls --format '{{.Name}}' | grep -Fxq "$NETWORK"; then
  echo "Docker network '${NETWORK}' already exists."
  build=1
else
  echo "Docker network '${NETWORK}' does not exist. Creating clean environment..."

  # Stop and remove compose stack (containers + networks)
  docker compose down --remove-orphans || true

  # Create network
  docker network create "$NETWORK"

  # Bring stack back up
  docker compose up -d
fi

if [ "$build" -eq 1 ]; then
  docker compose down #--remove-orphans || true
  docker compose up -d
fi
