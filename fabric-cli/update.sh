#!/bin/bash
# fabric-cli/update.sh - Handle projects without releases
set -euo pipefail

SPEC="fabric-cli.spec"
REPO="Fabric-Development/fabric-cli"
VERSION_FIELD="Version:"

# First check if there are any releases
LATEST_RELEASE=$(curl -s "https://api.github.com/repos/$REPO/releases/latest" | jq -r .tag_name 2>/dev/null || echo "null")

if [ "$LATEST_RELEASE" = "null" ] || [ -z "$LATEST_RELEASE" ]; then
    echo "No releases found for fabric-cli. Checking for tags..."
    
    # Try to get the latest tag
    LATEST_TAG=$(curl -s "https://api.github.com/repos/$REPO/tags" | jq -r '.[0].name' 2>/dev/null || echo "null")
    
    if [ "$LATEST_TAG" = "null" ] || [ -z "$LATEST_TAG" ]; then
        echo "No tags found either. This project needs manual version management."
        echo "Consider using a git snapshot approach or waiting for the first release."
        exit 0
    else
        LATEST="$LATEST_TAG"
    fi
else
    LATEST=$(echo "$LATEST_RELEASE" | sed 's/^v//')
fi

CURRENT=$(rpmspec -q --qf "%{version}\n" "$SPEC" | head -1)

# Only update if versions differ and are valid
if [ "$LATEST" != "$CURRENT" ] && [ "$LATEST" != "null" ]; then
    # Verify that the source tarball is available before updating
    SOURCE_URL="https://github.com/${REPO}/archive/v${LATEST}/fabric-cli-${LATEST}.tar.gz"
    
    # Check if source file exists
    if curl --output /dev/null --silent --head --fail "$SOURCE_URL"; then
        # Update the spec file version
        sed -i "s/^${VERSION_FIELD}.*/${VERSION_FIELD}        ${LATEST}/" "$SPEC"
        
        # Commit and push the changes with the build tag
        git add "$SPEC"
        git commit -m "Update fabric-cli to $LATEST [build-go]"
        git push
        
        echo "Updated $SPEC to version $LATEST"
    else
        echo "Warning: Source file for version ${LATEST} not available at ${SOURCE_URL}"
        exit 0
    fi
else
    echo "fabric-cli spec file is already at the latest version or no valid version found: $CURRENT"
fi
