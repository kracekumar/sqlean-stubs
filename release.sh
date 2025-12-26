#!/bin/bash
# Release script for sqlean-stubs package

set -e

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get current version
CURRENT_VERSION=$(grep '^version = ' pyproject.toml | head -1 | sed 's/version = "\(.*\)"/\1/')
echo -e "${YELLOW}Current version: ${CURRENT_VERSION}${NC}"

# Prompt for new version
read -p "Enter new version (e.g., 0.0.2): " NEW_VERSION

if [ -z "$NEW_VERSION" ]; then
    echo -e "${RED}Error: Version cannot be empty${NC}"
    exit 1
fi

# Validate version format (simple check)
if ! [[ $NEW_VERSION =~ ^[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9]+)?$ ]]; then
    echo -e "${RED}Error: Invalid version format. Use semantic versioning (e.g., 0.0.2)${NC}"
    exit 1
fi

TAG="v${NEW_VERSION}"

echo -e "${YELLOW}Preparing release ${NEW_VERSION}...${NC}"

# Update pyproject.toml
echo "Updating pyproject.toml..."
sed -i '' "s/^version = \"${CURRENT_VERSION}\"/version = \"${NEW_VERSION}\"/" pyproject.toml

# Update setup.py
echo "Updating setup.py..."
sed -i '' "s/version=\"${CURRENT_VERSION}\"/version=\"${NEW_VERSION}\"/" setup.py

# Verify files were updated
if ! grep -q "version = \"${NEW_VERSION}\"" pyproject.toml; then
    echo -e "${RED}Error: Failed to update pyproject.toml${NC}"
    exit 1
fi

if ! grep -q "version=\"${NEW_VERSION}\"" setup.py; then
    echo -e "${RED}Error: Failed to update setup.py${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Version updated to ${NEW_VERSION}${NC}"

# Commit changes
echo "Committing version changes..."
git add pyproject.toml setup.py
git commit -m "Bump version to ${NEW_VERSION}" || true

# Create git tag
echo "Creating git tag ${TAG}..."
git tag -a "${TAG}" -m "Release version ${NEW_VERSION}"

# Push changes and tag
echo "Pushing changes..."
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
