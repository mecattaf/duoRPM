#!/bin/bash
# Script to check for updates to Fabric and update the spec file accordingly

set -euo pipefail

SPEC="fabric.spec"
REPO="Fabric-Development/fabric"
VERSION_FIELD="Version:"

# Get the latest version from GitHub releases or tags
# Since Fabric doesn't seem to have formal releases yet, we'll check the default.nix for version
LATEST_TAG=$(curl -s "https://api.github.com/repos/$REPO/tags" | jq -r '.[0].name' | sed 's/^v//')

# Try to get version from default.nix if no tags
if [ "$LATEST_TAG" = "null" ] || [ -z "$LATEST_TAG" ]; then
    # Fetch the default.nix file and extract version
    LATEST=$(curl -s "https://raw.githubusercontent.com/$REPO/master/default.nix" | grep -E 'version = "' | sed 's/.*version = "//;s/";.*//' | head -1)
    if [ -z "$LATEST" ]; then
        LATEST="0.0.2"  # fallback to current version in nix file
    fi
else
    LATEST="$LATEST_TAG"
fi

CURRENT=$(rpmspec -q --qf "%{version}\n" "$SPEC" | head -1)

# Check if versions differ
if [ "$LATEST" != "$CURRENT" ]; then
    # Verify that the source is available before updating
    SOURCE_URL="https://github.com/${REPO}/archive/refs/heads/master.tar.gz"
    
    # Check if source exists (master branch should always exist)
    if curl --output /dev/null --silent --head --fail "$SOURCE_URL"; then
        
        # Update the spec file version
        sed -i "s/^${VERSION_FIELD}.*/${VERSION_FIELD}        ${LATEST}/" "$SPEC"
        
        # Commit and push the changes with the build tag
        git add "$SPEC"
        git commit -m "Update fabric to $LATEST [build-python]"
        git push
        
        echo "Updated $SPEC to version $LATEST"
    else
        echo "Warning: Source for version ${LATEST} not available at $SOURCE_URL"
        exit 0
    fi
else
    echo "fabric spec file is already at the latest version: $CURRENT"
fi
