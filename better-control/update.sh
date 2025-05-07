#!/bin/bash
# Script to check for updates to Better Control and update the spec file accordingly

set -euo pipefail

SPEC="better-control.spec"
REPO="quantumvoid0/better-control"
VERSION_FIELD="Version:"

# Get the latest version from GitHub
# The version is detected by examining the betterctl.sh file which contains the version
# This is more reliable than using tags which might not exist yet
LATEST=$(curl -s "https://raw.githubusercontent.com/$REPO/main/betterctl.sh" | grep -m 1 "your version :" | sed -E 's/.*version : \\e\[34m([0-9.]+)\\e\[0m.*/\1/')
CURRENT=$(rpmspec -q --qf "%{version}\n" "$SPEC" | head -1)

# Check if versions differ
if [ "$LATEST" != "$CURRENT" ]; then
    # Verify that the source is available before updating
    SOURCE_URL="https://github.com/${REPO}/archive/refs/tags/v${LATEST}/${REPO##*/}-${LATEST}.tar.gz"
    
    # Check if source file exists (GitHub may not have created the tarball yet)
    if curl --output /dev/null --silent --head --fail "$SOURCE_URL"; then
        # Update the spec file version
        sed -i "s/^${VERSION_FIELD}.*/${VERSION_FIELD}        ${LATEST}/" "$SPEC"
        
        # Update changelog
        TODAY=$(date "+%a %b %d %Y")
        sed -i "/%changelog/a* ${TODAY} Automated Build <builder@copr.fedoraproject.org> - ${LATEST}-1\n- Update to version ${LATEST}\n" "$SPEC"
        
        # Commit and push the changes with the build-python tag to trigger build
        git add "$SPEC"
        git commit -m "Update better-control to $LATEST [build-python]"
        git push
        
        echo "Updated $SPEC to version $LATEST"
    else
        echo "Warning: Source file for version ${LATEST} not available yet"
        exit 0
    fi
else
    echo "better-control spec file is already at the latest version: $CURRENT"
fi
