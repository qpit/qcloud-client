# QCloud Client

[![CodeQL](https://github.com/qpit/qcloud-client/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/qpit/qcloud-client/actions/workflows/github-code-scanning/codeql)
[![Lint](https://github.com/qpit/qcloud-client/actions/workflows/lint.yml/badge.svg?branch=main)](https://github.com/qpit/qcloud-client/actions/workflows/lint.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/qpit/qcloud-client/blob/main/LICENSE)

- [Overview](#overview)
- [Setup](#setup)
    - [Requirements](#requirements)
    - [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

# Overview
GitHub repository for the Python API wrapper for [QCloud](https://qcloud.dtu.dk), the quantum computing service operated by QPIT at the Technical University of Denmark.

> [!WARNING]
> The package is in early development and is not yet ready for stable public use. Expect breaking changes between minor versions until `1.0.0`.

# Setup
## Requirements
- Python 3.11 or newer
- An account on [QCloud](https://qcloud.dtu.dk)

## Installation
You can install the package from PyPI:
```bash
pip install qcloud-client
```

To install the latest unreleased code directly from the repository, run:
```bash
pip install git+https://github.com/qpit/qcloud-client.git@develop
```

# Usage
The public interface is not yet implemented. Usage examples will be published here alongside the first release that exposes a client.

Import the package using `import qcloud_client`

# Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md) for local setup, the branching workflow, linting and deployments.

# License
Released under the MIT License. See [LICENSE](https://github.com/qpit/qcloud-client/blob/main/LICENSE) for the full text.
