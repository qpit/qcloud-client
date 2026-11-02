# Contributing

- [Local Setup](#local-setup)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
- [Making Changes](#making-changes)
    - [Branches](#branches)
    - [Pull Requests](#pull-requests)
    - [Deployments](#deployments)
- [Testing](#testing)
    - [Linting](#linting)
- [Reporting Bugs](#reporting-bugs)

# Local Setup
## Prerequisites
You need Python 3.11 or newer and Git.

## Installation
1. Fork the repository (external contributors) or clone it directly (maintainers):
```bash
# Contributors: clone your fork
git clone https://github.com/<your-username>/qcloud-client.git

# Maintainers
git clone https://github.com/qpit/qcloud-client.git

cd qcloud-client
```

2. Create an activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install the package in editable mode together with development tools:
```bash
pip install -e ".[dev]"
```

> [!NOTE]
> The package version is generated from Git tags when you install the package, and is written to `qcloud_client/_version.py`. Do not edit or commit that file.

# Making Changes
## Branches
| Branch                      | Purpose                                                                       |
|-----------------------------|-------------------------------------------------------------------------------|
| `main`                      | Released code only. Updated by merging `develop` when a release is made.      |
| `develop`                   | Integration branch. All feature branches start from here and are merged here. |
| `feat/*`, `fix/*`, `test/*` | Short-lived branches for a single change, for example `fix/header-override`.  |

Never push directly to `main` or `develop`, as they are protected branches.
Keep branches small and focused on one change.

To start working on a change:
```bash
git switch develop
git pull
git switch -c fix/header-override
```

## Pull Requests
Open pull requests against `develop`.
In the description, explain what changed and why, and link the issue it closes if there is one.
A pull request is merged once the automated tests pass and a maintainer has approved it.

## Deployments
Releases are published to [PyPI](https://pypi.org/project/qcloud-client/) automatically by a GitHub Actions workflow using PyPI Trusted Publishing.
Only maintainers of this repository can create releases.

Versions follow [Semantic Versioning](https://semver.org).
The version number comes from the Git tag, so there is no version string to edit in the code.

How to make a release:
1. Make sure `develop` is green, with all linting and tests passing on the latest commit.
2. Open a pull request from `develop` to `main` and merge it once approved.
3. Create a tag on the merge commit on `main` and push it:
```bash
git switch main
git pull
git tag v1.1.0
git push origin v1.1.0
```
4. Approve the publish job manually on GitHub. A GitHub release with release notes is created automatically for the new version.

A version cannot be replaced once it is published to PyPI.
If a release turns out to be broken, fix the problem and push a new patch version.
If needed, yank the broken build on PyPI so that it is no longer available for users to install.

# Testing
## Linting
Code linting checks are performed by the Ruff package.
Read more here: https://docs.astral.sh/ruff/

To perform linting checks, run:
```bash
ruff check .
```

The linting rules can be configured in the `.ruff.toml` file found in the project's root directory with the available rules listed here: https://docs.astral.sh/ruff/rules/

# Reporting Bugs
Bugs and feature requests should be submitted in the [issue tracker](https://github.com/qpit/qcloud-client/issues).
Please include the `qcloud-client` and Python versions and a minimal example that reproduces the problem.

Do not report security vulnerabilities in public issues.
Follow [SECURITY.md](https://github.com/qpit/qcloud-client/blob/main/SECURITY.md) instead.
