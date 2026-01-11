"""
Streamlit UI for Multi-Agentic Framework
Provides an interactive interface for the multi-agent system
"""

import streamlit as st
import os
import json
from datetime import datetime
from main import MultiAgentFramework
import traceback
from dotenv import load_dotenv
import io
import zipfile
import json

# Load environment variables from .env file
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Multi-Agent Framework",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTextArea textarea {
        font-size: 14px;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        margin: 1rem 0;
    }
    .error-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        margin: 1rem 0;
    }
    .agent-card {
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #dee2e6;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'framework' not in st.session_state:
    st.session_state.framework = None
if 'results' not in st.session_state:
    st.session_state.results = None
if 'processing' not in st.session_state:
    st.session_state.processing = False
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'auto_init_done' not in st.session_state:
    st.session_state.auto_init_done = False

# Auto-initialize framework if API key is in environment
if not st.session_state.auto_init_done and os.getenv("GROQ_API_KEY"):
    try:
        api_key = os.getenv("GROQ_API_KEY")
        st.session_state.framework = MultiAgentFramework(
            api_key=api_key,
            model="llama-3.3-70b-versatile"
        )
        st.session_state.auto_init_done = True
    except:
        pass  # Silent fail for auto-init

def add_log(message, level="info"):
    """Add a log entry"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.logs.append({
        "timestamp": timestamp,
        "message": message,
        "level": level
    })

def initialize_framework(api_key, model):
    """Initialize the multi-agent framework"""
    try:
        st.session_state.framework = MultiAgentFramework(
            api_key=api_key,
            model=model
        )
        add_log("Framework initialized successfully", "success")
        return True
    except Exception as e:
        add_log(f"Error initializing framework: {str(e)}", "error")
        return False

def process_requirement(requirement):
    """Process the requirement through all agents"""
    if not st.session_state.framework:
        add_log("Framework not initialized", "error")
        return
    
    st.session_state.processing = True
    st.session_state.logs = []
    
    try:
        add_log("Starting multi-agent processing...", "info")
        
        # Process through framework
        results = st.session_state.framework.process_requirement(requirement)
        st.session_state.results = results
        
        # Save results
        st.session_state.framework.save_results("output")
        
        add_log("Processing completed successfully!", "success")
        
    except Exception as e:
        add_log(f"Error during processing: {str(e)}", "error")
        st.error(f"Error: {str(e)}\n\n{traceback.format_exc()}")
    
    finally:
        st.session_state.processing = False

# Main UI
st.title("🤖 Multi-Agentic Framework with AutoGen")
st.markdown("Collaborative AI agents working together to build software from requirements")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Check if API key is in environment
    env_api_key = os.getenv("GROQ_API_KEY", "")
    
    # Show status
    if env_api_key:
        st.success("✅ API Key loaded from .env file")
        if st.session_state.framework:
            st.success("✅ Framework initialized automatically")
    else:
        st.warning("⚠️ No API key found. Please enter below or create .env file.")
    
    # API Configuration
    api_key = st.text_input(
        "Groq API Key",
        type="password",
        value=env_api_key,
        help="Enter your Groq API key (or set GROQ_API_KEY in .env file)"
    )
    
    model = st.selectbox(
        "Select Model",
        [
            "llama-3.3-70b-versatile",
            "llama-3.1-70b-versatile",
            "mixtral-8x7b-32768"
        ],
        help="Choose the LLM model to use"
    )
    
    if st.button("Initialize Framework", type="primary"):
        if api_key:
            with st.spinner("Initializing framework..."):
                if initialize_framework(api_key, model):
                    st.success("✅ Framework initialized!")
        else:
            st.error("Please enter API key")
    
    st.divider()
    
    # Agent Status
    st.header("🔄 Agent Status")
    agents = [
        ("📋", "Requirement Analysis", "requirements"),
        ("💻", "Coding", "code"),
        ("🔍", "Code Review", "review"),
        ("📚", "Documentation", "documentation"),
        ("🧪", "Test Generation", "tests"),
        ("🚀", "Deployment Config", "deployment")
    ]
    
    for emoji, name, key in agents:
        if st.session_state.results and key in st.session_state.results:
            status = "✅"
        else:
            status = "⏸️"
        st.markdown(f"{emoji} **{name}** {status}")
    
    st.divider()
    
    # Download Results
    if st.session_state.results:
        st.header("📥 Download Results")
        
        # Requirements
        if 'requirements' in st.session_state.results:
            req_json = json.dumps(st.session_state.results['requirements'], indent=2)
            st.download_button(
                "📋 Requirements (JSON)",
                req_json,
                "requirements.json",
                "application/json",
                use_container_width=True
            )
        
        # Code
        if 'final_code' in st.session_state.results:
            st.download_button(
                "💻 Generated Code",
                st.session_state.results['final_code'],
                "generated_code.py",
                "text/plain",
                use_container_width=True
            )
        
        # Review
        if 'review' in st.session_state.results:
            review_json = json.dumps(st.session_state.results['review'], indent=2)
            st.download_button(
                "🔍 Code Review (JSON)",
                review_json,
                "code_review.json",
                "application/json",
                use_container_width=True
            )
        
        # Documentation
        if 'documentation' in st.session_state.results:
            st.download_button(
                "📚 Documentation",
                st.session_state.results['documentation'],
                "documentation.md",
                "text/markdown",
                use_container_width=True
            )
        
        # Tests
        if 'tests' in st.session_state.results:
            st.download_button(
                "🧪 Test Cases",
                st.session_state.results['tests'],
                "test_code.py",
                "text/plain",
                use_container_width=True
            )
        
        # Deployment
        if 'deployment' in st.session_state.results:
            deploy = st.session_state.results['deployment']
            deploy_content = deploy.get('script', deploy) if isinstance(deploy, dict) else deploy
            st.download_button(
                "🚀 Deployment Script",
                deploy_content,
                "deploy.sh",
                "text/plain",
                use_container_width=True
            )
        
        st.divider()
        

        # Download all as ZIP
        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            results = st.session_state.results

            if 'requirements' in results:
                zip_file.writestr(
                    "requirements.json",
                    json.dumps(results['requirements'], indent=2)
                    )

            if 'final_code' in results:
                zip_file.writestr("generated_code.py", results['final_code'])

            if 'review' in results:
                zip_file.writestr(
                    "code_review.json",
                    json.dumps(results['review'], indent=2)
                    )

            if 'documentation' in results:
                zip_file.writestr("documentation.md", results['documentation'])

            if 'tests' in results:
                zip_file.writestr("test_code.py", results['tests'])

            if 'deployment' in results:
                deploy = results['deployment']
                deploy_content = deploy.get('script', deploy) if isinstance(deploy, dict) else deploy
                zip_file.writestr("deploy.sh", deploy_content)

        zip_buffer.seek(0)

        st.download_button(
            label="📦 Download All Files (ZIP)",
            data=zip_buffer,
            file_name="project_outputs.zip",
            mime="application/zip",
            use_container_width=True
            )

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📝 Input Requirements")
    
    requirement = st.text_area(
        "Enter your software requirement in natural language:",
        height=200,
        placeholder="e.g., Create a calculator application that can perform basic arithmetic operations like addition, subtraction, multiplication, and division. It should handle errors gracefully and provide a simple user interface.",
        disabled=st.session_state.processing
    )
    
    if st.button(
        "🚀 Start Processing",
        type="primary",
        disabled=st.session_state.processing or not st.session_state.framework or not requirement.strip()
    ):
        process_requirement(requirement)
        st.rerun()
    
    # Display logs
    st.subheader("📊 Processing Logs")
    
    log_container = st.container()
    with log_container:
        if st.session_state.logs:
            for log in st.session_state.logs:
                icon = "ℹ️" if log['level'] == "info" else "✅" if log['level'] == "success" else "❌"
                st.text(f"[{log['timestamp']}] {icon} {log['message']}")
        else:
            st.info("No logs yet. Start processing to see activity.")
    
    # Show processing summary after completion
    if st.session_state.results and not st.session_state.processing:
        st.divider()
        st.subheader("✨ Processing Summary")
        
        summary_cols = st.columns(3)
        
        with summary_cols[0]:
            st.metric(
                "Files Generated",
                len([k for k in st.session_state.results.keys() if k in 
                     ['requirements', 'code', 'final_code', 'review', 'documentation', 'tests', 'deployment']])
            )
        
        with summary_cols[1]:
            if 'review' in st.session_state.results:
                score = st.session_state.results['review'].get('score', 'N/A')
                st.metric("Code Quality Score", f"{score}/10" if score != 'N/A' else 'N/A')
            else:
                st.metric("Code Quality Score", "N/A")
        
        with summary_cols[2]:
            if 'tests' in st.session_state.results:
                test_count = st.session_state.results['tests'].count('def test_')
                st.metric("Test Cases", test_count)
            else:
                st.metric("Test Cases", 0)
        
        st.success("✅ All files saved to output/ directory")

with col2:
    st.header("📦 Results")
    
    if st.session_state.results:
        tabs = st.tabs([
            "Requirements",
            "Code",
            "Review",
            "Documentation",
            "Tests",
            "Deployment",
            "Files"
        ])
        
        # Requirements Tab
        with tabs[0]:
            if 'requirements' in st.session_state.results:
                req = st.session_state.results['requirements']
                st.subheader("Structured Requirements")
                st.json(req)
                
                # Summary
                st.subheader("Summary")
                st.write(f"**Title:** {req.get('title', 'N/A')}")
                st.write(f"**Features:** {len(req.get('features', []))}")
                st.write(f"**Constraints:** {len(req.get('constraints', []))}")
                st.write(f"**Edge Cases:** {len(req.get('edge_cases', []))}")
        
        # Code Tab
        with tabs[1]:
            if 'final_code' in st.session_state.results:
                st.subheader("Final Code (After Review)")
                st.code(st.session_state.results['final_code'], language="python")
                
                # Show code stats
                code = st.session_state.results['final_code']
                lines = len(code.split('\n'))
                st.info(f"📊 Lines of code: {lines}")
            elif 'code' in st.session_state.results:
                st.subheader("Generated Code")
                st.code(st.session_state.results['code'], language="python")
        
        # Review Tab
        with tabs[2]:
            if 'review' in st.session_state.results:
                review = st.session_state.results['review']
                
                # Status and Score
                col_r1, col_r2 = st.columns(2)
                with col_r1:
                    status = review.get('status', 'unknown')
                    if status == 'approved':
                        st.success(f"✅ Status: {status.upper()}")
                    else:
                        st.warning(f"⚠️ Status: {status.upper()}")
                
                with col_r2:
                    score = review.get('score', 'N/A')
                    if isinstance(score, (int, float)):
                        if score >= 8:
                            st.success(f"🎯 Score: {score}/10")
                        elif score >= 6:
                            st.warning(f"⚠️ Score: {score}/10")
                        else:
                            st.error(f"❌ Score: {score}/10")
                    else:
                        st.info(f"Score: {score}")
                
                # Findings
                if 'findings' in review and review['findings']:
                    st.subheader("Findings")
                    for finding in review['findings']:
                        finding_type = finding.get('type', 'info')
                        message = finding.get('message', '')
                        
                        if finding_type == 'success':
                            st.success(f"✅ {message}")
                        elif finding_type == 'warning':
                            st.warning(f"⚠️ {message}")
                        elif finding_type == 'error':
                            st.error(f"❌ {message}")
                        else:
                            st.info(f"ℹ️ {message}")
                
                # Suggestions
                if 'suggestions' in review and review['suggestions']:
                    st.subheader("Suggestions for Improvement")
                    for i, suggestion in enumerate(review['suggestions'], 1):
                        st.write(f"{i}. {suggestion}")
                
                # Full JSON
                with st.expander("View Full Review JSON"):
                    st.json(review)
        
        # Documentation Tab
        with tabs[3]:
            if 'documentation' in st.session_state.results:
                st.markdown(st.session_state.results['documentation'])
        
        # Tests Tab
        with tabs[4]:
            if 'tests' in st.session_state.results:
                st.code(st.session_state.results['tests'], language="python")
                
                # Test stats
                test_code = st.session_state.results['tests']
                test_count = test_code.count('def test_')
                if test_count > 0:
                    st.info(f"🧪 Number of test functions: {test_count}")
        
        # Deployment Tab
        with tabs[5]:
            if 'deployment' in st.session_state.results:
                deploy = st.session_state.results['deployment']
                
                if isinstance(deploy, dict):
                    st.subheader("Deployment Script")
                    st.code(deploy.get('script', ''), language="bash")
                    
                    if 'timestamp' in deploy:
                        st.info(f"⏰ Generated at: {deploy['timestamp']}")
                else:
                    st.code(deploy, language="bash")
        
        # Files Tab
        with tabs[6]:
            st.subheader("Generated Files")
            st.write("All files have been saved to the `output/` directory:")
            
            files_info = [
                ("📋", "requirements.json", "Structured requirements"),
                ("💻", "generated_code.py", "Final production code"),
                ("🔍", "code_review.json", "Code review results"),
                ("📚", "documentation.md", "Technical documentation"),
                ("🧪", "test_generated_code.py", "Test suite"),
                ("🚀", "deploy.sh", "Deployment script"),
                ("📦", "full_results.json", "Complete results"),
                ("📄", "README.md", "Output guide")
            ]
            
            for emoji, filename, description in files_info:
                filepath = f"output/{filename}"
                if os.path.exists(filepath):
                    file_size = os.path.getsize(filepath)
                    st.write(f"{emoji} **{filename}** - {description}")
                    st.caption(f"   Size: {file_size:,} bytes | Path: `{filepath}`")
                else:
                    st.write(f"{emoji} **{filename}** - {description}")
                    st.caption(f"   ⚠️ File not found")
            
            st.divider()
            
            # Show directory structure
            if os.path.exists("output"):
                st.subheader("Output Directory Structure")
                st.code(f"""
output/
├── requirements.json          # Structured requirements
├── generated_code.py          # Final code
├── code_review.json          # Review results
├── documentation.md          # Documentation
├── test_generated_code.py    # Tests
├── deploy.sh                 # Deployment
├── deployment_info.json      # Deployment metadata
├── full_results.json         # All results
└── README.md                 # Usage guide
                """, language="text")
    
    else:
        st.info("👈 Enter requirements and click 'Start Processing' to see results here")

# Footer
st.divider()
st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>Multi-Agentic Framework v1.0 | Powered by AutoGen & Groq</p>
    </div>
""", unsafe_allow_html=True)