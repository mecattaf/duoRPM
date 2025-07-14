#!/bin/bash
# Script to check for updates to backlog and update the spec file accordingly

set -euo pipefail

SPEC="backlog.spec"
REPO="MrLesk/Backlog.md"
VERSION_FIELD="Version:"

# Get the latest version from GitHub
LATEST=$(curl -s "https://api.github.com/repos/$REPO/releases/latest" | jq -r .tag_name | sed 's/^v//')
CURRENT=$(rpmspec -q --qf "%{version}\n" "$SPEC" | head -1)

# Check if versions differ
if [ "$LATEST" != "$CURRENT" ]; then
    # Verify that the source files are available before updating
    X64_URL="https://github.com/${REPO}/releases/download/v${LATEST}/backlog-bun-linux-x64"
    ARM64_URL="https://github.com/${REPO}/releases/download/v${LATEST}/backlog-bun-linux-arm64"
    README_URL="https://raw.githubusercontent.com/${REPO}/v${LATEST}/README.md"
    LICENSE_URL="https://raw.githubusercontent.com/${REPO}/v${LATEST}/LICENSE"
    
    # Check if source files exist
    if curl --output /dev/null --silent --head --fail "$X64_URL" && \
       curl --output /dev/null --silent --head --fail "$ARM64_URL" && \
       curl --output /dev/null --silent --head --fail "$README_URL" && \
       curl --output /dev/null --silent --head --fail "$LICENSE_URL"; then
        
        # Update the spec file version
        sed -i "s/^${VERSION_FIELD}.*/${VERSION_FIELD}        ${LATEST}/" "$SPEC"
        
        # Commit and push the changes with the build tag
        git add "$SPEC"
        git commit -m "Update backlog to $LATEST [build-prebuilt]"
        git push
        
        echo "Updated $SPEC to version $LATEST"
    else
        echo "Warning: Source files for version ${LATEST} not available at expected URLs:"
        echo "x64 Binary: $X64_URL"
        echo "arm64 Binary: $ARM64_URL"
        echo "README: $README_URL"
        echo "LICENSE: $LICENSE_URL"
        exit 0
    fi
else
    echo "backlog spec file is already at the latest version: $CURRENT"
fi
