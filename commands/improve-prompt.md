---
description: Analyze and improve prompts using evidence-based prompt engineering techniques
argument-hint: <prompt to improve>
---

# Prompt Improvement Guide

Think deeply about the prompt engineering challenge and apply systematic improvement techniques to create a superior prompt for: $ARGUMENTS

## Pre-Analysis Assessment

Before improving the prompt, I will evaluate:
1. **Current Effectiveness**: What works and what doesn't?
2. **Intent Clarity**: What is the true goal?
3. **Complexity Level**: Simple task or multi-step process?
4. **Target Audience**: Who will use this prompt?
5. **Success Metrics**: How do we measure improvement?

## Improvement Methodology

### Phase 1: Deep Analysis
**Objective**: Understand the prompt's purpose and weaknesses

Analyze through these critical lenses:

<analysis_framework>
1. **Clarity & Specificity**
   - Is the desired outcome crystal clear?
   - Are success criteria explicit?
   - Any ambiguous language?

2. **Context & Motivation**
   - Does it explain WHY requirements matter?
   - Is background context provided?
   - Are constraints clearly stated?

3. **Structure & Organization**
   - Would XML tags improve clarity?
   - Is information logically sequenced?
   - Are instructions separated from content?

4. **Examples & Patterns**
   - Would multishot examples help?
   - Are edge cases demonstrated?
   - Is the pattern clear from examples?

5. **Reasoning Requirements**
   - Would chain-of-thought improve accuracy?
   - Should thinking be explicit or hidden?
   - How complex is the reasoning needed?

6. **Role & Expertise**
   - Would a specific persona help?
   - What expertise level is needed?
   - Should multiple perspectives be considered?

7. **Task Decomposition**
   - Should this be multiple prompts?
   - Are there natural breakpoints?
   - Would iteration improve results?
</analysis_framework>

**Analysis Checkpoint**:
- [ ] Core intent identified
- [ ] Weaknesses documented
- [ ] Improvement opportunities mapped
- [ ] Complexity assessed
- [ ] Success criteria defined

### Phase 2: Technique Selection
**Objective**: Choose optimal improvement strategies

Select from proven techniques:

#### 2.1: Explicitness Enhancement
**Before**: "Create a dashboard"
**After**: "Create a comprehensive analytics dashboard displaying real-time metrics. Include:
- Interactive charts with drill-down capability
- Responsive design for mobile/desktop
- Hover states showing detailed tooltips
- Smooth transitions between views
- Color-coded alerts for anomalies
- Export functionality for reports"

#### 2.2: Context Injection
**Before**: "Format this for readability"
**After**: "Format this text for optimal readability by a text-to-speech engine. Context: This will be read aloud to visually impaired users, so:
- Avoid special characters that confuse TTS
- Use clear sentence boundaries
- Spell out abbreviations on first use
- Structure with clear paragraph breaks"

#### 2.3: XML Structuring
```xml
<task>
Analyze the provided contract for risks and opportunities
</task>

<context>
This is a B2B software licensing agreement
Our company is the licensee
Budget constraint: $50,000 annually
</context>

<contract>
[Contract text here]
</contract>

<requirements>
1. Identify unfavorable terms
2. Flag missing standard clauses
3. Assess termination conditions
4. Review liability limitations
5. Suggest negotiation points
</requirements>

<output_format>
Use structured sections with clear headers
Prioritize findings by business impact
Include specific clause references
</output_format>
```

#### 2.4: Multishot Learning (3-5 examples)
```xml
<examples>
<example>
<input>Customer reports app crashes on login</input>
<analysis>
- Category: Technical bug
- Severity: Critical (blocks access)
- Pattern: Authentication flow issue
</analysis>
<action>
1. Escalate to engineering immediately
2. Check for similar reports
3. Provide workaround if available
</action>
</example>

<example>
<input>Feature request for dark mode</input>
<analysis>
- Category: Enhancement
- Severity: Low (cosmetic)
- Pattern: Common user request
</analysis>
<action>
1. Log in feature tracking system
2. Check product roadmap
3. Thank user and set expectations
</action>
</example>
</examples>
```

#### 2.5: Chain-of-Thought Integration
```xml
Think step-by-step about this problem:

<reasoning_steps>
1. First, identify the core challenge
2. Consider multiple solution approaches
3. Evaluate trade-offs of each approach
4. Select optimal solution based on constraints
5. Plan implementation details
6. Anticipate potential issues
7. Design validation criteria
</reasoning_steps>
```

