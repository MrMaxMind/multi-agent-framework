"""
Simple example demonstrating the Multi-Agentic Framework

This example shows how to:
1. Initialize the framework
2. Process a requirement
3. Access results
4. Save outputs
"""

import os
import sys
from pathlib import Path

# Add parent directory to path to import main module
sys.path.append(str(Path(__file__).parent.parent))

from main import MultiAgentFramework


def example_1_calculator():
    """Example 1: Generate a calculator application"""
    print("=" * 60)
    print("Example 1: Calculator Application")
    print("=" * 60)
    
    # Get API key from environment
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("Error: GROQ_API_KEY not set")
        print("Please set it: export GROQ_API_KEY=your_key")
        return
    
    # Initialize framework
    print("\n[1/3] Initializing framework...")
    framework = MultiAgentFramework(api_key=api_key)
    
    # Define requirement
    requirement = """
    Create a calculator application that can:
    - Perform basic arithmetic operations (add, subtract, multiply, divide)
    - Handle division by zero errors
    - Validate input types
    - Provide a simple command-line interface
    - Include a help function
    """
    
    print("\n[2/3] Processing requirement...")
    print(f"Requirement: {requirement[:80]}...")
    
    try:
        # Process requirement
        results = framework.process_requirement(requirement)
        
        # Display results summary
        print("\n[3/3] Results:")
        print(f"✓ Requirements analyzed: {results['requirements']['title']}")
        print(f"✓ Code generated: {len(results.get('final_code', ''))} characters")
        print(f"✓ Code review score: {results['review'].get('score', 'N/A')}/10")
        print(f"✓ Documentation: {len(results.get('documentation', ''))} characters")
        print(f"✓ Test cases: {len(results.get('tests', ''))} characters")
        
        # Save results
        output_dir = "output/calculator"
        framework.save_results(output_dir)
        print(f"\n✓ All files saved to {output_dir}/")
        
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")


def example_2_todo_list():
    """Example 2: Generate a todo list application"""
    print("\n" + "=" * 60)
    print("Example 2: Todo List Application")
    print("=" * 60)
    
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("Error: GROQ_API_KEY not set")
        return
    
    print("\n[1/3] Initializing framework...")
    framework = MultiAgentFramework(api_key=api_key)
    
    requirement = """
    Build a command-line todo list manager with these features:
    - Add new tasks with descriptions and priorities
    - Mark tasks as complete
    - List all tasks (with filtering by status)
    - Delete tasks
    - Persist tasks to a JSON file
    - Load tasks on startup
    """
    
    print("\n[2/3] Processing requirement...")
    print(f"Requirement: {requirement[:80]}...")
    
    try:
        results = framework.process_requirement(requirement)
        
        print("\n[3/3] Results:")
        print(f"✓ Project: {results['requirements']['title']}")
        print(f"✓ Features: {len(results['requirements']['features'])} identified")
        print(f"✓ Review: {results['review'].get('status', 'unknown').upper()}")
        
        output_dir = "output/todo_list"
        framework.save_results(output_dir)
        print(f"\n✓ Files saved to {output_dir}/")
        
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")


def example_3_data_processor():
    """Example 3: Generate a data processing script"""
    print("\n" + "=" * 60)
    print("Example 3: CSV Data Processor")
    print("=" * 60)
    
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("Error: GROQ_API_KEY not set")
        return
    
    print("\n[1/3] Initializing framework...")
    framework = MultiAgentFramework(api_key=api_key)
    
    requirement = """
    Create a CSV data processor that can:
    - Read CSV files with error handling
    - Calculate statistics (mean, median, mode, std dev)
    - Handle missing values
    - Generate a summary report
    - Export results to JSON
    - Support command-line arguments for file paths
    """
    
    print("\n[2/3] Processing requirement...")
    
    try:
        results = framework.process_requirement(requirement)
        
        print("\n[3/3] Results:")
        print(f"✓ Generated: {results['requirements']['title']}")
        
        # Show some code review findings
        if 'findings' in results['review']:
            print("\nCode Review Findings:")
            for finding in results['review']['findings'][:3]:
                icon = "✓" if finding['type'] == 'success' else "ℹ"
                print(f"  {icon} {finding['message']}")
        
        output_dir = "output/data_processor"
        framework.save_results(output_dir)
        print(f"\n✓ Complete package saved to {output_dir}/")
        
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")


def example_4_custom_config():
    """Example 4: Using custom configuration"""
    print("\n" + "=" * 60)
    print("Example 4: Custom Configuration")
    print("=" * 60)
    
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("Error: GROQ_API_KEY not set")
        return
    
    print("\n[1/2] Initializing with custom model...")
    
    # Use a different model
    framework = MultiAgentFramework(
        api_key=api_key,
        model="mixtral-8x7b-32768"  # Alternative model
    )
    
    requirement = "Create a simple password generator with customizable length"
    
    print("\n[2/2] Processing...")
    
    try:
        results = framework.process_requirement(requirement)
        print(f"✓ Generated with model: mixtral-8x7b-32768")
        print(f"✓ Code review: {results['review'].get('score', 'N/A')}/10")
        
    except Exception as e:
        print(f"✗ Error: {str(e)}")


def main():
    """Run all examples"""
    print("\n" + "=" * 60)
    print("Multi-Agentic Framework - Examples")
    print("=" * 60)
    
    # Check for API key
    if not os.getenv("GROQ_API_KEY"):
        print("\n⚠ Warning: GROQ_API_KEY not set!")
        print("Please set it before running examples:")
        print("  export GROQ_API_KEY=your_key_here")
        return
    
    # Menu
    print("\nAvailable examples:")
    print("1. Calculator Application")
    print("2. Todo List Manager")
    print("3. CSV Data Processor")
    print("4. Custom Configuration")
    print("5. Run all examples")
    print("0. Exit")
    
    choice = input("\nSelect example (0-5): ").strip()
    
    if choice == "1":
        example_1_calculator()
    elif choice == "2":
        example_2_todo_list()
    elif choice == "3":
        example_3_data_processor()
    elif choice == "4":
        example_4_custom_config()
    elif choice == "5":
        example_1_calculator()
        example_2_todo_list()
        example_3_data_processor()
        example_4_custom_config()
    elif choice == "0":
        print("Exiting...")
    else:
        print("Invalid choice")
    
    print("\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()