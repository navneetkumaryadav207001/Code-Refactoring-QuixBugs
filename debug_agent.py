import sys
import os
import subprocess
import json
import copy
from pathlib import Path
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
import re
# Set up API key
os.environ["GOOGLE_API_KEY"] = "AIzaSyDmRdVGppLT6FBq3ouKzk1YCxWNdAQTx0s"

class PythonDebugAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-001")
        self.search_tool = DuckDuckGoSearchRun()
        self.setup_agent()
        
    def setup_agent(self):
        """Initialize the ReAct agent with debugging tools"""
        tools = [
            self.search_tool,
            self.read_file_tool,
            self.write_file_tool,
            self.run_code_tool,
            #self.analyze_error_tool,
            self.get_python_docs_tool,
            self.test_algorithm
        ]
        
        prompt = hub.pull("hwchase17/react")
        
        self.agent = create_react_agent(
            llm=self.llm,
            tools=tools,
            prompt=prompt
        )
        
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=tools,
            verbose=True,
            max_iterations=10,
            handle_parsing_errors=True
        )
    
    @tool
    def read_file_tool(self, filepath: str) -> str:
        """Read the contents of a Python file"""
        try:
            with open(filepath, 'r') as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {str(e)}"
    
    @tool
    def write_file_tool(content: str) -> str:
        """Write content to a Python file, stripping code fences and language tags"""
        filepath = f"fixed_programs/{sys.argv[1]}.py"
        try:
            # Extract code inside markdown code fences (```), removing language tags
            # Pattern matches ```python\n ...code... \n```
            code_match = re.search(r"```(?:python)?\n(.*?)```", content, re.DOTALL | re.IGNORECASE)
            if code_match:
                code = code_match.group(1)
            else:
                # If no code fences found, write content as is
                code = content

            # Ensure directory exists
            os.makedirs(os.path.dirname(filepath), exist_ok=True)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(code.strip() + '\n')  # Strip leading/trailing spaces and add newline

            return f"Successfully wrote to {filepath}"
        except Exception as e:
            return f"Error writing file: {str(e)}"
    
    @tool
    def run_code_tool(self, code: str) -> str:
        """Execute Python code and return the result or error"""
        try:
            # Create a temporary file to run the code
            temp_file = "temp_debug.py"
            with open(temp_file, 'w') as f:
                f.write(code)
            
            result = subprocess.run([sys.executable, temp_file], 
                                  capture_output=True, text=True, timeout=10)
            
            os.remove(temp_file)
            
            if result.returncode == 0:
                return f"Success: {result.stdout}"
            else:
                return f"Error: {result.stderr}"
        except subprocess.TimeoutExpired:
            return "Error: Code execution timed out"
        except Exception as e:
            return f"Error running code: {str(e)}"
    
    @tool
    def analyze_error_tool(self, error_message: str) -> str:
        """Analyze Python error messages and suggest fixes"""
        error_patterns = {
            "SyntaxError": "Check for missing colons, parentheses, or incorrect indentation",
            "IndentationError": "Fix indentation - use consistent spaces or tabs",
            "NameError": "Variable or function not defined - check spelling and scope",
            "TypeError": "Check data types and function arguments",
            "IndexError": "Array/list index out of bounds - check array length",
            "KeyError": "Dictionary key doesn't exist - check key spelling",
            "AttributeError": "Object doesn't have the specified attribute or method",
            "ValueError": "Incorrect value passed to function",
            "ZeroDivisionError": "Division by zero - add zero check",
            "ImportError": "Module not found or import statement incorrect"
        }
        
        for error_type, suggestion in error_patterns.items():
            if error_type in error_message:
                return f"Error type: {error_type}. Suggestion: {suggestion}"
        
        return f"General error analysis: {error_message}"
    
    @tool
    def get_python_docs_tool(self, topic: str) -> str:
        """Search for Python documentation on a specific topic"""
        try:
            search_query = f"Python {topic} documentation site:docs.python.org"
            return self.search_tool.run(search_query)
        except Exception as e:
            return f"Error searching documentation: {str(e)}"

    @tool
    def test_algorithm() -> str:
        """Test the algorithm using the provided tester"""
        algo_name = sys.argv[1]
        try:
            result = subprocess.run([sys.executable, "tester.py", algo_name], 
                                  capture_output=True, text=True, timeout=30)
            return result.stdout + result.stderr
        except Exception as e:
            return f"Error testing algorithm: {str(e)}"

    def fix_algorithm(self, algo_name: str):
        """Main method to fix an algorithm"""
        try:
            # Construct file paths
            buggy_file = f"python_programs/{algo_name}.py"
            fixed_file = f"fixed_programs/{algo_name}.py"
            
            # Check if files exist
            if not os.path.exists(buggy_file):
                print(f"Error: {buggy_file} not found")
                return False
            
            # Create fixed_programs directory if it doesn't exist
            os.makedirs("fixed_programs", exist_ok=True)
            
            # Read the buggy code
            with open(buggy_file, 'r') as f:
                buggy_code = f.read()
            
            print(f"Original buggy code from {buggy_file}:")
            print(buggy_code)
            print("-" * 50)
            
            # Test the original code to see what errors occur
            print("Testing original code...")
            test_result = self.test_algorithm(algo_name)
            print("Test result:")
            print(test_result)
            print("-" * 50)
            
            # Use the agent to fix the code
            fix_prompt = f"""
            I need to fix a Python algorithm with bugs. Here's the information:
            
            Algorithm name: {algo_name}
            Buggy code:
            ```python
            {buggy_code}
            ```
            
            Test results showing the errors:
            ```
            {test_result}
            ```
            
            Please analyze the code, identify the bugs,check the solution online and provide the corrected version. 
            The fixed code should:
            1. Maintain the same function name and structure
            2. Fix any syntax, logic, or runtime errors
            3. Handle edge cases appropriately
            4. Follow Python best practices
            
            Use the available tools to:
            1. Analyze the error messages
            2. Search for Python documentation or StackOverFlow if needed
            3. Test code snippets using test_algorithm tool
            4. Write the final fixed

            do not use backticks while write the file:
            example:
            Action: write_file_tool # is correct
            but
            Action: `write_file_tool` is not 
            you can use it for action input though
            """
            
            response = self.agent_executor.invoke({"input": fix_prompt})
            
            print("Agent response:")
            print(response['output'])
            
            # Verify the fix worked by testing again
            if os.path.exists(fixed_file):
                print("\nTesting fixed code...")
                fixed_test_result = self.test_algorithm(algo_name)
                print("Fixed code test result:")
                print(fixed_test_result)
                
                return True
            else:
                print("Error: Fixed file was not created")
                return False
                
        except Exception as e:
            print(f"Error in fix_algorithm: {str(e)}")
            return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python debug_agent.py <algorithm_name>")
        sys.exit(1)
    
    algo_name = sys.argv[1]
    
    print(f"Starting Python Debug Agent for algorithm: {algo_name}")
    print("=" * 60)
    
    agent = PythonDebugAgent()
    success = agent.fix_algorithm(algo_name)
    
    if success:
        print(f"\n✅ Successfully fixed {algo_name}.py")
        print(f"Fixed code saved to: fixed_programs/{algo_name}.py")
    else:
            print(f"\n❌ Failed to fix {algo_name}.py")

if __name__ == "__main__":
    main()