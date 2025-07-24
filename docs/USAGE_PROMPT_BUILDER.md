# Interactive Prompt Builder Usage Guide

## Overview

The Interactive Prompt Builder (`prompt_builder.py`) provides an easy-to-use interface for selecting and configuring system prompts for your chatbot sessions. It supports both static prompts and template prompts with variable substitution.

## Features

- **Interactive Selection**: Browse all available prompts with previews
- **Template Support**: Configure variables for template prompts with helpful examples
- **Multiple Output Options**: Launch chat, save to file, or copy to clipboard
- **Variable Examples**: Get contextual examples for common template variables
- **Error Handling**: Comprehensive error handling and validation

## Usage

### Basic Usage

```bash
python prompt_builder.py
```

This launches the interactive interface where you can:
1. Browse available prompts
2. Select a prompt by number or name
3. Configure variables (for template prompts)
4. Preview the final prompt
5. Launch a chat session or save the prompt

### Available Prompts

#### Static Prompts (Ready to Use)
- `default` - Basic helpful assistant
- `financial_advisor` - Expert financial assistant with portfolio tools
- `coding_mentor` - Programming mentor and code reviewer
- `creative_writer` - Creative writing assistant
- `research_assistant` - Research and analysis helper
- `teacher` - Educational tutor for various subjects
- `prompt_optimizer` - AI prompt optimization specialist

#### Template Prompts (Require Variables)
- `reviewer` - Specialized reviewer (requires: topic, focus_area)
- `domain_expert` - Subject matter expert (requires: domain, experience_level, specialty)
- `tutor` - Educational tutor (requires: subject, student_level, teaching_style)
- `consultant` - Industry consultant (requires: industry, specialization, client_type, challenge_type)
- `content_creator` - Content creator (requires: content_type, niche, audience, style, goal)

### Example Session

```
🎯 Interactive Prompt Builder
==================================================
Select and configure template prompts for your chatbot session

📝 Available Prompts:
------------------------------
 1. default
    Preview: You are a helpful assistant.
    📄 Static prompt (5 words)

 9. reviewer
    Preview: You are a helpful reviewer specializing in {topic}...
    📝 Template variables: ['topic', 'focus_area']

🔹 Select a prompt:
Enter prompt number or name: 9

📝 Template 'reviewer' requires 2 variables:

🔹 Enter value for 'topic':
   Examples: movies, books, code, software, music
   topic = movies

🔹 Enter value for 'focus_area':
   Examples: cinematography, plot, best practices, usability, performance
   focus_area = cinematography

📋 Final Prompt Preview:
==================================================
You are a helpful reviewer specializing in movies. Your role is to provide thoughtful, constructive reviews and analysis...
==================================================

🚀 Launch Options:
1. Launch chat with this prompt
2. Save prompt to file
3. Copy prompt to clipboard
4. Go back to modify
5. Exit

Choose option (1-5): 1

🚀 Launching chat with configured prompt...
```

### Variable Examples

The prompt builder provides contextual examples for common variables:

| Variable | Examples |
|----------|----------|
| `topic` | movies, books, code, software, music |
| `domain` | machine learning, cybersecurity, web development |
| `experience_level` | beginner, intermediate, advanced, expert |
| `subject` | Python, JavaScript, mathematics, physics |
| `content_type` | video, blog, podcast, social media |
| `audience` | developers, students, professionals, beginners |

### Integration with Main.py

The prompt builder seamlessly integrates with the main chatbot framework:

```bash
# Static prompt
python main.py chat --prompt coding_mentor

# Template prompt with variables
python main.py chat --prompt reviewer --template-var topic=movies --template-var focus_area=cinematography

# List all prompts
python main.py prompts list

# Search prompts
python main.py prompts search financial
```

### Output Options

When you've configured your prompt, you can:

1. **Launch Chat**: Immediately start a chat session with the configured prompt
2. **Save to File**: Save the prompt to a text file for later use
3. **Copy to Clipboard**: Copy the prompt to your system clipboard
4. **Go Back**: Return to modify your selection or configuration
5. **Exit**: Quit the prompt builder

### Error Handling

The prompt builder includes comprehensive error handling:

- **Missing Variables**: Alerts when required template variables are missing
- **Invalid Templates**: Validates template syntax and variable references
- **File Operations**: Handles file save/load errors gracefully
- **User Input**: Validates user input and provides clear error messages

### Tips

1. **Use Numbers**: For quick selection, use prompt numbers (e.g., `9` for reviewer)
2. **Partial Names**: You can type partial prompt names (e.g., `review` for reviewer)
3. **Variable Examples**: Pay attention to the provided examples for consistent variable formatting
4. **Preview**: Always preview your final prompt before launching
5. **Save Templates**: Save configured templates to files for reuse

## Files

- `prompt_builder.py` - Main interactive prompt builder script
- `prompts.py` - Prompt definitions and template system
- `main.py` - Integration with chatbot framework
- `demo_prompt_builder.py` - Demo script showing functionality
- `test_prompt_builder.py` - Test script for validation

## Requirements

- Python 3.6+
- `pyperclip` (optional, for clipboard functionality)
- Chatbot framework dependencies (for launching chat sessions)

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
2. **Template Errors**: Check that all required variables are provided
3. **Clipboard Issues**: Install `pyperclip` with `pip install pyperclip`
4. **Launch Failures**: Verify main.py is in the same directory

### Getting Help

If you encounter issues:
1. Check the error messages for specific guidance
2. Use the demo script to test functionality
3. Review the test scripts for examples
4. Ensure all required files are present in the same directory