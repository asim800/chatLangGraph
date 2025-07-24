#!/usr/bin/env python3
"""
React Pattern with Full LangGraph Conventions
Uses invoke() method consistently for all components: agents, prompt templates, tools, etc.
"""

import sys
import os
import readline
from dotenv import load_dotenv
from typing import Dict, Any, List, Optional

# Load environment variables
load_dotenv()
sys.path.insert(0, os.path.dirname(__file__))

from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from typing_extensions import TypedDict

# Define tools using @tool decorator (LangGraph convention)
@tool
def calculate_risk(portfolio: str) -> str:
    """Calculate portfolio risk score (0-1, where 1 is highest risk)"""
    print(f"🔧 TOOL EXECUTION: calculate_risk.invoke({{'portfolio': '{portfolio}'}})")
    
    if "crypto" in portfolio.lower() or "bitcoin" in portfolio.lower():
        result = "0.8 (HIGH risk) - Cryptocurrency investments are highly volatile"
    elif "bonds" in portfolio.lower() or "treasury" in portfolio.lower():
        result = "0.2 (LOW risk) - Government bonds are stable investments"
    elif "stocks" in portfolio.lower() or "equity" in portfolio.lower():
        result = "0.6 (MODERATE risk) - Stock investments have moderate volatility"
    else:
        result = "0.4 (MODERATE risk) - Mixed portfolio with balanced risk"
    
    print(f"📊 TOOL RESULT: {result}")
    return result

@tool
def get_stock_info(symbol: str) -> str:
    """Get basic stock information"""
    print(f"🔧 TOOL EXECUTION: get_stock_info.invoke({{'symbol': '{symbol}'}})")
    
    stock_data = {
        "AAPL": "Apple Inc. - Current: $150.25, +2.5% today, Strong Buy rating",
        "MSFT": "Microsoft Corp. - Current: $300.75, +1.2% today, Buy rating", 
        "TSLA": "Tesla Inc. - Current: $200.50, -3.1% today, Hold rating",
        "SPY": "S&P 500 ETF - Current: $400.80, +0.8% today, Diversified index fund"
    }
    
    result = stock_data.get(symbol.upper(), f"Stock data for {symbol} not available in demo database")
    print(f"📊 TOOL RESULT: {result}")
    return result

@tool
def portfolio_analyzer(holdings: str) -> str:
    """Analyze portfolio diversification and provide recommendations"""
    print(f"🔧 TOOL EXECUTION: portfolio_analyzer.invoke({{'holdings': '{holdings}'}})")
    
    result = f"""Portfolio Analysis for: {holdings}
✅ Diversification: Good mix across sectors
📊 Risk Level: Moderate (0.45/1.0)  
💰 Expected Return: 8-12% annually
🎯 Recommendation: Consider adding international exposure
Key Insights: Well balanced portfolio with room for international exposure"""
    
    print(f"📊 TOOL RESULT: Analysis completed for {holdings}")
    return result

# State definition for LangGraph
class ReactState(TypedDict):
    question: str
    thoughts: List[str]
    actions: List[str]
    action_inputs: List[str]
    observations: List[str]
    final_answer: str
    step_count: int
    max_steps: int

