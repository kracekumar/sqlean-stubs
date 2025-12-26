#!/bin/bash
# Release script for sqlean-stubs package
# Uses version from pyproject.toml to create release tag and commit

set -e

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get version from pyproject.toml
NEW_VERSION=$(grep '^version = ' pyproject.toml | head -1 | sed 's/version = "\(.*\)"/\1/')
OLD_VERSION=$(grep '^version=' setup.py | head -1 | sed 's/.*version="\(.*\)".*/\1/')

if [ -z "$NEW_VERSION" ]; then
    echo -e "${RED}Error: Could not read version from pyproject.toml${NC}"
    exit 1
fi

echo -e "${YELLOW}Release Configuration:${NC}"
echo "  pyproject.toml version: ${NEW_VERSION}"
echo "  setup.py version: ${OLD_VERSION}"
echo ""

# Validate version format (simple check)
if ! [[ $NEW_VERSION =~ ^[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9]+)?$ ]]; then
    echo -e "${RED}Error: Invalid version format in pyproject.toml. Use semantic versioning (e.g., 0.0.2)${NC}"
    exit 1
fi

TAG="v${NEW_VERSION}"

# Update setup.py if versions don't match
if [ "$NEW_VERSION" != "$OLD_VERSION" ]; then
    echo -e "${YELLOW}Updating setup.py to match pyproject.toml...${NC}"
    sed -i '' "s/version=\"${OLD_VERSION}\"/version=\"${NEW_VERSION}\"/" setup.py
    
    if ! grep -q "version=\"${NEW_VERSION}\"" setup.py; then
        echo -e "${RED}Error: Failed to update setup.py${NC}"
        exit 1
    fi
    echo -e "${GREEN}✓ setup.py updated${NC}"
    git add setup.py
else
    echo -e "${GREEN}✓ Versions already in sync${NC}"
fi

# Commit version changes if any files changed
echo "Committing changes..."
git commit -m "Release version ${NEW_VERSION}" --allow-empty

# Create git tag
echo "Creating git tag ${TAG}..."
if git rev-parse "${TAG}" >/dev/null 2>&1; then
    echo -e "${RED}Error: Tag ${TAG} already exists${NC}"
    exit 1
fi

git tag -a "${TAG}" -m "Release version ${NEW_VERSION}"

# Push changes and tag
echo "Pushing changes and tag..."
git push origin main || git push origin master || true
git push origin "${TAG}"

echo -e "${GREEN}✓ Git push complete${NC}"
echo ""
echo -e "${YELLOW}Manual steps remaining:${NC}"
echo "1. Go to https://github.com/kracekumar/sqlean-stubs/releases"
echo "2. Find the tag '${TAG}' and click 'Create release'"
echo "3. Add release title and notes"
echo "4. Click 'Publish release'"
echo ""
echo "Or use GitHub CLI:"
echo "  gh release create ${TAG} --title 'Release ${NEW_VERSION}' --notes 'Release notes here'"
echo ""
echo -e "${GREEN}GitHub Actions will automatically publish to PyPI when release is published${NC}"
