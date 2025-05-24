import os
import subprocess
import sys
import json

def run_debug_agent(algo_name, logs):
    logs[algo_name] = {"debug_agent": ""}
    result = subprocess.run([sys.executable, "debug_agent.py", algo_name], capture_output=True, text=True)
    logs[algo_name]["debug_agent"] += result.stdout
    if result.stderr:
        logs[algo_name]["debug_agent"] += "\n⚠️ Debug Agent Error:\n" + result.stderr

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

            run_debug_agent(algo_name, logs)

            fixed_path = os.path.join(fixed_dir, f"{algo_name}.py")
            if not os.path.exists(fixed_path):
                print(f"❌ No fixed file found for {algo_name}")
                continue

            test_file = create_test_file(algo_name)

            run_pytest(test_file, "--correct", logs, algo_name)
            output = run_pytest(test_file, "--fixed", logs, algo_name)

            passed, total = count_passed_tests(output)
            print(f"✅ {algo_name}: Fixed version passed {passed}/{total} tests")

            if passed == total and total > 0:
                passed_algos += 1

            os.remove(test_file)

    print(f"\n🎯 Summary: {passed_algos} / {total_algos} algorithms passed all their test cases with the fixed code")

    with open("log.json", "w") as f:
        json.dump(logs, f, indent=2)

if __name__ == "__main__":
    main()
