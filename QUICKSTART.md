# Quick Start Guide

Get started with the Multi-Agentic Framework in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- pip package manager
- Groq API key ([Get one free here](https://console.groq.com))

## Step-by-Step Setup

### 1. Clone and Navigate

```bash
git clone <repository-url>
cd multi-agent-framework
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Key

**Manual Setup:**
```bash
# Copy the example file
cp .env.example .env

# Edit and add your key
nano .env  # or use any text editor
```

**Get Your API Key:**
1. Visit https://console.groq.com
2. Sign up (free tier available)
3. Go to API Keys section
4. Create new key
5. Copy and use in setup


### 5. Run the Application

**Using Streamlit UI (Recommended for first-time users):**
```bash
streamlit run streamlit_app.py
```

This will:
- Open your browser at `http://localhost:8501`
- Auto-load API key from .env
- Show framework status
- Provide interactive interface

**Expected behavior:**
- ✅ API Key loaded from .env file (shown in sidebar)
- ✅ Framework initialized automatically (if key present)
- Ready to process requirements!

**Using Python directly:**
```bash
python examples/simple_example.py
```

## Your First Project

### Example 1: Calculator (2 minutes)

1. **Open the Streamlit UI**
2. **Enter this requirement:**
   ```
   Create a calculator application that can perform basic arithmetic 
   operations (addition, subtraction, multiplication, division) with 
   proper error handling for division by zero
   ```
3. **Click "Start Processing"**
4. **Wait ~30 seconds**
5. **Download the generated files**

### Example 2: CLI Tool (3 minutes)

```python
from main import MultiAgentFramework
import os

# Initialize
api_key = os.getenv("GROQ_API_KEY")
framework = MultiAgentFramework(api_key=api_key)

# Define requirement
requirement = """
Create a command-line todo list manager that can:
- Add tasks with descriptions
- Mark tasks as complete
- List all tasks
- Delete tasks
- Save tasks to a JSON file
"""

# Process
results = framework.process_requirement(requirement)

# Save results
framework.save_results("output")

print("✓ Generated code saved to output/generated_code.py")
print("✓ Documentation saved to output/documentation.md")
print("✓ Tests saved to output/test_generated_code.py")
```

## What You Get

After processing, you'll find these files in the `output/` directory:

```
output/
├── requirements.json          # Structured requirements (JSON)
├── generated_code.py          # Final production code
├── initial_code.py           # Code before review
├── code_review.json          # Review results with score
├── documentation.md          # Complete documentation
├── test_generated_code.py    # Comprehensive test suite
├── deploy.sh                 # Deployment script
├── deployment_info.json      # Deployment metadata
├── full_results.json         # All results in one file
└── README.md                 # Usage guide for files
```

**Download Options:**
- Individual downloads from Streamlit sidebar (6 buttons)
- All files automatically saved locally
- Complete with usage instructions

## Testing Your Generated Code

```bash
# Navigate to output directory
cd output

# Run the generated tests
python -m pytest test_generated_code.py -v

# Run the application
python generated_code.py

# Deploy (if needed)
chmod +x deploy.sh
./deploy.sh
```

**View Results in UI:**
- 7 tabs: Requirements, Code, Review, Documentation, Tests, Deployment, Files
- Download any file from sidebar
- Processing summary shows metrics
- File browser shows all generated files

## Next Steps

- 📚 Read the full [README.md](README.md) for detailed documentation
- 🔧 Check [DOCUMENTATION.md](DOCUMENTATION.md) for technical details
- ⭐ Review [FEATURES.md](FEATURES.md) for 150+ features
- 🎯 Try more complex examples in the `examples/` directory
- 🧪 Run the test suite: `pytest tests/ -v`

## Example Requirements to Try

### Web Scraper
```
Create a web scraper that can extract article titles and dates 
from a news website, with rate limiting and error handling
```

### Data Analyzer
```
Build a CSV data analyzer that can read files, compute statistics 
(mean, median, mode), and generate visualizations using matplotlib
```

### API Client
```
Create a REST API client for GitHub that can list repositories, 
get repository details, and handle authentication via tokens
```

### File Organizer
```
Develop a file organizer script that categorizes files by extension, 
moves them to appropriate folders, and logs all operations
```

## Tips for Best Results

1. **Be Specific**: Include exact requirements and constraints
2. **Mention Technologies**: Specify frameworks or libraries if needed
3. **Define Scope**: Clear boundaries help agents understand limits
4. **Include Edge Cases**: Mention error conditions to handle

## Getting Help

- **Documentation**: Check DOCUMENTATION.md for detailed guides
- **Features**: Review FEATURES.md for all capabilities
- **Examples**: Look at examples/ directory for more use cases

## Quick Reference

```bash
# Copy the example file
cp .env.example .env

# Edit and add your key
nano .env  # or use any text editor    

# Start Application
streamlit run streamlit_app.py   # Web UI (recommended)
python examples/simple_example.py # CLI example

# Testing
pytest tests/ -v            # Framework tests
cd output && pytest test_generated_code.py -v  # Generated tests

# Logs & Monitoring
tail -f framework.log       # View logs (if enabled)

# Code Quality
black *.py                  # Format code
mypy main.py                # Type checking
flake8 main.py             # Style checking

# File Management
ls output/                  # View generated files
cat output/README.md        # Read output guide
```

**UI Features:**
- ✅ Auto-loads API key from .env
- ✅ Auto-initializes framework
- ✅ 6 download buttons in sidebar
- ✅ 7 result tabs
- ✅ Real-time agent status
- ✅ Processing summary with metrics

---

**Ready to build?** Start with the Streamlit UI and experiment with different requirements!

**Need help?** Check the [README.md](README.md) or [DOCUMENTATION.md](DOCUMENTATION.md)