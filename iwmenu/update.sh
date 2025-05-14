#!/bin/bash
# Script to check for updates to iwmenu and update the spec file accordingly

set -euo pipefail

SPEC="iwmenu.spec"
REPO="e-tho/iwmenu"

# Get the latest version from GitHub
LATEST=$(curl -s "https://api.github.com/repos/$REPO/releases/latest" | jq -r .tag_name | sed 's/^v//')
CURRENT=$(rpmspec -q --qf "%{version}\n" "$SPEC" | head -1)

# Check if versions differ
if [ "$LATEST" != "$CURRENT" ]; then
    # Verify that the binary assets are available before updating
    BINARY_URL="https://github.com/${REPO}/releases/download/v${LATEST}/${REPO##*/}-x86_64-linux-gnu"
    LICENSE_URL="https://github.com/${REPO}/releases/download/v${LATEST}/LICENSE.md"
    README_URL="https://github.com/${REPO}/releases/download/v${LATEST}/README.md"
    CONTRIB_URL="https://github.com/${REPO}/releases/download/v${LATEST}/CONTRIBUTING.md"
    
    # Check if required files exist
    if curl --output /dev/null --silent --head --fail "$BINARY_URL" && \
       curl --output /dev/null --silent --head --fail "$LICENSE_URL" && \
       curl --output /dev/null --silent --head --fail "$README_URL" && \
       curl --output /dev/null --silent --head --fail "$CONTRIB_URL"; then
        
        # Update the spec file version
        sed -i "s/Version:.*/Version:        ${LATEST}/" "$SPEC"
        
        # Update changelog
        TODAY=$(date "+%a %b %d %Y")
        sed -i "/%changelog/a* ${TODAY} Automated Build <builder@copr.fedoraproject.org> - ${LATEST}-1\n- Update to version ${LATEST}\n" "$SPEC"
        
        # Commit and push the changes with the build-prebuilt tag to trigger build
        git add "$SPEC"
        git commit -m "Update iwmenu to $LATEST [build-prebuilt]"
        git push
        
        echo "Updated $SPEC to version $LATEST"
    else
        echo "Warning: Required files for version ${LATEST} not available yet"
        exit 0
    fi
else
    echo "iwmenu spec file is already at the latest version: $CURRENT"
fi
