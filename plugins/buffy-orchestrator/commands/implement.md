# Implement Feature Command

Implement a feature following the Buffy orchestrator workflow.

## Workflow

Execute this workflow for: $ARGUMENTS

### Phase 1: Context Gathering

Spawn these in parallel:
1. @file-picker to find files related to this feature
2. @file-picker to find related tests
3. @code-searcher to find existing similar patterns

Read the most relevant files found.

### Phase 2: Planning

Create a todo list:
```markdown
## Implementation Plan for: $ARGUMENTS

- [ ] Step 1: ...
- [ ] Step 2: ...
- [ ] Step 3: ...
- [ ] Review changes
- [ ] Run tests/typecheck
```

For complex logic, spawn @thinker to analyze the best approach.

### Phase 3: Implementation

Spawn @editor to implement the changes. Let it make its own decisions about what files to modify based on the context gathered.

### Phase 4: Validation (Parallel)

Run all of these in parallel:
1. @code-reviewer to review the changes
2. @commander to run typecheck (if applicable)
3. @commander to run tests (if applicable)

### Phase 5: Summary

Provide:
- Brief summary of changes (1-3 bullet points)
- Any issues found and how they were fixed
- 2-3 suggested follow-up actions
