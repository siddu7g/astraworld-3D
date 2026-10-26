# Security Policy

## Supported Scope

This repository is a CLI-first open-source project for:

- Marble world generation wrappers
- local OpenUSD scene composition
- Marble PLY to Isaac conversion helpers

## Reporting A Vulnerability

Please do not open a public issue for undisclosed vulnerabilities.

Instead, contact the maintainer privately with:

- a description of the issue
- impact and affected workflow
- reproduction steps or a proof of concept
- any suggested mitigation

## Secrets And Sensitive Data

- Never commit API keys.
- Put user-provided credentials only in `.env`.
- Treat generated scenes and exported assets as potentially sensitive if they contain proprietary environments.

## Dependency And Runtime Notes

- The repo depends on external services such as World Labs Marble and local Isaac Sim installs.
- Validate third-party updates carefully, especially around `usd-core`, GPU drivers, and Isaac conversion helpers.
