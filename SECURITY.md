# Security Policy

## Supported Versions

`qcloud-client` is pre-1.0. Only the most recent release receives security fixes; there are no
long-term support branches, and fixes are not backported to earlier minor versions.

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |
| < 0.1   | :x:                |

If you are running an older version, upgrade to the latest release before reporting an issue.

## Reporting a Vulnerability
**Please do not report security vulnerabilities through public GitHub issues, pull requests, or
discussions.**

Report privately through GitHub Security Advisories:

1. Go to the [Security tab](https://github.com/qpit/qcloud-client/security) of this repository.
2. Select **Report a vulnerability**.
3. Fill in the advisory form.

This opens a private channel visible only to the maintainers. If you are unable to use GitHub
Security Advisories, contact a maintainer listed in
[CODEOWNERS](https://github.com/qpit/qcloud-client/blob/main/.github/CODEOWNERS) directly.

### What to include
A report is easiest to act on when it contains:

- The version of `qcloud-client` and the Python version you are running.
- A description of the vulnerability and its impact.
- Steps to reproduce, ideally a minimal proof of concept.
- Any suggested mitigation, if you have one.