class ReactAgent:
    """React Agent using full LangGraph conventions with invoke() throughout"""
    
    def __init__(self, model_name: str = "gpt-3.5-turbo", temperature: float = 0):
        # Initialize LLM (LangGraph convention)
        self.llm = ChatOpenAI(model=model_name, temperature=temperature)
        
        # Initialize tools (LangGraph convention)
        self.tools = [calculate_risk, get_stock_info, portfolio_analyzer]
        self.tool_node = ToolNode(self.tools)
        
        # Create tool mapping for easy lookup
        self.tool_map = {tool.name: tool for tool in self.tools}
        
        # Initialize prompt templates using LangGraph conventions
        self._setup_prompt_templates()
        
        # Build the React graph
        self.graph = self._build_react_graph()
    
    def _setup_prompt_templates(self):
        """Setup prompt templates using LangGraph PromptTemplate.invoke() convention"""
        
        # React reasoning prompt template
        self.react_prompt = PromptTemplate(
            input_variables=["question", "tools", "tool_names", "thoughts", "actions", "observations"],
            template="""Answer the following question using the React pattern. You have access to these tools:

{tools}

Available tool names: {tool_names}

Question: {question}

Previous reasoning (if any):
Thoughts: {thoughts}
Actions: {actions}  
Observations: {observations}

Continue with the React pattern:
Thought: (think about what to do next)
Action: (choose one tool from: {tool_names})
Action Input: (provide the input for the chosen tool)

If you have enough information, instead provide:
Thought: I now know the final answer
Final Answer: (the complete answer to the original question)
"""
        )
        
        # Tool descriptions template
        self.tool_desc_prompt = PromptTemplate(
            input_variables=["tools"],
            template="""Tools available:
{tools}"""
        )
    
    def _build_react_graph(self) -> StateGraph:
        """Build React graph using LangGraph conventions"""
        
        workflow = StateGraph(ReactState)
        
        # Add nodes
        workflow.add_node("reasoning", self._reasoning_node)
        workflow.add_node("tool_execution", self._tool_execution_node)
        workflow.add_node("final_answer", self._final_answer_node)
        
        # Set entry point
        workflow.set_entry_point("reasoning")
        
        # Add conditional edges
        workflow.add_conditional_edges(
            "reasoning",
            self._should_continue,
            {
                "continue": "tool_execution",
                "end": "final_answer"
            }
        )
        
        workflow.add_edge("tool_execution", "reasoning")
        workflow.add_edge("final_answer", END)
        
        return workflow.compile()
    
    def _reasoning_node(self, state: ReactState) -> ReactState:
        """Reasoning node using prompt template invoke()"""
        print(f"\n💭 REASONING STEP {state['step_count'] + 1}")
        print("-" * 40)
        
        # Prepare tool descriptions using prompt template invoke()
        tool_descriptions = []
        for tool in self.tools:
            tool_descriptions.append(f"- {tool.name}: {tool.description}")
        
        tools_desc = "\n".join(tool_descriptions)
        tool_names = [tool.name for tool in self.tools]
        
        # Use PromptTemplate.invoke() (LangGraph convention)
        prompt_input = {
            "question": state["question"],
            "tools": tools_desc,
            "tool_names": tool_names,
            "thoughts": " | ".join(state["thoughts"]) if state["thoughts"] else "None",
            "actions": " | ".join(state["actions"]) if state["actions"] else "None", 
            "observations": " | ".join(state["observations"]) if state["observations"] else "None"
        }
        
        formatted_prompt = self.react_prompt.invoke(prompt_input)
        print(f"📝 PROMPT: {formatted_prompt.text[:200]}...")
        
        # Use LLM.invoke() (LangGraph convention)
        response = self.llm.invoke([HumanMessage(content=formatted_prompt.text)])
        
        print(f"🤖 LLM RESPONSE:\n{response.content}")
        
        # Parse the response
        content = response.content.strip()
        lines = content.split('\n')
        
        new_thought = ""
        new_action = ""
        new_action_input = ""
        final_answer = ""
        
        for line in lines:
            line = line.strip()
            if line.startswith("Thought:"):
                new_thought = line[8:].strip()
                print(f"💭 THOUGHT: {new_thought}")
            elif line.startswith("Action:"):
                new_action = line[7:].strip()
                print(f"⚡ ACTION: {new_action}")
            elif line.startswith("Action Input:"):
                new_action_input = line[13:].strip()
                print(f"📥 ACTION INPUT: {new_action_input}")
            elif line.startswith("Final Answer:"):
                final_answer = line[13:].strip()
                print(f"🎯 FINAL ANSWER: {final_answer}")
        
        # Update state
        if new_thought:
            state["thoughts"].append(new_thought)
        if new_action:
            state["actions"].append(new_action)
        if new_action_input:
            state["action_inputs"].append(new_action_input)
        if final_answer:
            state["final_answer"] = final_answer
        
        state["step_count"] += 1
        
        return state
    
    def _tool_execution_node(self, state: ReactState) -> ReactState:
        """Tool execution node using tool.invoke()"""
        print(f"\n🔧 TOOL EXECUTION STEP")
        print("-" * 40)
        
        if not state["actions"] or not state["action_inputs"]:
            error_obs = "Error: No action or action input provided"
            state["observations"].append(error_obs)
            print(f"❌ {error_obs}")
            return state
        
        # Get the latest action and input
        action = state["actions"][-1]
        action_input = state["action_inputs"][-1]
        
        print(f"Executing: {action} with input: {action_input}")
        
        # Find and invoke the tool using tool.invoke() (LangGraph convention)
        if action in self.tool_map:
            try:
                tool = self.tool_map[action]
                
                # Parse action input (simple string parsing for demo)
                # In production, you'd want more robust parsing
                if action_input.startswith('"') and action_input.endswith('"'):
                    parsed_input = action_input[1:-1]  # Remove quotes
                else:
                    parsed_input = action_input
                
                # Use tool.invoke() (LangGraph convention) 
                if action == "calculate_risk":
                    result = tool.invoke({"portfolio": parsed_input})
                elif action == "get_stock_info":
                    result = tool.invoke({"symbol": parsed_input})
                elif action == "portfolio_analyzer":
                    result = tool.invoke({"holdings": parsed_input})
                else:
                    result = f"Unknown tool: {action}"
                
                observation = f"Tool {action} returned: {result}"
                state["observations"].append(observation)
                print(f"👀 OBSERVATION: {observation}")
                
            except Exception as e:
                error_obs = f"Error executing {action}: {str(e)}"
                state["observations"].append(error_obs)
                print(f"❌ {error_obs}")
        else:
            error_obs = f"Unknown tool: {action}"
            state["observations"].append(error_obs)
            print(f"❌ {error_obs}")
        
        return state
    
    def _final_answer_node(self, state: ReactState) -> ReactState:
        """Final answer node"""
        print(f"\n🎯 FINAL ANSWER NODE")
        print("-" * 40)
        print(f"Final Answer: {state['final_answer']}")
        return state
    
    def _should_continue(self, state: ReactState) -> str:
        """Determine whether to continue or end"""
        # End if we have a final answer or hit max steps
        if state["final_answer"] or state["step_count"] >= state["max_steps"]:
            return "end"
        return "continue"
    
    def invoke(self, question: str, max_steps: int = 5) -> Dict[str, Any]:
        """Main invoke method following LangGraph convention"""
        print(f"🚀 REACT AGENT.INVOKE() - Question: {question}")
        print("=" * 60)
        
        # Initial state
        initial_state = ReactState(
            question=question,
            thoughts=[],
            actions=[],
            action_inputs=[],
            observations=[],
            final_answer="",
            step_count=0,
            max_steps=max_steps
        )
        
        # Use graph.invoke() (LangGraph convention)
        final_state = self.graph.invoke(initial_state)
        
        # Return structured result
        return {
            "question": final_state["question"],
            "thoughts": final_state["thoughts"],
            "actions": final_state["actions"],
            "action_inputs": final_state["action_inputs"],
            "observations": final_state["observations"],
            "final_answer": final_state["final_answer"],
            "steps_taken": final_state["step_count"]
        }

