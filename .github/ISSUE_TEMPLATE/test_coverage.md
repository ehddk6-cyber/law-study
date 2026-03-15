name: ✅ Test Coverage
description: Suggest new tests or test improvements
title: "[TEST] "
labels: ["testing"]
body:
  - type: input
    id: component
    attributes:
      label: Component
      description: Which component needs testing?
      placeholder: "e.g., services/precedent_service.py"
  - type: textarea
    id: current_coverage
    attributes:
      label: Current Test Coverage
      description: What's currently tested (if anything)?
  - type: textarea
    id: proposed_tests
    attributes:
      label: Proposed Test Cases
      description: What test cases should be added?
      value: |
        - [ ] Test case 1
        - [ ] Test case 2
        - [ ] Test case 3
  - type: input
    id: priority
    attributes:
      label: Priority
      description: How critical is this test coverage?
      placeholder: "High/Medium/Low"
