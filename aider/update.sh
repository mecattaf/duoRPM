#!/bin/bash

set -euo pipefail

# Function to compare versions
version_gt() {
    test "$(echo -e "$1\n$2" | sort -V | head -n 1)" != "$1"
}

# Get the latest version from PyPI
LATEST=$(curl -s "https://pypi.org/pypi/aider-chat/json" | jq -r '.info.version')

# Get current version from spec file
CURRENT=$(rpmspec -q --qf "%{VERSION}" aider.spec)

if version_gt "$LATEST" "$CURRENT"; then
    # Update version in spec file
    sed -i "s/Version:        ${CURRENT}/Version:        ${LATEST}/" aider.spec
    
    # Commit and push changes
    git add aider.spec
    git commit -m "Update aider to ${LATEST} [build-python]"
    git push
fi