def demonstrate_full_langgraph_conventions():
    """Demonstrate full LangGraph conventions with invoke() throughout"""
    
    print("🎯 FULL LANGGRAPH CONVENTIONS DEMONSTRATION")
    print("=" * 60)
    print("Using invoke() method for:")
    print("• agent.invoke() - Main agent execution")
    print("• prompt_template.invoke() - Prompt formatting") 
    print("• llm.invoke() - Language model calls")
    print("• tool.invoke() - Tool execution")
    print("• graph.invoke() - Graph state transitions")
    print("=" * 60)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found")
        print("💡 Create a .env file with: OPENAI_API_KEY=your-key-here")
        return
    
    # Create agent using LangGraph conventions
    agent = ReactAgent()
    
    # Test questions
    questions = [
        "What's the risk of my crypto portfolio with Bitcoin and Ethereum?",
        "Get me information about AAPL stock and analyze if it's good for a conservative portfolio",
        "Analyze my portfolio with AAPL, MSFT, and Treasury bonds"
    ]
    
    for i, question in enumerate(questions, 1):
        print(f"\n{'='*60}")
        print(f"🧪 TEST {i}: {question}")
        print(f"{'='*60}")
        
        # Use agent.invoke() (LangGraph convention)
        result = agent.invoke(question, max_steps=3)
        
        print(f"\n📋 REACT PATTERN SUMMARY:")
        print(f"Question: {result['question']}")
        print(f"Steps taken: {result['steps_taken']}")
        
        print(f"\n💭 THOUGHTS:")
        for j, thought in enumerate(result['thoughts'], 1):
            print(f"   {j}. {thought}")
        
        print(f"\n⚡ ACTIONS:")
        for j, action in enumerate(result['actions'], 1):
            action_input = result['action_inputs'][j-1] if j <= len(result['action_inputs']) else "N/A"
            print(f"   {j}. {action} with input: {action_input}")
        
        print(f"\n👀 OBSERVATIONS:")
        for j, obs in enumerate(result['observations'], 1):
            print(f"   {j}. {obs}")
        
        print(f"\n🎯 FINAL ANSWER:")
        print(f"   {result['final_answer']}")
        
        if i < len(questions):
            input("\n⏸️  Press Enter to continue to next test...")

