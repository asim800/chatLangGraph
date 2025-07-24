#!/usr/bin/env python3
"""
Test script for web chat functionality
"""

import requests
import json
import time
import sys

def test_web_chat_api(base_url="http://localhost:8000"):
    """Test the web chat API endpoints"""
    
    print("🧪 Testing Web Chat API")
    print("=" * 30)
    
    # Test 1: Check if server is running
    try:
        response = requests.get(f"{base_url}/docs", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running")
        else:
            print(f"❌ Server responded with status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Server is not reachable: {e}")
        return False
    
    # Test 2: Get available prompts
    try:
        response = requests.get(f"{base_url}/api/prompts", timeout=5)
        if response.status_code == 200:
            prompts = response.json()
            print(f"✅ Available prompts: {prompts}")
        else:
            print(f"❌ Failed to get prompts: {response.status_code}")
    except Exception as e:
        print(f"❌ Error getting prompts: {e}")
    
    # Test 3: Send a chat message
    try:
        chat_data = {
            "message": "Hello! What financial advice can you give me?",
            "user_id": "test_user",
            "session_id": None,
            "prompt_name": "finchat_prompt"
        }
        
        response = requests.post(
            f"{base_url}/api/chat", 
            json=chat_data,
            timeout=30  # Chat can take longer
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Chat response received:")
            print(f"   Session ID: {result['session_id']}")
            print(f"   Response: {result['response'][:100]}...")
            print(f"   Engagement Score: {result['engagement_score']}")
            
            # Store session ID for history test
            session_id = result['session_id']
        else:
            print(f"❌ Chat failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error during chat: {e}")
        return False
    
    # Test 4: Get chat history
    try:
        response = requests.get(
            f"{base_url}/api/sessions/{session_id}/history",
            params={"user_id": "test_user", "limit": 10},
            timeout=10
        )
        
        if response.status_code == 200:
            history = response.json()
            print(f"✅ Chat history retrieved:")
            print(f"   Message count: {history['session_info']['message_count']}")
        else:
            print(f"❌ Failed to get history: {response.status_code}")
    except Exception as e:
        print(f"❌ Error getting history: {e}")
    
    # Test 5: Get statistics
    try:
        response = requests.get(f"{base_url}/api/stats", timeout=5)
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ Statistics retrieved: {len(stats)} metrics")
        else:
            print(f"❌ Failed to get stats: {response.status_code}")
    except Exception as e:
        print(f"❌ Error getting stats: {e}")
    
    print("\n🎉 Web chat API test completed!")
    return True

def test_ui_accessibility(base_url="http://localhost:8000"):
    """Test if the UI is accessible"""
    try:
        response = requests.get(base_url, timeout=5)
        if response.status_code == 200 and "LangGraph Chatbot" in response.text:
            print("✅ Web UI is accessible")
            return True
        else:
            print(f"❌ Web UI not accessible: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error accessing UI: {e}")
        return False

if __name__ == "__main__":
    # Check if a custom port was provided
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("Usage: python test_web_chat.py [port]")
            sys.exit(1)
    
    base_url = f"http://localhost:{port}"
    print(f"Testing web chat at: {base_url}")
    
    # Test UI accessibility
    ui_ok = test_ui_accessibility(base_url)
    
    # Test API functionality
    api_ok = test_web_chat_api(base_url)
    
    if ui_ok and api_ok:
        print("\n🎉 All tests passed! Web chat is working correctly.")
    else:
        print("\n❌ Some tests failed. Check the server logs.")
        sys.exit(1)