# Publishing Guide

This document describes how to build and publish the sqlean-stubs package.

## Automated Publishing (Recommended)

The package is automatically published to PyPI when you create a GitHub release.

### Step-by-Step Release Process

#### 1. Update Version Numbers

Update the version in both files (must match):

```bash
# Edit pyproject.toml
version = "0.0.2"

# Edit setup.py  
version="0.0.2"
```

#### 2. Commit Version Changes

```bash
git add pyproject.toml setup.py
git commit -m "Bump version to 0.0.2"
git push origin main
```

#### 3. Create GitHub Release

**Option A: Via GitHub Web UI (Easiest)**

1. Go to https://github.com/kracekumar/sqlean-stubs/releases
2. Click "Draft a new release" button
3. Fill in the form:
   - **Choose a tag**: Click "Create new tag" and enter `v0.0.2` (must match version)
   - **Release title**: `Release 0.0.2` or `v0.0.2`
   - **Description**: Add release notes (optional but recommended):
     ```
     ## Changes
     - Feature 1
     - Bug fix 2
     - Improvement 3
     
     ## Installation
     ```bash
     pip install sqlean-stubs==0.0.2
     ```
     ```
4. Click "Publish release"

**Option B: Via GitHub CLI**

```bash
# Install GitHub CLI if not present
# See: https://cli.github.com/

# Create and publish release
gh release create v0.0.2 --title "Release 0.0.2" --notes "Release notes here"

# Or with release notes from file
gh release create v0.0.2 --title "Release 0.0.2" -F RELEASE_NOTES.md
```

**Option C: Via Git Tags**

```bash
# Create and push tag
git tag -a v0.0.2 -m "Release version 0.0.2"
git push origin v0.0.2

# Then create release via web UI using the tag
```

#### 4. Verify Publication

The GitHub Actions workflow (`publish.yml`) will automatically:
1. Detect the release publication
2. Build the package (sdist and wheel)
3. Publish to PyPI using trusted publishers

Check the workflow:
- Go to https://github.com/kracekumar/sqlean-stubs/actions
- Find the "Publish to PyPI" workflow
- Verify it succeeded

Verify on PyPI:
```bash
# Check package is available
pip install --dry-run sqlean-stubs==0.0.2

# Or visit https://pypi.org/project/sqlean-stubs/
```

The GitHub Actions workflow (`publish.yml`) will:
- Trigger on release publication
- Build the package (sdist and wheel)
- Publish to PyPI using trusted publishers (no password needed)

## Manual Publishing (Local)

If you need to publish locally:

### Prerequisites

```bash
# Install build tools
pip install build twine
```

### Build the Package

```bash
# Build sdist and wheel
python -m build

# This creates:
# - dist/sqlean_stubs-0.0.1.tar.gz (source distribution)
# - dist/sqlean_stubs-0.0.1-py3-none-any.whl (wheel)
```

### Publish to PyPI

```bash
# Using twine (recommended)
python -m twine upload dist/*

# You'll be prompted for your PyPI API token
# Or set environment variable: TWINE_PASSWORD=pypi-xxx
```

### Test on TestPyPI First (Optional)

```bash
# Build package
python -m build

# Upload to test repository
python -m twine upload --repository testpypi dist/*

# Install from test to verify
pip install --index-url https://test.pypi.org/simple/ sqlean-stubs
```

## Version Management

The version is defined in two places:

1. **pyproject.toml**: `version = "0.0.1"` (recommended source)
2. **setup.py**: `version="0.0.1"` (kept for backwards compatibility)

Keep these in sync when releasing.

## PyPI Configuration

The package uses trusted publishers for PyPI authentication:
- No password/API token stored in repo
- Authentication via GitHub OIDC token
- Configured in GitHub repository settings

To set up for your fork:
1. Go to repository Settings → Environments
2. Create or verify `pypi` environment exists
3. GitHub Actions automatically uses OIDC for authentication

## Verifying Publication

```bash
# Check package on PyPI
pip install sqlean-stubs

# Or check on PyPI website
# https://pypi.org/project/sqlean-stubs/

# List available versions
pip index versions sqlean-stubs
```
