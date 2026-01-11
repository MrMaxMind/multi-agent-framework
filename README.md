# Multi-Agentic Framework with AutoGen

A sophisticated multi-agent system that collaboratively develops software from natural language requirements using AutoGen and Groq's LLM APIs.

## 🌟 Features

- **Requirement Analysis Agent**: Converts natural language into structured requirements
- **Coding Agent**: Generates functional Python code from requirements
- **Code Review Agent**: Reviews code for quality, security, and correctness with iterative feedback
- **Documentation Agent**: Creates comprehensive technical documentation
- **Test Case Generation Agent**: Generates unit and integration tests
- **Deployment Configuration Agent**: Creates deployment scripts and configurations
- **Streamlit UI**: Interactive web interface for the entire workflow

## 🏗️ Architecture

```
User Input (Natural Language)
    ↓
Requirement Analysis Agent
    ↓
Coding Agent
    ↓
Code Review Agent ←→ (Iterative feedback loop)
    ↓
[Parallel Processing]
    ├→ Documentation Agent
    ├→ Test Case Generation Agent
    └→ Deployment Configuration Agent
    ↓
Output (Code, Docs, Tests, Deployment)
```

## 📋 Prerequisites

- Python 3.8 or higher
- Groq API Key (free tier available)
- Git (for cloning the repository)

## 🚀 Installation

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd multi-agent-framework
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up API Key

**Option A: Manual .env File**

Create a `.env` file in the project root:

```bash
# Copy the example
cp .env.example .env

# Edit .env and add your key
nano .env  # or use any text editor
```

Add this content:
```
GROQ_API_KEY=your_groq_api_key_here
```

**Option B: Environment Variable**

```bash
# Linux/Mac
export GROQ_API_KEY=your_key_here

# Windows (Command Prompt)
set GROQ_API_KEY=your_key_here

# Windows (PowerShell)
$env:GROQ_API_KEY="your_key_here"
```

To get a Groq API key:
1. Visit https://console.groq.com
2. Sign up for a free account
3. Navigate to API Keys section
4. Generate a new API key

## 💻 Usage

### Using the Streamlit UI (Recommended)

```bash
streamlit run streamlit_app.py
```

The UI will open in your browser at `http://localhost:8501`

**Steps:**
1. Enter your Groq API key in the sidebar
2. Click "Initialize Framework"
3. Enter your requirement in natural language
4. Click "Start Processing"
5. View results in real-time
6. Download generated files

### Using the Command Line

```python
from main import MultiAgentFramework
import os

# Initialize framework
api_key = os.getenv("GROQ_API_KEY")
framework = MultiAgentFramework(api_key=api_key)

# Process requirement
requirement = """
Create a calculator application that can:
- Perform basic arithmetic operations
- Handle invalid inputs
- Provide a CLI interface
"""

results = framework.process_requirement(requirement)
framework.save_results("output")
```

### Using as a Module

```python
from main import MultiAgentFramework

# Create framework instance
framework = MultiAgentFramework(
    api_key="your-api-key",
    model="llama-3.3-70b-versatile"
)

# Process requirement
results = framework.process_requirement("Create a todo list app")

# Access individual results
print(results['requirements'])  # Structured requirements
print(results['final_code'])    # Generated code
print(results['review'])        # Code review
print(results['documentation']) # Documentation
print(results['tests'])         # Test cases
print(results['deployment'])    # Deployment config
```

## 📁 Project Structure

```
multi-agent-framework/
├── main.py                    # Core multi-agent system
├── streamlit_app.py           # Streamlit UI
├── requirements.txt           # Python dependencies
├── setup.py                   # Installation script
├── .env                       # Environment variables (create this)
├── .env.example              # Environment template
├── README.md                 # This file
├── DOCUMENTATION.md          # Technical documentation
├── FEATURES.md               # Quick Features guide
├── QUICKSTART.md             # Quick start guide
├── output/                   # Generated files (auto-created)
│   ├── requirements.json         # Structured requirements
│   ├── generated_code.py         # Final production code
│   ├── initial_code.py          # Code before review
│   ├── code_review.json         # Review results
│   ├── documentation.md         # Documentation
│   ├── test_generated_code.py   # Test suite
│   ├── deploy.sh                # Deployment script
│   ├── deployment_info.json     # Deployment metadata
│   ├── full_results.json        # All results
│   └── README.md                # Output guide
├── examples/                 # Example scripts
│   └── simple_example.py        # Basic examples
└── tests/                    # Framework tests
    └── test_framework.py        # Unit tests
```

