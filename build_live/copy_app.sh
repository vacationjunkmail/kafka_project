#!/usr/bin/env bash
rsync -hav /mnt/t/PennState/kafka_project/ /mnt/t/kafka_live --exclude ".git" --exclude ".gitignore" --exclude "__pycache__" --exclude "build_live" --exclude ".ruff" --progress
