#!/bin/bash
# Script to check for updates to Gray and update the spec file accordingly

set -euo pipefail

SPEC="gray.spec"
REPO="Fabric-Development/gray"

echo "Checking gray for updates..."

# Check if there are any releases
LATEST_RELEASE=$(curl -s "https://api.github.com/repos/$REPO/releases/latest" | jq -r .tag_name 2>/dev/null || echo "null")

if [ "$LATEST_RELEASE" = "null" ] || [ -z "$LATEST_RELEASE" ]; then
    echo "No releases found for gray. Checking for recent commits on main branch..."
    
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
        echo "New commit found: ${LATEST_COMMIT:0:7} (current: ${CURRENT_COMMIT:0:7})"
        
        # Update the spec file with new commit and snapshot date
        sed -i "s/^%global commit.*/%global commit          $LATEST_COMMIT/" "$SPEC"
        NEW_VERSION="0.1.0~git${COMMIT_DATE}"
        sed -i "s/^Version:.*/Version:        $NEW_VERSION/" "$SPEC"
        
        # Update changelog
        TODAY=$(date "+%a %b %d %Y")
        NEW_CHANGELOG="* $TODAY Automated Build <builder@copr.fedoraproject.org> - $NEW_VERSION-1"
else
    # Handle actual release
    LATEST=$(echo "$LATEST_RELEASE" | sed 's/^v//')
    CURRENT=$(rpmspec -q --qf "%{version}\n" "$SPEC" | head -1 | cut -d'~' -f1)
    
    if [ "$LATEST" != "$CURRENT" ]; then
        echo "New release found: $LATEST"
        
        # Verify that the source is available
        SOURCE_URL="https://github.com/${REPO}/archive/v${LATEST}/${REPO##*/}-${LATEST}.tar.gz"
        
        if curl --output /dev/null --silent --head --fail "$SOURCE_URL"; then
            # Update to use release instead of snapshot
            sed -i "s/^Version:.*/Version:        $LATEST/" "$SPEC"
            # Update source to use release tarball  
            sed -i "s|Source0:.*|Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz|" "$SPEC"
            sed -i "s|%autosetup -n %{name}-%{commit}|%autosetup -n %{name}-%{version}|" "$SPEC"
            
            # Update changelog
            TODAY=$(date "+%a %b %d %Y")
            NEW_CHANGELOG="* $TODAY Automated Build <builder@copr.fedoraproject.org> - $LATEST-1"$'\n'"- Update to release $LATEST"
            sed -i "/%changelog/a\\$NEW_CHANGELOG\\n" "$SPEC"
            
            git add "$SPEC"
            git commit -m "Update gray to release $LATEST [build-gcc]"
            git push
            
            echo "Updated $SPEC to release $LATEST"
        else
            echo "Warning: Source file for version ${LATEST} not available yet"
            exit 0
        fi
    else
        echo "gray is already at the latest release: $CURRENT"
    fi
fi\n'"- Update to latest git snapshot (${LATEST_COMMIT:0:7})"
        sed -i "/%changelog/a\\$NEW_CHANGELOG\\n" "$SPEC"
        
        # Commit and push the changes with the build tag
        git add "$SPEC"
        git commit -m "Update gray to snapshot ${LATEST_COMMIT:0:7} [build-gcc]"
        git push
        
        echo "Updated $SPEC to snapshot $NEW_VERSION"
    else
        echo "gray is already at the latest commit: ${CURRENT_COMMIT:0:7}"
    fi
else
    # Handle actual release
    LATEST=$(echo "$LATEST_RELEASE" | sed 's/^v//')
    CURRENT=$(rpmspec -q --qf "%{version}\n" "$SPEC" | head -1 | cut -d'~' -f1)
    
    if [ "$LATEST" != "$CURRENT" ]; then
        echo "New release found: $LATEST"
        
        # Verify that the source is available
        SOURCE_URL="https://github.com/${REPO}/archive/v${LATEST}/${REPO##*/}-${LATEST}.tar.gz"
        
        if curl --output /dev/null --silent --head --fail "$SOURCE_URL"; then
            # Update to use release instead of snapshot
            sed -i "s/^Version:.*/Version:        $LATEST/" "$SPEC"
            # Update source to use release tarball  
            sed -i "s|Source0:.*|Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz|" "$SPEC"
            sed -i "s|%autosetup -n %{name}-%{commit}|%autosetup -n %{name}-%{version}|" "$SPEC"
            
            # Update changelog
            TODAY=$(date "+%a %b %d %Y")
            NEW_CHANGELOG="* $TODAY Automated Build <builder@copr.fedoraproject.org> - $LATEST-1"$'\n'"- Update to release $LATEST"
            sed -i "/%changelog/a\\$NEW_CHANGELOG\\n" "$SPEC"
            
            git add "$SPEC"
            git commit -m "Update gray to release $LATEST [build-gcc]"
            git push
            
            echo "Updated $SPEC to release $LATEST"
        else
            echo "Warning: Source file for version ${LATEST} not available yet"
            exit 0
        fi
    else
        echo "gray is already at the latest release: $CURRENT"
    fi
fi
