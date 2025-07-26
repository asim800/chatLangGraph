# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Plan & Review

### Before starting work

- Always think through the problem in plan mode, read the codebase for relevant files, and then describe your plan for what to build at high level and write a step-by-step plan to tasks.md.
- The plan must be formated in a bullet list of tasks and the rationale behind each item.
- Once you write the plan, always ask me to review and approve.

### while implementing

- Prefer proven libraries over custom implementations
- Make every task and code change as simple and readable as possible. We want to avoid complex changes for little impact. Keep everything as simple as possible.
- Update the plan as we work through the project and append updates and detailed descriptions of changes to tasks.md.
- we should capture sufficient details in tasks.md to be able to hand-off project to another engineer.
- You do not need my permissions to update tasks.md and todo.md files.
- Add a review section to the tasks.md file with a summary of the changes you've made any relevant information as to why that change was required and append the summary to summary.md file as well

## Development Commands

## Python Notes

- Please use uv as package manager and Python version 3.12
- Use Pydantic for data validation and serialization
