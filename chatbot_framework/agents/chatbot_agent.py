"""
Core LangGraph-based chatbot agent with sticky conversation capabilities
"""

import os
from langgraph.graph import StateGraph, END
from .base_chatbot_agent import BaseChatbotAgent, ConversationState

# import ipdb

class ChatbotAgent(BaseChatbotAgent):
    def __init__(self, config, interaction_store):
        """Initialize ChatbotAgent with proper parent class initialization"""
        super().__init__(config, interaction_store)
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph conversation flow"""
        graph = StateGraph(ConversationState)
        
        # Add nodes
        graph.add_node("process_input", self._process_input)
        graph.add_node("generate_response", self._generate_response)
        
        # Add tool nodes if tools are available
        if self.tools:
            graph.add_node("call_tools", self._call_tools)
        
        graph.add_node("update_engagement", self._update_engagement)
        graph.add_node("store_interaction", self._store_interaction)
        
        # Add edges
        graph.add_edge("process_input", "generate_response")
        
        # Tool routing logic
        if self.tools:
            graph.add_conditional_edges(
                "generate_response",
                self._should_call_tools,
                {
                    "call_tools": "call_tools",
                    "continue": "update_engagement"
                }
            )
            graph.add_edge("call_tools", "generate_response")
        else:
            graph.add_edge("generate_response", "update_engagement")
        
        graph.add_edge("update_engagement", "store_interaction")
        graph.add_edge("store_interaction", END)
        
        # Set entry point
        graph.set_entry_point("process_input")
              
        app = graph.compile()
        # Generate mermaid PNG diagram
        try:
            png_data = app.get_graph().draw_mermaid_png()
            print(app.get_graph().draw_ascii())
            with open("chatbot_graph.png", "wb") as f:
                f.write(png_data)
            print("✅ Mermaid diagram saved as chatbot_graph.png")
        except Exception as e:
            print(f"⚠️  Could not generate PNG: {e}")

        return app
    

