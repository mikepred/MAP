# Global Rule: Default to Test-Aware Development with `pytest` (Python)

For all new Python functions, classes, or modules I generate or significantly refactor, I will proactively:

1.  **Include or Suggest `pytest`-Compatible Unit Tests:**
    *   Draft basic unit tests covering common use cases and important edge cases.
    *   Ensure these tests are compatible with the `pytest` framework.
    *   If providing suggestions rather than full implementations, clearly outline the test scenarios.

2.  **Offer to Manage `pytest` Dependency:**
    *   Check if `pytest` is already listed in the project's `requirements.txt` (or equivalent like `pyproject.toml`).
    *   If `pytest` is not present, I will offer to add it to the appropriate dependency file.

3.  **Structure Tests Appropriately:**
    *   Follow common `pytest` conventions, such as placing tests in a `tests/` directory and naming test files like `test_*.py` or `*_test.py`.
    *   Encourage clear separation of test code from application code.

**Rationale:**
This rule reinforces a commitment to robust testing as a default part of the Python development workflow. It aligns with the "Future-Proofing" principles (emphasizing comprehensive testing strategies) and existing development workflow guidelines. By making `pytest` the standard, we ensure consistency and leverage a powerful testing framework.

## Related Rules
- [21-workflow-tooling-security.md](21-workflow-tooling-security.md)
