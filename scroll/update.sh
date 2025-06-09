#!/bin/bash
set -euo pipefail

# Get the latest release from GitHub
LATEST_RELEASE=$(curl -s https://api.github.com/repos/dawsers/scroll/releases/latest | jq -r .tag_name)
CURRENT_VERSION=$(rpmspec -q --qf "%{version}\n" scroll.spec 2>/dev/null | head -1 || echo "0.0.0")

echo "Current version: $CURRENT_VERSION"
echo "Latest release: $LATEST_RELEASE"

if [ "$LATEST_RELEASE" != "$CURRENT_VERSION" ]; then
    echo "Updating scroll to $LATEST_RELEASE"
    
    # Update Version and tag in spec file
    sed -i "s/^%global tag.*/%global tag     $LATEST_RELEASE/" scroll.spec
    sed -i "s/^Version:.*/Version:        $LATEST_RELEASE/" scroll.spec
    
    # Update changelog
    DATE=$(date +"%a %b %d %Y")
    CHANGELOG_ENTRY="* $DATE Thomas Mecattaf <thomas@mecattaf.dev> - $LATEST_RELEASE-1\n- Update to $LATEST_RELEASE"
    
    # Insert the new changelog entry after %changelog
    sed -i "/%changelog/a $CHANGELOG_ENTRY" scroll.spec
    
    # Download the new sources
    spectool -g scroll.spec || true
    
    # Commit changes if in git
    if [ -d ../.git ]; then
        git add scroll.spec
        git commit -m "scroll: Update to $LATEST_RELEASE [build-gcc]" || true
    fi
    
    echo "Updated scroll to $LATEST_RELEASE"
else
    echo "scroll is already at the latest version"
fi
