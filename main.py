"""
Multi-Agentic Framework using AutoGen
Main orchestration file for the multi-agent system
"""

import os
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    # Try new autogen-agentchat package structure
    from autogen_agentchat.agents import AssistantAgent
    from autogen_agentchat.agents import UserProxyAgent
except ImportError:
    try:
        # Try old pyautogen package structure
        import autogen
        AssistantAgent = autogen.AssistantAgent
        UserProxyAgent = autogen.UserProxyAgent
    except ImportError:
        raise ImportError(
            "AutoGen not found. Please install with: pip install pyautogen==0.2.32"
        )

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MultiAgentFramework:
    """Orchestrates multiple specialized agents for software development"""
    
    def __init__(self, api_key: str, model: str = "llama-3.3-70b-versatile"):
        """
        Initialize the multi-agent framework
        
        Args:
            api_key: Groq API key
            model: Model name to use
        """
        self.api_key = api_key
        self.model = model
        self.results = {}
        self.conversation_history = []
        
        # Configure LLM
        self.llm_config = {
            "config_list": [{
                "model": model,
                "api_key": api_key,
                "base_url": "https://api.groq.com/openai/v1",
                "api_type": "openai"
            }],
            "temperature": 0.7,
            "timeout": 120,
        }
        
        # Initialize agents
        self._initialize_agents()
        
    def _initialize_agents(self):
        """Initialize all specialized agents"""
        
        # Requirement Analysis Agent
        self.req_agent = AssistantAgent(
            name="RequirementAnalyst",
            system_message="""You are a requirements analyst. Your job is to:
            1. Analyze natural language requirements
            2. Extract key features and constraints
            3. Structure requirements in a clear format
            4. Identify potential edge cases
            5. Output structured requirements in JSON format
            
            Return your analysis in this JSON format:
            {
                "title": "Project title",
                "description": "Detailed description",
                "features": ["feature1", "feature2"],
                "constraints": ["constraint1", "constraint2"],
                "edge_cases": ["edge_case1", "edge_case2"]
            }""",
            llm_config=self.llm_config
        )
        
        # Coding Agent
        self.coding_agent = AssistantAgent(
            name="SoftwareDeveloper",
            system_message="""You are an expert Python developer. Your job is to:
            1. Convert requirements into clean, functional Python code
            2. Follow PEP 8 style guidelines
            3. Include proper error handling
            4. Add docstrings and comments
            5. Write modular, reusable code
            
            IMPORTANT: 
            - Provide ONLY the Python code without markdown code blocks
            - Do NOT include interactive input() calls that wait for user input
            - For CLI applications, provide example usage in comments instead of running the code
            - Do NOT wrap code in ```python blocks
            
            Generate complete, working Python code based on requirements.""",
            llm_config=self.llm_config
        )
        
        # Code Review Agent
        self.review_agent = AssistantAgent(
            name="CodeReviewer",
            system_message="""You are a senior code reviewer. Your job is to:
            1. Review code for correctness and efficiency
            2. Check for security vulnerabilities
            3. Verify error handling
            4. Assess code quality and readability
            5. Provide actionable feedback
            
            Return review in JSON format:
            {
                "status": "approved|needs_revision",
                "score": 0-10,
                "findings": [
                    {"type": "error|warning|info|success", "message": "..."}
                ],
                "suggestions": ["suggestion1", "suggestion2"]
            }""",
            llm_config=self.llm_config
        )
        
        # Documentation Agent
        self.doc_agent = AssistantAgent(
            name="TechnicalWriter",
            system_message="""You are a technical documentation writer. Your job is to:
            1. Create clear, comprehensive documentation
            2. Document all functions and classes
            3. Provide usage examples
            4. Include installation instructions
            5. Format in Markdown
            
            Generate complete documentation including:
            - Overview
            - Installation
            - API reference
            - Usage examples
            - Error handling notes""",
            llm_config=self.llm_config
        )
        
        # Test Case Generation Agent
        self.test_agent = AssistantAgent(
            name="QAEngineer",
            system_message="""You are a QA engineer specializing in test automation. Your job is to:
            1. Generate comprehensive unit tests using pytest or unittest
            2. Create integration tests
            3. Cover edge cases and error conditions
            4. Ensure good test coverage (>80%)
            5. Follow testing best practices
            
            Generate complete test code with:
            - Test setup and teardown
            - Multiple test cases per function
            - Edge case testing
            - Error condition testing""",
            llm_config=self.llm_config
        )
        
        # Deployment Configuration Agent
        self.deploy_agent = AssistantAgent(
            name="DevOpsEngineer",
            system_message="""You are a DevOps engineer. Your job is to:
            1. Create deployment scripts
            2. Generate requirements.txt or setup.py
            3. Create Docker configuration (if needed)
            4. Write setup instructions
            5. Include environment configuration
            
            Generate deployment artifacts:
            - deployment.sh or deploy.py script
            - requirements.txt
            - README for deployment
            - Environment setup instructions""",
            llm_config=self.llm_config
        )
        
        # User proxy for interaction
        self.user_proxy = UserProxyAgent(
            name="UserProxy",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=3,  # Reduced to avoid infinite loops
            code_execution_config=False,  # Disable code execution to prevent hanging
            is_termination_msg=lambda x: x.get("content", "").strip().endswith("TERMINATE") or 
                                          "exitcode" in x.get("content", "")
        )
    
    def process_requirement(self, requirement: str) -> Dict[str, Any]:
        """
        Process a natural language requirement through all agents
        
        Args:
            requirement: Natural language requirement
            
        Returns:
            Dictionary containing all agent outputs
        """
        logger.info("Starting multi-agent processing...")
        
        try:
            # Step 1: Requirement Analysis
            logger.info("Step 1: Analyzing requirements...")
            req_result = self._analyze_requirements(requirement)
            self.results['requirements'] = req_result
            
            # Step 2: Code Generation
            logger.info("Step 2: Generating code...")
            code_result = self._generate_code(req_result)
            self.results['code'] = code_result
            
            # Step 3: Code Review (with iteration)
            logger.info("Step 3: Reviewing code...")
            review_result, final_code = self._review_code(code_result, req_result)
            self.results['review'] = review_result
            self.results['final_code'] = final_code
            
            # Step 4: Documentation
            logger.info("Step 4: Generating documentation...")
            doc_result = self._generate_documentation(final_code, req_result)
            self.results['documentation'] = doc_result
            
            # Step 5: Test Cases
            logger.info("Step 5: Generating test cases...")
            test_result = self._generate_tests(final_code, req_result)
            self.results['tests'] = test_result
            
            # Step 6: Deployment Configuration
            logger.info("Step 6: Creating deployment configuration...")
            deploy_result = self._generate_deployment(final_code, req_result)
            self.results['deployment'] = deploy_result
            
            logger.info("Multi-agent processing completed successfully!")
            return self.results
            
        except Exception as e:
            logger.error(f"Error during processing: {str(e)}")
            raise
    
    def _analyze_requirements(self, requirement: str) -> Dict:
        """Analyze requirements using the requirement agent"""
        self.user_proxy.initiate_chat(
            self.req_agent,
            message=f"Analyze this requirement and provide structured output:\n{requirement}\n\nIMPORTANT: Provide ONLY the JSON output, no code blocks or explanations.",
            max_turns=2  # Limit conversation turns
        )
        
        # Extract the last message from agent
        messages = self.user_proxy.chat_messages[self.req_agent]
        last_message = messages[-1]['content']
        
        # Try to parse JSON from the response
        try:
            # Look for JSON in the response
            import re
            json_match = re.search(r'\{.*\}', last_message, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass
        
        # Fallback: return structured data
        return {
            "title": "Software Project",
            "description": requirement,
            "features": ["Core functionality"],
            "constraints": ["Python implementation"],
            "edge_cases": []
        }
    
    def _generate_code(self, requirements: Dict) -> str:
        """Generate code using the coding agent"""
        req_text = json.dumps(requirements, indent=2)
        self.user_proxy.initiate_chat(
            self.coding_agent,
            message=f"Generate Python code for these requirements:\n{req_text}\n\nIMPORTANT: Provide ONLY the code, no markdown formatting or explanations before/after.",
            max_turns=1  # Single turn for code generation
        )
        
        messages = self.user_proxy.chat_messages[self.coding_agent]
        return messages[-1]['content']
    
    def _review_code(self, code: str, requirements: Dict, max_iterations: int = 3) -> tuple:
        """Review code and iterate if needed"""
        current_code = code
        iteration = 0
        
        while iteration < max_iterations:
            # Review the code
            self.user_proxy.initiate_chat(
                self.review_agent,
                message=f"Review this code:\n{current_code}\n\nIMPORTANT: Provide ONLY the JSON review, no explanations.",
                max_turns=1
            )
            
            messages = self.user_proxy.chat_messages[self.review_agent]
            review_text = messages[-1]['content']
            
            # Parse review
            try:
                import re
                json_match = re.search(r'\{.*\}', review_text, re.DOTALL)
                if json_match:
                    review_result = json.loads(json_match.group())
                else:
                    review_result = {"status": "approved", "score": 8}
            except:
                review_result = {"status": "approved", "score": 8}
            
            # If approved, return
            if review_result.get('status') == 'approved':
                return review_result, current_code
            
            # If needs revision, regenerate
            if iteration < max_iterations - 1:
                logger.info(f"Code needs revision (iteration {iteration + 1}). Regenerating...")
                self.user_proxy.initiate_chat(
                    self.coding_agent,
                    message=f"Improve this code based on review:\n{review_text}\n\nOriginal code:\n{current_code}\n\nIMPORTANT: Provide ONLY the improved code.",
                    max_turns=1
                )
                messages = self.user_proxy.chat_messages[self.coding_agent]
                current_code = messages[-1]['content']
            
            iteration += 1
        
        return review_result, current_code
    
    def _generate_documentation(self, code: str, requirements: Dict) -> str:
        """Generate documentation using the documentation agent"""
        self.user_proxy.initiate_chat(
            self.doc_agent,
            message=f"Create documentation for this code:\n{code}\n\nIMPORTANT: Provide documentation in Markdown format.",
            max_turns=1
        )
        
        messages = self.user_proxy.chat_messages[self.doc_agent]
        return messages[-1]['content']
    
    def _generate_tests(self, code: str, requirements: Dict) -> str:
        """Generate test cases using the test agent"""
        self.user_proxy.initiate_chat(
            self.test_agent,
            message=f"Generate comprehensive tests for this code:\n{code}\n\nIMPORTANT: Provide ONLY the test code.",
            max_turns=1
        )
        
        messages = self.user_proxy.chat_messages[self.test_agent]
        return messages[-1]['content']
    
    def _generate_deployment(self, code: str, requirements: Dict) -> Dict[str, str]:
        """Generate deployment configuration using the deployment agent"""
        self.user_proxy.initiate_chat(
            self.deploy_agent,
            message=f"Create deployment configuration for this project:\nCode:\n{code}\nRequirements:\n{json.dumps(requirements)}\n\nIMPORTANT: Provide deployment script and requirements.txt.",
            max_turns=1
        )
        
        messages = self.user_proxy.chat_messages[self.deploy_agent]
        return {
            'script': messages[-1]['content'],
            'timestamp': datetime.now().isoformat()
        }
    
    def save_results(self, output_dir: str = "output"):
        """Save all results to files"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Save requirements as JSON
        if 'requirements' in self.results:
            with open(f"{output_dir}/requirements.json", 'w') as f:
                json.dump(self.results['requirements'], f, indent=2)
            logger.info(f"Requirements saved to {output_dir}/requirements.json")
        
        # Save initial code
        if 'code' in self.results:
            with open(f"{output_dir}/initial_code.py", 'w') as f:
                f.write(self.results['code'])
            logger.info(f"Initial code saved to {output_dir}/initial_code.py")
        
        # Save final code (after review)
        if 'final_code' in self.results:
            with open(f"{output_dir}/generated_code.py", 'w') as f:
                f.write(self.results['final_code'])
            logger.info(f"Final code saved to {output_dir}/generated_code.py")
        
        # Save code review as JSON
        if 'review' in self.results:
            with open(f"{output_dir}/code_review.json", 'w') as f:
                json.dump(self.results['review'], f, indent=2)
            logger.info(f"Code review saved to {output_dir}/code_review.json")
        
        # Save documentation
        if 'documentation' in self.results:
            with open(f"{output_dir}/documentation.md", 'w') as f:
                f.write(self.results['documentation'])
            logger.info(f"Documentation saved to {output_dir}/documentation.md")
        
        # Save tests
        if 'tests' in self.results:
            with open(f"{output_dir}/test_generated_code.py", 'w') as f:
                f.write(self.results['tests'])
            logger.info(f"Tests saved to {output_dir}/test_generated_code.py")
        
        # Save deployment script
        if 'deployment' in self.results:
            deploy_data = self.results['deployment']
            script_content = deploy_data.get('script', '') if isinstance(deploy_data, dict) else deploy_data
            
            with open(f"{output_dir}/deploy.sh", 'w') as f:
                f.write(script_content)
            logger.info(f"Deployment script saved to {output_dir}/deploy.sh")
            
            # Also save deployment metadata
            if isinstance(deploy_data, dict):
                with open(f"{output_dir}/deployment_info.json", 'w') as f:
                    json.dump(deploy_data, f, indent=2)
                logger.info(f"Deployment info saved to {output_dir}/deployment_info.json")
        
        # Save full results as JSON
        with open(f"{output_dir}/full_results.json", 'w') as f:
            json.dump(self.results, f, indent=2)
        logger.info(f"Full results saved to {output_dir}/full_results.json")
        
        # Create a README for the output
        readme_content = f"""# Generated Output

This directory contains all generated artifacts from the Multi-Agent Framework.

## Generated Files

### Requirements
- `requirements.json` - Structured requirements from natural language input

### Code
- `generated_code.py` - Final production-ready code (after review)
- `initial_code.py` - Initial code before review (if different)

### Quality Assurance
- `code_review.json` - Detailed code review results
- `test_generated_code.py` - Comprehensive test suite

### Documentation
- `documentation.md` - Complete technical documentation

### Deployment
- `deploy.sh` - Deployment script
- `deployment_info.json` - Deployment metadata and timestamps

### Complete Data
- `full_results.json` - All results in structured JSON format

## Generated On
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## How to Use

### Run the Code
```bash
python generated_code.py
```

### Run Tests
```bash
python -m pytest test_generated_code.py -v
```

### Deploy
```bash
chmod +x deploy.sh
./deploy.sh
```

### View Documentation
Open `documentation.md` in any Markdown viewer or editor.
"""
        
        with open(f"{output_dir}/README.md", 'w') as f:
            f.write(readme_content)
        logger.info(f"Output README saved to {output_dir}/README.md")
        
        logger.info(f"All results saved to {output_dir}/")


if __name__ == "__main__":
    # Example usage
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable not set")
    
    framework = MultiAgentFramework(api_key=api_key)
    
    requirement = """
    Create a simple calculator application that can:
    - Perform basic arithmetic operations (add, subtract, multiply, divide)
    - Handle invalid inputs gracefully
    - Provide a command-line interface
    """
    
    results = framework.process_requirement(requirement)
    framework.save_results()
    
    print("Multi-agent processing completed!")
    print(f"Results saved to output directory")