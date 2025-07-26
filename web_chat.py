#!/usr/bin/env python3
"""
FastAPI Web Chat Server
Provides web access to the LangGraph Chatbot Framework
"""

import os
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse, Response
from pydantic import BaseModel
import uvicorn
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from chatbot_framework import ChatbotAgent, InteractionStore, ChatbotConfig
from prompts import get_prompt, list_prompts, render_template_with_tools, is_template
from tools.financial_tools import get_financial_tools


# Pydantic models for API
class ChatMessage(BaseModel):
    message: str
    user_id: Optional[str] = "web_user"
    session_id: Optional[str] = None
    prompt_name: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    session_id: str
    engagement_score: float
    timestamp: str


class SessionInfo(BaseModel):
    session_id: str
    user_id: str
    prompt_name: Optional[str]
    created_at: str
    message_count: int


class ChatHistory(BaseModel):
    messages: List[Dict[str, Any]]
    session_info: SessionInfo


# Global variables for chatbot instances
chatbot_instances: Dict[str, ChatbotAgent] = {}
interaction_store: InteractionStore = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize chatbot instances on startup"""
    global interaction_store
    
    # Initialize interaction store
    interaction_store = InteractionStore("/tmp/web_interactions")
    print("🌐 Web Chat Server initialized")
    yield
    print("🌐 Web Chat Server shutting down")


# Initialize interaction store for standalone usage too
if interaction_store is None:
    interaction_store = InteractionStore("/tmp/web_interactions")


# Initialize FastAPI app
app = FastAPI(
    title="LangGraph Chatbot Web Chat",
    description="Web interface for the LangGraph Chatbot Framework",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware for Next.js integration
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js dev server
        "http://localhost:3001",  # Alternative Next.js port
        "https://mystocks.ai",    # Production domain
        "https://*.mystocks.ai",  # Subdomains
        "https://*.vercel.app",   # Vercel deployments
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


def get_or_create_chatbot(prompt_name: str = "finchat_prompt") -> ChatbotAgent:
    """Get or create a chatbot instance for the given prompt"""
    global chatbot_instances, interaction_store
    
    print(f"🤖 get_or_create_chatbot called with: {prompt_name}")
    print(f"🤖 Current chatbot instances: {list(chatbot_instances.keys())}")
    
    if prompt_name not in chatbot_instances:
        # Create config for this prompt
        config = ChatbotConfig()
        
        # Set up the prompt
        predefined_prompt = get_prompt(prompt_name)
        if predefined_prompt:
            # Auto-configure financial tools for finchat_prompt and react_prompt
            if prompt_name in ["finchat_prompt", "react_prompt"]:
                financial_tools = get_financial_tools()
                config.tools = financial_tools
            
            # Check if it's a template prompt
            if is_template(prompt_name):
                try:
                    # Use the template rendering for all prompts including react_prompt
                    config.system_prompt = render_template_with_tools(prompt_name, tools=config.tools)
                    print(f"🤖 Rendered template prompt for: {prompt_name}")
                    print(f"🤖 Template preview: {config.system_prompt[:200]}...")
                except ValueError as e:
                    raise HTTPException(status_code=400, detail=f"Template error: {e}")
            else:
                config.system_prompt = predefined_prompt
        else:
            raise HTTPException(status_code=404, detail=f"Prompt '{prompt_name}' not found")
        
        # Create chatbot instance
        print(f"🤖 Creating new chatbot instance for: {prompt_name}")
        print(f"🤖 Config system_prompt preview: {config.system_prompt[:100] if config.system_prompt else 'None'}...")
        chatbot_instances[prompt_name] = ChatbotAgent(config, interaction_store)
    else:
        print(f"🤖 Reusing existing chatbot instance for: {prompt_name}")
    
    return chatbot_instances[prompt_name]


@app.get("/favicon.ico")
async def favicon():
    """Return 204 No Content for favicon requests"""
    return Response(status_code=204)

@app.get("/", response_class=HTMLResponse)
async def get_chat_ui():
    """Serve the chat UI"""
    html_content = r"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>LangGraph Chatbot</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #f5f5f5;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                background: white;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                overflow: hidden;
            }
            .header {
                background: #2563eb;
                color: white;
                padding: 20px;
                text-align: center;
            }
            .chat-container {
                height: 500px;
                overflow-y: auto;
                padding: 20px;
                border-bottom: 1px solid #e5e7eb;
            }
            .message {
                margin-bottom: 15px;
                padding: 10px 15px;
                border-radius: 10px;
                max-width: 80%;
                white-space: pre-wrap;
                word-wrap: break-word;
                line-height: 1.5;
            }
            .user-message {
                background: #dbeafe;
                margin-left: auto;
                text-align: right;
            }
            .bot-message {
                background: #f3f4f6;
                margin-right: auto;
            }
            .input-container {
                padding: 20px;
                display: flex;
                gap: 10px;
                align-items: center;
            }
            .prompt-select {
                padding: 10px;
                border: 1px solid #d1d5db;
                border-radius: 5px;
                background: white;
            }
            #messageInput {
                flex: 1;
                padding: 10px;
                border: 1px solid #d1d5db;
                border-radius: 5px;
                font-size: 16px;
                min-height: 40px;
                max-height: 120px;
                resize: vertical;
                font-family: inherit;
            }
            #sendButton {
                padding: 10px 20px;
                background: #2563eb;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
            }
            #sendButton:hover {
                background: #1d4ed8;
            }
            #sendButton:disabled {
                background: #9ca3af;
                cursor: not-allowed;
            }
            .loading {
                display: none;
                text-align: center;
                padding: 10px;
                color: #6b7280;
            }
            .engagement-score {
                font-size: 12px;
                color: #6b7280;
                margin-top: 5px;
            }
            .message code {
                background: #f3f4f6;
                padding: 2px 4px;
                border-radius: 3px;
                font-family: 'Courier New', monospace;
                font-size: 14px;
            }
            .message pre {
                background: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 5px;
                padding: 10px;
                margin: 10px 0;
                overflow-x: auto;
                font-family: 'Courier New', monospace;
                font-size: 14px;
            }
            .message pre code {
                background: none;
                padding: 0;
                border-radius: 0;
            }
            .react-steps {
                margin-top: 10px;
            }
            .react-step {
                margin-bottom: 8px;
                padding: 8px;
                border-left: 3px solid #e5e7eb;
                background: #f9fafb;
                border-radius: 0 5px 5px 0;
            }
            .react-question {
                border-left-color: #3b82f6;
                background: #eff6ff;
            }
            .react-thought {
                border-left-color: #8b5cf6;
                background: #f3e8ff;
            }
            .react-action {
                border-left-color: #f59e0b;
                background: #fffbeb;
            }
            .react-action_input {
                border-left-color: #10b981;
                background: #ecfdf5;
            }
            .react-observation {
                border-left-color: #06b6d4;
                background: #ecfeff;
            }
            .react-final_answer {
                border-left-color: #ef4444;
                background: #fef2f2;
                border: 1px solid #fecaca;
                margin-top: 15px;
                padding: 15px;
                font-weight: 500;
            }
            .session-info {
                padding: 10px 20px;
                background: #f9fafb;
                border-bottom: 1px solid #e5e7eb;
                font-size: 14px;
                color: #6b7280;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🤖 LangGraph Chatbot</h1>
                <p>Web Chat Interface</p>
            </div>
            <div class="session-info">
                <span>Session: <span id="sessionId">Starting new session...</span></span>
                <span style="margin-left: 20px;">Prompt: <span id="currentPrompt">finchat_prompt</span></span>
                <button onclick="toggleDebugPanel()" style="margin-left: 20px; padding: 2px 8px; font-size: 12px;">🔍 Debug</button>
            </div>
            <div id="debugPanel" style="display: none; background: #f0f0f0; padding: 10px; margin: 10px 0; border-radius: 5px; font-family: monospace; font-size: 12px;">
                <strong>Debug Info:</strong>
                <div id="debugInfo">Click debug button to load info...</div>
                <button onclick="loadDebugInfo()" style="margin-top: 5px;">Refresh Debug Info</button>
            </div>
            <div class="chat-container" id="chatContainer">
                <div class="message bot-message">
                    <strong>Bot:</strong> Hello! I'm your financial assistant. I use a thinking process that shows Question → Thought → Action → Observation → Final Answer. How can I help you today?
                </div>
            </div>
            <div class="loading" id="loading">
                <p>🤔 Thinking...</p>
            </div>
            <div class="input-container">
                <select class="prompt-select" id="promptSelect">
                    <option value="finchat_prompt">Financial Chat</option>
                    <option value="react_prompt">React Pattern (shows thinking)</option>
                    <option value="coding_mentor">Coding Mentor</option>
                    <option value="creative_writer">Creative Writer</option>
                </select>
                <textarea id="messageInput" placeholder="Type your message... (Enter to send, Shift+Enter for new line, ↑↓ for history)" 
                         onkeydown="handleKeyPress(event)" rows="1"></textarea>
                <button id="sendButton" onclick="sendMessage()">Send</button>
            </div>
        </div>

        <script>
            let currentSessionId = null;
            let currentPrompt = 'finchat_prompt';
            let messageHistory = [];
            let historyIndex = -1;

            async function loadAvailablePrompts() {
                try {
                    console.log('🔍 [FRONTEND] Loading available prompts...');
                    const response = await fetch('/api/fastapi/api/prompts');
                    const prompts = await response.json();
                    console.log('🔍 [FRONTEND] Available prompts:', prompts);
                    
                    const select = document.getElementById('promptSelect');
                    select.innerHTML = '';
                    
                    prompts.forEach(prompt => {
                        const option = document.createElement('option');
                        option.value = prompt;
                        option.textContent = prompt.replace(/_/g, ' ').replace(/\\b\\w/g, l => l.toUpperCase());
                        select.appendChild(option);
                    });
                    
                    console.log('🔍 [FRONTEND] Prompt dropdown populated');
                    
                    // Set default to finchat_prompt if available
                    if (prompts.includes('finchat_prompt')) {
                        select.value = 'finchat_prompt';
                    }
                } catch (error) {
                    console.error('Failed to load prompts:', error);
                }
            }

            function handleKeyPress(event) {
                if (event.key === 'Enter') {
                    if (event.shiftKey) {
                        // Allow new line with Shift+Enter
                        return true;
                    } else {
                        // Send message with Enter
                        event.preventDefault();
                        sendMessage();
                        return false;
                    }
                } else if (event.key === 'ArrowUp') {
                    event.preventDefault();
                    navigateHistory('up');
                    return false;
                } else if (event.key === 'ArrowDown') {
                    event.preventDefault();
                    navigateHistory('down');
                    return false;
                }
            }

            function navigateHistory(direction) {
                const input = document.getElementById('messageInput');
                
                if (messageHistory.length === 0) {
                    return;
                }

                if (direction === 'up') {
                    if (historyIndex === -1) {
                        // First time pressing up - save current input and go to most recent
                        if (input.value.trim()) {
                            // Save current input as temporary entry
                            messageHistory.unshift(input.value);
                            historyIndex = 1; // Skip the temp entry we just added
                        } else {
                            historyIndex = 0;
                        }
                    } else if (historyIndex < messageHistory.length - 1) {
                        historyIndex++;
                    }
                } else if (direction === 'down') {
                    if (historyIndex > 0) {
                        historyIndex--;
                    } else if (historyIndex === 0) {
                        // Back to empty or temp input
                        if (messageHistory[0] && messageHistory[0] === input.value) {
                            // Remove temp entry and clear
                            messageHistory.shift();
                        }
                        historyIndex = -1;
                        input.value = '';
                        autoResizeTextarea();
                        return;
                    }
                }

                if (historyIndex >= 0 && historyIndex < messageHistory.length) {
                    input.value = messageHistory[historyIndex];
                    autoResizeTextarea();
                    
                    // Move cursor to end
                    setTimeout(() => {
                        input.setSelectionRange(input.value.length, input.value.length);
                    }, 0);
                }
            }

            // Auto-resize textarea based on content
            function autoResizeTextarea() {
                const textarea = document.getElementById('messageInput');
                textarea.style.height = 'auto';
                textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
            }

            // Debug panel functions
            function toggleDebugPanel() {
                const panel = document.getElementById('debugPanel');
                if (panel.style.display === 'none') {
                    panel.style.display = 'block';
                    loadDebugInfo();
                } else {
                    panel.style.display = 'none';
                }
            }

            async function loadDebugInfo() {
                try {
                    const response = await fetch('/api/fastapi/api/debug/chatbot-instances');
                    const debugData = await response.json();
                    
                    const debugInfo = document.getElementById('debugInfo');
                    debugInfo.innerHTML = `
                        <div><strong>Current Prompt:</strong> ${currentPrompt}</div>
                        <div><strong>Current Session:</strong> ${currentSessionId || 'None'}</div>
                        <div><strong>Active Chatbot Instances:</strong> ${debugData.active_instances.join(', ') || 'None'}</div>
                        <div><strong>Instance Count:</strong> ${debugData.instance_count}</div>
                        <hr style="margin: 5px 0;">
                        <div><strong>Instance Details:</strong></div>
                        ${Object.entries(debugData.instances_detail || {}).map(([name, details]) => 
                            `<div style="margin-left: 10px; margin-bottom: 10px; border: 1px solid #ddd; padding: 5px; border-radius: 3px;">
                                <strong>${name}:</strong><br>
                                - Model: ${details.model_name || 'Unknown'}<br>
                                - Temperature: ${details.temperature || 'Unknown'}<br>
                                - Tools: ${details.tools_count || 0} (${(details.tool_names || []).join(', ') || 'None'})<br>
                                - API Key Set: ${details.openai_api_key_set ? 'Yes' : 'No'}<br>
                                - Prompt: ${(details.system_prompt_preview || 'None').substring(0, 150)}...
                            </div>`
                        ).join('')}
                    `;
                } catch (error) {
                    document.getElementById('debugInfo').innerHTML = `Error loading debug info: ${error}`;
                }
            }

            // Add event listener for auto-resize
            document.addEventListener('DOMContentLoaded', function() {
                const textarea = document.getElementById('messageInput');
                textarea.addEventListener('input', autoResizeTextarea);
                loadAvailablePrompts();
            });

            async function sendMessage() {
                const input = document.getElementById('messageInput');
                const message = input.value.trim();
                const promptSelect = document.getElementById('promptSelect');
                const selectedPrompt = promptSelect.value;
                
                if (!message) return;

                // Check if prompt changed
                if (selectedPrompt !== currentPrompt) {
                    console.log(`🔍 [FRONTEND] Prompt changed: ${currentPrompt} → ${selectedPrompt}`);
                    currentPrompt = selectedPrompt;
                    currentSessionId = null; // Start new session with new prompt
                    document.getElementById('currentPrompt').textContent = selectedPrompt;
                    
                    // Reset message history for navigation
                    resetMessageHistory();
                    
                    // Clear chat if prompt changed
                    const chatContainer = document.getElementById('chatContainer');
                    let welcomeMessage = '';
                    if (selectedPrompt === 'react_prompt') {
                        welcomeMessage = 'Switched to React Pattern mode. I will show my thinking process step by step: Question → Thought → Action → Observation → Final Answer.';
                    } else if (selectedPrompt === 'finchat_prompt') {
                        welcomeMessage = 'Switched to Financial Chat mode. I will show my reasoning process: Question → Thought → Action → Observation → Final Answer. How can I help you optimize your portfolio?';
                    } else {
                        welcomeMessage = 'Switched to ' + selectedPrompt.replace('_', ' ') + ' mode. How can I help you?';
                    }
                    chatContainer.innerHTML = '<div class="message bot-message"><strong>Bot:</strong> ' + welcomeMessage + '</div>';
                }

                // Add message to history and reset history navigation
                if (message && !messageHistory.includes(message)) {
                    // Remove temporary entry if it exists
                    if (messageHistory.length > 0 && messageHistory[0] === message) {
                        messageHistory.shift();
                    }
                    // Add to beginning of history (most recent first)
                    messageHistory.unshift(message);
                    
                    // Limit history size to 50 messages
                    if (messageHistory.length > 50) {
                        messageHistory = messageHistory.slice(0, 50);
                    }
                }
                historyIndex = -1; // Reset history navigation

                // Add user message to chat
                addMessageToChat('user', message);
                input.value = '';
                
                // Reset textarea height
                autoResizeTextarea();
                
                // Show loading
                document.getElementById('loading').style.display = 'block';
                document.getElementById('sendButton').disabled = true;

                const requestPayload = {
                    message: message,
                    session_id: currentSessionId,
                    prompt_name: currentPrompt
                };
                console.log('🔍 [FRONTEND] Request payload:', requestPayload);
                console.log(`🔍 [FRONTEND] Sending to: /api/fastapi/api/chat`);

                try {
                    const response = await fetch('/api/fastapi/api/chat', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(requestPayload)
                    });

                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }

                    const data = await response.json();
                    console.log('🔍 [FRONTEND] Response data:', data);
                    
                    // Update session ID if this is a new session
                    if (!currentSessionId) {
                        currentSessionId = data.session_id;
                        document.getElementById('sessionId').textContent = currentSessionId.substring(0, 8) + '...';
                        console.log(`🔍 [FRONTEND] Session updated: ${currentSessionId}`);
                        
                        // Load previous messages for history navigation (but don't display them)
                        loadMessageHistoryForNavigation();
                    }

                    // Add bot response to chat
                    addMessageToChat('bot', data.response, data.engagement_score);

                } catch (error) {
                    console.error('Error:', error);
                    addMessageToChat('bot', 'Sorry, there was an error processing your message. Please try again.');
                } finally {
                    // Hide loading
                    document.getElementById('loading').style.display = 'none';
                    document.getElementById('sendButton').disabled = false;
                }
            }

            function parseReactPattern(message) {
                // Parse React pattern steps from the message
                const steps = [];
                const lines = message.split('\n');
                let currentStep = null;
                
                for (let i = 0; i < lines.length; i++) {
                    let line = lines[i].trim();
                    
                    if (line.startsWith('Question:')) {
                        steps.push({type: 'question', content: line.substring(9).trim()});
                        currentStep = steps[steps.length - 1];
                    } else if (line.startsWith('Thought:')) {
                        steps.push({type: 'thought', content: line.substring(8).trim()});
                        currentStep = steps[steps.length - 1];
                    } else if (line.startsWith('Action:')) {
                        steps.push({type: 'action', content: line.substring(7).trim()});
                        currentStep = steps[steps.length - 1];
                    } else if (line.startsWith('Action Input:')) {
                        // Handle multiline Action Input
                        let actionInput = line.substring(13).trim();
                        
                        // Look ahead for numbered or bulleted items
                        for (let j = i + 1; j < lines.length; j++) {
                            const nextLine = lines[j].trim();
                            if (nextLine.match(/^\\\\d+\\./) || nextLine.match(/^[-*]/) || nextLine.match(/^\\\\w+:/)) {
                                actionInput += '\\n' + nextLine;
                                i = j; // Skip these lines in main loop
                            } else if (nextLine.startsWith('Observation:') || nextLine.startsWith('Thought:') || nextLine.startsWith('Action:') || nextLine.startsWith('Final Answer:')) {
                                break;
                            } else if (nextLine && !nextLine.startsWith('Question:')) {
                                actionInput += ' ' + nextLine;
                                i = j;
                            } else {
                                break;
                            }
                        }
                        
                        steps.push({type: 'action_input', content: actionInput});
                        currentStep = steps[steps.length - 1];
                    } else if (line.startsWith('Observation:')) {
                        steps.push({type: 'observation', content: line.substring(12).trim()});
                        currentStep = steps[steps.length - 1];
                    } else if (line.startsWith('Final Answer:')) {
                        // Handle multiline Final Answer
                        let finalAnswer = line.substring(13).trim();
                        
                        // Continue reading until end of message
                        for (let j = i + 1; j < lines.length; j++) {
                            const nextLine = lines[j].trim();
                            if (nextLine) {
                                finalAnswer += '\\n' + nextLine;
                                i = j;
                            }
                        }
                        
                        steps.push({type: 'final_answer', content: finalAnswer});
                        currentStep = steps[steps.length - 1];
                    } else if (line && currentStep && !line.startsWith('Question:') && !line.startsWith('Thought:') && !line.startsWith('Action:') && !line.startsWith('Observation:') && !line.startsWith('Final Answer:')) {
                        // Continue previous step if it's multiline (but not another step type)
                        if (steps.length > 0 && currentStep) {
                            steps[steps.length - 1].content += ' ' + line;
                        }
                    }
                }
                
                return steps;
            }

            function addMessageToChat(sender, message, engagementScore = null) {
                const chatContainer = document.getElementById('chatContainer');
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${sender}-message`;
                
                // Create message content with proper newline handling
                const messageContent = document.createElement('div');
                
                // Add sender label
                const senderLabel = document.createElement('strong');
                senderLabel.textContent = sender === 'user' ? 'You: ' : 'Bot: ';
                messageContent.appendChild(senderLabel);
                
                // Check if this is a React pattern response
                const isReactPattern = sender === 'bot' && 
                    (message.includes('Thought:') || message.includes('Action:') || message.includes('Observation:'));
                
                console.log(`🔍 [FRONTEND] ReAct pattern check: isReactPattern=${isReactPattern}, currentPrompt=${currentPrompt}, message contains 'Thought:'=${message.includes('Thought:')}`);
                
                if (isReactPattern && (currentPrompt === 'react_prompt' || currentPrompt === 'finchat_prompt')) {
                    console.log('🔍 [FRONTEND] Parsing ReAct pattern message');
                    // Parse and display React pattern steps
                    const steps = parseReactPattern(message);
                    console.log('🔍 [FRONTEND] Parsed ReAct steps:', steps);
                    
                    const reactContainer = document.createElement('div');
                    reactContainer.className = 'react-steps';
                    
                    steps.forEach(step => {
                        const stepDiv = document.createElement('div');
                        stepDiv.className = `react-step react-${step.type}`;
                        
                        const stepLabel = document.createElement('strong');
                        const stepContent = document.createElement('span');
                        
                        switch(step.type) {
                            case 'question':
                                stepLabel.textContent = '❓ Question: ';
                                stepLabel.style.color = '#3b82f6';
                                break;
                            case 'thought':
                                stepLabel.textContent = '🤔 Thought: ';
                                stepLabel.style.color = '#8b5cf6';
                                break;
                            case 'action':
                                stepLabel.textContent = '⚡ Action: ';
                                stepLabel.style.color = '#f59e0b';
                                break;
                            case 'action_input':
                                stepLabel.textContent = '📥 Action Input: ';
                                stepLabel.style.color = '#10b981';
                                break;
                            case 'observation':
                                stepLabel.textContent = '👁️ Observation: ';
                                stepLabel.style.color = '#06b6d4';
                                break;
                            case 'final_answer':
                                stepLabel.textContent = '✅ Final Answer: ';
                                stepLabel.style.color = '#ef4444';
                                stepDiv.style.backgroundColor = '#fef2f2';
                                stepDiv.style.border = '1px solid #fecaca';
                                stepDiv.style.borderRadius = '5px';
                                stepDiv.style.padding = '10px';
                                stepDiv.style.marginTop = '10px';
                                break;
                        }
                        
                        stepContent.textContent = step.content;
                        stepDiv.appendChild(stepLabel);
                        stepDiv.appendChild(stepContent);
                        reactContainer.appendChild(stepDiv);
                        
                        // Add spacing between steps
                        if (step.type !== 'final_answer') {
                            const spacer = document.createElement('div');
                            spacer.style.height = '8px';
                            reactContainer.appendChild(spacer);
                        }
                    });
                    
                    messageContent.appendChild(reactContainer);
                } else {
                    // Regular message formatting
                    const messageText = document.createElement('span');
                    
                    // Convert markdown-like formatting for better display
                    let formattedMessage = message
                        .replace(/```([^`]+)```/g, '<pre><code>$1</code></pre>')  // Code blocks
                        .replace(/`([^`]+)`/g, '<code>$1</code>')  // Inline code
                        .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')  // Bold
                        .replace(/\*([^*]+)\*/g, '<em>$1</em>');  // Italic
                    
                    messageText.innerHTML = formattedMessage;
                    messageContent.appendChild(messageText);
                }
                
                // Add engagement score if provided
                if (engagementScore !== null) {
                    const scoreDiv = document.createElement('div');
                    scoreDiv.className = 'engagement-score';
                    scoreDiv.textContent = `💯 Engagement: ${engagementScore.toFixed(2)}`;
                    messageContent.appendChild(scoreDiv);
                }
                
                messageDiv.appendChild(messageContent);
                chatContainer.appendChild(messageDiv);
                
                // Scroll to bottom
                chatContainer.scrollTop = chatContainer.scrollHeight;
            }

            async function loadMessageHistoryForNavigation() {
                if (!currentSessionId) return;
                
                try {
                    const response = await fetch(`/api/fastapi/api/sessions/${currentSessionId}/history?user_id=web_user&limit=20`);
                    if (response.ok) {
                        const historyData = await response.json();
                        
                        // Extract user messages for history navigation (reverse order, most recent first)
                        const userMessages = historyData.messages
                            .filter(msg => msg.user && msg.user.trim())
                            .map(msg => msg.user)
                            .reverse(); // Most recent first
                        
                        // Add to message history (avoid duplicates)
                        userMessages.forEach(msg => {
                            if (msg && !messageHistory.includes(msg)) {
                                messageHistory.push(msg);
                            }
                        });
                        
                        // Limit total history size
                        if (messageHistory.length > 50) {
                            messageHistory = messageHistory.slice(0, 50);
                        }
                    }
                } catch (error) {
                    console.log('Could not load message history for navigation:', error);
                }
            }

            // Reset history when prompt changes
            function resetMessageHistory() {
                messageHistory = [];
                historyIndex = -1;
            }

            // Load prompts on page load
            window.addEventListener('load', loadAvailablePrompts);
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(message: ChatMessage, background_tasks: BackgroundTasks):
    """Main chat endpoint"""
    try:
        # Get or create chatbot for the specified prompt
        prompt_name = message.prompt_name or "finchat_prompt"
        print(f"🔍 [DIRECT] Received prompt_name: {message.prompt_name} -> Using: {prompt_name}")
        print(f"🔍 [DIRECT] Message: {message.message[:50]}...")
        print(f"🔍 [DIRECT] Session: {message.session_id}, User: {message.user_id}")
        
        chatbot = get_or_create_chatbot(prompt_name)
        print(f"🔍 [DIRECT] Chatbot instance created/retrieved for: {prompt_name}")
        print(f"🔍 [DIRECT] System prompt preview: {chatbot.config.system_prompt[:150]}...")
        print(f"🔍 [DIRECT] Tools available: {len(chatbot.config.tools) if chatbot.config.tools else 0}")
        
        # Process the chat message using invoke() method (LangGraph convention)
        response = chatbot.invoke({
            "message": message.message,
            "user_id": message.user_id,
            "session_id": message.session_id
        })
        
        return ChatResponse(
            response=response["response"],
            session_id=response["session_id"],
            engagement_score=response["engagement_score"],
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")


@app.get("/api/prompts")
async def get_available_prompts():
    """Get list of available prompts"""
    try:
        prompts = list_prompts()
        return prompts
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading prompts: {str(e)}")


@app.get("/api/sessions/{session_id}/history")
async def get_chat_history(session_id: str, user_id: str = "web_user", limit: int = 50):
    """Get chat history for a session"""
    try:
        # Get the appropriate chatbot (defaulting to finchat_prompt)
        chatbot = get_or_create_chatbot("finchat_prompt")
        
        messages = chatbot.get_chat_history(user_id, session_id, limit=limit)
        formatted_messages = []
        
        for msg in messages:
            formatted_messages.append({
                "timestamp": msg.get("timestamp", ""),
                "user": msg.get("user_input", ""),
                "bot": msg.get("bot_response", ""),
                "engagement_score": msg.get("engagement_score", 0.0)
            })
        
        session_info = SessionInfo(
            session_id=session_id,
            user_id=user_id,
            prompt_name="finchat_prompt",  # Default for now
            created_at=formatted_messages[0]["timestamp"] if formatted_messages else datetime.now().isoformat(),
            message_count=len(formatted_messages)
        )
        
        return ChatHistory(
            messages=formatted_messages,
            session_info=session_info
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving chat history: {str(e)}")


@app.get("/api/stats")
async def get_chat_statistics():
    """Get chat engagement statistics"""
    try:
        global interaction_store
        metrics = interaction_store.get_engagement_metrics()
        return metrics
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving statistics: {str(e)}")


@app.delete("/api/sessions/{session_id}")
async def delete_session(session_id: str, user_id: str = "web_user"):
    """Delete a chat session"""
    try:
        # This would require implementing session deletion in InteractionStore
        return {"message": f"Session {session_id} deletion requested"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting session: {str(e)}")


# Duplicate endpoints with /api/fastapi/api/ prefix for Next.js proxy integration
@app.post("/api/fastapi/api/chat", response_model=ChatResponse)
async def chat_endpoint_proxy(message: ChatMessage, background_tasks: BackgroundTasks):
    """Main chat endpoint (Next.js proxy version)"""
    print(f"🔍 [PROXY] Received prompt_name: {message.prompt_name}")
    print(f"🔍 [PROXY] Message: {message.message[:50]}...")
    print(f"🔍 [PROXY] Session: {message.session_id}, User: {message.user_id}")
    print(f"🔍 [PROXY] Forwarding to direct endpoint...")
    
    result = await chat_endpoint(message, background_tasks)
    print(f"🔍 [PROXY] Response generated successfully")
    return result

@app.get("/api/fastapi/api/prompts")
async def get_prompts_proxy():
    """Get available prompts (Next.js proxy version)"""
    return await get_available_prompts()

@app.get("/api/fastapi/api/sessions/{session_id}/history")
async def get_session_history_proxy(session_id: str, user_id: str = "web_user", limit: int = 20):
    """Get chat history for a session (Next.js proxy version)"""
    return await get_chat_history(session_id, user_id, limit)

@app.get("/api/fastapi/api/stats")
async def get_chat_stats_proxy():
    """Get chat statistics (Next.js proxy version)"""
    return await get_chat_statistics()

@app.delete("/api/fastapi/api/sessions/{session_id}")
async def delete_session_proxy(session_id: str, user_id: str = "web_user"):
    """Delete a chat session (Next.js proxy version)"""
    return await delete_session(session_id, user_id)


# Debug endpoints for troubleshooting prompt issues
@app.get("/api/debug/chatbot-instances")
async def get_debug_chatbot_instances():
    """Debug endpoint to show active chatbot configurations"""
    global chatbot_instances
    
    debug_info = {
        "active_instances": list(chatbot_instances.keys()),
        "instance_count": len(chatbot_instances),
        "instances_detail": {}
    }
    
    for prompt_name, chatbot in chatbot_instances.items():
        try:
            system_prompt_preview = chatbot.config.system_prompt[:200] if chatbot.config.system_prompt else "None"
            tools_count = len(chatbot.config.tools) if chatbot.config.tools else 0
            
            debug_info["instances_detail"][prompt_name] = {
                "system_prompt_preview": system_prompt_preview + "..." if len(system_prompt_preview) == 200 else system_prompt_preview,
                "tools_count": tools_count,
                "has_tools": tools_count > 0,
                "config_type": type(chatbot.config).__name__,
                "model_name": getattr(chatbot.config, 'model_name', 'Unknown'),
                "temperature": getattr(chatbot.config, 'temperature', 'Unknown'),
                "max_tokens": getattr(chatbot.config, 'max_tokens', 'Unknown'),
                "openai_api_key_set": bool(getattr(chatbot.config, 'openai_api_key', None)),
                "tool_names": [tool.__name__ if hasattr(tool, '__name__') else str(tool) for tool in (chatbot.config.tools or [])]
            }
        except Exception as e:
            debug_info["instances_detail"][prompt_name] = {
                "error": str(e)
            }
    
    return debug_info

@app.get("/api/fastapi/api/debug/chatbot-instances")
async def get_debug_chatbot_instances_proxy():
    """Debug endpoint (proxy version)"""
    return await get_debug_chatbot_instances()


def run_web_server(host: str = "0.0.0.0", port: int = 8000, debug: bool = False):
    """Run the FastAPI web server"""
    print(f"🌐 Starting LangGraph Chatbot Web Server")
    print(f"📍 Access the chat interface at: http://{host}:{port}")
    print(f"📚 API documentation at: http://{host}:{port}/docs")
    print(f"🔧 Debug mode: {debug}")
    
    uvicorn.run(
        "web_chat:app",
        host=host,
        port=port,
        reload=debug,
        log_level="info" if debug else "warning"
    )


if __name__ == "__main__":
    # Allow command line arguments for development
    import sys
    
    host = "0.0.0.0"
    port = 8000
    debug = False
    
    if len(sys.argv) > 1:
        if "--debug" in sys.argv:
            debug = True
        if "--port" in sys.argv:
            port_index = sys.argv.index("--port") + 1
            if port_index < len(sys.argv):
                port = int(sys.argv[port_index])
    
    run_web_server(host=host, port=port, debug=debug)