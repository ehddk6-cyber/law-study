name: 🐛 Bug Report
description: Report a bug or unexpected behavior
title: "[BUG] "
labels: ["bug"]
body:
  - type: textarea
    id: description
    attributes:
      label: Description
      description: Briefly describe the bug
    validations:
      required: true
  - type: textarea
    id: reproduction
    attributes:
      label: Steps to Reproduce
      description: How can we reproduce this?
      value: |
        1. 
        2. 
        3. 
    validations:
      required: true
  - type: textarea
    id: expected
    attributes:
      label: Expected Behavior
      description: What should happen?
    validations:
      required: true
  - type: textarea
    id: logs
    attributes:
      label: Logs/Error Messages
      description: Paste any relevant logs or error messages
      render: shell
  - type: input
    id: environment
    attributes:
      label: Environment
      description: OS, Python version, etc.
      placeholder: "e.g., Ubuntu 22.04, Python 3.10"
