# Publishing Guide

This document describes how to build and publish the sqlean-stubs package to PyPI.

## Publishing with uv (Recommended)

The simplest way to build and publish:

```bash
uv build && uv publish
```

This will:
1. Build the package (sdist and wheel)
2. Prompt for PyPI credentials (or use `TWINE_USERNAME` and `TWINE_PASSWORD` env vars)
3. Upload to PyPI

## Test Publishing

Test publish to TestPyPI before releasing to production:

```bash
uv build && uv publish --publish-url https://test.pypi.org/legacy/
```

Then verify the package:

```bash
pip install --index-url https://test.pypi.org/simple/ sqlean-stubs
```

## Release Process

1. Update version in `pyproject.toml` and `setup.py`:
   ```bash
   ./release.sh
   ```

2. Build and publish:
   ```bash
   uv build && uv publish
   ```

3. Verify on PyPI:
   ```bash
   pip install sqlean-stubs
   # or visit https://pypi.org/project/sqlean-stubs/
   ```

## Version Management

The version is defined in two places (keep in sync):
- `pyproject.toml`: `version = "0.0.1"`
- `setup.py`: `version="0.0.1"`

Use `./release.sh` to automate version updates.

## Authentication

PyPI authentication options:
1. Prompt at publish time (default)
2. Environment variables:
   ```bash
   export TWINE_USERNAME=__token__
   export TWINE_PASSWORD=pypi-xxx
   uv publish
   ```
3. API token stored in `.pypirc` (see PyPI docs)

## Troubleshooting

If publish fails, check:
1. Version is valid (semantic versioning: X.Y.Z)
2. Package name and classifiers are valid
3. You have PyPI account and permissions
4. Run `pip install twine` to get detailed error messages:
   ```bash
   python -m twine upload dist/*
   ```
