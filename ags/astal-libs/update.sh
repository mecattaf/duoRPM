#!/bin/bash
set -euo pipefail

SPEC="astal-libs.spec"
REPO="Aylur/astal"

# Get latest commit from main branch (no release tags)
LATEST=$(curl -s "https://api.github.com/repos/$REPO/commits/main" | jq -r .sha)
CURRENT=$(grep "^%global astal_commit" "$SPEC" | awk '{print $3}')

if [ "$LATEST" != "$CURRENT" ]; then
    # Get current bumpver and increment
    CURRENT_BUMPVER=$(grep "^%global bumpver" "$SPEC" | awk '{print $3}')
    NEW_BUMPVER=$((CURRENT_BUMPVER + 1))
    
    # Update commit and bumpver
    sed -i "s/^%global astal_commit.*/%global astal_commit ${LATEST}/" "$SPEC"
    sed -i "s/^%global bumpver.*/%global bumpver ${NEW_BUMPVER}/" "$SPEC"
    
    # Commit and push changes
    git add "$SPEC"
    git commit -m "Update astal-libs to ${LATEST:0:7} [build-ags-v3]"
    git push
fi
