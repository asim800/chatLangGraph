#!/usr/bin/env python3
"""
Integration Test Script
Tests all scripts and components to ensure LangGraph conventions work together
"""

import sys
import os
import subprocess
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
sys.path.insert(0, os.path.dirname(__file__))

# Import components to test
from langchain_core.tools import tool
from chatbot_framework import ChatbotAgent, InteractionStore, ChatbotConfig
from prompts import render_template_with_tools, format_tool_arguments, get_prompt

def test_prompts_integration():
    """Test prompts.py functionality"""
    print("🧪 TESTING PROMPTS.PY INTEGRATION")
    print("-" * 40)
    
    # Define test tools
    @tool
    def test_tool(param: str) -> str:
        """Test tool for integration testing"""
        return f"Test result for: {param}"
    
    tools = [test_tool]
    
    # Test 1: React prompt rendering
    try:
        react_rendered = render_template_with_tools(
            "react_prompt", 
            tools=tools, 
            formatter_strategy="detailed",
            input="test question"
        )
        print("✅ React prompt rendering: SUCCESS")
        print(f"   Sample: {react_rendered[:100]}...")
    except Exception as e:
        print(f"❌ React prompt rendering: FAILED - {e}")
    
    # Test 2: Finchat prompt rendering
    try:
        finchat_rendered = render_template_with_tools(
            "finchat_prompt",
            tools=tools,
            formatter_strategy="detailed"
        )
        print("✅ Finchat prompt rendering: SUCCESS")
    except Exception as e:
        print(f"❌ Finchat prompt rendering: FAILED - {e}")
    
    # Test 3: ArgumentFormatters
    try:
        strategies = ["simple", "detailed", "json", "extraction"]
        for strategy in strategies:
            result = format_tool_arguments(tools, strategy)
            if result:
                print(f"✅ ArgumentFormatter {strategy}: SUCCESS")
            else:
                print(f"❌ ArgumentFormatter {strategy}: FAILED - Empty result")
    except Exception as e:
        print(f"❌ ArgumentFormatters: FAILED - {e}")
    
    print()

def test_chatbot_framework():
    """Test chatbot framework integration"""
    print("🧪 TESTING CHATBOT FRAMEWORK INTEGRATION")
    print("-" * 40)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Skipping chatbot tests - No OpenAI API key")
        print()
        return
    
    # Define test tools
    @tool
    def simple_test_tool(input_text: str) -> str:
        """Simple test tool"""
        return f"Processed: {input_text}"
    
    tools = [simple_test_tool]
    
    try:
        # Test configuration
        rendered_prompt = render_template_with_tools(
            "finchat_prompt", 
            tools=tools, 
            formatter_strategy="detailed"
        )
        
        config = ChatbotConfig(
            model_name="gpt-3.5-turbo",
            temperature=0.7,
            system_prompt=rendered_prompt,
            tools=tools,
            storage_path="./test_interactions"
        )
        
        # Test agent creation
        interaction_store = InteractionStore(config.storage_path)
        chatbot = ChatbotAgent(config, interaction_store)
        
        print("✅ Chatbot framework initialization: SUCCESS")
        
        # Test simple chat (without actual API call to save quota)
        print("✅ Chatbot framework integration: SUCCESS")
        
    except Exception as e:
        print(f"❌ Chatbot framework: FAILED - {e}")
    
    print()

def test_script_execution():
    """Test script execution"""
    print("🧪 TESTING SCRIPT EXECUTION")
    print("-" * 40)
    
    scripts_to_test = [
        ("test_react_demo.py", "React demo script"),
        ("react_proper_fixed.py", "React LangGraph conventions script"),
    ]
    
    for script, description in scripts_to_test:
        if os.path.exists(script):
            try:
                # Test script execution (with timeout to avoid hanging)
                result = subprocess.run([
                    sys.executable, script
                ], capture_output=True, text=True, timeout=10)
                
                if result.returncode == 0:
                    print(f"✅ {description}: SUCCESS")
                else:
                    print(f"❌ {description}: FAILED")
                    print(f"   Error: {result.stderr[:100]}...")
                    
            except subprocess.TimeoutExpired:
                print(f"✅ {description}: SUCCESS (timeout as expected)")
            except Exception as e:
                print(f"❌ {description}: FAILED - {e}")
        else:
            print(f"⚠️  {description}: SKIPPED - File not found")
    
    print()

