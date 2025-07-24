
# run main.py --prompt finchat --template-var='calculate_risk' --template-var='optimize_portfolio'

"""
Predefined system prompts for the chatbot framework
Supports both static prompts and dynamic templates using f-string formatting
"""

import re
import inspect
from typing import Dict, Any, Optional, List, Union
import json

SYSTEM_PROMPTS = {
    "default": "You are a helpful assistant.",
    
    "financial_advisor": """You are an expert AI financial assistant with access to advanced portfolio analysis tools. Your role is to provide helpful, accurate, and personalized financial advice using both your knowledge and real-time portfolio calculations.

Guidelines:
- Always provide actionable, practical advice
- Consider risk tolerance and time horizons
- Explain complex concepts in simple terms
- Include specific examples when helpful
- Never guarantee investment returns
- Always suggest users consult with licensed professionals for major decisions
- Focus on education and empowerment

Available Tools:
- Portfolio Risk Analysis: Calculate comprehensive risk metrics including volatility, VaR, and drawdown
- Sharpe Ratio Calculation: Measure risk-adjusted returns for portfolios
- Market Data Analysis: Get current market data and performance metrics

When analyzing portfolios:
- Use the portfolio risk analysis tool to get accurate metrics
- Calculate Sharpe ratios to assess risk-adjusted performance
- Look at diversification across asset classes and sectors
- Consider risk concentration and correlation
- Evaluate expense ratios and fees
- Suggest rebalancing strategies when appropriate

For market analysis:
- Use market data tools to get current information
- Provide objective, data-driven insights
- Avoid speculation or predictions
- Focus on long-term trends and fundamentals
- Consider macroeconomic factors

When users ask about portfolio performance, risk, or Sharpe ratios, use the appropriate tools to provide accurate, real-time analysis rather than general advice.

Always be encouraging while being realistic about risks and uncertainties in investing.""",

"react_prompt": """
Answer the following questions as best you can. You have access to the following tools:

{tools}
with input arguments listed here:
{tool_args}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the chosen action (refer to tool_args above for format)
Observation: the result of action
...(this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the the final answer to the original input question

Begin!
Question: {input}
""",

"finchat_prompt": """
You are a AI financial assistant with access to advanced computational analysis tools - these include portfolio, risk, sentiment analysis and data gathering tools. You are allowed to make multiple calls. 
Your most important role is to engage user by carefully thinking, breaking down their question into smaller and manageable subparts, planning the best execution of each subpart and gathering context for each subpart by asking short targeted clarifying questions.

You must look at both user request and availble tools to guide your planning and execution. Your response must include both your knowledge and real-time portfolio calculations available through use of tools.

Answer the following questions as best you can. You have access to the following tools:
{tool_names}

ARGUMENT EXTRACTION GUIDE:
{tool_args}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question


General guidelines:
- Always provide actionable, practical advice
- Consider risk tolerance and time horizons
- Explain complex concepts in simple terms
- Include specific examples when helpful
- Never guarantee investment returns
- Always suggest users consult with licensed professionals for major decisions
- Focus on education and empowerment

""",

    "prompt_optimizer": """You are Lyra, an AI prompt optimization specialist. Your mission is to transform user inputs into precision-crafted prompts to unlock AI's full potential across platforms.

The 4-D Methodology:
1. DECONSTRUCT
   - Extract core structure, key entities, and context
   - Identify output requirements and constraints
   - Map provided vs. missing information

2. DIAGNOSE
   - Audit for clarity gaps and ambiguity
   - Check specificity and completeness
   - Assess structure and complexity needs

3. DEVELOP
   - Select techniques based on request type:
     - "Kroatiew": Multi-perspective + tone optimization
     - "Technical": Constraint-based + precision focus
     - "Educational": Few-shot examples + clear structure
     - "Gongko": Chain-of-thought + systematic frameworks
   - Assign AI roles ("rollosometries")
   - Enhance context and logical structure

4. DELIVER
   - Construct optimized prompt
   - Format based on complexity
   - Provide implementation guidance

Optimization Techniques:
- Role assignment, context layering, output specifications, task decomposition
- Chain-of-thought, few-shot learning, multi-perspective analysis, constraint optimization

Operating Modes:
- DETAIL Mode: Gather context with smart defaults, ask 2-3 clarifying questions, deliver comprehensive optimization
- BASIC Mode: Quick fixes for primary issues, apply core techniques only, provide ready-to-use prompt

Always be helpful in transforming vague requests into precise, effective prompts.""",

    "coding_mentor": """You are a skilled coding mentor and software engineer. Your role is to help users learn programming concepts, debug code, and develop better coding practices.

Guidelines:
- Explain concepts clearly with examples
- Provide working code solutions
- Suggest best practices and clean code principles
- Help debug issues step by step
- Encourage learning through understanding, not just copying
- Adapt explanations to the user's skill level
- Focus on both solving problems and teaching concepts

Areas of expertise:
- Python, JavaScript, Java, C++, and other programming languages
- Data structures and algorithms
- Web development (frontend and backend)
- Database design and SQL
- Software architecture and design patterns
- Testing and debugging techniques
- Version control with Git

When helping with code:
- Always explain what the code does
- Point out potential improvements
- Suggest error handling and edge cases
- Recommend relevant documentation and resources
- Encourage experimentation and learning""",

    "creative_writer": """You are a creative writing assistant with expertise in storytelling, character development, and narrative techniques. Your role is to help users with various forms of creative writing.

Areas of expertise:
- Fiction writing (novels, short stories, flash fiction)
- Character development and dialogue
- Plot structure and pacing
- World-building and setting
- Poetry and verse
- Screenwriting and scriptwriting
- Creative non-fiction

Guidelines:
- Provide constructive feedback on writing
- Suggest improvements for clarity and impact
- Help develop characters and storylines
- Offer writing prompts and exercises
- Explain literary techniques and devices
- Encourage experimentation with style and voice
- Support the writer's unique vision while offering guidance

When reviewing work:
- Focus on both technical and creative aspects
- Provide specific, actionable feedback
- Highlight strengths as well as areas for improvement
- Suggest alternative approaches when appropriate
- Encourage revision and refinement""",

    "research_assistant": """You are a knowledgeable research assistant with expertise in information gathering, analysis, and synthesis. Your role is to help users conduct thorough research and organize their findings.

Capabilities:
- Literature reviews and source evaluation
- Data analysis and interpretation
- Fact-checking and verification
- Research methodology guidance
- Academic writing support
- Citation and referencing help

Guidelines:
- Always verify information from multiple sources
- Provide balanced, objective analysis
- Cite sources and explain methodology
- Help organize and structure research findings
- Suggest relevant databases and resources
- Explain research limitations and biases
- Support evidence-based conclusions

When conducting research:
- Start with reliable, authoritative sources
- Consider multiple perspectives on topics
- Evaluate source credibility and bias
- Organize findings logically
- Identify gaps in knowledge or research
- Suggest follow-up questions or investigations""",

    "teacher": """You are an experienced educator and teacher. Your role is to help students learn and understand various subjects through clear explanations, engaging examples, and supportive guidance.

Teaching philosophy:
- Make learning accessible and enjoyable
- Adapt to different learning styles
- Use real-world examples and applications
- Encourage questions and curiosity
- Build confidence through positive reinforcement
- Break complex topics into manageable parts

Subject areas:
- Mathematics (algebra, calculus, statistics)
- Sciences (physics, chemistry, biology)
- Languages and literature
- History and social studies
- Computer science and technology
- Study skills and academic strategies

Guidelines:
- Explain concepts step-by-step
- Use analogies and visual examples
- Check for understanding regularly
- Provide practice problems and exercises
- Offer multiple ways to approach problems
- Encourage critical thinking and analysis
- Create a supportive learning environment

When teaching:
- Start with what the student knows
- Build understanding gradually
- Use active learning techniques
- Provide immediate feedback
- Celebrate progress and achievements
- Help develop independent learning skills""",

    # Template prompts using f-string formatting
    "reviewer": """You are a helpful reviewer specializing in {topic}. Your role is to provide thoughtful, constructive reviews and analysis.

Areas of expertise:
- {topic} analysis and critique
- Identifying strengths and weaknesses
- Providing actionable feedback
- Offering improvement suggestions

Guidelines:
- Be objective and fair in your assessments
- Provide specific examples and evidence
- Balance critique with positive feedback
- Focus on {focus_area} when relevant
- Tailor your review style to the context

When reviewing:
- Consider the target audience and purpose
- Evaluate against established standards
- Provide clear, actionable recommendations
- Suggest specific improvements or alternatives""",

    "domain_expert": """You are a domain expert in {domain} with {experience_level} experience. Your role is to provide authoritative guidance and insights in your field of expertise.

Expertise areas:
- {domain} fundamentals and advanced concepts
- Best practices and industry standards
- Current trends and developments
- Problem-solving and troubleshooting

Background:
- {experience_level} experience in {domain}
- Deep understanding of {specialty} 
- Practical knowledge of tools and methodologies
- Awareness of common challenges and solutions

Guidelines:
- Provide accurate, up-to-date information
- Explain complex concepts clearly
- Share practical insights and examples
- Acknowledge limitations and uncertainties
- Suggest additional resources when helpful""",

    "tutor": """You are a {subject} tutor working with {student_level} students. Your teaching approach is {teaching_style} and focuses on helping students understand {subject} concepts effectively.

Teaching specialization:
- {subject} instruction and guidance
- {student_level} appropriate explanations
- {teaching_style} teaching methodology
- Building confidence and understanding

Approach:
- Adapt explanations to {student_level} level
- Use {teaching_style} teaching methods
- Provide relevant examples and practice
- Encourage questions and curiosity
- Track progress and adjust as needed

When tutoring:
- Start with the student's current knowledge
- Break down complex topics into manageable parts
- Use interactive and engaging techniques
- Provide immediate feedback and support
- Celebrate achievements and progress""",

    "consultant": """You are a {industry} consultant with expertise in {specialization}. Your role is to provide strategic advice and practical solutions for {client_type} facing {challenge_type} challenges.

Consulting expertise:
- {industry} industry knowledge
- {specialization} specialized skills
- {client_type} client experience
- {challenge_type} problem-solving

Service approach:
- Understand client needs and context
- Analyze problems systematically
- Develop practical, actionable solutions
- Consider industry best practices
- Focus on measurable outcomes

When consulting:
- Ask clarifying questions to understand the situation
- Provide evidence-based recommendations
- Consider budget and resource constraints
- Offer implementation guidance
- Suggest success metrics and follow-up steps""",

    "content_creator": """You are a {content_type} content creator specializing in {niche} for {audience}. Your content style is {style} and your goal is to {goal}.

Content focus:
- {content_type} creation and optimization
- {niche} subject matter expertise
- {audience} audience understanding
- {style} presentation style

Objectives:
- {goal} through engaging content
- Build connection with {audience}
- Provide value in {niche} area
- Maintain {style} voice and tone

Content guidelines:
- Create {content_type} that resonates with {audience}
- Use {style} approach consistently
- Focus on {niche} topics and themes
- Aim to {goal} with every piece
- Encourage engagement and interaction"""
}

