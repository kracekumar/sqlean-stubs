# Branch Protection Configuration

This document describes the required GitHub Actions checks that must pass before merging PRs.

## Required Status Checks

To enforce these checks on the `main` branches, follow these steps:

1. Go to your repository settings: **Settings** → **Branches**
2. Under "Branch protection rules", click **Add rule**
3. Configure for branch name pattern: `main`
4. Enable the following settings:
   - ✅ **Require a pull request before merging**
   - ✅ **Require status checks to pass before merging**
   - ✅ **Require branches to be up to date before merging**

5. Search for and select these required status checks:
   - `test (3.9)`
   - `test (3.10)`
   - `test (3.11)`
   - `test (3.12)`
   - `test (3.13)`
   - `test (3.14)`
   - `lint`
   - `type-check`

## What Each Check Does

- **test (3.x)**: Runs pytest, mypy, and ty checks on the specified Python version
- **lint**: Runs ruff linting and formatting checks
- **type-check**: Runs mypy and ty type checking
