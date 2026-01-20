# Review Code Command

Review code changes for quality, bugs, and best practices.

## Target

Review: $ARGUMENTS

## Workflow

### 1. Gather Context

First, understand what changed:
- If specific files mentioned, read those files
- If "recent changes" or similar, check `git diff` or `git diff HEAD~1`
- If PR/branch mentioned, check the diff for that

### 2. Spawn Code Reviewer

@code-reviewer Review the changes in the specified files/commits.

Focus on:
- **Correctness**: Logic errors, edge cases, null handling
- **Security**: Input validation, data exposure, auth issues
- **Performance**: N+1 queries, memory leaks, inefficient code
- **Quality**: Duplication, complexity, naming, style
- **Maintainability**: Types, documentation, testability

### 3. Run Validation

In parallel:
- @commander run typecheck (npm run typecheck / tsc --noEmit / mypy)
- @commander run tests (npm test / pytest / go test)
- @commander run lint (npm run lint / eslint / ruff)

### 4. Summary

Provide a review summary:

```markdown
## Code Review Summary

### Critical Issues 🔴
{List any blocking issues}

### Warnings 🟡
{List concerns that should be addressed}

### Suggestions 🟢
{List optional improvements}

### Validation Results
- Typecheck: ✅/❌
- Tests: ✅/❌
- Lint: ✅/❌

### Verdict
{Ready to merge / Needs fixes / Major rework needed}
```