# Tool-specific argument specifications for enhanced extraction
TOOL_ARGUMENT_SPECS = {
    "calculate_risk": {
        "portfolio": {
            "type": "str", 
            "required": True, 
            "hints": ["portfolio description", "asset types mentioned", "investment mix", "crypto/stocks/bonds"]
        }
    },
    "get_stock_info": {
        "symbol": {
            "type": "str", 
            "required": True, 
            "hints": ["stock ticker symbols", "AAPL, MSFT, TSLA", "company abbreviations", "stock codes"]
        }
    },
    "portfolio_analyzer": {
        "holdings": {
            "type": "str", 
            "required": True, 
            "hints": ["portfolio holdings", "list of investments", "asset allocation", "stock/bond mix"]
        }
    }
}

class ArgumentFormatters:
    """Multiple strategies for formatting tool arguments to help LLMs extract parameters correctly."""
    
    @staticmethod
    def simple(tools: List) -> str:
        """Simple argument listing with types and required/optional status."""
        result = ""
        for tool in tools:
            result += f"\n{tool.name}:\n"
            sig = inspect.signature(tool.func)
            for param_name, param in sig.parameters.items():
                param_type = getattr(param.annotation, '__name__', 'any')
                required = param.default == inspect.Parameter.empty
                status = "required" if required else f"optional (default: {param.default})"
                result += f"  - {param_name} ({param_type}): {status}\n"
        return result

    @staticmethod
    def detailed_with_hints(tools: List) -> str:
        """Detailed formatting with extraction hints for better LLM understanding."""
        result = ""
        for tool in tools:
            if tool.name in TOOL_ARGUMENT_SPECS:
                result += f"\n=== {tool.name.upper()} ARGUMENTS ===\n"
                specs = TOOL_ARGUMENT_SPECS[tool.name]
                
                # Also get actual function signature for completeness
                sig = inspect.signature(tool.func)
                for param_name, param in sig.parameters.items():
                    if param_name in specs:
                        spec = specs[param_name]
                        required = param.default == inspect.Parameter.empty
                        status = "REQUIRED" if required else f"OPTIONAL (default: {param.default})"
                        result += f"• {param_name} ({spec['type']}) - {status}\n"
                        result += f"  Look for: {', '.join(spec['hints'])}\n\n"
                    else:
                        # Fallback for params not in specs
                        param_type = getattr(param.annotation, '__name__', 'any')
                        required = param.default == inspect.Parameter.empty
                        status = "REQUIRED" if required else f"OPTIONAL (default: {param.default})"
                        result += f"• {param_name} ({param_type}) - {status}\n\n"
            else:
                # Fallback to simple format for tools without specs
                result += f"\n{tool.name}:\n"
                sig = inspect.signature(tool.func)
                for param_name, param in sig.parameters.items():
                    param_type = getattr(param.annotation, '__name__', 'any')
                    required = param.default == inspect.Parameter.empty
                    status = "required" if required else f"optional (default: {param.default})"
                    result += f"  - {param_name} ({param_type}): {status}\n"
        return result

    @staticmethod
    def json_schema(tools: List) -> str:
        """JSON schema format for structured argument extraction."""
        schemas = {}
        for tool in tools:
            sig = inspect.signature(tool.func)
            schema = {"type": "object", "properties": {}, "required": []}
            
            for param_name, param in sig.parameters.items():
                param_type = getattr(param.annotation, '__name__', 'string')
                type_mapping = {"str": "string", "int": "integer", "float": "number", "bool": "boolean"}
                json_type = type_mapping.get(param_type, "string")
                
                schema["properties"][param_name] = {"type": json_type}
                
                # Add hints if available
                if tool.name in TOOL_ARGUMENT_SPECS and param_name in TOOL_ARGUMENT_SPECS[tool.name]:
                    hints = TOOL_ARGUMENT_SPECS[tool.name][param_name]["hints"]
                    schema["properties"][param_name]["description"] = f"Look for: {', '.join(hints)}"
                
                if param.default == inspect.Parameter.empty:
                    schema["required"].append(param_name)
                else:
                    schema["properties"][param_name]["default"] = param.default
                    
            schemas[tool.name] = schema
        
        return json.dumps(schemas, indent=2)

    @staticmethod
    def extraction_focused(tools: List) -> str:
        """Format focused on clear extraction patterns with visual indicators."""
        result = ""
        for tool in tools:
            result += f"\n🔍 {tool.name.upper()} - What to extract:\n"
            sig = inspect.signature(tool.func)
            
            for param_name, param in sig.parameters.items():
                required = param.default == inspect.Parameter.empty
                if required:
                    result += f"  ✅ MUST FIND: {param_name}"
                    if tool.name in TOOL_ARGUMENT_SPECS and param_name in TOOL_ARGUMENT_SPECS[tool.name]:
                        hints = TOOL_ARGUMENT_SPECS[tool.name][param_name]["hints"]
                        result += f" (Look for: {', '.join(hints[:2])}...)"
                    result += "\n"
                else:
                    result += f"  🔶 OPTIONAL: {param_name} (default: {param.default})\n"
        return result

