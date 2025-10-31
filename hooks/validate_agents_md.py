#!/usr/bin/env python3
"""
Pre-commit hook to validate AGENTS.md file existence and quality.

This hook requires AGENTS.md to exist in the repository and validates
that it contains meaningful content (not empty, not just a placeholder).

Based on: https://agentsmd.net/
"""

import subprocess
import sys
from pathlib import Path


MIN_LENGTH = 100  # Minimum character count to avoid placeholder files


def is_file_committed(filename):
    """Check if a file is tracked and committed in git."""
    try:
        # Check if file is in the git index (staged or committed)
        result = subprocess.run(
            ["git", "ls-files", "--error-unmatch", filename],
            capture_output=True,
            text=True,
            timeout=5,
        )
        return result.returncode == 0
    except Exception:
        # If git command fails, assume file is not committed
        return False


def validate_agents_md():
    """Validate AGENTS.md file exists and has quality content."""
    agents_file = Path("AGENTS.md")

    # Check if file is committed to git (not just on disk)
    if not is_file_committed("AGENTS.md"):
        print("❌ ERROR: AGENTS.md is not committed to git")
        print()
        print("This repository requires an AGENTS.md file to provide context")
        print("for AI coding assistants and developers.")
        print()
        print("To fix this:")
        print("  1. Create AGENTS.md in your repository root (if it doesn't exist)")
        print("  2. Add project context, architecture, and coding guidelines")
        print("  3. Commit the file: git add AGENTS.md && git commit")
        print()
        print(
            "See template: https://github.com/openshift-hyperfleet/rh-hooks-ai/blob/main/templates/AGENTS.md.template"
        )
        print("Standard: https://agentsmd.net/")
        return False

    content = agents_file.read_text()

    # Check 1: File is not empty
    if not content.strip():
        print("❌ ERROR: AGENTS.md exists but is empty")
        print()
        print("If you include an AGENTS.md file, it should contain useful")
        print("context and instructions for AI coding assistants.")
        print()
        print("Either add content or remove the file.")
        print()
        print("See: https://agentsmd.net/")
        return False

    # Check 2: File has minimum content (not just a placeholder)
    if len(content.strip()) < MIN_LENGTH:
        print("❌ ERROR: AGENTS.md is too short (less than 100 characters)")
        print()
        print("AGENTS.md should provide meaningful context for AI tools,")
        print("such as project overview, architecture notes, or coding guidelines.")
        print()
        print("Current length:", len(content.strip()), "characters")
        print("Minimum expected:", MIN_LENGTH, "characters")
        print()
        print("See: https://agentsmd.net/")
        return False

    # All checks passed - file exists and has sufficient content
    return True


def main():
    """Main entry point for the hook."""
    if not validate_agents_md():
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
