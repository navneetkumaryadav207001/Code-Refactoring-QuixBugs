import os
import subprocess
import sys
import json
import re



def run_debug_agent(algo_name, logs):
    logs[algo_name] = {"debug_agent": ""}
    result = subprocess.run([sys.executable, "debug_agent.py", algo_name], capture_output=True, text=True)
    logs[algo_name]["debug_agent"] += result.stdout
    if result.stderr:
        logs[algo_name]["debug_agent"] += "\n⚠️ Debug Agent Error:\n" + result.stderr

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

    return f"./test_{algo_name}.py"

def run_pytest(test_file, flag, logs, algo_name):
    flag_key = flag.lstrip('-')
    logs[algo_name][flag_key] = ""
    result = subprocess.run(["pytest", test_file, flag], capture_output=True, text=True)
    logs[algo_name][flag_key] += result.stdout
    if result.stderr:
        logs[algo_name][flag_key] += "\n⚠️ Pytest Error:\n" + result.stderr
    return result.stdout

def count_passed_tests(output):
    passed = 0
    total = 0
    for line in output.splitlines():
        if line.strip().startswith("PASSED"):
            passed += 1
        if "collected" in line and "items" in line:
            try:
                total = int(line.strip().split()[1])
            except:
                pass
        if "== " in line and "passed" in line:
            try:
                parts = line.split()
                passed = int(parts[parts.index("passed") - 1])
                total = int(parts[parts.index("passed") + 1].strip("()"))
            except:
                pass
    return passed, total

def main():
    source_dir = "python_programs"
    fixed_dir = "fixed_programs"

    logs = {}
    total_algos = 0
    passed_algos = 0

    for filename in os.listdir(source_dir):
        if filename.endswith(".py"):
            algo_name = filename[:-3]

            total_algos += 1
            if algo_name == "levenshtein" or algo_name=="knapsack":  # You can comment this line if you want to run these code as well
                print("skipping levenshtein cause it takes way too long to run it.")
                continue

            run_debug_agent(algo_name, logs)

            test_file = create_test_file(algo_name)

            if not len(test_file):
                continue

            fixed_path = os.path.join(fixed_dir, f"{algo_name}.py")
            if not os.path.exists(fixed_path):
                print(f"❌ No fixed file found for {algo_name}")
                continue
            

            
            run_pytest(test_file, "--correct", logs, algo_name)
            output = run_pytest(test_file, "--fixed", logs, algo_name)

            passed, total = count_passed_tests(output)
            print(f"✅ {algo_name}: Fixed version passed {passed}/{total} tests")

            if passed == total and total > 0:
                passed_algos += 1

            os.remove(test_file)

    print(f"\n🎯 Summary: {passed_algos} / {40} algorithms passed all their test cases with the fixed code")

    with open("log3.json", "w") as f:
        json.dump(logs, f, indent=2)

if __name__ == "__main__":
    main()
