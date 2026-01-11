"""
Test suite for the Multi-Agentic Framework
Tests all components and integration points
"""

import pytest
import os
import json
from unittest.mock import Mock, patch, MagicMock
from main import MultiAgentFramework


class TestMultiAgentFramework:
    """Test cases for the MultiAgentFramework class"""
    
    @pytest.fixture
    def mock_api_key(self):
        """Provide a mock API key for testing"""
        return "test_api_key_123"
    
    @pytest.fixture
    def framework(self, mock_api_key):
        """Create a framework instance for testing"""
        with patch('autogen.AssistantAgent'):
            with patch('autogen.UserProxyAgent'):
                return MultiAgentFramework(api_key=mock_api_key)
    
    def test_initialization(self, mock_api_key):
        """Test framework initialization"""
        with patch('autogen.AssistantAgent'):
            with patch('autogen.UserProxyAgent'):
                framework = MultiAgentFramework(api_key=mock_api_key)
                
                assert framework.api_key == mock_api_key
                assert framework.model == "llama-3.3-70b-versatile"
                assert isinstance(framework.results, dict)
                assert len(framework.results) == 0
    
    def test_custom_model_initialization(self, mock_api_key):
        """Test initialization with custom model"""
        with patch('autogen.AssistantAgent'):
            with patch('autogen.UserProxyAgent'):
                custom_model = "llama-3.1-70b-versatile"
                framework = MultiAgentFramework(
                    api_key=mock_api_key,
                    model=custom_model
                )
                
                assert framework.model == custom_model
    
    def test_llm_config_structure(self, framework):
        """Test LLM configuration structure"""
        assert 'config_list' in framework.llm_config
        assert 'temperature' in framework.llm_config
        assert 'timeout' in framework.llm_config
        
        config = framework.llm_config['config_list'][0]
        assert 'model' in config
        assert 'api_key' in config
        assert 'base_url' in config
    
    def test_agents_initialized(self, framework):
        """Test that all agents are initialized"""
        assert hasattr(framework, 'req_agent')
        assert hasattr(framework, 'coding_agent')
        assert hasattr(framework, 'review_agent')
        assert hasattr(framework, 'doc_agent')
        assert hasattr(framework, 'test_agent')
        assert hasattr(framework, 'deploy_agent')
        assert hasattr(framework, 'user_proxy')
    
    def test_analyze_requirements_with_json(self, framework):
        """Test requirement analysis with valid JSON response"""
        mock_response = {
            "title": "Test Project",
            "description": "Test description",
            "features": ["feature1", "feature2"],
            "constraints": ["constraint1"],
            "edge_cases": ["edge1"]
        }
        
        framework.user_proxy.chat_messages = {
            framework.req_agent: [
                {'content': json.dumps(mock_response)}
            ]
        }
        
        with patch.object(framework.user_proxy, 'initiate_chat'):
            result = framework._analyze_requirements("test requirement")
            
            assert result['title'] == "Test Project"
            assert len(result['features']) == 2
    
    def test_analyze_requirements_fallback(self, framework):
        """Test requirement analysis fallback for non-JSON response"""
        framework.user_proxy.chat_messages = {
            framework.req_agent: [
                {'content': 'This is not JSON'}
            ]
        }
        
        with patch.object(framework.user_proxy, 'initiate_chat'):
            result = framework._analyze_requirements("test requirement")
            
            assert 'title' in result
            assert 'description' in result
            assert result['description'] == "test requirement"
    
    def test_generate_code(self, framework):
        """Test code generation"""
        mock_code = "def hello():\n    print('Hello, World!')"
        
        framework.user_proxy.chat_messages = {
            framework.coding_agent: [
                {'content': mock_code}
            ]
        }
        
        requirements = {"title": "Test", "features": ["test"]}
        
        with patch.object(framework.user_proxy, 'initiate_chat'):
            result = framework._generate_code(requirements)
            
            assert result == mock_code
    
    def test_review_code_approved(self, framework):
        """Test code review with approved status"""
        mock_review = {
            "status": "approved",
            "score": 9,
            "findings": []
        }
        
        framework.user_proxy.chat_messages = {
            framework.review_agent: [
                {'content': json.dumps(mock_review)}
            ]
        }
        
        code = "def test(): pass"
        requirements = {}
        
        with patch.object(framework.user_proxy, 'initiate_chat'):
            review, final_code = framework._review_code(code, requirements)
            
            assert review['status'] == 'approved'
            assert final_code == code
    
    def test_review_code_needs_revision(self, framework):
        """Test code review with revision needed"""
        mock_review_reject = {
            "status": "needs_revision",
            "score": 5,
            "suggestions": ["Add error handling"]
        }
        
        mock_review_approve = {
            "status": "approved",
            "score": 8
        }
        
        improved_code = "def test():\n    try:\n        pass\n    except: pass"
        
        # First review rejects, second approves
        call_count = [0]
        
        def mock_chat(*args, **kwargs):
            if call_count[0] == 0:
                framework.user_proxy.chat_messages = {
                    framework.review_agent: [
                        {'content': json.dumps(mock_review_reject)}
                    ]
                }
            elif call_count[0] == 1:
                framework.user_proxy.chat_messages = {
                    framework.coding_agent: [
                        {'content': improved_code}
                    ]
                }
            else:
                framework.user_proxy.chat_messages = {
                    framework.review_agent: [
                        {'content': json.dumps(mock_review_approve)}
                    ]
                }
            call_count[0] += 1
        
        with patch.object(framework.user_proxy, 'initiate_chat', side_effect=mock_chat):
            review, final_code = framework._review_code("def test(): pass", {})
            
            assert review['status'] == 'approved'
    
    def test_generate_documentation(self, framework):
        """Test documentation generation"""
        mock_docs = "# Documentation\n\nThis is test documentation."
        
        framework.user_proxy.chat_messages = {
            framework.doc_agent: [
                {'content': mock_docs}
            ]
        }
        
        with patch.object(framework.user_proxy, 'initiate_chat'):
            result = framework._generate_documentation("code", {})
            
            assert result == mock_docs
            assert "Documentation" in result
    
    def test_generate_tests(self, framework):
        """Test test case generation"""
        mock_tests = "import unittest\n\nclass TestCode(unittest.TestCase):\n    pass"
        
        framework.user_proxy.chat_messages = {
            framework.test_agent: [
                {'content': mock_tests}
            ]
        }
        
        with patch.object(framework.user_proxy, 'initiate_chat'):
            result = framework._generate_tests("code", {})
            
            assert "unittest" in result
            assert "TestCode" in result
    
    def test_generate_deployment(self, framework):
        """Test deployment configuration generation"""
        mock_deploy = "#!/bin/bash\necho 'Deploying...'"
        
        framework.user_proxy.chat_messages = {
            framework.deploy_agent: [
                {'content': mock_deploy}
            ]
        }
        
        with patch.object(framework.user_proxy, 'initiate_chat'):
            result = framework._generate_deployment("code", {})
            
            assert isinstance(result, dict)
            assert 'script' in result
            assert 'timestamp' in result
    
    def test_save_results(self, framework, tmp_path):
        """Test saving results to files"""
        framework.results = {
            'final_code': 'def test(): pass',
            'documentation': '# Docs',
            'tests': 'import unittest',
            'deployment': {'script': '#!/bin/bash'}
        }
        
        output_dir = str(tmp_path / "output")
        framework.save_results(output_dir)
        
        assert os.path.exists(f"{output_dir}/generated_code.py")
        assert os.path.exists(f"{output_dir}/documentation.md")
        assert os.path.exists(f"{output_dir}/test_generated_code.py")
        assert os.path.exists(f"{output_dir}/deploy.sh")
        assert os.path.exists(f"{output_dir}/full_results.json")
    
    def test_process_requirement_integration(self, framework):
        """Integration test for full processing workflow"""
        # Mock all agent responses
        framework.user_proxy.chat_messages = {}
        
        def mock_chat(agent, message):
            agent_name = agent.name
            
            if agent_name == "RequirementAnalyst":
                response = json.dumps({
                    "title": "Calculator",
                    "description": "A calculator",
                    "features": ["add", "subtract"],
                    "constraints": ["Python"],
                    "edge_cases": []
                })
            elif agent_name == "SoftwareDeveloper":
                response = "def add(a, b):\n    return a + b"
            elif agent_name == "CodeReviewer":
                response = json.dumps({
                    "status": "approved",
                    "score": 9
                })
            elif agent_name == "TechnicalWriter":
                response = "# Calculator Documentation"
            elif agent_name == "QAEngineer":
                response = "def test_add():\n    assert add(1, 2) == 3"
            elif agent_name == "DevOpsEngineer":
                response = "#!/bin/bash\necho 'Deploy'"
            else:
                response = "OK"
            
            framework.user_proxy.chat_messages[agent] = [
                {'content': response}
            ]
        
        with patch.object(framework.user_proxy, 'initiate_chat', side_effect=mock_chat):
            results = framework.process_requirement("Create a calculator")
            
            assert 'requirements' in results
            assert 'code' in results
            assert 'review' in results
            assert 'final_code' in results
            assert 'documentation' in results
            assert 'tests' in results
            assert 'deployment' in results
    
    def test_error_handling_no_api_key(self):
        """Test error handling for missing API key"""
        with patch('autogen.AssistantAgent'):
            with patch('autogen.UserProxyAgent'):
                # Should not raise error during init
                framework = MultiAgentFramework(api_key="")
                assert framework.api_key == ""