FORMATTERS = {
    "simple": ArgumentFormatters.simple,
    "detailed": ArgumentFormatters.detailed_with_hints,
    "json": ArgumentFormatters.json_schema,
    "extraction": ArgumentFormatters.extraction_focused
}

def format_tool_arguments(tools: List, formatter_strategy: str = "detailed") -> str:
    """
    Format tool arguments using the specified formatting strategy.
    
    Args:
        tools: List of tool objects
        formatter_strategy: Strategy to use ("simple", "detailed", "json", "extraction")
        
    Returns:
        Formatted string describing tool arguments
    """
    if not tools:
        return ""
    
    formatter = FORMATTERS.get(formatter_strategy, ArgumentFormatters.detailed_with_hints)
    return formatter(tools)

def get_prompt(prompt_name: str) -> str:
    """
    Retrieve a system prompt by name
    
    Args:
        prompt_name: The name of the prompt to retrieve
        
    Returns:
        The system prompt string, or None if not found
    """
    return SYSTEM_PROMPTS.get(prompt_name.lower())


def render_template(template_name: str, **kwargs) -> Optional[str]:
    """
    Render a template prompt with provided variables
    
    Args:
        template_name: Name of the template prompt
        **kwargs: Variables to substitute in the template
        
    Returns:
        Rendered prompt string, or None if template not found
        
    Example:
        render_template("reviewer", topic="movies", focus_area="cinematography")
    """
    template = get_prompt(template_name)
    if template is None:
        return None
    
    try:
        return template.format(**kwargs)
    except KeyError as e:
        raise ValueError(f"Missing required template variable: {e}")
    except Exception as e:
        raise ValueError(f"Error rendering template: {e}")


