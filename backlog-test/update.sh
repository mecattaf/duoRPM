#!/bin/bash
# Script to check for updates to backlog and update the spec file accordingly

set -euo pipefail

SPEC="backlog-test.spec"
REPO="MrLesk/Backlog.md"
VERSION_FIELD="Version:"

# Get the latest version from GitHub
LATEST=$(curl -s "https://api.github.com/repos/$REPO/releases/latest" | jq -r .tag_name | sed 's/^v//')
CURRENT=$(rpmspec -q --qf "%{version}\n" "$SPEC" | head -1)

# Check if versions differ
if [ "$LATEST" != "$CURRENT" ]; then
    # Verify that the source tarball is available before updating
    SOURCE_URL="https://github.com/${REPO}/archive/v${LATEST}/Backlog.md-${LATEST}.tar.gz"
    
    # Check if source tarball exists
    if curl --output /dev/null --silent --head --fail "$SOURCE_URL"; then
        
        # Update the spec file version
        sed -i "s/^${VERSION_FIELD}.*/${VERSION_FIELD}        ${LATEST}/" "$SPEC"
        
        # Commit and push the changes with the build tag
        git add "$SPEC"
        git commit -m "Update backlog-test to $LATEST [build-bun]"
        git push
        
        echo "Updated $SPEC to version $LATEST"
    else
        echo "Warning: Source tarball for version ${LATEST} not available at expected URL:"
        echo "$SOURCE_URL"
        exit 0
    fi
else
    echo "backlog-test spec file is already at the latest version: $CURRENT"
fi
