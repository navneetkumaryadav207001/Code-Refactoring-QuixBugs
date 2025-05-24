# QuixBugs Benchmark

The following benchmark consists of 40 programs from the Quixey Challenge translated into both Python and Java. Each contains a one-line defect, along with passing (when possible) and failing test cases. Defects fall into one of 14 defect classes. Corrected Python programs are also supplied. QuixBugs is intended for investigating cross-language performance by _multi-lingual_ program repair tools.

## Background: Quixey Challenge
From 2011 to 2013, mobile app search startup Quixey ran a challenge in which programmers were given an implementation of a classic algorithm with a bug on a single line and had one minute to supply a fix. Success entailed $100 and a possible interview. These programs were developed as challenges for humans by people unaware of program repair.

## Usage

All Python is written in Python3.

To run both defective versions of a program against their tests, as well as the corrected Python version, use the test driver:

🛠️ Current Progress: Debug Agent for QuixBugs
We are currently building a LangChain-based autonomous debugging agent to automatically fix buggy algorithms in the QuixBugs benchmark.

✅ Changes Made So Far
Fixed a bug in tester.py to ensure accurate and consistent results when testing the algorithms.

Developed debug_agent.py:

Uses LangChain + Gemini (Google Generative AI) with the ReAct paradigm.

Equipped with tools for:

File reading and writing

Code execution

Algorithm testing

Python docs and DuckDuckGo search

(Optional) Error analysis tools

Built testall.py:

Automatically iterates over all buggy programs and invokes the debug agent on each.

Built testerall2.py:

Enhanced logging and testing for batch evaluation.

🐞 Day 1 Observations & Known Limitations
❌ The agent fails for all graph-based algorithms (e.g., BFS, DFS) due to lack of test coverage.

🔁 Algorithms like Knapsack enter an infinite loop; termination conditions need stricter handling.

🐢 Agent is very slow, especially when invoking search tools or running multiple iterations.

❌ No RAG (Retrieval-Augmented Generation) or memory module yet. Will be added on Day 2.

❌ Error analysis tool exists but not actively used in current agent loop.

⚠️ No model-based validation or confidence metrics implemented.

🚀 Planned Improvements
For Day 2:
Add memory (LangChain Memory or custom implementation).

Integrate a RAG system to fetch relevant bug fixes/code patterns dynamically.

Use error pattern analysis to improve early diagnosis.

Add graph algorithm testcases to tester.py.

Build a performance dashboard for agent benchmarking.

🧪 Quick Start: Running the Debug Agent
bash
Copy
Edit
# Fix a specific algorithm
python debug_agent.py <algorithm_name>

# Run the agent over all QuixBugs programs
python testall.py

# Test all original/fixed programs with enhanced logging
python testerall2.py

Copy
Edit
