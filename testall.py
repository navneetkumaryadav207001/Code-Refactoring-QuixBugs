import os
import subprocess
import sys

def run_debug_agent(algo_name):
    print(f"\n🚧 Running debug agent for {algo_name}.py")
    result = subprocess.run([sys.executable, "debug_agent.py", algo_name], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("⚠️ Debug Agent Error:\n", result.stderr)

def create_test_file(algo_name):
    test_code = f'''
import pytest
from python_testcases.load_testdata import load_json_testcases

if pytest.use_correct:
    from correct_python_programs.{algo_name} import {algo_name}
elif pytest.fixed:
    from fixed_programs.{algo_name} import {algo_name}
else:
    from python_programs.{algo_name} import {algo_name}

testdata = load_json_testcases({algo_name}.__name__)

@pytest.mark.parametrize("input_data,expected", testdata)
def test_{algo_name}(input_data, expected):
    assert {algo_name}(*input_data) == expected
'''
    test_file_path = f"test_{algo_name}.py"
    with open(test_file_path, "w") as f:
        f.write(test_code)
    return test_file_path

def run_pytest(test_file, flag):
    print(f"\n🧪 Running pytest {flag} for {test_file}")
    result = subprocess.run(["pytest", test_file, flag], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("⚠️ Pytest Error:\n", result.stderr)

def main():
    source_dir = "python_programs"
    fixed_dir = "fixed_programs"
    correct_dir = "correct_python_programs"

    for filename in os.listdir(source_dir):
        if filename.endswith(".py"):
            algo_name = filename[:-3]  # remove .py

            run_debug_agent(algo_name)

            fixed_path = os.path.join(fixed_dir, f"{algo_name}.py")
            if not os.path.exists(fixed_path):
                print(f"❌ No fixed file found for {algo_name}")
                continue

            test_file = create_test_file(algo_name)

            # Run against correct version
            run_pytest(test_file, "--correct")

            # Run against fixed version
            run_pytest(test_file, "--fixed")

            # Optionally delete test file
            os.remove(test_file)

if __name__ == "__main__":
    main()
