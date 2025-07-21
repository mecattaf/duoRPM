#!/bin/bash
# fabric-cli/update.sh - Handle projects without releases
set -euo pipefail

SPEC="fabric-cli.spec"
REPO="Fabric-Development/fabric-cli"

echo "Checking fabric-cli for updates..."

# First check if there are any releases
LATEST_RELEASE=$(curl -s "https://api.github.com/repos/$REPO/releases/latest" | jq -r .tag_name 2>/dev/null || echo "null")

if [ "$LATEST_RELEASE" = "null" ] || [ -z "$LATEST_RELEASE" ]; then
    echo "No releases found for fabric-cli. Checking for recent commits on main branch..."
    
    # Get latest commit info from main branch
    LATEST_COMMIT=$(curl -s "https://api.github.com/repos/$REPO/commits/main" | jq -r '.sha' 2>/dev/null || echo "null")
    COMMIT_DATE=$(curl -s "https://api.github.com/repos/$REPO/commits/main" | jq -r '.commit.committer.date' | cut -d'T' -f1 | tr -d '-' 2>/dev/null || echo "null")
    
    if [ "$LATEST_COMMIT" = "null" ] || [ "$COMMIT_DATE" = "null" ]; then
        echo "Unable to fetch commit information. Skipping update."
        exit 0
    fi
    
    # Get current commit from spec file
    CURRENT_COMMIT=$(grep "^%global commit" "$SPEC" | awk '{print $3}' 2>/dev/null || echo "unknown")
    
    if [ "$LATEST_COMMIT" != "$CURRENT_COMMIT" ]; then
        echo "New commit found: ${LATEST_COMMIT:0:7} (was: ${CURRENT_COMMIT:0:7})"
        
        # Update the spec file with new commit and date
        sed -i "s/^%global commit.*/%global commit          ${LATEST_COMMIT}/" "$SPEC"
        sed -i "s/^%global snapdate.*/%global snapdate        ${COMMIT_DATE}/" "$SPEC"
        
        # Commit and push the changes with the build tag
        git add "$SPEC"
        git commit -m "Update fabric-cli to commit ${LATEST_COMMIT:0:7} [build-go]"
        git push
        
        echo "Updated $SPEC to commit ${LATEST_COMMIT:0:7}"
    else
        echo "fabric-cli is already at the latest commit: ${CURRENT_COMMIT:0:7}"
    fi
else
    # Handle actual release
    LATEST=$(echo "$LATEST_RELEASE" | sed 's/^v//')
    CURRENT=$(rpmspec -q --qf "%{version}\n" "$SPEC" | head -1 | cut -d'~' -f1)
    
    if [ "$LATEST" != "$CURRENT" ]; then
        echo "New release found: $LATEST"
        
        # Update to use release instead of snapshot
        sed -i "s/^Version:.*/Version:        $LATEST/" "$SPEC"
        # Remove snapshot-specific globals
        sed -i '/^%global commit/d' "$SPEC"
        sed -i '/^%global shortcommit/d' "$SPEC"  
        sed -i '/^%global snapdate/d' "$SPEC"
        # Update source to use release tarball
        sed -i "s|Source:.*|Source:         %{url}/archive/v%{version}/%{name}-%{version}.tar.gz|" "$SPEC"
        
        git add "$SPEC"
        git commit -m "Update fabric-cli to release $LATEST [build-go]"
        git push
        
        echo "Updated $SPEC to release $LATEST"
    else
        echo "fabric-cli is already at the latest release: $CURRENT"
    fi
fi