def get_template_variables(template_name: str) -> list:
    """
    Extract template variables from a prompt template
    
    Args:
        template_name: Name of the template prompt
        
    Returns:
        List of variable names used in the template
    """
    template = get_prompt(template_name)
    if template is None:
        return []
    
    # Use regex to find all {variable} patterns
    import re
    variables = re.findall(r'\{([^}]+)\}', template)
    return list(set(variables))  # Remove duplicates


def is_template(prompt_name: str) -> bool:
    """
    Check if a prompt is a template (contains {variable} patterns)
    
    Args:
        prompt_name: Name of the prompt to check
        
    Returns:
        True if the prompt contains template variables, False otherwise
    """
    template = get_prompt(prompt_name)
    if template is None:
        return False
    
    import re
    return bool(re.search(r'\{[^}]+\}', template))

def list_prompts() -> list:
    """
    Get a list of all available prompt names
    
    Returns:
        List of prompt names
    """
    return list(SYSTEM_PROMPTS.keys())

def search_prompts(search_term: str) -> list:
    """
    Search for prompts containing a specific term
    
    Args:
        search_term: Term to search for in prompt names and content
        
    Returns:
        List of matching prompt names
    """
    search_term = search_term.lower()
    matches = []
    
    for name, content in SYSTEM_PROMPTS.items():
        if search_term in name.lower() or search_term in content.lower():
            matches.append(name)
    
    return matches

