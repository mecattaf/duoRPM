#!/bin/bash
set -euo pipefail

SPEC="gtk4-layer-shell.spec"
REPO="wmww/gtk4-layer-shell"

# Get latest version from GitHub releases
LATEST=$(curl -s "https://api.github.com/repos/$REPO/releases/latest" | jq -r .tag_name | sed 's/^v//')
CURRENT=$(rpmspec -q --qf "%{version}\n" "$SPEC" | head -1)

if [ "$LATEST" != "$CURRENT" ]; then
    # Update version in spec file
    sed -i "s/Version:.*/Version:        ${LATEST}/" "$SPEC"
    
    # Commit and push changes
    git add "$SPEC"
    git commit -m "Update gtk4-layer-shell to ${LATEST} [build-ags-v3]"
    git push
fi
