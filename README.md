# Kantra CLI tests

[![Nightly CLI test for main](https://github.com/konveyor-ecosystem/kantra-cli-tests/actions/workflows/nightly-main-latest.yaml/badge.svg)](https://github.com/konveyor-ecosystem/kantra-cli-tests/actions/workflows/nightly-main-latest.yaml)
[![Nightly CLI test for release-0.7](https://github.com/konveyor-ecosystem/kantra-cli-tests/actions/workflows/nightly-main-release07.yaml/badge.svg)](https://github.com/konveyor-ecosystem/kantra-cli-tests/actions/workflows/nightly-main-release07.yaml)
[![Nightly CLI test for release-0.6](https://github.com/konveyor-ecosystem/kantra-cli-tests/actions/workflows/nightly-main-release06.yaml/badge.svg)](https://github.com/konveyor-ecosystem/kantra-cli-tests/actions/workflows/nightly-main-release06.yaml)

Kantra is an experimental CLI that unifies analysis and transformation capabilities of Konveyor.

This repository contains the e2e tests for Kantra.

## Setup

1. Clone the repository
2. Navigate to the project's root folder and execute `pip install -r requirements.txt` to install the required
   dependencies.
3. Copy the `.env.example` file and remove the `.example` extension.
4. Replace each variable with your custom values.

## Run tests

### TIER0
Tier 0 includes only 1 test, analysis on tackle-testapp-public-cloud-readiness.

To run tier0 use below command:

```
$ pytest -s tests/analysis/java/test_tier0.py
```

## Code of Conduct

Refer to Konveyor's Code of Conduct [here](https://github.com/konveyor/community/blob/main/CODE_OF_CONDUCT.md).
