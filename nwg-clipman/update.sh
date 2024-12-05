#!/bin/bash
# This script checks for new versions of nwg-clipman and updates the spec file accordingly

set -euo pipefail

# Define key variables for version checking
SPEC="nwg-clipman.spec"
REPO="nwg-piotr/nwg-clipman"
VERSION_FIELD="Version:"

# Get the latest version from GitHub
# Note: nwg-clipman uses 'v' prefix in its tags
LATEST=$(curl -s "https://api.github.com/repos/$REPO/releases/latest" | jq -r .tag_name | sed 's/^v//')
CURRENT=$(rpmspec -q --qf "%{version}\n" "$SPEC" | head -1)

# Only update if versions differ
if [ "$LATEST" != "$CURRENT" ]; then
    # Update the spec file version
    sed -i "s/^${VERSION_FIELD}.*/${VERSION_FIELD}        ${LATEST}/" "$SPEC"
    
    # Commit and push the changes
    # Note the [build-python] tag instead of [build-go]
    git add "$SPEC"
    git commit -m "Update nwg-clipman to $LATEST [build-python]"
    git push
fi
