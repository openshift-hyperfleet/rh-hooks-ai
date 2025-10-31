#!/usr/bin/env bash
#
# Quick setup script for rh-hooks-ai
#
# This script configures a repository with AI-ready pre-commit hooks:
# 1. Installs pre-commit (if needed)
# 2. Copies baseline pre-commit config
# 3. Sets up git commit message template
# 4. Optionally adds AGENTS.md template
#
# Usage: ./bootstrap/quick-setup.sh

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Red Hat AI-Ready Hooks Setup${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Function to print status messages
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    print_error "Not in a git repository!"
    echo "Please run this script from the root of your git repository."
    exit 1
fi

print_status "Git repository detected"

# Check if pre-commit is installed
if ! command -v pre-commit &> /dev/null; then
    print_warning "pre-commit is not installed"
    echo ""
    echo "Install pre-commit using one of these methods:"
    echo "  pip install pre-commit"
    echo "  brew install pre-commit  (macOS)"
    echo "  dnf install pre-commit   (Fedora/RHEL)"
    echo ""
    read -p "Would you like to install via pip now? [y/N] " -n 1 -r </dev/tty
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        pip install --user pre-commit
        print_status "pre-commit installed"
    else
        print_error "Setup cannot continue without pre-commit"
        exit 1
    fi
else
    print_status "pre-commit is installed ($(pre-commit --version))"
fi

# GitHub raw URL for fetching template files
GITHUB_RAW="https://raw.githubusercontent.com/openshift-hyperfleet/rh-hooks-ai/main"

# Copy baseline config
if [ -f ".pre-commit-config.yaml" ]; then
    print_warning ".pre-commit-config.yaml already exists"
    read -p "Overwrite with baseline config? [y/N] " -n 1 -r </dev/tty
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        curl -fsSL "$GITHUB_RAW/configs/baseline.yaml" -o .pre-commit-config.yaml
        print_status "Baseline config downloaded to .pre-commit-config.yaml"
    else
        print_warning "Skipping config copy - using existing file"
    fi
else
    curl -fsSL "$GITHUB_RAW/configs/baseline.yaml" -o .pre-commit-config.yaml
    print_status "Baseline config downloaded to .pre-commit-config.yaml"
fi

# Install pre-commit hooks
echo ""
echo "Installing pre-commit hooks..."
pre-commit install
pre-commit install --hook-type pre-push
print_status "Pre-commit and pre-push hooks installed"

# Set up commit message template (local to this repo)
if [ -f ".gitmessage" ]; then
    print_warning ".gitmessage already exists"
else
    curl -fsSL "$GITHUB_RAW/templates/gitmessage.txt" -o .gitmessage
    git config commit.template .gitmessage
    print_status "Commit message template configured"
fi

# Offer to add AGENTS.md template
echo ""
if [ -f "AGENTS.md" ]; then
    print_status "AGENTS.md already exists"
else
    read -p "Would you like to add an AGENTS.md template? [y/N] " -n 1 -r </dev/tty
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        curl -fsSL "$GITHUB_RAW/templates/AGENTS.md.template" -o AGENTS.md
        print_status "AGENTS.md template created - please customize it!"
        echo "   Edit AGENTS.md to add project-specific context for AI assistants"
    fi
fi

# Success message
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Setup Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Next steps:"
echo "  1. Review and customize .pre-commit-config.yaml"
echo "  2. If you added AGENTS.md, fill it with project context"
echo "  3. Test hooks: pre-commit run --all-files"
echo ""
echo "Resources:"
echo "  - rh-pre-commit: https://gitlab.cee.redhat.com/infosec-public/developer-workbench/tools/-/tree/main/rh-pre-commit"
echo "  - AGENTS.md standard: https://agentsmd.net/"
echo "  - AI Guidelines: https://source.redhat.com/projects_and_programs/ai/wiki/code_assistants_guidelines_for_responsible_use_of_ai_code_assistants"
echo ""
