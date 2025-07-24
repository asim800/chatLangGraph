# Template Prompt Quick Reference

## 🚀 Quick Start

### 1. List Available Templates
```bash
python main.py prompts list
```
Look for prompts with 📝 Template variables

### 2. Basic Usage Pattern
```bash
python main.py chat --prompt <template_name> --template-var key=value --template-var key2=value2
```

## 📝 Available Templates

| Template | Variables | Use Case |
|----------|-----------|----------|
| `reviewer` | `topic`, `focus_area` | Review movies, books, code, etc. |
| `domain_expert` | `domain`, `experience_level`, `specialty` | Expert in specific field |
| `tutor` | `subject`, `student_level`, `teaching_style` | Educational assistance |
| `consultant` | `industry`, `specialization`, `client_type`, `challenge_type` | Business consulting |
| `content_creator` | `content_type`, `niche`, `audience`, `style`, `goal` | Content creation |

## 🎯 Common Examples

### Movie Reviewer
```bash
python main.py chat --prompt reviewer \
  --template-var topic=movies \
  --template-var focus_area=cinematography
```

### Python Tutor
```bash
python main.py chat --prompt tutor \
  --template-var subject=Python \
  --template-var student_level=beginner \
  --template-var teaching_style=interactive
```

### Machine Learning Expert
```bash
python main.py chat --prompt domain_expert \
  --template-var domain='machine learning' \
  --template-var experience_level=senior \
  --template-var specialty='deep learning'
```

### Business Consultant
```bash
python main.py chat --prompt consultant \
  --template-var industry=technology \
  --template-var specialization=strategy \
  --template-var client_type=startups \
  --template-var challenge_type=scaling
```

### YouTube Creator
```bash
python main.py chat --prompt content_creator \
  --template-var content_type=video \
  --template-var niche=programming \
  --template-var audience=developers \
  --template-var style=educational \
  --template-var goal='teach concepts'
```

## 🔧 Programmatic Usage

### Import Functions
```python
from prompts import render_template, get_template_variables, is_template
```

### Render Template
```python
# Your original f-string example equivalent:
# promptA = f"Please provide helpful review on {topic}" where topic="movies"
prompt = render_template('reviewer', 
                        topic='movies', 
                        focus_area='overall quality')
```

### Check Template Variables
```python
# Get required variables
vars = get_template_variables('reviewer')
# Returns: ['topic', 'focus_area']

# Check if prompt is template
is_template('reviewer')  # Returns: True
```

### Error Handling
```python
try:
    prompt = render_template('reviewer', topic='movies')
except ValueError as e:
    print(f"Error: {e}")
    # Error: Missing required template variable: 'focus_area'
```

## ⚠️ Common Errors & Solutions

### Missing Variables
```bash
# ❌ Error
python main.py chat --prompt reviewer --template-var topic=movies
# Missing required variable 'focus_area'

# ✅ Fix
python main.py chat --prompt reviewer --template-var topic=movies --template-var focus_area=plot
```

### Invalid Format
```bash
# ❌ Error
python main.py chat --prompt reviewer --template-var topic movies

# ✅ Fix
python main.py chat --prompt reviewer --template-var topic=movies
```

### Multi-word Values
```bash
# ❌ Error
python main.py chat --prompt reviewer --template-var focus_area=character development

# ✅ Fix
python main.py chat --prompt reviewer --template-var 'focus_area=character development'
```

## 🎨 Creative Examples

### Code Reviewer
```bash
python main.py chat --prompt reviewer \
  --template-var topic=code \
  --template-var 'focus_area=best practices'
```

### Cooking Tutor
```bash
python main.py chat --prompt tutor \
  --template-var subject=cooking \
  --template-var student_level=beginner \
  --template-var teaching_style=hands-on
```

### Cybersecurity Expert
```bash
python main.py chat --prompt domain_expert \
  --template-var domain=cybersecurity \
  --template-var experience_level=expert \
  --template-var specialty='threat analysis'
```

### Healthcare Consultant
```bash
python main.py chat --prompt consultant \
  --template-var industry=healthcare \
  --template-var specialization='digital transformation' \
  --template-var client_type=hospitals \
  --template-var challenge_type=modernization
```

### TikTok Creator
```bash
python main.py chat --prompt content_creator \
  --template-var content_type=video \
  --template-var niche=dance \
  --template-var audience=teenagers \
  --template-var style=energetic \
  --template-var goal='inspire creativity'
```

## 🛠️ Discovery Commands

```bash
# List all prompts (templates marked with 📝)
python main.py prompts list

# Search for templates
python main.py prompts search template

# Search by keyword
python main.py prompts search tutor
```

## 💡 Pro Tips

1. **Use quotes for multi-word values**: `'focus_area=character development'`
2. **Check variables first**: `python main.py prompts list`
3. **Test templates programmatically**: `get_template_variables('template_name')`
4. **Combine with config files**: `--config my_config.json --prompt template_name`
5. **Create variations**: Same template, different variables for different contexts

## 🔄 Template vs Static Prompts

| Feature | Template Prompts | Static Prompts |
|---------|------------------|----------------|
| Usage | Require variables | Use directly |
| Flexibility | High - customize per use | Low - fixed content |
| Examples | `reviewer`, `tutor` | `default`, `coding_mentor` |
| Command | `--template-var key=value` | Just `--prompt name` |

---

**Need help?** Run `python3 template_usage_guide.py` for comprehensive examples!