def interactive_react_demo():
    """Interactive demo with history navigation"""
    print("\n" + "="*60)
    print("🎮 INTERACTIVE REACT DEMO")
    print("="*60)
    print("💬 Type your questions (or 'quit' to exit)")
    print("🔄 Use ↑/↓ arrow keys to navigate history")
    print()
    
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found")
        return
    
    # Enable readline history
    readline.set_history_length(1000)
    
    # Create agent
    agent = ReactAgent()
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() == 'quit':
                print("👋 Goodbye!")
                break
                
            if not user_input:
                continue
            
            # Add to readline history
            readline.add_history(user_input)
            
            # Use agent.invoke() (LangGraph convention)
            result = agent.invoke(user_input, max_steps=3)
            
            print(f"\n🤖 React Agent Result:")
            print(f"🎯 {result['final_answer']}")
            print(f"📊 Completed in {result['steps_taken']} steps")
            print()
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except EOFError:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def main():
    """Main function showcasing LangGraph conventions"""
    
    # Run demonstration
    demonstrate_full_langgraph_conventions()
    
    # Ask if user wants interactive demo
    try:
        choice = input("\n🎮 Run interactive demo? (y/n): ").strip().lower()
        if choice in ['y', 'yes']:
            interactive_react_demo()
    except (KeyboardInterrupt, EOFError):
        print("\n👋 Goodbye!")
    
    print("\n" + "="*60)
    print("✅ LANGGRAPH CONVENTIONS DEMONSTRATION COMPLETE!")
    print("🔧 All components used invoke() method:")
    print("   • ReactAgent.invoke() - Main agent execution")
    print("   • PromptTemplate.invoke() - Prompt formatting")
    print("   • ChatOpenAI.invoke() - LLM calls")
    print("   • Tool.invoke() - Tool executions")
    print("   • StateGraph.invoke() - Graph state management")
    print("="*60)

if __name__ == "__main__":
    main()