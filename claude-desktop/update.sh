#!/bin/bash
# Script to check for updates to Claude Desktop and update the spec file accordingly

set -euo pipefail

SPEC="claude-desktop.spec"
VERSION_FIELD="Version:"
DOWNLOAD_URL="https://storage.googleapis.com/osprey-downloads-c02f6a0d-347c-492b-a752-3e0651722e97/nest-win-x64/Claude-Setup-x64.exe"

# Download the installer temporarily to check its version
echo "Downloading Claude Desktop installer to check version..."
TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

curl -s -L -o "$TEMP_DIR/Claude-Setup-x64.exe" "$DOWNLOAD_URL"

# Extract basic information
cd "$TEMP_DIR"
7z x -y "Claude-Setup-x64.exe" > /dev/null

# Find the nupkg file
NUPKG_FILE=$(find . -name "AnthropicClaude-*-full.nupkg" | head -1)
if [ -z "$NUPKG_FILE" ]; then
    echo "Could not find AnthropicClaude nupkg file"
    exit 1
fi

# Extract the version from the nupkg filename
LATEST=$(echo "$NUPKG_FILE" | grep -oP 'AnthropicClaude-\K[0-9]+\.[0-9]+\.[0-9]+(?=-full\.nupkg)')
echo "Latest Claude Desktop version: $LATEST"

# Get current version
CURRENT=$(rpmspec -q --qf "%{version}\n" "$SPEC" | head -1)
echo "Current spec file version: $CURRENT"

# Check if versions differ
if [ "$LATEST" != "$CURRENT" ]; then
    echo "Updating spec file to version $LATEST"
    
    # Update the spec file version
    sed -i "s/^${VERSION_FIELD}.*/${VERSION_FIELD}        ${LATEST}/" "$SPEC"
    
    # Update changelog
    TODAY=$(date "+%a %b %d %Y")
    sed -i "/%changelog/a* ${TODAY} Automated Update <auto@update.com> - ${LATEST}-1\n- Update to version ${LATEST}\n" "$SPEC"
    
    # Commit and push the changes with the build tag for prebuilt packages
    git add "$SPEC"
    git commit -m "Update claude-desktop to $LATEST [build-prebuilt]"
    git push
    
    echo "Updated $SPEC to version $LATEST"
else
    echo "Claude Desktop spec file is already at the latest version: $CURRENT"
fi
