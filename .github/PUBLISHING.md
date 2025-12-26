# Publishing Guide

This document describes how to build and publish the sqlean-stubs package to PyPI and GitHub.

## Full Release Process

The simplest way to release:

```bash
# Release using current version in pyproject.toml
python release.py

# Or specify a new version
python release.py 0.0.3
```

This will:
1. Update version in `pyproject.toml` (if specified)
2. Commit changes to git
3. Push to origin
4. Build the package (sdist and wheel)
5. Publish to PyPI using `~/.pypirc` token
6. Create a GitHub release

## Prerequisites

### PyPI Authentication

1. Create `~/.pypirc`:
```ini
[distutils]
index-servers =
    pypi

[pypi]
username = __token__
password = pypi-AgEIcHlwaS5vcmc...
```

2. Get token from https://pypi.org/manage/account/token/
3. Replace `pypi-AgEIcHlwaS5vcmc...` with your actual token

### GitHub Release (Optional)

Install GitHub CLI to enable automatic GitHub release creation:

```bash
# macOS
brew install gh

# Linux
# Visit https://cli.github.com/

# Windows
# Visit https://cli.github.com/
```

Authenticate:
```bash
gh auth login
```

## Manual Publishing

For build and publish separately:

```bash
# Build only
uv build

# Publish to PyPI
uv publish
```

Environment variables for publish (alternative to ~/.pypirc):
```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-AgEIcHlwaS5vcmc...
uv publish
```

## Test Publishing

Test publish to TestPyPI before releasing to production:

```bash
uv build && uv publish --publish-url https://test.pypi.org/legacy/
```

Then verify the package:

```bash
pip install --index-url https://test.pypi.org/simple/ sqlean-stubs
```

## Version Management

The version is defined in `pyproject.toml`:
```toml
version = "0.0.1"
```

You can:
- Update manually, then run `python release.py`
- Let release.py update it: `python release.py 0.0.2`

## Troubleshooting

### Release fails with "pyproject.toml not found"
Ensure you're running from the repository root.

### "PyPI token not found in ~/.pypirc"
Check that `~/.pypirc` exists and has the correct format with `[pypi]` section and `password = pypi-...`

### "GitHub CLI (gh) not found"
Install gh from https://cli.github.com/ or run the release script without GitHub CLI (it will skip GitHub release creation).

### Publishing fails with authentication error
Ensure your PyPI token is valid at https://pypi.org/manage/account/token/

## Version Constraints

- Must use semantic versioning: `MAJOR.MINOR.PATCH` or `MAJOR.MINOR.PATCH-PRERELEASE`
- Examples: `0.0.1`, `0.1.0`, `1.0.0-alpha`, `1.0.0-beta.1`
