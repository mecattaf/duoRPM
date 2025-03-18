#!/bin/bash
# Script to check for updates to Fabric and update the spec file accordingly

set -euo pipefail

SPEC="python-fabric.spec"
REPO="Fabric-Development/fabric"
COMMIT_FIELD="%global commit"
VERSION_FIELD="Version:"

# Get the latest commit from the main branch
LATEST_COMMIT=$(curl -s "https://api.github.com/repos/$REPO/commits/main" | jq -r .sha)
CURRENT_COMMIT=$(grep -E "^%global commit" "$SPEC" | awk '{print $3}')

# Check pyproject.toml from main branch for latest version
LATEST_VERSION=$(curl -s "https://raw.githubusercontent.com/$REPO/main/pyproject.toml" | grep "version" | head -1 | cut -d'"' -f2 || echo "")
CURRENT_VERSION=$(rpmspec -q --qf "%{version}\n" "$SPEC" | head -1)

# Check if either commit or version has changed
if [ "$LATEST_COMMIT" != "$CURRENT_COMMIT" ] || [ "$LATEST_VERSION" != "$CURRENT_VERSION" -a -n "$LATEST_VERSION" ]; then
    # Verify that the source is available
    SOURCE_URL="https://github.com/${REPO}/archive/${LATEST_COMMIT}.tar.gz"
    
    # Check if source file exists
    if curl --output /dev/null --silent --head --fail "$SOURCE_URL"; then
        # Update commit in spec file
        sed -i "s/^${COMMIT_FIELD}.*/${COMMIT_FIELD} ${LATEST_COMMIT}/" "$SPEC"
        
        # Update version if available
        if [ -n "$LATEST_VERSION" -a "$LATEST_VERSION" != "$CURRENT_VERSION" ]; then
            sed -i "s/^${VERSION_FIELD}.*/${VERSION_FIELD}        ${LATEST_VERSION}/" "$SPEC"
        fi
        
        # Calculate short commit for the commit message
        SHORT_COMMIT="${LATEST_COMMIT:0:7}"
        
        # Update changelog
        TODAY=$(date "+%a %b %d %Y")
        sed -i "/^%changelog/a* ${TODAY} Automated Package Build <builder@copr.fedoraproject.org> - ${LATEST_VERSION:-$CURRENT_VERSION}-1\n- Update to commit ${SHORT_COMMIT}\n" "$SPEC"
        
        # Commit and push changes with build tag
        git add "$SPEC"
        git commit -m "Update python-fabric to ${LATEST_VERSION:-$CURRENT_VERSION} (commit ${SHORT_COMMIT}) [build-python]"
        git push
    else
        echo "Warning: Source file for commit ${LATEST_COMMIT} not available yet"
        exit 0
    fi
fi
