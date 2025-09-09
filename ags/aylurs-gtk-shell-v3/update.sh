#!/bin/bash
set -euo pipefail

SPEC="aylurs-gtk-shell-v3.spec"
REPO="Aylur/ags"

# Get latest commit from v3 branch
LATEST=$(curl -s "https://api.github.com/repos/$REPO/commits/v3" | jq -r .sha)
CURRENT=$(grep "^%global commit0" "$SPEC" | awk '{print $3}')

if [ "$LATEST" != "$CURRENT" ]; then
    # Get current bumpver and increment
    CURRENT_BUMPVER=$(grep "^%global bumpver" "$SPEC" | awk '{print $3}')
    NEW_BUMPVER=$((CURRENT_BUMPVER + 1))
    
    # Update commit and bumpver
    sed -i "s/^%global commit0.*/%global commit0 ${LATEST}/" "$SPEC"
    sed -i "s/^%global bumpver.*/%global bumpver ${NEW_BUMPVER}/" "$SPEC"
    
    # Commit and push changes
    git add "$SPEC"
    git commit -m "Update aylurs-gtk-shell-v3 to ${LATEST:0:7} [build-ags-v3]"
    git push
fi
