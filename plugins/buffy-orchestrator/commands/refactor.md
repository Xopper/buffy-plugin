# Refactor Code Command

Refactor code with full validation and safety checks.

## Target

Refactor: $ARGUMENTS

## Workflow

### Phase 1: Analysis

1. @file-picker find all files related to this refactor
2. @code-searcher find all usages of the code being refactored
3. Read all affected files to understand the full impact

### Phase 2: Planning

Spawn @thinker to analyze:
- Current state of the code
- Best refactoring approach
- Files that will be affected
- Potential risks and how to mitigate them

Create a detailed plan:
```markdown
## Refactoring Plan: $ARGUMENTS

### Current State
{Description of current implementation}

### Target State
{Description of desired implementation}

### Steps
- [ ] Step 1: ...
- [ ] Step 2: ...
- [ ] Update all usages
- [ ] Update tests
- [ ] Review and validate
```

### Phase 3: Implementation

Execute the refactor step by step:
1. @editor make the core changes
2. @code-searcher verify all usages are found
3. @editor update all usages
4. @editor update any affected tests

### Phase 4: Validation (Parallel)

Run all validation in parallel:
1. @code-reviewer review all changes
2. @commander run full test suite
3. @commander run typecheck
4. @commander run lint

### Phase 5: Summary

Provide:
- Summary of what was refactored
- List of all files modified
- Any manual steps required
- Suggested follow-up actions
