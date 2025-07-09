#!/bin/bash

# Check if there are staged changes
if [ -z "$(git diff --cached)" ]; then
  echo "No staged changes found. Please stage your changes with 'git add' first."
  exit 1
fi

# Run the generate-commit-message.js script with LEFTHOOK=0 to bypass hooks
LEFTHOOK=0 node "$(dirname "$0")/generate-commit-message.js"
