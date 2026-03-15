name: 🔧 Refactoring
description: Propose code refactoring or structural improvements
title: "[REFACTOR] "
labels: ["refactoring"]
body:
  - type: textarea
    id: current
    attributes:
      label: Current Structure
      description: Describe the current code structure
    validations:
      required: true
  - type: textarea
    id: proposed
    attributes:
      label: Proposed Improvement
      description: What improvements do you suggest?
    validations:
      required: true
  - type: textarea
    id: benefits
    attributes:
      label: Benefits
      description: How will this improve the codebase?
  - type: input
    id: priority
    attributes:
      label: Priority
      description: How urgent is this refactoring?
      placeholder: "High/Medium/Low"
