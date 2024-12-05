#!/bin/bash
set -euo pipefail

SPEC="catppuccin-theme.spec"
REPO="catppuccin/gtk"

# Get the latest version from GitHub releases
LATEST=$(curl -s "https://api.github.com/repos/$REPO/releases/latest" | jq -r .tag_name | sed 's/^v//')
CURRENT=$(rpmspec -q --qf "%{version}\n" "$SPEC" | head -1)

if [ "$LATEST" != "$CURRENT" ]; then
    sed -i "s/Version:.*/Version:        ${LATEST}/" "$SPEC"
    git add "$SPEC"
    git commit -m "Update catppuccin-theme to $LATEST [build-themes]"
    git push
fi
