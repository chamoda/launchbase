## Python Development

- We are using uv in the project. So every command you run related to python start them with `uv run`

### UV Package Management Best Practices

- **Always use `uv add` and `uv remove`** for managing project dependencies
  - `uv add <package>` - Adds package to pyproject.toml AND installs it
  - `uv remove <package>` - Removes package from pyproject.toml AND uninstalls it
  - `uv sync` - Syncs environment with pyproject.toml after manual edits

- **Avoid using `uv pip`** for project dependencies
  - `uv pip` only modifies the virtual environment without updating pyproject.toml
  - This can lead to inconsistencies between the project definition and actual environment
  - Only use `uv pip` for temporary testing or debugging

- **Examples:**
  ```bash
  # Correct way to add a dependency
  uv add "fastapi>=0.100.0"

  # Correct way to remove a dependency
  uv remove fastapi

  # If you manually edit pyproject.toml, sync the environment
  uv sync
  ```

### API Development Best Practices

- When you make any changes to APIs make sure to update requests.org file (it's emacs verb plugin file written in org mode)

## Git and Pull Request Workflow

### PR Creation Best Practices

**ALWAYS create a feature branch FIRST** before making any commits when planning to create a pull request.

**Correct Workflow:**
1. `git checkout -b feature/descriptive-name` (create feature branch first)
2. Make changes and commits on the feature branch
3. `git push -u origin feature/descriptive-name` (push feature branch)
4. Create PR from feature branch to main using `gh pr create`

**NEVER:**
- Commit directly to main when planning to create a PR
- Try to create a branch after committing to main
- This leads to "no commits between branches" errors

**Why this matters:**
- Maintains clean Git history
- Enables proper code review workflow
- Prevents merge conflicts and branch management issues
