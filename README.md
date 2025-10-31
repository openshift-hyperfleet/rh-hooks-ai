# Red Hat AI-Ready Hooks

Pre-commit hooks enforcing AI-readiness best practices for Red Hat development teams.

Currently, the hooks available from this repo have minimal scope. This serves to drive
early adoption to solicit feedback and identify additional practices that can be codified, without
significant adopter friction.

[Issues](https://github.com/openshift-hyperfleet/rh-hooks-ai/issues/new) and PRs that add hooks
for enforcing AI-enabled software development practices are welcomed!

## Installation

Run from the root of a git repo to automatically install all available `rh-hooks-ai` hooks (except version check):
```bash
curl -sSL https://raw.githubusercontent.com/openshift-hyperfleet/rh-hooks-ai/main/bootstrap/quick-setup.sh | bash
```

Or manually add to `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/openshift-hyperfleet/rh-hooks-ai
    rev: v1.0.0  # Use latest release
    hooks:
      - id: check-rh-precommit
      - id: validate-agents-md  # Optional: Remove if not using AGENTS.md
      - id: ai-attribution-reminder
      # - id: check-version  # Optional: Enable for update notifications
```

Then run:
```bash
pre-commit install
pre-commit install --hook-type pre-push
```

## Hooks

### `check-rh-precommit` (blocking)
Enforces [rh-pre-commit](https://gitlab.cee.redhat.com/infosec-public/developer-workbench/tools/-/tree/main/rh-pre-commit) configuration in `.pre-commit-config.yaml`. Blocks commits if missing.

### `validate-agents-md` (blocking, pre-push only)
Validates AGENTS.md file exists in git and contains meaningful content (>100 chars). Runs on `git push` to avoid blocking local commits. Based on [agentsmd.net](https://agentsmd.net/) standard.


### `ai-attribution-reminder` (non-blocking)
One-time reminder to use `Assisted-by:` or `Generated-by:` trailers in commit messages for AI-assisted code.

Example:
```
Add authentication feature

Implements JWT-based auth with refresh tokens.

Assisted-by: Claude Code
```

### `check-version` (non-blocking, optional)
Checks for updates once per 24 hours. Commented out by default in baseline config.

## Templates

- `templates/AGENTS.md.template` - Starter template for AI context files
- `templates/gitmessage.txt` - Commit message template with AI attribution reminder

Configure commit template:
```bash
git config commit.template .gitmessage
```

## Configuration Examples

**Minimal setup (security enforcement only):**
```yaml
repos:
  - repo: https://github.com/openshift-hyperfleet/rh-hooks-ai
    rev: v1.0.0 # Replace with latest tag
    hooks:
      - id: check-rh-precommit
```

**Full AI-ready setup:**
```yaml
repos:
  - repo: https://github.com/openshift-hyperfleet/rh-hooks-ai
    rev: v1.0.0 # Replace with latest tag
    hooks:
      - id: check-rh-precommit
      - id: validate-agents-md
      - id: ai-attribution-reminder
      - id: check-version
```

## Resources

- [Red Hat AI Code Assistants Guidelines](https://source.redhat.com/projects_and_programs/ai/wiki/code_assistants_guidelines_for_responsible_use_of_ai_code_assistants)
- [rh-pre-commit](https://gitlab.cee.redhat.com/infosec-public/developer-workbench/tools/-/tree/main/rh-pre-commit)
- [AGENTS.md Standard](https://agentsmd.net/)
- [pre-commit Framework](https://pre-commit.com/)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup, testing, and release process.
