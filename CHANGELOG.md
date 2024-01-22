# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## Unreleased

## v0.1.2 (2024-01-22)

### Fixed

- An empty line (whitespace only) did not end the sorting block.
  Now it does.

## v0.1.1 (2024-01-22)

### Fixed

- `pre-commit` example configuration in README used an incorrect project/hook name
- The package was not built correctly, causing an error:

  ```pytb
  ModuleNotFoundError: No module named 'sort_lines'
  ``````

## v0.1.0 (2024-01-22)

First release.
