#!/bin/bash
#
# This script automatically checks for new git commits in the scroll repository
# and updates the spec file accordingly.
#
# Since scroll is under active development with no official releases yet,
# we use git commits as our versioning source.
#
# Intended to be run by GitHub Actions workflow

set -euo pipefail

SPEC_FILE="scroll.spec"
GITHUB_REPO="dawsers/scroll"
PACKAGE_NAME="scroll"

# Check if we're in the right directory
if [[ ! -f "$SPEC_FILE" ]]; then
    echo "Error: $SPEC_FILE not found in current directory"
    exit 1
fi

# Get current commit hash from spec
CURRENT_COMMIT=$(grep -oP '(?<=commit\s+)[a-f0-9]+' "$SPEC_FILE" | head -1)
echo "Current commit in spec: ${CURRENT_COMMIT:0:10}..."

# Get latest commit from GitHub API
LATEST_COMMIT=$(curl -s "https://api.github.com/repos/$GITHUB_REPO/commits/HEAD" | jq -r .sha)

# If GitHub API rate limit is hit or no commit is found, exit gracefully
if [[ -z "$LATEST_COMMIT" || "$LATEST_COMMIT" == "null" ]]; then
    echo "Could not determine latest commit, skipping update"
    exit 0
fi

echo "Latest commit on GitHub: ${LATEST_COMMIT:0:10}..."

# Compare commits
if [[ "$CURRENT_COMMIT" == "$LATEST_COMMIT" ]]; then
    echo "Already at latest commit, no update needed"
    exit 0
fi

# Get current date in YYYYMMDD format for the version
TODAY=$(date +"%Y%m%d")
SHORT_COMMIT="${LATEST_COMMIT:0:7}"

echo "Updating spec file to commit $SHORT_COMMIT (dated $TODAY)"

# Update commit in spec file
sed -i "s/^%global commit.*/%global commit   $LATEST_COMMIT/" "$SPEC_FILE"
sed -i "s/^%global shortcommit.*/%global shortcommit $SHORT_COMMIT/" "$SPEC_FILE"
sed -i "s/^%global commitdate.*/%global commitdate $TODAY/" "$SPEC_FILE"

# Update version in changelog example with current date and shortcommit
sed -i "s/- 0.0.1.*-1/- 0.0.1^${TODAY}git${SHORT_COMMIT}-1/" "$SPEC_FILE"

# Update changelog
DATE=$(date +"%a %b %d %Y")
PACKAGER=${PACKAGER:-"Automated Update <github-actions@github.com>"}
CHANGELOG_ENTRY="* $DATE $PACKAGER - 0.0.1^${TODAY}git${SHORT_COMMIT}-1\n- Update to latest git commit ${SHORT_COMMIT}"

# Find the changelog section and add new entry at the top
sed -i "/%changelog/a $CHANGELOG_ENTRY" "$SPEC_FILE"

echo "Committing changes"
git config --local user.name "github-actions[bot]"
git config --local user.email "41898282+github-actions[bot]@users.noreply.github.com"
git add "$SPEC_FILE"
git commit -m "Update $PACKAGE_NAME to latest commit $SHORT_COMMIT [build-gcc]"
git push

echo "Spec file updated successfully"