def get_prompt_info(prompt_name: str) -> dict:
    """
    Get detailed information about a prompt
    
    Args:
        prompt_name: The name of the prompt
        
    Returns:
        Dictionary with prompt information, or None if prompt not found
    """
    prompt = get_prompt(prompt_name)
    if prompt is None:
        return None
    
    # Handle case where prompt might be empty or invalid
    if not isinstance(prompt, str):
        return None
    
    is_template_prompt = is_template(prompt_name)
    template_vars = get_template_variables(prompt_name) if is_template_prompt else []
    
    return {
        "name": prompt_name,
        "content": prompt,
        "length": len(prompt),
        "word_count": len(prompt.split()),
        "preview": prompt[:200] + "..." if len(prompt) > 200 else prompt,
        "is_template": is_template_prompt,
        "template_variables": template_vars
    }


def extract_tool_info(tool) -> Dict[str, Any]:
    """
    Extract metadata from a tool object
    
    Args:
        tool: Tool object (LangChain tool or custom function)
        
    Returns:
        Dictionary with tool metadata
    """
    tool_info = {
        "name": getattr(tool, 'name', tool.__name__ if hasattr(tool, '__name__') else str(tool)),
        "description": "",
        "schema": {}
    }
    
    # Handle LangChain tools
    if hasattr(tool, 'description'):
        tool_info["description"] = tool.description
    elif hasattr(tool, '__doc__') and tool.__doc__:
        tool_info["description"] = tool.__doc__.strip()
    
    # Handle schema for LangChain tools
    if hasattr(tool, 'args_schema') and tool.args_schema:
        try:
            tool_info["schema"] = tool.args_schema.schema()
        except:
            tool_info["schema"] = {}
    
    return tool_info


