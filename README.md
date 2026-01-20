# Buffy Orchestrator

A Claude Code plugin that implements Codebuff's base2 "Buffy the Orchestrator" pattern for complex coding tasks.

## Features

- **Multi-agent orchestration** - Coordinates specialized agents for different tasks
- **Smart file discovery** - Finds relevant files before making changes
- **Code pattern search** - Locates definitions, usages, and imports
- **Deep thinking** - Analyzes complex problems thoroughly
- **Precise editing** - Makes surgical code changes following conventions
- **Code review** - Reviews changes for bugs, security, and quality
- **Terminal commands** - Runs tests, builds, and other CLI operations

## Installation

### Via Claude Code Plugin Marketplace

```bash
# Add this marketplace to Claude Code
/plugin marketplace add yourusername/buffy-plugin

# Install the plugin
/plugin install buffy-orchestrator@yourusername-buffy-plugin
```

Replace `yourusername` with your GitHub username after pushing to GitHub.

### Manual Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/buffy-plugin.git

# Copy to your project's .claude directory
cp -r buffy-plugin/plugins/buffy-orchestrator/agents /path/to/your/project/.claude/
cp -r buffy-plugin/plugins/buffy-orchestrator/skills /path/to/your/project/.claude/
cp -r buffy-plugin/plugins/buffy-orchestrator/commands /path/to/your/project/.claude/

# Or copy to user-level (available in all projects)
cp -r buffy-plugin/plugins/buffy-orchestrator/agents ~/.claude/
cp -r buffy-plugin/plugins/buffy-orchestrator/skills ~/.claude/
cp -r buffy-plugin/plugins/buffy-orchestrator/commands ~/.claude/
```

## Usage

### Slash Commands

```bash
# Implement a new feature
/implement add rate limiting to all API endpoints

# Review code changes
/review src/auth/

# Refactor code
/refactor extract authentication logic into separate module
```

### Direct Agent Invocation

```bash
# Find relevant files
@file-picker find files related to user authentication

# Search for code patterns
@code-searcher find all usages of validateToken function

# Deep analysis
@thinker analyze the best approach for implementing caching

# Make code changes
@editor implement the rate limiting middleware

# Review changes
@code-reviewer review the changes in src/middleware/

# Run commands
@commander npm test
```

### Using the Skill

```bash
# Trigger the full orchestration workflow
"Use buffy-orchestrator to add payment processing"
```

## Agents

| Agent | Description | Use When |
|-------|-------------|----------|
| `@file-picker` | Discovers relevant files | Before any edits |
| `@code-searcher` | Searches code patterns | Finding definitions/usages |
| `@thinker` | Deep problem analysis | Complex decisions |
| `@editor` | Implements changes | Making code edits |
| `@code-reviewer` | Reviews code quality | After implementation |
| `@commander` | Runs terminal commands | Tests, builds, etc. |

## Workflow Pattern

The orchestrator follows this pattern for complex tasks:

```
1. Context Gathering (Parallel)
   ├── @file-picker "find feature files"
   ├── @file-picker "find test files"
   ├── @code-searcher "find related patterns"
   └── Read relevant files

2. Planning
   └── Create todo list or spawn @thinker

3. Implementation
   └── @editor "implement the changes"

4. Validation (Parallel)
   ├── @code-reviewer "review changes"
   ├── @commander "npm run typecheck"
   └── @commander "npm test"

5. Summary
   └── Brief summary + follow-up suggestions
```

## Configuration

### Project-Level

Add a `CLAUDE.md` file to your project root to provide project-specific context:

```markdown
# My Project

## Tech Stack
- Next.js 14
- TypeScript
- Prisma + PostgreSQL

## Conventions
- Use functional components
- Prefer server components
- Follow existing naming patterns
```

### Customizing Agents

You can override any agent by creating a file with the same name in your project's `.claude/agents/` directory.

## Scripts

The plugin includes Python helper scripts:

```bash
# Analyze codebase structure
python3 plugins/buffy-orchestrator/skills/buffy-orchestrator/scripts/analyze_codebase.py .

# Search for code patterns
python3 plugins/buffy-orchestrator/skills/buffy-orchestrator/scripts/find_patterns.py "functionName" --type ts,js
```

## Repository Structure

```
buffy-plugin/
├── .claude-plugin/
│   └── marketplace.json          # Marketplace configuration
├── plugins/
│   └── buffy-orchestrator/
│       ├── .claude-plugin/
│       │   └── plugin.json       # Plugin manifest
│       ├── agents/               # Specialized agents
│       │   ├── file-picker.md
│       │   ├── code-searcher.md
│       │   ├── thinker.md
│       │   ├── editor.md
│       │   ├── code-reviewer.md
│       │   └── commander.md
│       ├── skills/
│       │   └── buffy-orchestrator/
│       │       ├── SKILL.md
│       │       └── scripts/
│       └── commands/
│           ├── implement.md
│           ├── review.md
│           └── refactor.md
├── README.md
└── LICENSE
```

## Publishing to GitHub

1. Create a new repository on GitHub
2. Push this code:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Buffy Orchestrator plugin"
   git remote add origin https://github.com/yourusername/buffy-plugin.git
   git push -u origin main
   ```

3. Users can then install with:
   ```bash
   /plugin marketplace add yourusername/buffy-plugin
   /plugin install buffy-orchestrator@yourusername-buffy-plugin
   ```

## License

MIT License - see [LICENSE](LICENSE) for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Credits

Inspired by [Codebuff](https://codebuff.com)'s base2 agent architecture.
