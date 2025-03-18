#!/usr/bin/env python3
"""
Linting script for the X.com Poster project.
This script checks code quality and ensures files end with a newline.
"""

import os
import sys
import subprocess
from pathlib import Path


def ensure_newlines(directory="."):
    """Check all Python files to ensure they end with a newline."""
    python_files = list(Path(directory).glob("**/*.py"))
    fixed_files = []

    for file_path in python_files:
        # Skip virtual environment files
        if "venv" in str(file_path):
            continue

        with open(file_path, "r") as f:
            content = f.read()

        if content and not content.endswith("\n"):
            with open(file_path, "a") as f:
                f.write("\n")
            fixed_files.append(file_path)
            print(f"Added newline to {file_path}")

    return fixed_files


def run_flake8():
    """Run flake8 linting."""
    print("\nRunning flake8...")
    result = subprocess.run(
        ["flake8", "--exclude=venv,__pycache__"], capture_output=True, text=True
    )
    if result.returncode != 0:
        print("Flake8 found issues:")
        print(result.stdout)
        return False
    else:
        print("Flake8: No issues found!")
        return True


def run_black(check_only=True):
    """Run black formatter."""
    print("\nRunning black...")
    cmd = ["black", ".", "--exclude", "venv"]
    if check_only:
        cmd.append("--check")

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("Black found formatting issues:")
        print(result.stdout)
        return False
    else:
        print("Black: Code is properly formatted!")
        return True


def main():
    """Run all linting checks."""
    print("Running linting checks for X.com Poster project...")

    # Check if tools are installed
    try:
        subprocess.run(["flake8", "--version"], capture_output=True, check=True)
        subprocess.run(["black", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: Linting tools not found. Please install with:")
        print("pip install flake8 black")
        sys.exit(1)

    # Process arguments
    check_only = True
    if len(sys.argv) > 1 and sys.argv[1] == "--fix":
        check_only = False

    # Check for missing newlines
    fixed_files = ensure_newlines()

    # Run linters
    flake8_passed = run_flake8()
    black_passed = run_black(check_only)

    # Report results
    if fixed_files:
        print(f"\nAdded newlines to {len(fixed_files)} files.")
    else:
        print("\nNo files missing newlines.")

    if flake8_passed and black_passed and not fixed_files:
        print("\n✅ All checks passed!")
        return 0
    elif not check_only and (not flake8_passed or not black_passed):
        print("\n⚠️  Some issues were found but fixable ones were addressed.")
        return 0
    else:
        print(
            "\n❌ Some issues were found. Run with --fix to attempt to fix formatting issues."
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
