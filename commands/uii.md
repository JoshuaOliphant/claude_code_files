---
description: UI Iteration workflow - write code, screenshot result, iterate until UI is visually correct
argument-hint: <UI feature description>
---

# UI Iteration Workflow

You will implement the following UI feature using an iterative visual feedback approach: $ARGUMENTS

## Workflow Overview

Follow the visual-first development cycle using structured phases with appropriate sub-agents:

### Phase 1: Initial Implementation
Use the `coder` sub-agent to:
- Understand the UI feature requirements thoroughly
- Implement the initial UI feature based on the description
- Focus on creating a working implementation that can be visually tested
- Include all necessary styling, layout, and interactive elements
- Ensure the feature is integrated into the existing UI structure
- Make the feature accessible for screenshot testing

### Phase 2: Visual Verification
Use the `screenshot` sub-agent to:
- Take a screenshot of the implemented UI feature
- Analyze the visual result against the requirements
- Identify any issues with layout, styling, positioning, or appearance
- Document the current state of the UI
- Provide specific feedback on what needs to be adjusted
- Compare against design expectations or similar UI patterns

### Phase 3: Iterative Refinement
Repeat the following cycle until UI is visually correct:

**Code Adjustment** (using `coder` sub-agent):
- Address specific visual issues identified in the screenshot
- Make targeted improvements to styling, layout, or behavior
- Implement responsive design considerations if needed
- Fix alignment, spacing, colors, or typography issues
- Ensure cross-browser compatibility where relevant

**Visual Re-verification** (using `screenshot` sub-agent):
- Take a new screenshot after each code change
- Compare with previous screenshots to track progress
- Verify that fixes didn't introduce new visual problems
- Document improvement or identify remaining issues
- Provide feedback for the next iteration

### Phase 4: Final Validation & Commit
Use the `committer` sub-agent to:
- Take a final screenshot showing the completed UI feature
- Verify that all visual requirements have been met
- Review the code changes for quality and maintainability
- Create a meaningful commit message describing the UI feature
- Include screenshot documentation of the final result
- Ensure the feature works as intended across different screen sizes

## UI Development Principles

1. **Visual-First**: Every code change should be immediately verified visually
2. **Rapid Iteration**: Small, focused changes with immediate visual feedback
3. **Screenshot Documentation**: Maintain visual history of development progress
4. **User Experience Focus**: Prioritize how the UI looks and feels to users
5. **Responsive Design**: Consider different screen sizes and devices
6. **Accessibility**: Ensure UI is usable by all users

## Success Criteria

- UI feature matches the described requirements visually
- Screenshots demonstrate proper layout, styling, and behavior
- Code is clean, maintainable, and follows existing patterns
- Feature works correctly across different screen sizes
- Visual elements are properly aligned and styled
- Interactive elements function as expected
- Final commit includes visual documentation

## Iteration Guidelines

- **Start with functionality, refine the visuals**: Get a working version first, then iterate on appearance
- **Make incremental changes**: Small adjustments are easier to verify and debug
- **Document visual progress**: Each screenshot should show clear progress toward the goal
- **Consider edge cases**: Test with different content lengths, screen sizes, and user interactions
- **Match existing design patterns**: Ensure consistency with the rest of the application
- **Test interactive states**: Hover, focus, active, and disabled states where applicable

## Important Notes

- **Screenshots are mandatory** after each code change - visual verification is key
- Take screenshots from multiple angles/states if the UI has interactive elements
- If visual requirements are unclear, ask for clarification before proceeding
- Don't commit until the UI is visually verified and meets all requirements
- Each iteration should show measurable visual improvement
- Consider both desktop and mobile viewports where relevant
- Pay attention to accessibility concerns (contrast, focus indicators, etc.)

## Phase Transitions

- Only move from Phase 1 to Phase 2 when initial implementation is complete
- Stay in Phase 3 iteration cycle until visual requirements are fully met
- Only proceed to Phase 4 when all stakeholders would approve the visual result
- If major design changes are needed, consider returning to Phase 1

Begin with Phase 1: Initial Implementation.