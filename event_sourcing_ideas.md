# Event Sourcing Ideas for Claude Code Long-Term Memory

## Overview
Transform Claude Code's hook-generated event logs into a persistent, project-specific memory system using event sourcing patterns. Each project directory (`cwd`) becomes its own event stream, enabling knowledge accumulation over time.

## Core Concepts
- **Event Stream**: Immutable, append-only log of all Claude Code actions
- **Project Segmentation**: Events filtered by `cwd` for project-specific memory
- **Multiple Projections**: Different views/aggregations from the same event stream
- **State Reconstruction**: Rebuild any state by replaying events from the beginning

## Implementation Ideas

### 1. Project Context Accumulator
Build `.claude/knowledge/` directories per project that aggregate all events by `cwd`. Every interaction enriches markdown files tracking:
- Common file edit patterns
- Frequently used commands
- Project-specific terminology
- Error resolutions that worked
- Team conventions discovered over time

**Structure:**
```
project/.claude/knowledge/
├── patterns.md          # Recurring code patterns
├── conventions.md       # Discovered project conventions
├── solutions.md         # Problem-solution pairs
└── context.md          # General project understanding
```

### 2. Pattern Mining Engine
Detect recurring event sequences and proactively suggest workflows.

**Example Pattern Storage:**
```json
{
  "pattern_id": "test_workflow_1",
  "trigger": "test-related prompt",
  "action_sequence": [
    "grep **/*test*",
    "read test file",
    "edit implementation",
    "run tests"
  ],
  "success_rate": 0.85,
  "last_used": "2024-01-15T10:30:00Z",
  "frequency": 12
}
```

**Benefits:**
- Suggests common workflows automatically
- Learns project-specific development patterns
- Reduces repetitive instruction needs

### 3. Architectural Decision Records (ADR)
Extract key decisions from conversations and tool usage, creating timestamped ADRs.

**Auto-captured decisions:**
- Authentication implementation (from auth-related file edits)
- Library choices (from package.json/requirements.txt changes)
- API design decisions (from route definitions)
- Database schema evolution (from migration files)

**Format:**
```markdown
# ADR-001: Authentication Strategy
Date: 2024-01-15
Session: a0e6afa3-4a19-4592-9fb2-abf17eeef37c

## Decision
Implemented JWT-based authentication

## Context
User requested secure API endpoints

## Evidence
- Created auth/jwt.py
- Modified user_model.py
- Added jsonwebtoken to package.json
```

### 4. Smart Failure Memory
Track error patterns and resolutions across sessions.

**Storage Structure:**
```python
{
  "error_signature": "TypeError: Cannot read property 'timestamp'",
  "occurrences": [
    {
      "session_id": "abc123",
      "file": "dashboard.py",
      "resolution": "Added None check for timestamps",
      "success": True
    }
  ],
  "suggested_fixes": [
    "Check for None timestamps",
    "Ensure datetime objects are properly formatted"
  ]
}
```

**Features:**
- Prevents repeating same mistakes
- Suggests proven solutions
- Builds error resolution knowledge base

### 5. Temporal Query System
Enable time-based memory queries for project history.

**Query Examples:**
- "What did we implement last week?"
- "Show all database schema changes"
- "When did we last modify authentication?"
- "What features were added in January?"

**Implementation:**
```python
class TemporalMemory:
    def query(self, project_id: str, timeframe: str, filter: str):
        # Returns events matching criteria
        return self.event_store.query(
            project=project_id,
            start_time=parse_timeframe(timeframe),
            event_type=filter
        )
```

### 6. Project Fingerprinting
Learn project conventions from accumulated events.

**Tracked Patterns:**
- **Coding Style**: Indentation, naming conventions, comment style
- **Preferred Libraries**: Most frequently imported packages
- **Testing Patterns**: Test file locations, naming conventions
- **Commit Format**: Conventional commits, emoji usage, message length
- **File Organization**: Directory structure preferences