#### 2.6: Role Definition
**Generic**: "Review this code"
**Enhanced**: "You are a senior software architect with 15 years of experience in distributed systems. Review this microservice code focusing on:
- Scalability bottlenecks
- Security vulnerabilities
- Design pattern adherence
- Error handling robustness
- Performance optimization opportunities"

#### 2.7: Task Chaining
For complex multi-step processes:
```
Chain Structure:
1. Prompt A: Initial analysis and planning
2. Prompt B: Detailed implementation based on A's output
3. Prompt C: Quality review and refinement of B's work
4. Prompt D: Final optimization and documentation
```

**Technique Selection Checkpoint**:
- [ ] Appropriate techniques chosen
- [ ] Techniques address identified weaknesses
- [ ] No conflicting approaches
- [ ] Complexity matches task needs
- [ ] Clear improvement path

### Phase 3: Prompt Reconstruction
**Objective**: Build improved prompt systematically

Follow this construction sequence:
1. **Role/Context Setting**: Establish expertise and situation
2. **Task Definition**: Clear, specific objective
3. **Input Structure**: Organized with XML tags
4. **Examples**: If beneficial, 3-5 diverse cases
5. **Reasoning**: Explicit thinking instructions
6. **Constraints**: Boundaries and requirements
7. **Output Format**: Precise structure expected
8. **Validation**: Success criteria

**Construction Template**:
```xml
<role>
[Specific expertise and perspective]
</role>

<context>
[Background and situational information]
</context>

<task>
[Clear, specific objective]
</task>

<thinking_instruction>
[How to approach the problem]
</thinking_instruction>

<inputs>
[Structured input data/content]
</inputs>

<requirements>
[Specific constraints and needs]
</requirements>

<output_specification>
[Exact format and structure needed]
</output_specification>

<success_criteria>
[How to measure quality]
</success_criteria>
```

### Phase 4: Enhancement Validation
**Objective**: Ensure improvements are effective

Test improved prompt against criteria:
1. **Clarity Test**: Could someone else understand intent?
2. **Completeness Test**: All edge cases covered?
3. **Consistency Test**: No contradictions?
4. **Efficiency Test**: Streamlined without losing detail?
5. **Measurability Test**: Success clearly defined?

**Validation Checkpoint**:
- [ ] Intent clearer than original
- [ ] Ambiguity eliminated
- [ ] Structure logical
- [ ] Examples helpful
- [ ] Output predictable

## Output Format

### Improved Prompt
```xml
<improved_prompt>
[The enhanced version with all improvements applied]
</improved_prompt>
```

### Improvement Analysis
```xml
<improvements_made>
<improvement>
<technique>Explicitness Enhancement</technique>
<before>[Original unclear instruction]</before>
<after>[Specific, detailed instruction]</after>
<impact>Reduces ambiguity by 80%</impact>
</improvement>

<improvement>
<technique>XML Structuring</technique>
<before>[Unstructured text]</before>
<after>[Organized with XML tags]</after>
<impact>Improves parseability and clarity</impact>
</improvement>
</improvements_made>
```

### Optional Enhancements
```xml
<further_improvements>
<suggestion>
<enhancement>Add performance benchmarks</enhancement>
<rationale>Would provide concrete targets</rationale>
<implementation>Include specific metrics in success criteria</implementation>
</suggestion>
</further_improvements>
```

## Key Principles

**DO**:
- Tell Claude what TO do (not what to avoid)
- Be more specific than seems necessary
- Match prompt style to desired output
- Use consistent XML tagging
- Provide context for requirements
- Enable parallel execution where possible
- Include validation criteria

**AVOID**:
- Vague instructions
- Conflicting requirements
- Assumed knowledge
- Overly complex single prompts
- Missing success criteria
- Unclear output formats

## Meta-Prompting Considerations

When creating prompts for prompt improvement:
1. **Recursive Enhancement**: Apply these techniques to this prompt
2. **Self-Evaluation**: Include validation of improvements
3. **Iteration Planning**: Design for multiple refinement rounds
4. **Pattern Recognition**: Identify reusable improvement patterns
5. **Documentation**: Explain why changes improve performance

Begin with Phase 1: Deep Analysis of the provided prompt.