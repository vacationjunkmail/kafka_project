#!/usr/bin/env bash
branch="$1"

if [ -z "$branch" ]; then
  echo "Usage: ./delete_branch.sh <branch>"
fi
current_dir=$(pwd)

# update remote-tracking branches.
git fetch --prune

# Check if remote branch exists
if [ -n "$(git ls-remote --heads origin "$branch")" ]; then
  echo "Remote branch '${branch}' still exists. Not deleting."
else
  echo "Remote branch '${branch}' does NOT exist. Deleting local branch..."
  git branch -d "$branch" 2>/dev/null || git branch -D "$branch"
fi

