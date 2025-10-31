# Red Hat AI-Ready Hooks

Pre-commit hooks enforcing AI-readiness best practices for Red Hat development teams.

Currently, the hooks available from this repo have minimal scope. This serves to drive
early adoption to solicit feedback and identify additional practices that can be codified, without
significant adopter friction.

[Issues](https://github.com/openshift-hyperfleet/rh-hooks-ai/issues/new) and PRs that add hooks
for enforcing AI-enabled software development practices are welcomed!

## Installation

First, navigate to the repository that you want to configure with Red Hat security and AI-readiness practices.

Then run the quick setup script:

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
pre-commit run --all-files # Test
```

**First-time setup note:** If this is your first time running `pre-commit run --all-files` with rh-pre-commit on this machine, the command may fail with an authentication error. If you see "Could not find pattern server auth token!", follow the instructions in the error message to authenticate:

```bash
python3 -m rh_gitleaks login
```

After logging in and copying the authentication token when prompted, re-run `pre-commit run --all-files` to complete the setup.

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

## Important: What to Commit vs. Ignore

**DO commit** `.pre-commit-config.yaml` to your repository - this is a repository-wide configuration that ensures all contributors run the same security and quality checks. It should never be added to `.gitignore`.

**DO add to `.gitignore`:** `.gitmessage` - this is a personal workflow file that each developer can customize locally. The quick-setup script generates it automatically for each user.

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
