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

# Push changes
echo "Pushing changes..."
git push origin main || git push origin master || true

echo -e "${GREEN}✓ Version updated and pushed${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Build and publish: uv build && uv publish"
echo ""
echo "Or test publish to TestPyPI first:"
echo "  uv build && uv publish --publish-url https://test.pypi.org/legacy/"