## 🔧 Configuration

### Available Models

The framework supports various Groq models:

- `llama-3.3-70b-versatile` (default, recommended)
- `llama-3.1-70b-versatile`
- `mixtral-8x7b-32768`

### Customizing Agents

You can modify agent behavior in `main.py`:

```python
# Example: Customize the coding agent
self.coding_agent = autogen.AssistantAgent(
    name="SoftwareDeveloper",
    system_message="Your custom instructions here...",
    llm_config=self.llm_config
)
```

## 📊 Output Files

After processing, the following files are generated in the `output/` directory:

| File | Description | Format |
|------|-------------|--------|
| `requirements.json` | Structured requirements from NL input | JSON |
| `generated_code.py` | Final production-ready code | Python |
| `initial_code.py` | Code before review (if different) | Python |
| `code_review.json` | Detailed code review with score & findings | JSON |
| `documentation.md` | Complete technical documentation | Markdown |
| `test_generated_code.py` | Comprehensive test suite | Python |
| `deploy.sh` | Deployment script | Bash |
| `deployment_info.json` | Deployment metadata & timestamps | JSON |
| `full_results.json` | All results in structured format | JSON |
| `README.md` | Guide for using generated files | Markdown |

### How to Use Generated Files

```bash
# Navigate to output
cd output

# Run the generated code
python generated_code.py

# Run tests
python -m pytest test_generated_code.py -v

# Deploy (make script executable first)
chmod +x deploy.sh
./deploy.sh

# View documentation
cat documentation.md
# or open in any Markdown viewer
```

### Download Options

**From Streamlit UI:**
- Individual file downloads from sidebar
- Click any download button for specific files
- All files automatically saved to `output/`

**From Command Line:**
```bash
# Copy all generated files
cp -r output/ my-project/

# Or copy specific files
cp output/generated_code.py .
cp output/test_generated_code.py .
```

## 🧪 Testing

### Run Framework Tests

```bash
python -m pytest tests/ -v
```

### Run Generated Tests

After processing a requirement:

```bash
cd output
python -m pytest test_generated_code.py -v
```

## 🔍 Example Workflows

### Example 1: Simple Calculator

**Input:**
```
Create a calculator that performs addition, subtraction, 
multiplication, and division with error handling
```

**Output:**
- Complete calculator class
- Documentation with usage examples
- Comprehensive test suite
- Deployment script

### Example 2: REST API

**Input:**
```
Build a REST API for a todo list application with 
CRUD operations using Flask
```

**Output:**
- Flask application with routes
- API documentation
- Integration tests
- Docker deployment configuration

### Example 3: Data Processing

**Input:**
```
Create a CSV data processor that can read files, 
clean data, and generate statistics
```

**Output:**
- Data processing module
- Documentation with examples
- Unit tests for each function
- Setup script

## 🐛 Troubleshooting

### Common Issues

**Issue: "GROQ_API_KEY not found"**
```bash
# Solution: Set the environment variable
export GROQ_API_KEY=your_key_here  # Linux/Mac
set GROQ_API_KEY=your_key_here     # Windows
```

**Issue: "Module not found: autogen"**
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

**Issue: "Rate limit exceeded"**
```
Solution: Groq free tier has rate limits. Wait a few minutes or upgrade your plan.
```

**Issue: Streamlit not starting**
```bash
# Solution: Ensure Streamlit is installed
pip install streamlit
streamlit run streamlit_app.py
```

## 🔒 Security

- API keys are never stored in code
- All user inputs are validated
- Generated code is reviewed for security issues
- No code execution by default (can be enabled)

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 📚 Additional Resources

- [AutoGen Documentation](https://microsoft.github.io/autogen/)
- [Groq API Documentation](https://console.groq.com/docs)
- [Streamlit Documentation](https://docs.streamlit.io/)