#!/bin/bash
# Build script for sqlean-stubs package

set -e

echo "Building sqlean-stubs..."
uv build

echo ""
echo "Build complete. Artifacts in dist/"
echo ""
echo "To publish to PyPI:"
echo "  uv publish"
echo ""
echo "To publish to TestPyPI:"
echo "  uv publish --publish-url https://test.pypi.org/legacy/"