**Output Example:**
```json
{
  "project_fingerprint": {
    "style": {
      "indent": "4_spaces",
      "quotes": "double",
      "naming": "snake_case"
    },
    "testing": {
      "framework": "pytest",
      "location": "tests/",
      "naming": "test_*.py"
    },
    "dependencies": {
      "primary": ["fastapi", "sqlalchemy", "pydantic"],
      "dev": ["pytest", "black", "mypy"]
    }
  }
}
```

### 7. Dependency Intelligence Graph
Track which files are edited together to understand implicit relationships.

**Graph Structure:**
```python
{
  "nodes": {
    "auth.py": {"type": "module", "domain": "authentication"},
    "user_model.py": {"type": "model", "domain": "authentication"},
    "test_auth.py": {"type": "test", "domain": "authentication"}
  },
  "edges": [
    {
      "source": "auth.py",
      "target": "user_model.py",
      "weight": 0.8,  # Edited together 80% of the time
      "relationship": "implements"
    }
  ]
}
```

**Benefits:**
- Understands implicit file relationships
- Suggests related files to check/update
- Identifies architectural boundaries

### 8. Intelligent Session Synthesis
Synthesize all past sessions into coherent project understanding.

**Features:**
- Loads project context automatically when entering directory
- Merges insights from all previous sessions
- Maintains running summary of project state
- Provides "where we left off" context

**Session Synthesis Example:**
```markdown
## Project Summary
Last worked: 2024-01-15 (2 days ago)
Total sessions: 15
Active features: User authentication, API endpoints

## Recent Work
- Implemented JWT authentication
- Fixed timestamp handling in dashboard
- Added user registration endpoint

## Known Issues
- Performance bottleneck in data processing
- TODO: Add rate limiting to API

## Upcoming Tasks
(From previous conversations)
- Implement password reset flow
- Add logging system
- Create admin dashboard
```

## Implementation Architecture

### Event Processor
```python
class ProjectMemorySystem:
    def __init__(self):
        self.pattern_detector = PatternMiningEngine()
        self.decision_extractor = ADRExtractor()
        self.failure_tracker = SmartFailureMemory()
        self.fingerprinter = ProjectFingerprinter()
        self.graph_builder = DependencyGraphBuilder()
        
    def process_event(self, event):
        project_id = self.get_project_id(event['cwd'])
        
        # Route to appropriate aggregators
        self.pattern_detector.process(project_id, event)
        self.decision_extractor.process(project_id, event)
        self.failure_tracker.process(project_id, event)
        self.fingerprinter.analyze(project_id, event)
        self.graph_builder.update(project_id, event)
        
        # Update project knowledge base
        self.update_knowledge(project_id, event)
        
    def get_project_id(self, cwd):
        # Generate stable project ID from directory path
        return hashlib.md5(cwd.encode()).hexdigest()
```

### Storage Strategy
Each project gets its own SQLite database:
```
~/.claude/memory/
├── project_abc123.db    # Project-specific event store
├── project_def456.db    # Another project
└── global_patterns.db   # Cross-project patterns
```

### Query Interface
Hooks can query memory:
```python
# In a hook file
memory = ProjectMemory(project_path)
recent_errors = memory.query_failures(days=7)
related_files = memory.get_related_files("auth.py")
patterns = memory.suggest_workflow(user_prompt)
```

## Benefits

1. **Continuous Learning**: Every interaction improves project understanding
2. **Context Preservation**: Never lose valuable project knowledge
3. **Error Prevention**: Learn from past mistakes automatically
4. **Workflow Optimization**: Suggest proven patterns proactively
5. **Team Knowledge Sharing**: Captured knowledge can be committed to repo
6. **Temporal Navigation**: Query project history naturally
7. **Reduced Cognitive Load**: Claude Code remembers so you don't have to

## Next Steps

1. Build event processor daemon
2. Create SQLite schema for event storage
3. Implement aggregator modules
4. Add query API for hooks
5. Create visualization dashboard
6. Test with real project workflows