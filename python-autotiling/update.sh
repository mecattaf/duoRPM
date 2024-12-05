#!/bin/bash
set -euo pipefail

SPEC="python-autotiling.spec"
PYPI_NAME="autotiling"
GITHUB_REPO="nwg-piotr/autotiling"

# Check both PyPI and GitHub for versions
PYPI_LATEST=$(curl -s "https://pypi.org/pypi/${PYPI_NAME}/json" | jq -r .info.version)
GITHUB_LATEST=$(curl -s "https://api.github.com/repos/${GITHUB_REPO}/releases/latest" | jq -r .tag_name | sed 's/^v//')

# Use PyPI version as source of truth, but warn if versions don't match
if [ "$PYPI_LATEST" != "$GITHUB_LATEST" ]; then
    echo "Warning: PyPI version ($PYPI_LATEST) differs from GitHub version ($GITHUB_LATEST)"
fi

CURRENT=$(rpmspec -q --qf "%{version}\n" "$SPEC" | head -1)

if [ "$PYPI_LATEST" != "$CURRENT" ]; then
    # Update the version in the spec file
    sed -i "s/^%global pypi_version.*/%global pypi_version ${PYPI_LATEST}/" "$SPEC"
    
    # Commit and push the changes
    git add "$SPEC"
    git commit -m "Update python-autotiling to $PYPI_LATEST [build-python]"
    git push
fi