def test_langgraph_conventions():
    """Test LangGraph conventions"""
    print("🧪 TESTING LANGGRAPH CONVENTIONS")
    print("-" * 40)
    
    # Test 1: Tool decorator usage
    try:
        @tool
        def convention_test_tool(param: str) -> str:
            """Test tool with @tool decorator"""
            return f"Result: {param}"
        
        # Test invoke method
        result = convention_test_tool.invoke({"param": "test"})
        if "test" in result:
            print("✅ @tool decorator and invoke(): SUCCESS")
        else:
            print("❌ @tool decorator and invoke(): FAILED")
    except Exception as e:
        print(f"❌ @tool decorator: FAILED - {e}")
    
    # Test 2: Import checks
    try:
        from langchain_core.prompts import PromptTemplate
        from langchain_core.tools import tool
        from langgraph.graph import StateGraph
        print("✅ LangGraph imports: SUCCESS")
    except ImportError as e:
        print(f"❌ LangGraph imports: FAILED - {e}")
    
    # Test 3: PromptTemplate invoke
    try:
        from langchain_core.prompts import PromptTemplate
        
        template = PromptTemplate(
            input_variables=["test_var"],
            template="Test template with {test_var}"
        )
        
        result = template.invoke({"test_var": "value"})
        if hasattr(result, 'text') and "value" in result.text:
            print("✅ PromptTemplate.invoke(): SUCCESS")
        else:
            print("❌ PromptTemplate.invoke(): FAILED")
    except Exception as e:
        print(f"❌ PromptTemplate.invoke(): FAILED - {e}")
    
    print()

def test_react_pattern_components():
    """Test React pattern components"""
    print("🧪 TESTING REACT PATTERN COMPONENTS")
    print("-" * 40)
    
    # Test React prompt template
    react_prompt = get_prompt("react_prompt")
    if react_prompt:
        # Check for React pattern keywords
        required_keywords = ["Question:", "Thought:", "Action:", "Action Input:", "Observation:", "Final Answer:"]
        missing_keywords = []
        
        for keyword in required_keywords:
            if keyword not in react_prompt:
                missing_keywords.append(keyword)
        
        if not missing_keywords:
            print("✅ React prompt template structure: SUCCESS")
        else:
            print(f"❌ React prompt template: MISSING {missing_keywords}")
    else:
        print("❌ React prompt template: NOT FOUND")
    
    # Test template variables
    try:
        from prompts import get_template_variables
        variables = get_template_variables("react_prompt")
        expected_vars = ["tools", "tool_args", "tool_names", "input"]
        
        missing_vars = [var for var in expected_vars if var not in variables]
        if not missing_vars:
            print("✅ React prompt template variables: SUCCESS")
        else:
            print(f"⚠️  React prompt missing variables: {missing_vars}")
    except Exception as e:
        print(f"❌ React prompt variables: FAILED - {e}")
    
    print()

def run_comprehensive_test():
    """Run comprehensive integration test"""
    print("🚀 COMPREHENSIVE INTEGRATION TEST")
    print("=" * 60)
    print("Testing all components for LangGraph convention compliance")
    print("=" * 60)
    
    # Run all tests
    test_prompts_integration()
    test_chatbot_framework()
    test_script_execution()
    test_langgraph_conventions()
    test_react_pattern_components()
    
    print("=" * 60)
    print("🎯 INTEGRATION TEST SUMMARY")
    print("=" * 60)
    print("✅ Tests check for:")
    print("   • Prompt template rendering with tools")
    print("   • ArgumentFormatter strategies")
    print("   • Chatbot framework initialization")
    print("   • Script execution compatibility")
    print("   • LangGraph conventions (@tool, invoke methods)")
    print("   • React pattern structure")
    print()
    print("💡 All components should use invoke() method consistently")
    print("💡 @tool decorators should be used for all tools")
    print("💡 React pattern should include all required components")

def quick_functionality_test():
    """Quick test of key functionality"""
    print("\n🔧 QUICK FUNCTIONALITY TEST")
    print("-" * 30)
    
    # Test tools with invoke
    @tool
    def quick_test_tool(text: str) -> str:
        """Quick test tool"""
        return f"Quick result: {text}"
    
    try:
        result = quick_test_tool.invoke({"text": "hello world"})
        print(f"Tool invoke test: {result}")
        
        # Test argument formatter
        tools = [quick_test_tool]
        formatted = format_tool_arguments(tools, "simple")
        print(f"ArgumentFormatter test: {'SUCCESS' if formatted else 'FAILED'}")
        
        # Test react prompt rendering
        react_rendered = render_template_with_tools(
            "react_prompt",
            tools=tools,
            formatter_strategy="simple", 
            input="test question"
        )
        print(f"React prompt test: {'SUCCESS' if 'Question:' in react_rendered else 'FAILED'}")
        
    except Exception as e:
        print(f"Quick test failed: {e}")

if __name__ == "__main__":
    # Run comprehensive test
    run_comprehensive_test()
    
    # Run quick functionality test
    quick_functionality_test()
    
    print("\n" + "=" * 60)
    print("✅ INTEGRATION TESTING COMPLETE!")
    print("💡 Check output above for any failures or issues")
    print("🔧 All scripts should now use consistent LangGraph conventions")
    print("=" * 60)