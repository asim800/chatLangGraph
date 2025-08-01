"""
Abstract base class for LangGraph-based chatbot agents
"""

from abc import ABC, abstractmethod
from typing import TypedDict, List, Dict, Any, Optional
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from langchain_core.messages import ToolMessage
from datetime import datetime
import uuid
import re

from ..storage.interaction_store import InteractionStore
from ..config.settings import ChatbotConfig


class ConversationState(TypedDict):
    messages: List[Dict[str, Any]]
    user_id: str
    session_id: str
    context: Dict[str, Any]
    engagement_score: float
    last_activity: datetime
    tool_calls: Optional[List[Dict[str, Any]]]


class BaseChatbotAgent(ABC):
    """Abstract base class for chatbot agents with common functionality"""
    
    def __init__(self, config: ChatbotConfig, interaction_store: InteractionStore):
        self.config = config
        self.interaction_store = interaction_store
        self.tools = config.tools or []
        
        # Initialize LLM with tool binding if tools are available
        self.llm = ChatOpenAI(
            model=config.model_name,
            temperature=config.temperature,
            api_key=config.openai_api_key
        )
        
        # Configure tool binding based on tool_mode setting
        if self.tools and config.tool_mode == "function":
            self.llm = self.llm.bind_tools(self.tools)
            print(f"🔧 Tool mode: function calling enabled")
        elif self.tools and config.tool_mode == "text":
            print(f"🔧 Tool mode: text-based ReAct pattern enabled")
        else:
            print(f"🔧 Tool mode: {config.tool_mode} (no tools available)")
        
        # Initialize tool node if tools are available
        self.tool_node = ToolNode(self.tools) if self.tools else None
        
        # Create tool mapping for easy lookup (LangGraph best practice)
        self.tool_map = {tool.name: tool for tool in self.tools} if self.tools else {}
        
        self.graph = self._build_graph()
    
    @abstractmethod
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph conversation flow - must be implemented by subclasses"""
        pass
    
    def _process_input(self, state: ConversationState) -> ConversationState:
        """Process and contextualize user input"""
        # Add conversation history context
        if len(state["messages"]) > 1:
            recent_messages = state["messages"][-self.config.context_window:]
            state["context"]["recent_history"] = recent_messages
        
        # Update last activity
        state["last_activity"] = datetime.now()
        
        return state
    
    def _generate_response(self, state: ConversationState) -> ConversationState:
        """Generate AI response using LLM"""
        # Build message history for LLM
        messages = []
        
        # Add system prompt
        system_prompt = self.config.system_prompt
        messages.append(SystemMessage(content=system_prompt))
        
        # Add conversation history
        for msg in state["messages"]:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                ai_msg = AIMessage(content=msg["content"])
                # Preserve tool_calls if present
                if "tool_calls" in msg:
                    ai_msg.tool_calls = msg["tool_calls"]
                messages.append(ai_msg)
            elif msg["role"] == "tool":
                # Handle tool messages (these come from ToolNode results)
                tool_msg = ToolMessage(
                    content=msg["content"],
                    tool_call_id=msg.get("tool_call_id", "unknown")
                )
                if "tool_name" in msg:
                    tool_msg.name = msg["tool_name"]  
                messages.append(tool_msg)
        
        # Generate response
        response = self.llm.invoke(messages)
        
        # Check for tool calls
        tool_calls = getattr(response, 'tool_calls', []) or []
        
        # Add AI response to state
        ai_message = {
            "role": "assistant",
            "content": response.content,
            "timestamp": datetime.now().isoformat(),
            "message_id": str(uuid.uuid4())
        }
        
        # Add tool calls if present
        if tool_calls:
            ai_message["tool_calls"] = tool_calls
            state["tool_calls"] = tool_calls
        else:
            state["tool_calls"] = None
        
        state["messages"].append(ai_message)
        
        return state
    
    def _should_call_tools(self, state: ConversationState) -> str:
        """Determine if tools should be called (following l2.py pattern)"""
        # Simple check: if last message has tool calls, execute them
        if state.get("tool_calls"):
            return "call_tools"
        return "continue"
    
    
    def _call_tools(self, state: ConversationState) -> ConversationState:
        """Execute tool calls using LangGraph ToolNode"""
        if not self.tool_node or not state.get("tool_calls"):
            return state
        
        # Execute tools using ToolNode
        try:
            # Convert dictionary messages to LangChain message objects for ToolNode
            langchain_messages = []
            for msg in state["messages"]:
                if msg["role"] == "user":
                    langchain_messages.append(HumanMessage(content=msg["content"]))
                elif msg["role"] == "assistant":
                    # Create AIMessage with tool_calls if present
                    ai_msg = AIMessage(content=msg["content"])
                    if "tool_calls" in msg:
                        # Set tool_calls on the AIMessage
                        ai_msg.tool_calls = msg["tool_calls"]
                    langchain_messages.append(ai_msg)
            
            # Create a compatible state for ToolNode
            tool_state = {"messages": langchain_messages}
            
            # Execute tools using ToolNode
            tool_result = self.tool_node.invoke(tool_state)
            
            # Convert tool result messages back to dictionary format and add to state
            if "messages" in tool_result:
                for msg in tool_result["messages"]:
                    if hasattr(msg, 'content'):
                        tool_message = {
                            "role": "tool",
                            "content": msg.content,
                            "timestamp": datetime.now().isoformat(),
                            "message_id": str(uuid.uuid4())
                        }
                        # Add tool metadata if available
                        if hasattr(msg, 'name'):
                            tool_message["tool_name"] = msg.name
                        if hasattr(msg, 'tool_call_id'):
                            tool_message["tool_call_id"] = msg.tool_call_id
                        state["messages"].append(tool_message)
            
            # Clear tool calls after execution
            state["tool_calls"] = None
            
        except Exception as e:
            # Handle tool execution errors gracefully
            error_message = {
                "role": "assistant",
                "content": f"I encountered an error while using tools: {str(e)}",
                "timestamp": datetime.now().isoformat(),
                "message_id": str(uuid.uuid4())
            }
            state["messages"].append(error_message)
            state["tool_calls"] = None
        
        return state
    
    def _update_engagement(self, state: ConversationState) -> ConversationState:
        """Update engagement metrics"""
        # Simple engagement scoring based on conversation length and recency
        message_count = len(state["messages"])
        time_since_start = (datetime.now() - datetime.fromisoformat(state["messages"][0]["timestamp"])).total_seconds()
        
        # Calculate engagement score (0-1)
        engagement_score = min(1.0, (message_count * 0.1) + (1.0 / max(1, time_since_start / 3600)))
        state["engagement_score"] = engagement_score
        
        return state
    
    def _store_interaction(self, state: ConversationState) -> ConversationState:
        """Store the interaction for later analysis"""
        interaction_data = {
            "user_id": state["user_id"],
            "session_id": state["session_id"],
            "messages": state["messages"],
            "engagement_score": state["engagement_score"],
            "context": state["context"],
            "timestamp": datetime.now().isoformat()
        }
        
        self.interaction_store.store_interaction(interaction_data)
        return state
    
    def get_chat_history(self, user_id: str, session_id: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get chat history for a user session"""
        conversation = self.interaction_store.get_conversation(user_id, session_id)
        
        if not conversation or not conversation.get("messages"):
            return []
        
        messages = conversation["messages"]
        
        if limit is None:
            return messages
        else:
            return messages[-limit:] if limit > 0 else messages
    
    def format_chat_history(self, messages: List[Dict[str, Any]]) -> str:
        """Format chat history for display"""
        if not messages:
            return "No chat history found."
        
        formatted_lines = []
        for msg in messages:
            timestamp = msg.get("timestamp", "")
            role = msg.get("role", "").upper()
            content = msg.get("content", "")
            
            # Format timestamp for better readability
            if timestamp:
                try:
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    formatted_time = dt.strftime("%Y-%m-%d %H:%M:%S")
                except:
                    formatted_time = timestamp
            else:
                formatted_time = "Unknown time"
            
            formatted_lines.append(f"[{formatted_time}] {role}: {content}")
        
        return "\n".join(formatted_lines)
    
    def chat(self, user_message: str, user_id: str, session_id: Optional[str] = None) -> Dict[str, Any]:
        """Main chat interface"""
        if not session_id:
            session_id = str(uuid.uuid4())
        
        # Load existing conversation or create new one
        existing_conversation = self.interaction_store.get_conversation(user_id, session_id)
        
        if existing_conversation:
            messages = existing_conversation["messages"]
            context = existing_conversation.get("context", {})
        else:
            messages = []
            context = {}
        
        # Add user message
        user_msg = {
            "role": "user",
            "content": user_message,
            "timestamp": datetime.now().isoformat(),
            "message_id": str(uuid.uuid4())
        }
        messages.append(user_msg)
        
        # Create initial state
        initial_state = ConversationState(
            messages=messages,
            user_id=user_id,
            session_id=session_id,
            context=context,
            engagement_score=0.0,
            last_activity=datetime.now(),
            tool_calls=None
        )
        
        # Run the graph
        final_state = self.graph.invoke(initial_state)
        
        # Debug: Dump all messages from graph execution
        print(f"\n🔍 [GRAPH_INVOKE] Total messages in final_state: {len(final_state['messages'])}")
        for i, msg in enumerate(final_state["messages"]):
            print(f"🔍 [MESSAGE_{i}] Role: {msg.get('role', 'unknown')}")
            content = msg.get('content', '')
            print(f"🔍 [MESSAGE_{i}] Content preview: {content[:200]}...")
            if len(content) > 200:
                print(f"🔍 [MESSAGE_{i}] Full content: {content}")
        
        # Concatenate all assistant messages for display (supports all agentic patterns)
        assistant_messages = []
        for msg in final_state["messages"]:
            if msg.get("role") == "assistant":
                content = msg.get("content", "").strip()
                if content:  # Only add non-empty messages
                    assistant_messages.append(content)
        
        # Join all assistant messages with newlines for clear separation
        full_response = "\n\n".join(assistant_messages)
        
        # Return the concatenated AI response and metadata
        ai_response = final_state["messages"][-1]
        return {
            "response": full_response if full_response else ai_response.get("content", ""),
            "session_id": session_id,
            "engagement_score": final_state["engagement_score"],
            "message_id": ai_response["message_id"]
        }
    
    def invoke(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        LangGraph convention: invoke method for agent execution
        
        Args:
            input_data: Dictionary containing 'message', 'user_id', and optionally 'session_id'
            
        Returns:
            Dictionary with response data
        """
        message = input_data.get("message", "")
        user_id = input_data.get("user_id", "default_user")
        session_id = input_data.get("session_id")
        
        # Use the existing chat method but maintain LangGraph invoke convention
        return self.chat(message, user_id, session_id)