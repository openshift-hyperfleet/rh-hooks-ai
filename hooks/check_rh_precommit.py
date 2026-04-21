#!/usr/bin/env python3
"""
Pre-commit hook to ensure rh-pre-commit is installed and configured.

This hook:
1. Checks if .pre-commit-config.yaml exists and contains rh-pre-commit
2. Warns (non-blocking) if rh-pre-commit is not installed globally
"""

import sys
import subprocess
from pathlib import Path


RH_PRECOMMIT_URL = "https://gitlab.cee.redhat.com/infosec-public/developer-workbench/tools/-/tree/main/rh-pre-commit?ref_type=heads"


def check_local_config():
    """Check if a pre-commit config exists and contains rh-pre-commit."""
    yaml_config = Path(".pre-commit-config.yaml")
    toml_config = Path("prek.toml")

    if yaml_config.exists():
        config_file = yaml_config
    elif toml_config.exists():
        config_file = toml_config
    else:
        print("❌ ERROR: No pre-commit configuration found in repository root")
        print()
        print("This repository requires a pre-commit configuration file.")
        print("Please create one of:")
        print("  - .pre-commit-config.yaml (for pre-commit)")
        print("  - prek.toml (for prek)")
        return False

    content = config_file.read_text()

    if "rh-pre-commit" not in content:
        print(f"❌ ERROR: {config_file} does not include rh-pre-commit")
        print()
        print(
            "Red Hat repositories should include rh-pre-commit hooks for security/compliance."
        )
        print()
        if config_file == yaml_config:
            print("Add this to your .pre-commit-config.yaml:")
            print("  repos:")
            print(
                "    - repo: https://gitlab.cee.redhat.com/infosec-public/developer-workbench/tools"
            )
            print("      rev: rh-pre-commit-2.3.2")
            print("      hooks:")
            print("        - id: rh-pre-commit")
        else:
            print("Add this to your prek.toml:")
            print("  [[repos]]")
            print(
                '  repo = "https://gitlab.cee.redhat.com/infosec-public/developer-workbench/tools"'
            )
            print('  rev = "rh-pre-commit-2.3.2"')
            print("  hooks = [")
            print('    { id = "rh-pre-commit" }')
            print("  ]")
        print()
        print(f"Learn more: {RH_PRECOMMIT_URL}")
        return False

    return True


def check_global_config():
    """Check if rh-pre-commit is installed globally (warning only)."""
    try:
        # Check if pre-commit is installed
        result = subprocess.run(
            ["pre-commit", "--version"], capture_output=True, text=True, timeout=5
        )

        if result.returncode != 0:
            return  # pre-commit not installed, skip global check

        # Check global git config for pre-commit template
        result = subprocess.run(
            ["git", "config", "--global", "init.templateDir"],
            capture_output=True,
            text=True,
            timeout=5,
        )

        template_dir = result.stdout.strip()

        if not template_dir or not Path(template_dir).exists():
            print()
            print("⚠️  WARNING: rh-pre-commit does not appear to be installed globally")
            print()
            print(
                "For system-wide security, consider installing rh-pre-commit globally"
            )
            print("so all new repositories automatically get these hooks.")
            print()
            print(f"Installation instructions: {RH_PRECOMMIT_URL}")
            print()
            print("(This is just a warning - your commit will proceed)")
            print()

    except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
        # If we can't check, don't show warnings
        pass


def main():
    """Main entry point for the hook."""
    # Always check local config (blocking)
    if not check_local_config():
        sys.exit(1)

    # Check global config (non-blocking warning)
    check_global_config()

    # Success
    sys.exit(0)


if __name__ == "__main__":
    main()
