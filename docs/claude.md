# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## standard Workflow

- Always think through the problem, read the codebase for relevant files, and then describe your plan for what to build at high level and write a step-by-step plan to tasks.md.
- The plan should have a list of todo items that you can check off as you complete them.
- Give me a high level explanantion of what changes you are make at each step.
- Then, begin working on the todo items, marking them as complete as you go.
- Always keep a history of my input prompts, datetime stamp and your high level approach and append to the todo.md file
- Always write correct, best practice, DRY principle (Dont Repeat Yourself), bug free, fully functional and working code also it should be aligned to listed rules down below at Code Implementation Guidelines .
- Prefer proven libraries over custom implementations
- You do not need my permissions to update tasks.md and todo.md files.
- Make every task and code change as simple and readable as possible. We want to avoid complex changes for little impact. Keep everything as simple as possible.
- Add a review section to the tasks.md file with a summary of the changes you've made any relevant information as to why that change was required and append the summary to summary.md file as well

## Python Notes

- Please use uv as package manager and Python version 3.12
- Both MCP server and FastAPI service use consistent dependency management
- Environment variables required for database connections in Python services

##
