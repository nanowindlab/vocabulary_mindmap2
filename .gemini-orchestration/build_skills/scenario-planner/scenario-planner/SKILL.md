---
name: scenario-planner
description: Plans and defines user journeys, state transitions, and interaction scenarios. Use when mapping out how a user navigates between views, tabs, or data links. Do not use for visual UI design or CSS styling.
---

# Scenario Planner

This skill guides the creation of robust, step-by-step user interaction scenarios. It ensures all edge cases in navigation and state changes are accounted for.

## Core Principles: Sequential Workflow Orchestration

Every scenario must clearly define the user's intent, the trigger action, the system's state change, and the resulting feedback.

## Workflow: Scenario Generation

When tasked with creating a scenario, structure your output using the following format:

### Scenario Structure Template

**Scenario Name:** [Action] in [Context]
**User Goal:** [What the user wants to achieve]
**Pre-conditions:** [What must be true before this starts (e.g., Tab A is active, Word X is selected)]

**Steps:**
1.  **Trigger:** User performs [Action] (e.g., Clicks the 'Meta' tab).
2.  **Logic/State Change:** The system performs [Data lookup / State update]. (e.g., System fetches Meta category structure, preserves current selected word if applicable).
3.  **UI Feedback:** The UI updates to show [Visual result]. (e.g., The mindmap re-renders with Meta roots; the detail panel stays open but updates its context label).

**Post-conditions:** [The new state of the app]

## Specific Contexts to Cover (Checklist)
When planning complex app navigation, ensure you generate scenarios for:
- [ ] **Tab Switching:** Moving between Core, Expression, and Meta tabs. (Does the category tree reset? What happens to the selected term?)
- [ ] **View Mode Switching:** Toggling between Mindmap, List, and Card View. (Does the view switch smoothly while keeping the same data pool? What if a term is selected vs. unselected?)
- [ ] **Cross-link Navigation:** Clicking a related term that belongs to a different Tab or Root. (How does the app route the user to the new location visually?)

## Troubleshooting edge cases
*   *What if a user clicks a cross-link that leads to a tab they aren't currently on?* The scenario must explicitly state that the system forces a Tab change and updates the Active Tab state before rendering the target.