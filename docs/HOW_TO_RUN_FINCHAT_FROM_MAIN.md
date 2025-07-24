# How to Run Finchat from main.py

## ✅ **UPDATED**: main.py now supports finchat with full functionality!

---

## 🚀 **Quick Start**

### **Simplest Way:**
```bash
python main.py chat --prompt finchat_prompt
```

**What happens:**
- ✅ Auto-configures financial tools (`calculate_risk`, `get_stock_info`, `portfolio_analyzer`)
- ✅ Renders `finchat_prompt` template with tools
- ✅ Uses LangGraph `invoke()` patterns throughout
- ✅ Provides full CLI framework features

---

## 📋 **All Ways to Run Finchat from main.py**

### **1. Basic Auto-Configuration** ⭐ **RECOMMENDED**
```bash
python main.py chat --prompt finchat_prompt
```
- Automatically loads financial tools
- Uses finchat_prompt template
- No configuration needed

### **2. With Configuration File**
```bash
python main.py chat --config finchat_config.json
```
- Use custom configuration
- Override settings as needed

### **3. With Template Variables**
```bash
python main.py chat --prompt finchat_prompt --template-var key=value
```
- Add custom template variables if needed

### **4. Discovery Commands**
```bash
# List all available prompts
python main.py prompts list

# Search for financial prompts  
python main.py prompts search financial

# Get help
python main.py --help
```

---

## 🎯 **Interactive Commands Available**

Once you're in the chat session:

```
You: What's the risk of AAPL stock?
Bot: [Financial analysis using tools]

You: stats              # Show engagement statistics
You: history 5          # Show last 5 messages
You: history all        # Show all messages
You: new               # Start new session
You: quit              # Exit
```

---

## 🔧 **Features You Get with main.py**

### **Auto-Configured Financial Tools:**
- **`calculate_risk`** - Portfolio risk assessment
- **`get_stock_info`** - Stock information lookup
- **`portfolio_analyzer`** - Portfolio analysis and recommendations

### **CLI Framework Features:**
- **Statistics tracking** - Engagement metrics and analytics
- **Chat history management** - View past conversations
- **Session management** - Multiple sessions, new session command
- **Data export** - Export conversations to JSON/CSV
- **Configuration support** - Custom config files
- **Template system** - Variable substitution

### **LangGraph Compliance:**
- **`chatbot.invoke()`** - Proper agent invocation
- **`tool.invoke()`** - Tool execution patterns
- **`template.invoke()`** - Prompt template rendering
- **Consistent patterns** throughout

---

## 🆚 **main.py vs run_finchat_with_tools.py**

| Feature | main.py | run_finchat_with_tools.py |
|---------|---------|---------------------------|
| **Financial Tools** | ✅ Auto-configured | ✅ Hardcoded |
| **CLI Interface** | ✅ Full CLI | ❌ Interactive only |
| **Statistics** | ✅ Advanced | ⚠️ Basic |
| **History Management** | ✅ Commands | ⚠️ Arrow keys only |
| **Export Data** | ✅ JSON/CSV | ❌ None |
| **Configuration** | ✅ File-based | ❌ Hardcoded |
| **Session Management** | ✅ Advanced | ⚠️ Basic |
| **Template Variables** | ✅ Yes | ❌ No |
| **LangGraph invoke()** | ✅ Yes | ✅ Yes |
| **Ease of Use** | ⚠️ CLI complexity | ✅ Simple |

---

## 💡 **When to Use Which**

### **Use main.py when you want:**
- **Production deployment** with full features
- **CLI interface** with subcommands
- **Advanced analytics** and statistics
- **Data export** capabilities
- **Configuration management**
- **Multiple prompt support**

### **Use run_finchat_with_tools.py when you want:**
- **Simple demo/example**
- **Quick testing** without CLI complexity
- **Arrow key history** navigation
- **Immediate interactive mode**
- **Minimal setup**

---

## 🎉 **Example Session**

```bash
$ python main.py chat --prompt finchat_prompt

🏦 Auto-configured financial tools: ['calculate_risk', 'get_stock_info', 'portfolio_analyzer']
Using financial template prompt: 'finchat_prompt' with tools

🤖 LangGraph Chatbot Framework
===================================
Commands: 'quit' to exit, 'new' for new session, 'stats' for statistics
          'history' or 'history X' for chat history

Enter your user ID (or press Enter for 'default_user'): demo_user

demo_user: What's the risk of my crypto portfolio?
Bot: I'll help you assess the risk of your crypto portfolio...

Question: What's the risk of my crypto portfolio?
Thought: I need to calculate the risk using the portfolio risk tool
Action: calculate_risk  
Action Input: crypto portfolio
Observation: 0.8 (HIGH risk) - Cryptocurrency investments are highly volatile
Thought: I now know the final answer
Final Answer: Your crypto portfolio has a HIGH risk score of 0.8...

💯 Engagement: 0.95

demo_user: stats
📈 Engagement Statistics
------------------------
Total Interactions: 1
Average Engagement: 0.950
...

demo_user: quit
```

---

## ✅ **Summary**

**You can now run the complete finchat functionality from main.py with:**

```bash
python main.py chat --prompt finchat_prompt
```

**This gives you:**
- ✅ Same financial tools as `run_finchat_with_tools.py`
- ✅ Same finchat_prompt template  
- ✅ LangGraph invoke() patterns
- ✅ **PLUS** all the CLI framework features

**Both scripts are now fully LangGraph compliant and serve different purposes!** 🎯