def format_tools_for_template(tools: List[Any], pattern: str, formatter_strategy: str = "detailed") -> str:
    """
    Format tools based on the template injection pattern
    
    Args:
        tools: List of tool objects
        pattern: Template pattern ('tool_names', 'tools', 'tool_list', 'tool_schemas', 'tool_args')
        formatter_strategy: Strategy for tool_args formatting ("simple", "detailed", "json", "extraction")
        
    Returns:
        Formatted string for template injection
    """
    if not tools:
        return ""
    
    tool_infos = [extract_tool_info(tool) for tool in tools]
    
    if pattern == "tool_names":
        return ", ".join([info["name"] for info in tool_infos])
    
    elif pattern == "tool_list":
        lines = []
        for info in tool_infos:
            desc = info["description"] or "No description available"
            lines.append(f"- {info['name']}: {desc}")
        return "\n".join(lines)
    
    elif pattern == "tools":
        lines = []
        for info in tool_infos:
            desc = info["description"] or "No description available"
            lines.append(f"{info['name']}: {desc}")
        return "\n".join(lines)
    
    elif pattern == "tool_schemas":
        schemas = {}
        for info in tool_infos:
            schemas[info["name"]] = {
                "description": info["description"],
                "schema": info["schema"]
            }
        return json.dumps(schemas, indent=2)
    
    elif pattern == "tool_args":
        return format_tool_arguments(tools, formatter_strategy)
    
    else:
        # Default to tool_names format
        return ", ".join([info["name"] for info in tool_infos])


def render_template_with_tools(template_name: str, tools: List[Any] = None, formatter_strategy: str = "simple", **kwargs) -> Optional[str]:
    """
    Render a template prompt with tool support and provided variables
    
    Args:
        template_name: Name of the template prompt
        tools: List of tool objects to inject into template
        formatter_strategy: Strategy for tool_args formatting ("simple", "detailed", "json", "extraction")
        **kwargs: Additional variables to substitute in the template
        
    Returns:
        Rendered prompt string, or None if template not found
        
    Example:
        render_template_with_tools("finchat_prompt", tools=[calculate_risk, get_stock_info], formatter_strategy="detailed")
    """
    template = get_prompt(template_name)
    if template is None:
        return None
    
    # Get template variables
    template_vars = get_template_variables(template_name)
    
    # Prepare tool-related variables if tools are provided
    if tools:
        tool_variables = {}
        
        # Check which tool patterns are needed
        # ipdb.set_trace()
        for var in template_vars:
            if var in ["tool_names", "tools", "tool_list", "tool_schemas", "tool_args"]:
                tool_variables[var] = format_tools_for_template(tools, var, formatter_strategy)
        
        # Merge tool variables with user-provided kwargs
        kwargs.update(tool_variables)
    
    try:
        return template.format(**kwargs)
    except KeyError as e:
        missing_var = str(e).strip("'")
        if missing_var in ["tool_names", "tools", "tool_list", "tool_schemas", "tool_args"]:
            raise ValueError(f"Template requires tools but none provided. Missing variable: {missing_var}")
        else:
            raise ValueError(f"Missing required template variable: {e}")
    except Exception as e:
        raise ValueError(f"Error rendering template: {e}")