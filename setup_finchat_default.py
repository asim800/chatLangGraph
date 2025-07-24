#!/usr/bin/env python3
"""
Setup script to configure main.py to run like run_finchat_with_tools.py by default
"""

import json
import os
import sys

def create_default_finchat_config():
    """Create a default configuration that makes main.py behave like run_finchat_with_tools.py"""
    
    config = {
        "model_name": "gpt-3.5-turbo",
        "temperature": 0.7,
        "system_prompt": "finchat_prompt",
        "storage_path": "./demo_interactions",
        "context_window": 10,
        "max_conversation_length": 50,
        "engagement_tracking": True,
        "available_tools": ["calculate_risk", "get_stock_info", "portfolio_analyzer"]
    }
    
    # Create config directory if it doesn't exist
    os.makedirs("config", exist_ok=True)
    
    # Save the default configuration
    config_path = "config/default_config.json"
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Created default configuration: {config_path}")
    return config_path

def create_finchat_launcher():
    """Create a simple launcher script that runs main.py with finchat configuration"""
    
    launcher_content = '''#!/usr/bin/env python3
"""
Finchat Launcher - Runs main.py with finchat configuration
This makes main.py behave exactly like run_finchat_with_tools.py
"""

import sys
import subprocess

def main():
    """Launch main.py with finchat configuration"""
    
    # Arguments to make main.py behave like run_finchat_with_tools.py
    args = [
        sys.executable, 
        "main.py", 
        "chat", 
        "--prompt", "finchat_prompt"
    ]
    
    print("🏦 Launching Financial Chat (via main.py)")
    print("=" * 45)
    print("This runs main.py with finchat_prompt configuration")
    print("Same functionality as run_finchat_with_tools.py + CLI features")
    print()
    
    # Execute main.py with finchat configuration
    subprocess.run(args)

if __name__ == "__main__":
    main()
'''
    
    with open("launch_finchat.py", 'w') as f:
        f.write(launcher_content)
    
    # Make it executable
    os.chmod("launch_finchat.py", 0o755)
    
    print("✅ Created launcher script: launch_finchat.py")

def update_main_py_for_finchat_default():
    """Show how to modify main.py to default to finchat mode"""
    
    print("\\n📝 To make main.py default to finchat mode, you can:")
    print("\\n1. Modify the main() function in main.py to default to finchat:")
    print("   Change: args = parser.parse_args()")
    print("   To:     args = parser.parse_args() or create default args")
    
    print("\\n2. Or modify the default behavior in the parser")
    
    instructions = '''
# Add this to main.py after the parser setup:

def main():
    parser = argparse.ArgumentParser(description="LangGraph Chatbot Framework")
    # ... existing parser setup ...
    
    args = parser.parse_args()
    
    # DEFAULT TO FINCHAT MODE if no command provided
    if not args.command:
        print("🏦 Defaulting to Financial Chat mode")
        print("💡 Use 'python main.py --help' to see all options")
        run_interactive_chat(None, "finchat_prompt", None)
        return
    
    # ... rest of existing main() function ...
'''
    
    print("\\n📋 Code to add to main.py:")
    print(instructions)

def main():
    """Main setup function"""
    print("🔧 SETTING UP MAIN.PY TO RUN LIKE run_finchat_with_tools.py")
    print("=" * 60)
    
    # Create configurations
    config_path = create_default_finchat_config()
    create_finchat_launcher()
    update_main_py_for_finchat_default()
    
    print("\\n" + "=" * 60)
    print("✅ SETUP COMPLETE!")
    print("\\n🎯 You now have several ways to run main.py like run_finchat_with_tools.py:")
    print("\\n1. Command line (ready now):")
    print("   python main.py chat --prompt finchat_prompt")
    print("\\n2. With configuration file:")
    print("   python main.py chat --config config/finchat_simple_mode.json")
    print("\\n3. Use the launcher script:")
    print("   python launch_finchat.py")
    print("\\n4. Modify main.py to default to finchat (see instructions above)")
    
    print("\\n💡 All methods provide the same finchat functionality + CLI features!")

if __name__ == "__main__":
    main()