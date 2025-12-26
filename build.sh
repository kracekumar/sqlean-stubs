#!/bin/bash
# Build script for sqlean-stubs package

set -e

echo "Building sqlean-stubs..."

# Clean previous builds
rm -rf build/ dist/ sqlean_stubs.egg-info/

# Install build tools if not present
if ! command -v python -m build &> /dev/null; then
    echo "Installing build tools..."
    pip install --upgrade build wheel
fi

# Build
python -m build

echo "Build complete. Artifacts in dist/"
echo ""
echo "To publish to PyPI:"
echo "  python -m twine upload dist/*"
echo ""
echo "To publish to TestPyPI:"
echo "  python -m twine upload --repository testpypi dist/*"
