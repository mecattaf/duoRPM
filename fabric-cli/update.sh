#!/bin/bash
# This script checks for new versions of fabric-cli and updates the spec file accordingly

set -euo pipefail

# Define key variables for version checking
SPEC="fabric-cli.spec"
REPO="Fabric-Development/fabric-cli"
VERSION_FIELD="Version:"

# Get the latest version from GitHub
# Note: fabric-cli uses 'v' prefix in its tags, so we remove it
LATEST=$(curl -s "https://api.github.com/repos/$REPO/releases/latest" | jq -r .tag_name | sed 's/^v//')
CURRENT=$(rpmspec -q --qf "%{version}\n" "$SPEC" | head -1)

# Only update if versions differ
if [ "$LATEST" != "$CURRENT" ]; then
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
    echo "fabric-cli spec file is already at the latest version: $CURRENT"
fi
