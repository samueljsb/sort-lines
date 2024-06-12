# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## Unreleased

## v0.3.0 (2024-06-13)

### Changed

- Return 0 when lines have been sorted successfully.

  A non-zero return code is reserved for when the tool has not been able to do its job.

## v0.2.0 (2024-06-06)

### Added

- The pragma can be passed options: `pragma: alphabetize[options]`.

  Option                   | Effect
  ------------------------ | --------------------------------------------
  `cs`, `case-sensitive`   | all upper-case letters before all lower-case
  `ci`, `case-insensitive` | sorted without regard for case

  The default behaviour remains case-sensitive.

- The default case-sensitivity can be controlled on the command line.

  Use `--case-insensitive` to make all sorting case-insensitive
  unless specified to be case-sensitive explicitly.
  `--case-sensitive` can also be used;
  this is the default.

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
