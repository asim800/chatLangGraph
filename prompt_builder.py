#!/usr/bin/env python3
"""
Interactive prompt builder for template prompts
Allows selection and configuration of templates, then launches main.py with the configured prompt
"""

import sys
import os
import subprocess
import tempfile
from typing import Dict, Any, Optional

# Add the current directory to path so we can import prompts
sys.path.insert(0, os.path.dirname(__file__))

from prompts import SYSTEM_PROMPTS, get_template_variables, is_template, render_template, get_prompt_info

class PromptBuilder:
    def __init__(self):
        self.selected_prompt = None
        self.template_variables = {}
        self.final_prompt = None
    
    def show_welcome(self):
        """Show welcome message and instructions"""
        print("🎯 Interactive Prompt Builder")
        print("=" * 50)
        print("Select and configure template prompts for your chatbot session")
        print("The configured prompt will be passed to main.py for chatting")
        print()
    
    def list_available_prompts(self):
        """List all available prompts with template indicators"""
        print("📝 Available Prompts:")
        print("-" * 30)
        
        static_prompts = []
        template_prompts = []
        
        for i, prompt_name in enumerate(SYSTEM_PROMPTS.keys(), 1):
            prompt_info = get_prompt_info(prompt_name)
            if prompt_info is None:
                continue
                
            print(f"{i:2d}. {prompt_name}")
            print(f"    Preview: {prompt_info['preview'][:80]}{'...' if len(prompt_info['preview']) > 80 else ''}")
            
            if prompt_info['is_template']:
                print(f"    📝 Template variables: {prompt_info['template_variables']}")
                template_prompts.append(prompt_name)
            else:
                print(f"    📄 Static prompt ({prompt_info['word_count']} words)")
                static_prompts.append(prompt_name)
            print()
        
        print(f"Summary: {len(static_prompts)} static prompts, {len(template_prompts)} template prompts")
        return list(SYSTEM_PROMPTS.keys())
    
    def select_prompt(self, prompt_names):
        """Allow user to select a prompt"""
        while True:
            try:
                print("\n🔹 Select a prompt:")
                choice = input("Enter prompt number or name: ").strip()
                
                # Try to parse as number
                try:
                    choice_num = int(choice)
                    if 1 <= choice_num <= len(prompt_names):
                        selected = prompt_names[choice_num - 1]
                        break
                    else:
                        print(f"❌ Please enter a number between 1 and {len(prompt_names)}")
                        continue
                except ValueError:
                    # Try to find by name
                    matching = [name for name in prompt_names if choice.lower() in name.lower()]
                    if len(matching) == 1:
                        selected = matching[0]
                        break
                    elif len(matching) > 1:
                        print(f"❌ Multiple matches found: {matching}")
                        print("Please be more specific or use the number")
                        continue
                    else:
                        print(f"❌ No prompt found matching '{choice}'")
                        continue
                        
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                sys.exit(0)
            except EOFError:
                print("\n👋 Goodbye!")
                sys.exit(0)
        
        self.selected_prompt = selected
        print(f"✅ Selected: {selected}")
        return selected
    
    def configure_template_variables(self, prompt_name):
        """Configure variables for template prompts"""
        if not is_template(prompt_name):
            print(f"📄 '{prompt_name}' is a static prompt - no variables needed")
            return {}
        
        variables = get_template_variables(prompt_name)
        print(f"\n📝 Template '{prompt_name}' requires {len(variables)} variables:")
        
        configured_vars = {}
        
        for var in variables:
            while True:
                try:
                    print(f"\n🔹 Enter value for '{var}':")
                    
                    # Show examples based on variable name
                    examples = self.get_variable_examples(var)
                    if examples:
                        print(f"   Examples: {', '.join(examples)}")
                    
                    value = input(f"   {var} = ").strip()
                    
                    if value:
                        configured_vars[var] = value
                        print(f"   ✅ Set {var} = '{value}'")
                        break
                    else:
                        print("   ❌ Value cannot be empty")
                        
                except KeyboardInterrupt:
                    print("\n👋 Goodbye!")
                    sys.exit(0)
                except EOFError:
                    print("\n👋 Goodbye!")
                    sys.exit(0)
        
        self.template_variables = configured_vars
        return configured_vars
    
    def get_variable_examples(self, var_name):
        """Get example values for common variable names"""
        examples = {
            'topic': ['movies', 'books', 'code', 'software', 'music'],
            'focus_area': ['cinematography', 'plot', 'best practices', 'usability', 'performance'],
            'domain': ['machine learning', 'cybersecurity', 'web development', 'data science'],
            'experience_level': ['beginner', 'intermediate', 'advanced', 'expert', 'senior'],
            'specialty': ['deep learning', 'threat analysis', 'frontend', 'backend', 'DevOps'],
            'subject': ['Python', 'JavaScript', 'mathematics', 'physics', 'history'],
            'student_level': ['beginner', 'intermediate', 'advanced', 'high school', 'college'],
            'teaching_style': ['interactive', 'methodical', 'hands-on', 'visual', 'step-by-step'],
            'industry': ['technology', 'healthcare', 'finance', 'education', 'retail'],
            'specialization': ['strategy', 'operations', 'marketing', 'finance', 'HR'],
            'client_type': ['startups', 'enterprises', 'SMBs', 'nonprofits', 'government'],
            'challenge_type': ['scaling', 'modernization', 'efficiency', 'growth', 'transformation'],
            'content_type': ['video', 'blog', 'podcast', 'social media', 'newsletter'],
            'niche': ['programming', 'cooking', 'fitness', 'travel', 'photography'],
            'audience': ['developers', 'students', 'professionals', 'beginners', 'experts'],
            'style': ['educational', 'entertaining', 'professional', 'casual', 'technical'],
            'goal': ['educate', 'entertain', 'inspire', 'inform', 'motivate'],
            'tools': ['portfolio_analyzer', 'risk_calculator', 'market_data_fetcher'],
            'tool_names': ['portfolio_analyzer', 'risk_calculator', 'market_data_fetcher']
        }
        
        return examples.get(var_name.lower(), [])
    
    def preview_final_prompt(self):
        """Preview the final configured prompt"""
        if not self.selected_prompt:
            return
        
        try:
            if is_template(self.selected_prompt):
                if not self.template_variables:
                    print("❌ No variables configured for template")
                    return
                
                self.final_prompt = render_template(self.selected_prompt, **self.template_variables)
            else:
                self.final_prompt = SYSTEM_PROMPTS[self.selected_prompt]
            
            print(f"\n📋 Final Prompt Preview:")
            print("=" * 50)
            print(self.final_prompt)
            print("=" * 50)
            print(f"Length: {len(self.final_prompt)} characters, {len(self.final_prompt.split())} words")
            
        except Exception as e:
            print(f"❌ Error generating prompt: {e}")
            return False
        
        return True
    
    def confirm_and_launch(self):
        """Confirm the prompt and launch main.py"""
        if not self.final_prompt:
            print("❌ No prompt configured")
            return False
        
        print(f"\n🚀 Launch Options:")
        print("1. Launch chat with this prompt")
        print("2. Save prompt to file")
        print("3. Copy prompt to clipboard")
        print("4. Go back to modify")
        print("5. Exit")
        
        while True:
            try:
                choice = input("\nChoose option (1-5): ").strip()
                
                if choice == '1':
                    return self.launch_chat()
                elif choice == '2':
                    return self.save_prompt_to_file()
                elif choice == '3':
                    return self.copy_to_clipboard()
                elif choice == '4':
                    return False  # Go back
                elif choice == '5':
                    print("👋 Goodbye!")
                    sys.exit(0)
                else:
                    print("❌ Please enter 1, 2, 3, 4, or 5")
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                sys.exit(0)
            except EOFError:
                print("\n👋 Goodbye!")
                sys.exit(0)
    
    def launch_chat(self):
        """Launch main.py with the configured prompt"""
        print(f"\n🚀 Launching chat with configured prompt...")
        
        # Create a temporary file with the prompt
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(self.final_prompt)
            temp_file = f.name
        
        try:
            # Launch main.py with the prompt
            cmd = [sys.executable, 'main.py', 'chat', '--prompt', self.final_prompt]
            print(f"Running: python main.py chat --prompt \"[{len(self.final_prompt)} chars]\"")
            print("=" * 50)
            
            # Execute the command
            result = subprocess.run(cmd, cwd=os.path.dirname(__file__))
            
            if result.returncode == 0:
                print("\n✅ Chat session completed successfully")
            else:
                print(f"\n❌ Chat session ended with error code: {result.returncode}")
                
        except Exception as e:
            print(f"❌ Error launching chat: {e}")
        finally:
            # Clean up temp file
            try:
                os.unlink(temp_file)
            except:
                pass
        
        return True
    
    def save_prompt_to_file(self):
        """Save the prompt to a file"""
        try:
            filename = input("\nEnter filename (default: my_prompt.txt): ").strip()
            if not filename:
                filename = "my_prompt.txt"
            
            with open(filename, 'w') as f:
                f.write(self.final_prompt)
            
            print(f"✅ Prompt saved to: {filename}")
            
            # Ask if they want to launch with this file
            launch = input("Launch chat with this prompt? (y/n): ").strip().lower()
            if launch in ['y', 'yes']:
                return self.launch_chat()
                
        except Exception as e:
            print(f"❌ Error saving file: {e}")
        
        return False
    
    def copy_to_clipboard(self):
        """Copy prompt to clipboard"""
        try:
            import pyperclip
            pyperclip.copy(self.final_prompt)
            print("✅ Prompt copied to clipboard!")
        except ImportError:
            print("❌ pyperclip not installed. Install with: pip install pyperclip")
            print("📋 Manual copy - here's your prompt:")
            print("-" * 40)
            print(self.final_prompt)
            print("-" * 40)
        except Exception as e:
            print(f"❌ Error copying to clipboard: {e}")
        
        return False
    
    def run(self):
        """Main interactive loop"""
        self.show_welcome()
        
        while True:
            try:
                # List and select prompt
                prompt_names = self.list_available_prompts()
                selected = self.select_prompt(prompt_names)
                
                # Configure variables if needed
                variables = self.configure_template_variables(selected)
                
                # Preview final prompt
                if self.preview_final_prompt():
                    # Confirm and launch
                    if self.confirm_and_launch():
                        break
                    else:
                        # Go back to start
                        print("\n🔄 Starting over...")
                        continue
                else:
                    print("\n❌ Failed to generate prompt. Starting over...")
                    continue
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except EOFError:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Unexpected error: {e}")
                print("🔄 Starting over...")
                continue

def main():
    """Main entry point"""
    builder = PromptBuilder()
    builder.run()

if __name__ == "__main__":
    main()