#!/bin/bash
set -euo pipefail

SPEC="matugen.spec"
REPO="InfernoEmbedded/matugen"

# Get latest version tag from GitHub
LATEST=$(curl -s "https://api.github.com/repos/$REPO/releases/latest" | jq -r .tag_name | sed 's/^v//')
CURRENT=$(rpmspec -q --qf "%{version}\n" "$SPEC" | head -1)

if [ "$LATEST" != "$CURRENT" ]; then
    echo "Updating from $CURRENT to $LATEST"
    sed -i "s/^Version:.*/Version:        ${LATEST}/" "$SPEC"

    git add "$SPEC"
    git commit -m "Update matugen to $LATEST [build-rust]"
    git push
else
    echo "Already up to date: $CURRENT"
fi
