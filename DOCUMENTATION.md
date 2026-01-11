# Multi-Agentic Framework - Technical Documentation

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Agent Specifications](#agent-specifications)
4. [Workflow](#workflow)
5. [API Reference](#api-reference)
6. [Configuration](#configuration)
7. [Error Handling](#error-handling)
8. [Performance Optimization](#performance-optimization)

## Overview

The Multi-Agentic Framework is a sophisticated software development system that leverages multiple specialized AI agents working collaboratively to transform natural language requirements into production-ready code, documentation, tests, and deployment configurations.

### Key Components

- **AutoGen Framework**: Orchestrates agent communication
- **Groq API**: Provides fast LLM inference
- **Specialized Agents**: Each agent handles a specific aspect of software development
- **Streamlit UI**: User-friendly interface for interaction

### Design Principles

1. **Modularity**: Each agent is independent and specialized
2. **Iterative Refinement**: Code review enables quality improvement
3. **Parallel Processing**: Documentation, testing, and deployment run concurrently
4. **Fault Tolerance**: Robust error handling and fallback mechanisms

## Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     User Interface Layer                     │
│                    (Streamlit / CLI)                         │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                  Orchestration Layer                         │
│              (MultiAgentFramework)                           │
│  ┌──────────────────────────────────────────────────────┐  │
│  │          Agent Communication Manager                  │  │
│  │         (AutoGen Group Chat / Sequential)            │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                    Agent Layer                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │   Req    │  │  Coding  │  │  Review  │  │   Doc    │  │
│  │ Analysis │→ │  Agent   │→ │  Agent   │→ │  Agent   │  │
│  └──────────┘  └──────────┘  └────┬─────┘  └──────────┘  │
│                                    │                        │
│                              ┌─────▼─────┐                  │
│                              │ Iteration │                  │
│                              │   Loop    │                  │
│                              └─────┬─────┘                  │
│                                    │                        │
│  ┌──────────┐  ┌──────────┐       │                        │
│  │   Test   │  │  Deploy  │◄──────┘                        │
│  │   Agent  │  │  Agent   │                                │
│  └──────────┘  └──────────┘                                │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                     LLM Layer                                │
│              (Groq API / Llama Models)                       │
└──────────────────────────────────────────────────────────────┘
```

### Data Flow

```
Natural Language Requirement
    │
    ├─[Parse & Structure]─> Structured Requirements (JSON)
    │
    ├─[Code Generation]───> Initial Code (Python)
    │
    ├─[Quality Review]────> Review Feedback (JSON)
    │   │
    │   └─[If Rejected]───> [Iterate Code Generation]
    │
    ├─[Approved Code]─────> Final Code
    │
    ├─[Parallel Processing]
    │   ├─> Documentation (Markdown)
    │   ├─> Test Cases (Python/pytest)
    │   └─> Deployment Config (Shell/Docker)
    │
    └─[Output]────────────> Complete Software Package
```

## Agent Specifications

### 1. Requirement Analysis Agent

**Purpose**: Transform natural language into structured, actionable requirements.

**Input**: 
- Natural language description of desired software

**Output**: JSON structure
```json
{
  "title": "Project name",
  "description": "Detailed description",
  "features": ["list", "of", "features"],
  "constraints": ["technical", "constraints"],
  "edge_cases": ["potential", "edge_cases"]
}
```

**Capabilities**:
- Natural language understanding
- Feature extraction
- Constraint identification
- Edge case detection
- Requirement prioritization

**System Prompt**:
```
You are a requirements analyst. Your job is to:
1. Analyze natural language requirements
2. Extract key features and constraints
3. Structure requirements in a clear format
4. Identify potential edge cases
5. Output structured requirements in JSON format
```

### 2. Coding Agent

**Purpose**: Generate functional, clean Python code from requirements.

**Input**: 
- Structured requirements (JSON)
- Feedback from code review (if iterating)

**Output**: 
- Python code with proper structure
- Docstrings and comments
- Error handling

**Capabilities**:
- Code generation
- PEP 8 compliance
- Design pattern implementation
- Error handling
- Code organization

**Quality Standards**:
- Modular functions/classes
- Comprehensive docstrings
- Type hints (when appropriate)
- Error handling for edge cases
- Clean, readable code

### 3. Code Review Agent

**Purpose**: Ensure code quality, correctness, and security.

**Input**: 
- Generated Python code
- Original requirements

**Output**: JSON review
```json
{
  "status": "approved|needs_revision",
  "score": 8.5,
  "findings": [
    {
      "type": "error|warning|info|success",
      "message": "Detailed feedback"
    }
  ],
  "suggestions": ["improvement1", "improvement2"]
}
```

**Review Criteria**:
1. **Correctness**: Does code meet requirements?
2. **Efficiency**: Are algorithms optimal?
3. **Security**: Any vulnerabilities?
4. **Readability**: Is code clear and maintainable?
5. **Error Handling**: Are edge cases covered?

**Iteration Process**:
- Max 3 iterations by default
- Provides specific, actionable feedback
- Tracks improvements across iterations

### 4. Documentation Agent

**Purpose**: Create comprehensive technical documentation.

**Input**: 
- Final approved code
- Requirements

**Output**: Markdown documentation

**Sections Generated**:
1. Overview
2. Installation instructions
3. API/Function reference
4. Usage examples
5. Error handling notes
6. Dependencies

**Documentation Standards**:
- Clear, concise language
- Practical examples
- Complete API coverage
- Troubleshooting guide

### 5. Test Case Generation Agent

**Purpose**: Generate comprehensive test suites.

**Input**: 
- Final code
- Requirements

**Output**: Python test file (pytest/unittest)

**Test Coverage**:
- Unit tests for each function
- Integration tests for workflows
- Edge case testing
- Error condition testing
- Typical coverage: >80%

**Test Structure**:
```python
import unittest

class TestModule(unittest.TestCase):
    def setUp(self):
        # Setup code
        pass
    
    def test_feature_1(self):
        # Test implementation
        pass
    
    def test_edge_case(self):
        # Edge case testing
        pass
    
    def tearDown(self):
        # Cleanup
        pass
```

### 6. Deployment Configuration Agent

**Purpose**: Create deployment artifacts and scripts.

**Input**: 
- Final code
- Requirements
- Dependencies

**Output**:
- deployment.sh or deploy.py
- requirements.txt
- Environment setup instructions
- Optional: Dockerfile, docker-compose.yml

**Deployment Artifacts**:
1. **Setup Script**: Automates environment setup
2. **Dependencies**: requirements.txt or setup.py
3. **Configuration**: Environment variables, configs
4. **Instructions**: Step-by-step deployment guide

## Workflow

### Sequential Processing Flow

```python
def process_requirement(requirement: str) -> dict:
    # Step 1: Analyze
    structured_req = analyze_requirements(requirement)
    
    # Step 2: Generate Code
    initial_code = generate_code(structured_req)
    
    # Step 3: Review & Iterate
    review, final_code = review_code(initial_code, structured_req)
    
    # Step 4-6: Parallel Processing
    documentation = generate_documentation(final_code, structured_req)
    tests = generate_tests(final_code, structured_req)
    deployment = generate_deployment(final_code, structured_req)
    
    return {
        'requirements': structured_req,
        'code': final_code,
        'review': review,
        'documentation': documentation,
        'tests': tests,
        'deployment': deployment
    }
```

### State Management

The framework maintains comprehensive state throughout processing:

```python
self.results = {
    'requirements': {},      # Structured requirements (JSON)
    'code': "",             # Initial code (before review)
    'review': {},           # Review results with score
    'final_code': "",       # Approved code (after review)
    'documentation': "",    # Generated docs (Markdown)
    'tests': "",           # Test suite (Python)
    'deployment': {}       # Deployment config (script + metadata)
}
```

**Key Differences:**
- `code` vs `final_code`: Initial vs. reviewed version
- `review`: Contains status, score, findings, suggestions
- `deployment`: Dictionary with script and metadata

### Error Recovery

Each stage includes comprehensive error handling:

1. **Validation**: Input validation at each stage
2. **Retry Logic**: Automatic retry for transient failures
3. **Fallbacks**: Default responses for parsing errors
4. **Logging**: Comprehensive logging for debugging
5. **Termination**: Max turns to prevent infinite loops
6. **Code Execution**: Disabled to prevent hanging

**New Safety Features:**
- `code_execution_config=False` - Prevents hanging
- `max_turns` parameter - Limits conversation length
- `max_consecutive_auto_reply=3` - Prevents loops
- Better JSON parsing with fallbacks

## API Reference

### MultiAgentFramework Class

```python
class MultiAgentFramework:
    def __init__(self, api_key: str, model: str = "llama-3.3-70b-versatile")
```

**Parameters**:
- `api_key` (str): Groq API key
- `model` (str, optional): Model name. Default: "llama-3.3-70b-versatile"

**Methods**:

#### process_requirement

```python
def process_requirement(requirement: str) -> Dict[str, Any]
```

Process a natural language requirement through all agents.

**Parameters**:
- `requirement` (str): Natural language description

**Returns**:
- `dict`: Complete results from all agents

**Example**:
```python
framework = MultiAgentFramework(api_key="your-key")
results = framework.process_requirement("Create a calculator app")
```

#### save_results

```python
def save_results(output_dir: str = "output") -> None
```

Save all generated artifacts to files.

**Parameters**:
- `output_dir` (str): Output directory path. Default: "output"

**Generated Files**:
- `requirements.json` - Structured requirements
- `generated_code.py` - Final production code
- `initial_code.py` - Code before review
- `code_review.json` - Review results
- `documentation.md` - Technical documentation
- `test_generated_code.py` - Test suite
- `deploy.sh` - Deployment script
- `deployment_info.json` - Deployment metadata
- `full_results.json` - Complete results
- `README.md` - Output usage guide

### Configuration

#### LLM Configuration

```python
llm_config = {
    "config_list": [{
        "model": "llama-3.3-70b-versatile",
        "api_key": "your-api-key",
        "base_url": "https://api.groq.com/openai/v1",
        "api_type": "openai"
    }],
    "temperature": 0.7,
    "timeout": 120
}
```

**Adjustable Parameters**:
- `temperature`: Controls randomness (0.0-1.0)
- `timeout`: Request timeout in seconds
- `max_tokens`: Maximum response length

**Available Models**:
- `llama-3.3-70b-versatile` (default, recommended)
- `llama-3.1-70b-versatile`
- `mixtral-8x7b-32768`

#### Environment Configuration

Set in `.env` file:
```bash
GROQ_API_KEY=your_key_here
DEFAULT_MODEL=llama-3.3-70b-versatile
MAX_REVIEW_ITERATIONS=3
TIMEOUT_SECONDS=120
TEMPERATURE=0.7
OUTPUT_DIR=output
LOG_LEVEL=INFO
```

**Setup Methods**:
1. Copy `.env.example` to `.env` and edit
2. Set environment variables directly

#### Agent Configuration

Each agent can be customized:

```python
self.coding_agent = AssistantAgent(
    name="SoftwareDeveloper",
    system_message="Custom instructions...",
    llm_config=self.llm_config
)
```

**Important Settings**:
- `code_execution_config=False` - Prevents code execution
- `max_consecutive_auto_reply=3` - Limits loops
- `max_turns` in chat - Controls conversation length

## Error Handling

### Exception Hierarchy

```
Exception
├── FrameworkError (base custom exception)
│   ├── AgentError
│   │   ├── RequirementAnalysisError
│   │   ├── CodeGenerationError
│   │   ├── CodeReviewError
│   │   └── ... (other agent errors)
│   ├── ConfigurationError
│   └── ProcessingError
```

### Error Handling Strategy

1. **Validation Errors**: Caught early with clear messages
2. **API Errors**: Retry with exponential backoff
3. **Parsing Errors**: Fallback to default structures
4. **Timeout Errors**: Configurable timeout with warnings

### Example Error Handling

```python
try:
    results = framework.process_requirement(requirement)
except ValueError as e:
    logger.error(f"Invalid input: {e}")
except TimeoutError as e:
    logger.error(f"Request timeout: {e}")
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    # Implement recovery or cleanup
```

## Performance Optimization

### Optimization Strategies

1. **Parallel Processing**: Run independent agents concurrently
2. **Caching**: Cache agent responses for similar inputs
3. **Batch Processing**: Process multiple requirements together
4. **Model Selection**: Use appropriate model for task complexity

### Monitoring

```python
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

start_time = time.time()
results = framework.process_requirement(requirement)
elapsed = time.time() - start_time

logger.info(f"Processing completed in {elapsed:.2f} seconds")
```

### Common Issues and Solutions

#### Issue 1: API Authentication Failed

**Symptoms**:
```
Error: Authentication failed - Invalid API key
```

**Solution**:
```bash

# check manually
echo $GROQ_API_KEY

# Verify .env file
cat .env
```

#### Issue 2: Agent Status Not Updating

**Symptoms**:
- Only some agents show ✅ after completion
- Results tab shows data but status is ⏸️

**Solution**:
This has been fixed in the latest version. If you still see it:
```python
# Verify results structure
print(st.session_state.results.keys())
# Should show: requirements, code, review, final_code, etc.

# Refresh Streamlit page
# Press 'R' or reload browser
```

#### Issue 3: .env File Not Loading

**Symptoms**:
- Need to manually export GROQ_API_KEY every time
- "API key not found" errors

**Solution**:
```bash
# Verify file exists
ls -la .env

# Check it's in the right location
# Should be in same directory as main.py

# Test loading
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('GROQ_API_KEY'))"

# If None, create .env file properly
```

#### Issue 4: Code Execution Hanging

**Symptoms**:
- Processing gets stuck during code generation
- Terminal shows "Executing code block"

**Solution**:
Already fixed with `code_execution_config=False`. If you modified the code:
```python
# In main.py, ensure:
self.user_proxy = UserProxyAgent(
    name="UserProxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=3,
    code_execution_config=False  # Must be False
)
```

#### Issue 5: Rate Limiting

**Symptoms**:
```
Error: Rate limit exceeded - 429 Too Many Requests
```

**Solution**:
- Wait 60 seconds before retrying
- Free tier limits: 30 req/min, 14,400 req/day
- Upgrade at https://console.groq.com
- Check usage in Groq dashboard

#### Issue 6: Missing Downloads

**Symptoms**:
- Download buttons not showing all files
- Some files missing from output/

**Solution**:
```bash
# Check what was generated
ls -la output/

# Verify save_results was called
# Should see 10 files:
# requirements.json, generated_code.py, initial_code.py,
# code_review.json, documentation.md, test_generated_code.py,
# deploy.sh, deployment_info.json, full_results.json, README.md

# If files missing, check logs for errors
```

## Best Practices

### Writing Good Requirements

✅ **Good**:
```
Create a REST API for a todo list application with:
- CRUD operations for todos
- User authentication via JWT
- SQLite database
- Input validation
- Error handling
```

❌ **Bad**:
```
Make a todo app
```

### Interpreting Results

1. **Review the Score**: Aim for 8+ for production use
2. **Check Findings**: Address any errors or warnings
3. **Test Generated Code**: Run the test suite
4. **Review Documentation**: Ensure completeness

### Deployment Checklist

- [ ] Review generated code manually
- [ ] Run all test cases
- [ ] Check security findings
- [ ] Verify dependencies
- [ ] Test deployment script
- [ ] Review documentation for accuracy

---

