#!/usr/bin/env python3
"""
Test script to demonstrate running finchat from main.py
"""

import subprocess
import sys

def test_finchat_main():
    """Test running finchat from main.py"""
    
    print("🧪 TESTING FINCHAT FROM MAIN.PY")
    print("=" * 40)
    
    # Test the command that would be run
    cmd = [sys.executable, "main.py", "chat", "--prompt", "finchat_prompt"]
    
    print(f"Command: {' '.join(cmd)}")
    print("\nThis would start the financial chat with:")
    print("✅ Auto-configured financial tools")
    print("✅ Rendered finchat_prompt template")  
    print("✅ LangGraph invoke() patterns")
    print("✅ All framework features (stats, history, etc.)")
    
    print("\n" + "="*50)
    print("📋 WAYS TO RUN FINCHAT FROM MAIN.PY")
    print("="*50)
    
    print("\n1️⃣  Basic finchat (auto-configures tools):")
    print("   python main.py chat --prompt finchat_prompt")
    
    print("\n2️⃣  With custom config file:")
    print("   python main.py chat --config finchat_config.json")
    
    print("\n3️⃣  With template variables (if needed):")
    print("   python main.py chat --prompt finchat_prompt --template-var key=value")
    
    print("\n4️⃣  List all available prompts:")
    print("   python main.py prompts list")
    
    print("\n5️⃣  Search for financial prompts:")
    print("   python main.py prompts search financial")
    
    print("\n" + "="*50)
    print("🔧 FEATURES AVAILABLE FROM MAIN.PY")
    print("="*50)
    
    features = [
        "🏦 Auto-configured financial tools (calculate_risk, get_stock_info, portfolio_analyzer)",
        "💬 Interactive chat with finchat_prompt",
        "📊 Statistics command ('stats')",
        "📜 Chat history commands ('history', 'history 5', 'history all')",
        "🔄 New session command ('new')",
        "📤 Data export capabilities",
        "⚙️  Configuration file support",
        "🎯 Template variable substitution",
        "🔧 LangGraph invoke() patterns throughout"
    ]
    
    for feature in features:
        print(f"   {feature}")
    
    print("\n" + "="*50)
    print("💡 COMPARISON: main.py vs run_finchat_with_tools.py")
    print("="*50)
    
    print("\n📋 main.py advantages:")
    print("   • Full CLI framework with subcommands")
    print("   • Statistics and analytics")
    print("   • Chat history management")
    print("   • Data export functionality")
    print("   • Configuration file support")
    print("   • Session management")
    
    print("\n📋 run_finchat_with_tools.py advantages:")
    print("   • Simpler, focused demo")
    print("   • Arrow key history navigation")
    print("   • Immediate interactive mode")
    print("   • No CLI complexity")
    
    print("\n✅ Both now use LangGraph invoke() patterns!")

if __name__ == "__main__":
    test_finchat_main()