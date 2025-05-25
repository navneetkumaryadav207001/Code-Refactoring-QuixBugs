import os
import subprocess
import sys
import re

def run_debug_agent(algo_name):
    print(f"\n🚧 Running debug agent for {algo_name}.py")
    result = subprocess.run([sys.executable, "debug_agent.py", algo_name], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("⚠️ Debug Agent Error:\n", result.stderr)

def create_test_file(algo_name):
    file_path = f"python_testcases/test_{algo_name}.py"

    if not os.path.exists(file_path):
        return ""
    with open(file_path, "r") as file:
        content = file.read()

    # Check if `elif pytest.fixed` already exists
    if "elif pytest.fixed" in content:
        print(f"`elif pytest.fixed` already present in {file_path}")
        return file_path

    # Insert elif between if and else
    pattern = rf"(if pytest\.use_correct:\s*\n\s*from correct_python_programs\.{algo_name} import {algo_name})(\s*\n\s*else:\s*\n\s*from python_programs\.{algo_name} import {algo_name})"
    replacement = (
        rf"\1"
        f"\nelif pytest.fixed:\n    from fixed_programs.{algo_name} import {algo_name}"
        rf"\2"
    )

    updated_content, count = re.subn(pattern, replacement, content)

    
    with open(f"./test_{algo_name}.py", "w") as file:
        file.write(updated_content)
    print(f"Patched existing test file: {file_path}")

    return f"./test_{algo_name}.py"

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
            algo_name = filename[:-3]  # remove .py\

            run_debug_agent(algo_name)

            fixed_path = os.path.join(fixed_dir, f"{algo_name}.py")
            if not os.path.exists(fixed_path):
                print(f"❌ No fixed file found for {algo_name}")
                continue
            

            test_file = create_test_file(algo_name)

            if not len(test_file):
                print(f'Test file doesnt Extst for {algo_name}')
                continue
            # Run against correct version
            run_pytest(test_file, "--correct")

            # Run against fixed version
            run_pytest(test_file, "--fixed")

            # Optionally delete test file
            os.remove(test_file)

if __name__ == "__main__":
    main()