class TestEdgeCases:
    """Test edge cases and error conditions"""
    
    def test_empty_requirement(self):
        """Test processing empty requirement"""
        with patch('autogen.AssistantAgent'):
            with patch('autogen.UserProxyAgent'):
                framework = MultiAgentFramework(api_key="test")
                
                # Should handle gracefully
                framework.user_proxy.chat_messages = {}
                
                with patch.object(framework.user_proxy, 'initiate_chat'):
                    result = framework._analyze_requirements("")
                    assert isinstance(result, dict)
    
    def test_malformed_json_response(self):
        """Test handling of malformed JSON in agent responses"""
        with patch('autogen.AssistantAgent'):
            with patch('autogen.UserProxyAgent'):
                framework = MultiAgentFramework(api_key="test")
                
                framework.user_proxy.chat_messages = {
                    framework.req_agent: [
                        {'content': '{incomplete json'}
                    ]
                }
                
                with patch.object(framework.user_proxy, 'initiate_chat'):
                    result = framework._analyze_requirements("test")
                    
                    # Should fallback to default structure
                    assert 'title' in result
                    assert 'description' in result
    
    def test_max_review_iterations(self):
        """Test that review doesn't exceed max iterations"""
        with patch('autogen.AssistantAgent'):
            with patch('autogen.UserProxyAgent'):
                framework = MultiAgentFramework(api_key="test")
                
                # Always return needs_revision
                mock_review = {
                    "status": "needs_revision",
                    "score": 5
                }
                
                framework.user_proxy.chat_messages = {
                    framework.review_agent: [
                        {'content': json.dumps(mock_review)}
                    ],
                    framework.coding_agent: [
                        {'content': 'improved code'}
                    ]
                }
                
                with patch.object(framework.user_proxy, 'initiate_chat'):
                    review, code = framework._review_code("code", {}, max_iterations=2)
                    
                    # Should complete after max iterations
                    assert review is not None
                    assert code is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=main", "--cov-report=html"])