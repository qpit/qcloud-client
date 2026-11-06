# Security Policy

## Supported Versions
Only the latest release of the current major version receives security fixes.

| Version | Supported          |
| ------- | ------------------ |
| 1.x     | :white_check_mark: |
| < 1.0.0 | :x:                |

If you are running an older version, upgrade to the latest release before reporting an issue.

## Reporting a Vulnerability
**Please do not report security vulnerabilities through public GitHub issues, pull requests, or
discussions.**

Report privately through GitHub Security Advisories:

1. Go to the [Security tab](https://github.com/qpit/qcloud-client/security) of this repository.
2. Select **Report a vulnerability** (or use [this direct link](https://github.com/qpit/qcloud-client/security/advisories/new)).
3. Fill in the advisory form.

This opens a private channel visible only to the maintainers.
If you are unable to use GitHub Security Advisories, open a public issue that only asks for a private way to contact the maintainers.
Do not include any details of the vulnerability in that issue.

### What to include
A report is easiest to act on when it contains:

- The version of `qcloud-client` and the Python version you are running.
- A description of the vulnerability and its impact.
- Steps to reproduce, ideally a minimal proof of concept.
- Any suggested mitigation, if you have one.

Please do not include real API keys in a report, and use a placeholder value instead.

## Scope
This policy covers the `qcloud-client` Python package in this repository.
Vulnerabilities in the [QCloud service](https://qcloud.dtu.dk) itself (frontend and backend) can be reported the same way.
