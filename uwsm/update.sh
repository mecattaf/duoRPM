#!/bin/bash
# Script to check for updates to uwsm and update the spec file accordingly

set -euo pipefail

SPEC="uwsm.spec"
REPO="Vladimir-csp/uwsm"
VERSION_FIELD="Version:"

# Get the latest version from GitHub
LATEST=$(curl -s "https://api.github.com/repos/$REPO/releases/latest" | jq -r .tag_name | sed 's/^v//')
CURRENT=$(rpmspec -q --qf "%{version}\n" "$SPEC" | head -1)

# Check if versions differ
if [ "$LATEST" != "$CURRENT" ]; then
    # Verify that the source is available before updating
    SOURCE_URL="https://github.com/${REPO}/archive/v${LATEST}/${REPO##*/}-${LATEST}.tar.gz"
    
    # Check if source file exists
    if curl --output /dev/null --silent --head --fail "$SOURCE_URL"; then
        
        # Update the spec file version
        sed -i "s/^${VERSION_FIELD}.*/${VERSION_FIELD}        ${LATEST}/" "$SPEC"
        
        # Commit and push the changes with the build tag
        git add "$SPEC"
        git commit -m "Update uwsm to $LATEST [build-python]"
        git push
        
        echo "Updated $SPEC to version $LATEST"
    else
        echo "Warning: Source file for version ${LATEST} not available at expected URL:"
        echo "Source: $SOURCE_URL"
        exit 0
    fi
else
    echo "uwsm spec file is already at the latest version: $CURRENT"
fi
