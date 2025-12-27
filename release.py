#!/usr/bin/env python3
"""Release script for sqlean-stubs package."""

import argparse
import re
import subprocess
import sys
from configparser import ConfigParser
from configparser import Error as ConfigParserError
from pathlib import Path


class Colors:
    """Terminal colors."""

    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    RESET = "\033[0m"


def print_header(text: str) -> None:
    """Print a formatted header."""
    separator = "=" * 60
    print(f"\n{Colors.YELLOW}{separator}{Colors.RESET}")
    print(f"{Colors.YELLOW}{text}{Colors.RESET}")
    print(f"{Colors.YELLOW}{separator}{Colors.RESET}\n")


def print_success(text: str) -> None:
    """Print a success message."""
    print(f"{Colors.GREEN}✓ {text}{Colors.RESET}\n")


def print_error(text: str) -> None:
    """Print an error message."""
    print(f"{Colors.RED}✗ {text}{Colors.RESET}\n")


def run_command(cmd: str, check: bool = True) -> tuple[int, str, str]:
    """Run a shell command and return exit code, stdout, and stderr."""
    print(f"{Colors.BLUE}→ {cmd}{Colors.RESET}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=False)
    if check and result.returncode != 0:
        print_error(result.stderr or f"Command failed with exit code {result.returncode}")
        sys.exit(1)
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def read_version_from_pyproject() -> str:
    """Read version from pyproject.toml."""
    pyproject = Path("pyproject.toml")
    if not pyproject.exists():
        print_error("pyproject.toml not found")
        sys.exit(1)

    with open(pyproject) as f:
        for line in f:
            if line.startswith("version = "):
                match = re.search(r'version = "([^"]+)"', line)
                if match:
                    return match.group(1)

    print_error("Could not read version from pyproject.toml")
    sys.exit(1)


def update_version_in_pyproject(new_version: str) -> None:
    """Update version in pyproject.toml using uv."""
    run_command(f"uv version {new_version}")
    print_success(f"Updated version to {new_version}")


def validate_version(version: str) -> None:
    """Validate version format (semantic versioning)."""
    if not re.match(r"^[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9]+)?$", version):
        print_error(f"Invalid version format '{version}'. Use semantic versioning (e.g., 0.0.2)")
        sys.exit(1)


def read_pypi_token() -> str:
    """Read PyPI token from ~/.pypirc.

    Expected format:
    [pypi]
    username = __token__
    password = pypi-...
    """
    pypirc = Path.home() / ".pypirc"
    if not pypirc.exists():
        print_error("~/.pypirc not found. Please create it with your PyPI token.\n")
        print("Expected format:")
        print("[pypi]")
        print("username = __token__")
        print("password = pypi-AgEIcHlwaS5vcmc...")
        sys.exit(1)

    config = ConfigParser()
    try:
        config.read(pypirc)
    except Exception as e:
        print_error(f"Failed to parse ~/.pypirc: {e}")
        sys.exit(1)

    try:
        if "pypi" not in config.sections():
            print_error("No [pypi] section found in ~/.pypirc")
            sys.exit(1)

        if not config.has_option("pypi", "password"):
            print_error("No 'password' option found in [pypi] section of ~/.pypirc")
            sys.exit(1)

        token = config.get("pypi", "password")

        if not token or not isinstance(token, str):
            print_error("PyPI token is empty or invalid in ~/.pypirc")
            sys.exit(1)

        # Validate token starts with 'pypi-'
        if not token.startswith("pypi-"):
            print_error("PyPI token should start with 'pypi-'. Check ~/.pypirc")
            sys.exit(1)

        return token.strip()
    except ConfigParserError as e:
        print_error(f"Failed to read PyPI token from ~/.pypirc: {e}")
        sys.exit(1)


def build_package() -> None:
    """Build the package."""
    print("Building package...")
    run_command("uv build")
    print_success("Build complete")


def publish_to_pypi(token: str) -> None:
    """Publish package to PyPI."""
    print("Publishing to PyPI...")
    print("(Authenticating using PyPI token from ~/.pypirc)\n")

    # Use uv publish with username and password flags
    cmd = f'uv publish --username __token__ --password "{token}"'
    run_command(cmd)

    print_success("Published to PyPI")


def create_github_release(version: str) -> None:
    """Create a GitHub release."""
    print("Creating GitHub release...")

    # Check if gh CLI is available
    returncode, _, _ = run_command("which gh", check=False)
    if returncode != 0:
        print(
            f"{Colors.YELLOW}⚠ GitHub CLI (gh) not found. Skipping GitHub release creation.{Colors.RESET}"
        )
        print(f"{Colors.YELLOW}  Install from https://cli.github.com/{Colors.RESET}\n")
        return

    tag = f"v{version}"

    # Create release
    run_command(
        f'gh release create {tag} --title "Release {version}" '
        f'--notes "Version {version} released to PyPI"',
        check=False,
    )
    print_success(f"GitHub release created: {tag}")


def commit_and_push(version: str) -> None:
    """Commit and push changes."""
    print("Committing and pushing changes...")
    run_command("git add pyproject.toml")

    # Commit with check=False to handle pre-commit hooks
    returncode, stdout, stderr = run_command(
        f'git commit -m "Bump version to {version}"', check=False
    )
    if returncode != 0:
        print_error(f"Git commit failed (possibly due to pre-commit hooks): {stderr}")
        sys.exit(1)

    # Get current branch
    returncode, branch, stderr = run_command("git rev-parse --abbrev-ref HEAD", check=False)
    if returncode != 0:
        print_error(f"Failed to get current branch: {stderr}")
        sys.exit(1)

    # Push to current branch
    returncode, stdout, stderr = run_command(f"git push origin {branch}", check=False)
    if returncode != 0:
        print_error(f"Failed to push to {branch}: {stderr}")
        sys.exit(1)

    print_success("Changes pushed")


def main() -> None:
    """Main release function."""
    parser = argparse.ArgumentParser(
        description="Release sqlean-stubs to PyPI and GitHub",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python release.py              # Use current version in pyproject.toml
  python release.py 0.0.3        # Update to version 0.0.3 and release
        """,
    )
    parser.add_argument(
        "version",
        nargs="?",
        help="Version to release (e.g., 0.0.3). If not provided, uses current version in pyproject.toml",
    )
    args = parser.parse_args()

    print_header("SQLean-Stubs Release")

    # Get or validate version
    if args.version:
        validate_version(args.version)
        new_version = args.version
        print(f"{Colors.YELLOW}Release Configuration:{Colors.RESET}")
        print(f"  Target version: {new_version}\n")
        update_version_in_pyproject(new_version)
    else:
        new_version = read_version_from_pyproject()
        print(f"{Colors.YELLOW}Release Configuration:{Colors.RESET}")
        print(f"  pyproject.toml version: {new_version}\n")

    # Validate version format
    validate_version(new_version)

    # Commit and push
    commit_and_push(new_version)

    # Build package
    build_package()

    # Read PyPI token
    print("Reading PyPI credentials...")
    token = read_pypi_token()
    print_success("Credentials loaded")

    # Publish to PyPI
    publish_to_pypi(token)

    # Create GitHub release
    create_github_release(new_version)

    # Summary
    print_header("Release Complete!")
    print(f"{Colors.GREEN}Version {new_version} released successfully!{Colors.RESET}\n")
    print("Verify on PyPI:")
    print(f"  pip install sqlean-stubs=={new_version}")
    print("  https://pypi.org/project/sqlean-stubs/\n")


if __name__ == "__main__":
    main()
