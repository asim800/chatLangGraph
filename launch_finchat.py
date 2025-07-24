#!/usr/bin/env python3
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
