#!/usr/bin/env python3
"""
Complete guide on how to use template prompts
"""

import sys
import os

# Add the current directory to path so we can import prompts
sys.path.insert(0, os.path.dirname(__file__))

from prompts import render_template, get_template_variables, is_template, list_prompts, get_prompt_info

def show_available_templates():
    """Show all available template prompts"""
    print("=== Available Template Prompts ===\n")
    
    prompts = list_prompts()
    template_prompts = []
    
    for prompt_name in prompts:
        if is_template(prompt_name):
            template_prompts.append(prompt_name)
            prompt_info = get_prompt_info(prompt_name)
            print(f"🔹 {prompt_name}")
            print(f"   Variables: {prompt_info['template_variables']}")
            print(f"   Preview: {prompt_info['preview']}")
            print()
    
    print(f"Found {len(template_prompts)} template prompts: {', '.join(template_prompts)}")
    return template_prompts

def show_basic_usage():
    """Show basic template usage examples"""
    print("\n=== Basic Template Usage ===\n")
    
    print("1. Using render_template() function:")
    print("   from prompts import render_template")
    print()
    
    # Example 1: Reviewer template
    print("   # Movie reviewer example")
    print("   prompt = render_template('reviewer', topic='movies', focus_area='cinematography')")
    
    try:
        movie_prompt = render_template('reviewer', topic='movies', focus_area='cinematography')
        print(f"   ✅ Success! Generated {len(movie_prompt)} characters")
        print(f"   Preview: {movie_prompt[:200]}...")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    
    # Example 2: Domain expert template
    print("   # Domain expert example")
    print("   prompt = render_template('domain_expert',")
    print("                          domain='machine learning',")
    print("                          experience_level='senior',")
    print("                          specialty='deep learning')")
    
    try:
        ml_prompt = render_template('domain_expert',
                                  domain='machine learning',
                                  experience_level='senior',
                                  specialty='deep learning')
        print(f"   ✅ Success! Generated {len(ml_prompt)} characters")
        print(f"   Preview: {ml_prompt[:200]}...")
    except Exception as e:
        print(f"   ❌ Error: {e}")

