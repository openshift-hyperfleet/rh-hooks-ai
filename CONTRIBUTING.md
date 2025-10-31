# Contributing to rh-ai-hooks

## Development Setup

```bash
# Clone the repository
git clone https://github.com/openshift-hyperfleet/rh-hooks-ai.git
cd rh-hooks-ai

# Install pre-commit
pip install pre-commit

# Install hooks (includes conventional commit enforcement)
pre-commit install --hook-type commit-msg

# Test your changes
pre-commit run --all-files
```

## Repository Structure

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

## Testing

```bash
# Test a specific hook
python hooks/check_rh_precommit.py

# Test all hooks via pre-commit
pre-commit run --all-files

# Test on specific files
pre-commit run --files AGENTS.md
```

## Commit Message Format

This project uses [Conventional Commits](https://www.conventionalcommits.org/) for automated versioning.

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Types:**
- `feat:` - New feature (minor version bump)
- `fix:` - Bug fix (patch version bump)
- `docs:` - Documentation changes
- `chore:` - Maintenance tasks
- `refactor:` - Code refactoring
- `test:` - Test changes
- `ci:` - CI/CD changes

**Examples:**
```
feat: add version checking hook
fix(hooks): correct regex pattern in validation
docs: update README with versioning info
feat!: breaking change to hook API
```

## Release Process

Releases are automated via [release-please](https://github.com/googleapis/release-please):

1. Commit changes using conventional commit format
2. Push to main branch
3. release-please creates/updates a release PR
4. When PR is merged, a new version is tagged and released
5. baseline.yaml is automatically updated with the new version

**Note:** Use merge commits (not squash) when merging release-please PRs to preserve version tags.

## Maintainers

- Red Hat AI Transformation Team
- OpenShift Hyperfleet Team
