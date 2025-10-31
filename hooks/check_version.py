#!/usr/bin/env python3
"""
Pre-commit hook to check if a newer version of rh-hooks-ai is available.

This hook is non-blocking and caches results for 24 hours to avoid
slowing down commits with network calls.
"""

import json
import sys
import time
import urllib.request
from pathlib import Path


GITHUB_API_URL = (
    "https://api.github.com/repos/openshift-hyperfleet/rh-hooks-ai/releases/latest"
)
CACHE_FILE = Path(".git/.rh-hooks-version-check")
CACHE_DURATION = 24 * 60 * 60  # 24 hours in seconds
CURRENT_VERSION = "main"  # Will be replaced by actual version in pre-commit config


def get_cached_result():
    """Get cached version check result if still valid."""
    if not CACHE_FILE.exists():
        return None

    try:
        cache_data = json.loads(CACHE_FILE.read_text())
        cache_time = cache_data.get("timestamp", 0)

        # Check if cache is still valid
        if time.time() - cache_time < CACHE_DURATION:
            return cache_data.get("result")
    except Exception:
        pass

    return None


def cache_result(result):
    """Cache the version check result."""
    try:
        CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
        cache_data = {"timestamp": time.time(), "result": result}
        CACHE_FILE.write_text(json.dumps(cache_data))
    except Exception:
        # If we can't write cache, that's okay
        pass


def check_latest_version():
    """Check GitHub for the latest release version."""
    try:
        req = urllib.request.Request(GITHUB_API_URL)
        req.add_header("Accept", "application/vnd.github.v3+json")

        with urllib.request.urlopen(req, timeout=2) as response:
            data = json.loads(response.read().decode())
            return data.get("tag_name")
    except Exception:
        # Network error, GitHub down, timeout, etc. - fail silently
        return None


def compare_versions(current, latest):
    """
    Simple version comparison.
    Returns True if latest > current.
    """
    # Handle 'main' branch
    if current == "main":
        # Always suggest upgrading from main to a tagged version
        return True

    # Strip 'v' prefix if present
    current = current.lstrip("v")
    latest = latest.lstrip("v")

    # Simple string comparison (works for semantic versioning)
    return latest > current


def main():
    """Main entry point for the hook."""
    # Check cache first
    cached = get_cached_result()
    if cached is not None:
        if cached.get("update_available"):
            show_update_message(cached.get("latest_version"))
        # Always succeed (non-blocking)
        sys.exit(0)

    # Check for latest version
    latest_version = check_latest_version()

    if latest_version is None:
        # Couldn't check - cache negative result and exit
        cache_result({"update_available": False})
        sys.exit(0)

    # Compare versions
    update_available = compare_versions(CURRENT_VERSION, latest_version)

    # Cache the result
    cache_result(
        {"update_available": update_available, "latest_version": latest_version}
    )

    # Show message if update available
    if update_available:
        show_update_message(latest_version)

    # Always succeed (non-blocking)
    sys.exit(0)


def show_update_message(latest_version):
    """Show a non-blocking message about available updates."""
    print()
    print(f"📦 A newer version of rh-hooks-ai is available: {latest_version}")
    print(f"   Current: {CURRENT_VERSION}")
    print()
    print("   To update, run:")
    print("     pre-commit autoupdate")
    print()
    print("   Or manually update .pre-commit-config.yaml:")
    print(f"     rev: {latest_version}")
    print()
    print("   (This check runs once every 24 hours)")
    print()


if __name__ == "__main__":
    main()
