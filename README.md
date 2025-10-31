# Red Hat AI-Ready Hooks

Pre-commit hooks to help Red Hat teams adopt AI coding assistants responsibly and maintain code quality.

## Overview

This repository provides [pre-commit](https://pre-commit.com/) hooks that enforce AI-readiness best practices for Red Hat development teams. These hooks work alongside existing Red Hat security hooks ([rh-pre-commit](https://gitlab.cee.redhat.com/infosec-public/developer-workbench/tools/-/tree/main/rh-pre-commit)) to ensure:

- Security and compliance hooks are installed
- AI context files (AGENTS.md) are high quality
- AI-assisted code is properly attributed in commits

## Quick Start

### 1. Install in Your Repository

From your repository root:

```bash
# Clone this repo or download the bootstrap script
curl -sSL https://raw.githubusercontent.com/openshift-hyperfleet/rh-hooks-ai/main/bootstrap/quick-setup.sh | bash
```

Or manually:

```bash
# Ensure pre-commit is installed
pip install pre-commit

# Add to your .pre-commit-config.yaml
cat >> .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/openshift-hyperfleet/rh-hooks-ai
    rev: main  # Use specific commit SHA in production
    hooks:
      - id: check-rh-precommit
      - id: validate-agents-md
      - id: ai-attribution-reminder
EOF

# Install the hooks
pre-commit install
```

### 2. Test the Hooks

```bash
pre-commit run --all-files
```

### 3. Make Your First Commit

The hooks will now run on every commit automatically!

## What's Included

### Hooks

#### `check-rh-precommit`
**Purpose:** Ensures [rh-pre-commit](https://gitlab.cee.redhat.com/infosec-public/developer-workbench/tools/-/tree/main/rh-pre-commit) is installed and configured.

**Behavior:**
- **Blocks commit** if `.pre-commit-config.yaml` is missing or doesn't include rh-pre-commit
- **Warns** (non-blocking) if rh-pre-commit is not installed globally

**Why it matters:** Enforces baseline security and compliance checks that all Red Hat repos should have.

#### `validate-agents-md`
**Purpose:** Requires AGENTS.md file and validates its quality.

**Behavior:**
- **Blocks commit** if `AGENTS.md` doesn't exist
- **Blocks commit** if file is empty
- **Blocks commit** if file is too short (<100 chars)

**Why it matters:** Ensures repositories have meaningful AI context for coding assistants. If a team adds this hook, they're committing to maintaining quality AI context.

**Standard:** Follows [agentsmd.net](https://agentsmd.net/)

**Note:** This hook enforces AGENTS.md presence - only add it if your team requires this file.

#### `ai-attribution-reminder`
**Purpose:** Reminds developers to attribute AI-assisted code.

**Behavior:**
- Shows a **one-time tip** per repository about using `Assisted-by:` or `Generated-by:` trailers
- Non-blocking (never prevents commits)
- Creates `.git/.ai-tip-shown` marker after first display

**Why it matters:** Encourages transparency about AI usage without being annoying.

### Templates

#### `templates/AGENTS.md.template`
A starter template for creating AI context files based on the [AGENTS.md standard](https://agentsmd.net/). Customize this for your project to help AI assistants understand your codebase.

#### `templates/gitmessage.txt`
A git commit message template that reminds developers about AI attribution trailers. Configure it locally with:

```bash
git config commit.template .gitmessage
```

### Configs

#### `configs/baseline.yaml`
An example `.pre-commit-config.yaml` that includes both rh-pre-commit and these AI-ready hooks.

## How to Use

### For Individual Developers

1. Run the quick-setup script in your repo
2. Customize AGENTS.md with project context (optional but recommended)
3. Commit as usual - hooks run automatically
4. When using AI assistants, add trailers to commit messages:
   ```
   Add user authentication feature

   Implements JWT-based auth with refresh tokens.

   Assisted-by: Claude Code
   ```

### For Team Leads

1. Add these hooks to your team's repository templates
2. Include in onboarding documentation
3. Encourage teams to create and maintain AGENTS.md files
4. Track adoption and gather feedback

### Customizing Hooks

You can selectively enable hooks in your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/openshift-hyperfleet/rh-hooks-ai
    rev: main
    hooks:
      - id: check-rh-precommit  # Always recommended
      # - id: validate-agents-md  # Optional if not using AGENTS.md
      # - id: ai-attribution-reminder  # Optional if you prefer other methods
```

## Philosophy

These hooks follow a "helpful, not annoying" philosophy:

- **Enforce security** (blocking): rh-pre-commit must be configured
- **Validate quality** (blocking): AGENTS.md must be useful if present
- **Encourage best practices** (non-blocking): Gentle reminders about attribution

We prioritize developer experience while maintaining standards.

## Development

### Repository Structure

```
rh-hooks-ai/
├── hooks/                       # Hook implementations
│   ├── check_rh_precommit.py
│   ├── validate_agents_md.py
│   └── ai_attribution_reminder.py
├── configs/
│   └── baseline.yaml            # Example config
├── templates/
│   ├── AGENTS.md.template
│   └── gitmessage.txt
├── bootstrap/
│   └── quick-setup.sh           # One-command setup
├── .pre-commit-hooks.yaml       # Hook definitions
└── README.md
```

### Testing Locally

```bash
# Test a specific hook
python hooks/check_rh_precommit.py

# Test all hooks via pre-commit
pre-commit run --all-files

# Test on specific files
pre-commit run --files AGENTS.md
```

## Resources

- **Red Hat AI Guidelines:** [Code Assistants Guidelines](https://source.redhat.com/projects_and_programs/ai/wiki/code_assistants_guidelines_for_responsible_use_of_ai_code_assistants)
- **rh-pre-commit:** [GitLab Repository](https://gitlab.cee.redhat.com/infosec-public/developer-workbench/tools/-/tree/main/rh-pre-commit)
- **AGENTS.md Standard:** [agentsmd.net](https://agentsmd.net/)
- **pre-commit Framework:** [pre-commit.com](https://pre-commit.com/)

## Contributing

Contributions welcome! This is an early MVP focused on:
- Simple, reliable hooks
- Clear documentation
- Good developer experience

Please open issues or PRs with suggestions for improvement.

## License

[TBD - Add Red Hat appropriate license]

## Maintainers

- Red Hat AI Transformation Team
- [Your Team Name/Contact]

## FAQ

### Why another pre-commit hook repository?

These hooks complement existing security hooks (rh-pre-commit) with AI-specific best practices. They work together, not as replacements.

### Do I have to use AGENTS.md?

No! The validate-agents-md hook only runs if AGENTS.md exists. It's optional but recommended for teams using AI assistants.

### Can I disable the AI attribution reminder?

Yes, simply don't include the `ai-attribution-reminder` hook in your config.

### How do I update to the latest version?

```bash
pre-commit autoupdate
```

### What if my team doesn't use AI assistants?

The `check-rh-precommit` hook is still valuable for ensuring security compliance. The AI-specific hooks are optional.

## Changelog

### v0.1.0 (Initial Release)
- Three core hooks: check-rh-precommit, validate-agents-md, ai-attribution-reminder
- Bootstrap script for easy adoption
- AGENTS.md and commit message templates
- Baseline configuration example
