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
The complete documentation can be found at [QCloud's documentation page](https://qcloud.dtu.dk/docs).
Usage examples and the API reference will be published there.

Below is a quick start example:
```python
from qcloud_client import JobTimeoutError, QCloudClient, TNCovariance

with QCloudClient(api_key="...") as client:
    cov = TNCovariance(nmodes=64, r_db=8, loss=0.5, basis="pi4")
    job = client.submit(cov)

    try:
        job = client.wait(job, timeout=300)
    except JobTimeoutError as e:
        print(e)
    else:
        if job.succeeded:
            print(job.result)
        else:
            print(job.error)
```

For more, see the [documentation](https://qcloud.dtu.dk/docs).

# Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md) for local setup, the branching workflow, linting and deployments.

# License
Released under the MIT License. See [LICENSE](https://github.com/qpit/qcloud-client/blob/main/LICENSE) for the full text.
