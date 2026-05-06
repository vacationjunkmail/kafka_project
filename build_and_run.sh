#!/usr/bin/env bash
set -euo pipefail

NETWORK="kafka-net"

# Check if network exists
if docker network ls --format '{{.Name}}' | grep -Fxq "$NETWORK"; then
  echo "Docker network '${NETWORK}' already exists."
else
  echo "Docker network '${NETWORK}' does not exist. Creating clean environment..."

  # Stop and remove compose stack (containers + networks)
  docker compose down --remove-orphans || true

  # Create network
  docker network create "$NETWORK"

  # Bring stack back up
  docker compose up -d
fi
