#!/usr/bin/env python3
"""
Pre-commit hook to remind developers about AI attribution in commit messages.

This hook shows a one-time tip per repository about using Assisted-by: and
Generated-by: trailers for AI-assisted code contributions.

This is non-blocking and only displays once per repository.
"""

import sys
from pathlib import Path


MARKER_FILE = Path(".git/.ai-tip-shown")


def show_reminder():
    """Show the AI attribution reminder if not already shown."""
    # Check if we've already shown the tip in this repo
    if MARKER_FILE.exists():
        # Already shown, skip
        return True

    # Show the one-time reminder (write to stderr so pre-commit displays it)
    print(file=sys.stderr)
    print(
        "💡 Reminder: For AI-assisted commits, consider adding a trailer:",
        file=sys.stderr,
    )
    print(file=sys.stderr)
    print("    Assisted-by: Claude Code", file=sys.stderr)
    print("    Generated-by: GitHub Copilot", file=sys.stderr)
    print(file=sys.stderr)
    print(
        "A commit template has been configured in this repo to remind you.",
        file=sys.stderr,
    )
    print("Use 'git commit' (without -m) to see it in your editor.", file=sys.stderr)
    print(file=sys.stderr)
    print("Learn more:", file=sys.stderr)
    print(
        "  https://source.redhat.com/projects_and_programs/ai/wiki/code_assistants_guidelines_for_responsible_use_of_ai_code_assistants",
        file=sys.stderr,
    )
    print(file=sys.stderr)
    print("(This reminder will only be shown once per repository)", file=sys.stderr)
    print(file=sys.stderr)

    # Create marker file so we don't show again
    try:
        MARKER_FILE.parent.mkdir(parents=True, exist_ok=True)
        MARKER_FILE.touch()
    except Exception:
        # If we can't create the marker, that's okay - we'll show the reminder again next time
        pass

    # Non-blocking, always succeed
    return True


def main():
    """Main entry point for the hook."""
    show_reminder()
    sys.exit(0)


if __name__ == "__main__":
    main()