def show_command_line_usage():
    """Show command-line usage examples"""
    print("\n=== Command-Line Usage ===\n")
    
    print("1. Basic template command structure:")
    print("   python main.py chat --prompt <template_name> --template-var key=value")
    print()
    
    print("2. Practical examples:")
    print()
    
    examples = [
        {
            "name": "Movie Reviewer",
            "template": "reviewer",
            "vars": {"topic": "movies", "focus_area": "cinematography"},
            "command": "python main.py chat --prompt reviewer --template-var topic=movies --template-var focus_area=cinematography"
        },
        {
            "name": "Book Reviewer", 
            "template": "reviewer",
            "vars": {"topic": "books", "focus_area": "character development"},
            "command": "python main.py chat --prompt reviewer --template-var topic=books --template-var 'focus_area=character development'"
        },
        {
            "name": "Python Tutor",
            "template": "tutor",
            "vars": {"subject": "Python", "student_level": "beginner", "teaching_style": "interactive"},
            "command": "python main.py chat --prompt tutor --template-var subject=Python --template-var student_level=beginner --template-var teaching_style=interactive"
        },
        {
            "name": "ML Expert",
            "template": "domain_expert",
            "vars": {"domain": "machine learning", "experience_level": "senior", "specialty": "deep learning"},
            "command": "python main.py chat --prompt domain_expert --template-var domain='machine learning' --template-var experience_level=senior --template-var specialty='deep learning'"
        },
        {
            "name": "Tech Consultant",
            "template": "consultant",
            "vars": {"industry": "technology", "specialization": "strategy", "client_type": "startups", "challenge_type": "scaling"},
            "command": "python main.py chat --prompt consultant --template-var industry=technology --template-var specialization=strategy --template-var client_type=startups --template-var challenge_type=scaling"
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"   {i}. {example['name']}:")
        print(f"      {example['command']}")
        print()

def show_error_handling():
    """Show error handling examples"""
    print("\n=== Error Handling ===\n")
    
    print("1. Missing variables:")
    print("   python main.py chat --prompt reviewer --template-var topic=movies")
    print("   ❌ Error: Missing required variable 'focus_area'")
    print()
    
    print("2. Invalid format:")
    print("   python main.py chat --prompt reviewer --template-var topic movies")
    print("   ❌ Error: Invalid format. Use key=value")
    print()
    
    print("3. Using template without variables:")
    print("   python main.py chat --prompt reviewer")
    print("   ❌ Error: Template requires variables: ['topic', 'focus_area']")
    print()
    
    print("4. Checking required variables:")
    print("   from prompts import get_template_variables")
    print("   vars = get_template_variables('reviewer')")
    print(f"   Result: {get_template_variables('reviewer')}")

def show_advanced_usage():
    """Show advanced usage patterns"""
    print("\n=== Advanced Usage Patterns ===\n")
    
    print("1. Dynamic template selection:")
    print("   # Check if prompt is template before using")
    print("   if is_template('reviewer'):")
    print("       prompt = render_template('reviewer', topic='movies', focus_area='plot')")
    print("   else:")
    print("       prompt = get_prompt('reviewer')")
    print()
    
    print("2. Variable validation:")
    print("   required_vars = get_template_variables('reviewer')")
    print("   user_vars = {'topic': 'movies', 'focus_area': 'cinematography'}")
    print("   missing = set(required_vars) - set(user_vars.keys())")
    print("   if missing:")
    print("       print(f'Missing variables: {missing}')")
    print()
    
    print("3. Template discovery:")
    print("   # Find all template prompts")
    print("   templates = [name for name in list_prompts() if is_template(name)]")
    templates = [name for name in list_prompts() if is_template(name)]
    print(f"   Result: {templates}")
    print()
    
    print("4. Batch template rendering:")
    print("   configs = [")
    print("       {'template': 'reviewer', 'vars': {'topic': 'movies', 'focus_area': 'plot'}},")
    print("       {'template': 'reviewer', 'vars': {'topic': 'books', 'focus_area': 'style'}},")
    print("   ]")
    print("   prompts = [render_template(cfg['template'], **cfg['vars']) for cfg in configs]")

def show_practical_examples():
    """Show practical real-world examples"""
    print("\n=== Practical Real-World Examples ===\n")
    
    scenarios = [
        {
            "scenario": "Creating a Code Review Bot",
            "template": "reviewer",
            "variables": {"topic": "code", "focus_area": "best practices"},
            "command": "python main.py chat --prompt reviewer --template-var topic=code --template-var 'focus_area=best practices'"
        },
        {
            "scenario": "Setting up a Math Tutor",
            "template": "tutor", 
            "variables": {"subject": "calculus", "student_level": "college", "teaching_style": "step-by-step"},
            "command": "python main.py chat --prompt tutor --template-var subject=calculus --template-var student_level=college --template-var teaching_style=step-by-step"
        },
        {
            "scenario": "Creating a Cybersecurity Expert",
            "template": "domain_expert",
            "variables": {"domain": "cybersecurity", "experience_level": "expert", "specialty": "threat analysis"},
            "command": "python main.py chat --prompt domain_expert --template-var domain=cybersecurity --template-var experience_level=expert --template-var specialty='threat analysis'"
        },
        {
            "scenario": "Business Strategy Consultant",
            "template": "consultant",
            "variables": {"industry": "healthcare", "specialization": "digital transformation", "client_type": "hospitals", "challenge_type": "modernization"},
            "command": "python main.py chat --prompt consultant --template-var industry=healthcare --template-var specialization='digital transformation' --template-var client_type=hospitals --template-var challenge_type=modernization"
        },
        {
            "scenario": "YouTube Content Creator",
            "template": "content_creator",
            "variables": {"content_type": "video", "niche": "programming", "audience": "developers", "style": "educational", "goal": "teach concepts"},
            "command": "python main.py chat --prompt content_creator --template-var content_type=video --template-var niche=programming --template-var audience=developers --template-var style=educational --template-var goal='teach concepts'"
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"{i}. {scenario['scenario']}:")
        print(f"   Template: {scenario['template']}")
        print(f"   Variables: {scenario['variables']}")
        print(f"   Command: {scenario['command']}")
        print()

def show_tips_and_best_practices():
    """Show tips and best practices"""
    print("\n=== Tips and Best Practices ===\n")
    
    print("1. Variable naming:")
    print("   ✅ Use descriptive names: topic, focus_area, experience_level")
    print("   ❌ Avoid generic names: var1, x, temp")
    print()
    
    print("2. Quoting values with spaces:")
    print("   ✅ --template-var 'focus_area=character development'")
    print("   ✅ --template-var focus_area='character development'")
    print("   ❌ --template-var focus_area=character development")
    print()
    
    print("3. Check variables before using:")
    print("   python main.py prompts list  # Shows template variables")
    print("   python main.py prompts search template  # Find templates")
    print()
    
    print("4. Template discovery workflow:")
    print("   1. List all prompts: python main.py prompts list")
    print("   2. Find templates by looking for 📝 Template variables")
    print("   3. Use template: python main.py chat --prompt <name> --template-var key=value")
    print()
    
    print("5. Error debugging:")
    print("   - If template fails, check required variables")
    print("   - Use quotes for multi-word values")
    print("   - Check spelling of template names")
    print("   - Validate variable names match template exactly")

def interactive_demo():
    """Interactive demonstration"""
    print("\n=== Interactive Demo ===\n")
    
    print("Let's create a movie reviewer prompt step by step:")
    print()
    
    print("Step 1: Check if 'reviewer' is a template")
    is_template_result = is_template('reviewer')
    print(f"   is_template('reviewer') = {is_template_result}")
    print()
    
    print("Step 2: Get required variables")
    required_vars = get_template_variables('reviewer')
    print(f"   get_template_variables('reviewer') = {required_vars}")
    print()
    
    print("Step 3: Render the template")
    print("   render_template('reviewer', topic='movies', focus_area='cinematography')")
    try:
        result = render_template('reviewer', topic='movies', focus_area='cinematography')
        print(f"   ✅ Success! Generated prompt:")
        print(f"   Length: {len(result)} characters")
        print(f"   Preview: {result[:300]}...")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    print()
    
    print("Step 4: Command-line equivalent")
    print("   python main.py chat --prompt reviewer --template-var topic=movies --template-var focus_area=cinematography")

if __name__ == "__main__":
    print("🎯 Template Prompt Usage Guide")
    print("=" * 50)
    
    show_available_templates()
    show_basic_usage()
    show_command_line_usage()
    show_error_handling()
    show_advanced_usage()
    show_practical_examples()
    show_tips_and_best_practices()
    interactive_demo()
    
    print("\n" + "=" * 50)
    print("✅ Template usage guide complete!")
    print("💡 Try: python main.py prompts list")
    print("💡 Try: python main.py chat --prompt reviewer --template-var topic=movies --template-var focus_area=plot")