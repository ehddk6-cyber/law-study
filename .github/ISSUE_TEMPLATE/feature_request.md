name: ✨ Feature Request
description: Suggest a new feature or improvement
title: "[FEATURE] "
labels: ["enhancement"]
body:
  - type: textarea
    id: problem
    attributes:
      label: Problem Statement
      description: Is your feature request related to a problem?
      placeholder: "I'm always frustrated when..."
  - type: textarea
    id: solution
    attributes:
      label: Proposed Solution
      description: What would you like to see happen?
    validations:
      required: true
  - type: textarea
    id: alternatives
    attributes:
      label: Alternative Solutions
      description: Have you considered any alternatives?
  - type: textarea
    id: context
    attributes:
      label: Additional Context
      description: Any other context or screenshots
