#!/bin/bash
# Script to check for updates to Fabric and update the spec file accordingly

set -euo pipefail

SPEC="python-fabric.spec"
REPO="Fabric-Development/fabric"
VERSION_FIELD="Version:"

# Check both release tag and pyproject.toml for the latest version
GITHUB_LATEST=$(curl -s "https://api.github.com/repos/$REPO/releases/latest" 2>/dev/null | jq -r .tag_name 2>/dev/null | sed 's/^v//' || echo "")
if [ -z "$GITHUB_LATEST" ]; then
    # If no releases, check pyproject.toml from main branch
    GITHUB_LATEST=$(curl -s "https://raw.githubusercontent.com/$REPO/main/pyproject.toml" | grep "version" | head -1 | cut -d'"' -f2 || echo "")
fi

# Fallback to checking the Python package index
if [ -z "$GITHUB_LATEST" ]; then
    GITHUB_LATEST=$(curl -s "https://pypi.org/pypi/fabric/json" 2>/dev/null | jq -r .info.version 2>/dev/null || echo "")
fi

# If we still don't have a version, exit
if [ -z "$GITHUB_LATEST" ]; then
    echo "Could not determine latest version. Exiting."
    exit 0
fi

CURRENT=$(rpmspec -q --qf "%{version}\n" "$SPEC" | head -1)

if [ "$GITHUB_LATEST" != "$CURRENT" ]; then
    # Verify that the source is available
    SOURCE_URL="https://github.com/${REPO}/archive/v${GITHUB_LATEST}/${GITHUB_LATEST}.tar.gz"
    
    # Check if source file exists or if we can use a different format
    if ! curl --output /dev/null --silent --head --fail "$SOURCE_URL"; then
        SOURCE_URL="https://github.com/${REPO}/archive/${GITHUB_LATEST}/${GITHUB_LATEST}.tar.gz"
        if ! curl --output /dev/null --silent --head --fail "$SOURCE_URL"; then
            echo "Warning: Source file for version ${GITHUB_LATEST} not available yet"
            exit 0
        fi
    fi
    
    # Update version in spec file
    sed -i "s/^${VERSION_FIELD}.*/${VERSION_FIELD}        ${GITHUB_LATEST}/" "$SPEC"
    
    # Update changelog
    TODAY=$(date "+%a %b %d %Y")
    sed -i "/^%changelog/a* ${TODAY} Automated Package Build <builder@copr.fedoraproject.org> - ${GITHUB_LATEST}-1\n- Update to version ${GITHUB_LATEST}\n" "$SPEC"
    
    # Commit and push changes with build tag
    git add "$SPEC"
    git commit -m "Update python-fabric to ${GITHUB_LATEST} [build-python]"
    git push
fi
