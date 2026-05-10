#!/usr/bin/env bash
set -euo pipefail

NETWORK="kafka-net"
CONTAINERS=("python-env" "kafka-ui" "kafka")
CURRENT_DIR=$(pwd)

if [[ "$CURRENT_DIR" == *"kafka_project"* ]]; then
  echo "You are inside the kakfa_project - stopping script"
  echo "This should be run from kafka_live. cd to that directory"
  exit 1
fi


echo "Stopping containers..."
for c in "${CONTAINERS[@]}"; do
    if docker ps -a --format '{{.Names}}' | grep -q "^${c}$"; then
        docker stop "$c" || true
    fi
done

echo "Removing containers..."
for c in "${CONTAINERS[@]}"; do
    if docker ps -a --format '{{.Names}}' | grep -q "^${c}$"; then
        docker rm "$c" || true
    fi
done

echo "Disconnecting containers from network..."
for c in "${CONTAINERS[@]}"; do
    if docker network inspect "$NETWORK" >/dev/null 2>&1; then
        docker network disconnect "$NETWORK" "$c" 2>/dev/null || true
    fi
done

echo "Removing network..."
if docker network inspect "$NETWORK" >/dev/null 2>&1; then
    docker network rm "$NETWORK" || true
fi

echo "Teardown complete."
