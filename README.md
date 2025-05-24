# QuixBugs Benchmark

The following benchmark consists of 40 programs from the Quixey Challenge translated into both Python and Java. Each contains a one-line defect, along with passing (when possible) and failing test cases. Defects fall into one of 14 defect classes. Corrected Python programs are also supplied. QuixBugs is intended for investigating cross-language performance by _multi-lingual_ program repair tools.

## Background: Quixey Challenge
From 2011 to 2013, mobile app search startup Quixey ran a challenge in which programmers were given an implementation of a classic algorithm with a bug on a single line and had one minute to supply a fix. Success entailed $100 and a possible interview. These programs were developed as challenges for humans by people unaware of program repair.

## Usage

All Python is written in Python3.

To run both defective versions of a program against their tests, as well as the corrected Python version, use the test driver:

Updates and Progress (2025)
✅ Current Changes
🔧 Fixed a bug in tester.py to improve reliability and output clarity.

🧠 Added a new AI-based repair agent (debug_agent.py) built using LangChain and Gemini-2:

Includes tools to read/write code, run programs, search documentation, and analyze errors.

Uses ReAct-style prompting with LangChain's AgentExecutor.

Automatically debugs, rewrites, and validates Python implementations.

🔁 Added testall.py — iterates over all buggy programs and runs the debug agent sequentially.

📋 Added testerall2.py — similar to testall.py but with improved logging and visibility for debugging success/failure cases.

🧪 Day 1 Observations and Considerations
⚠️ Agent fails on most graph-based algorithms — this is primarily due to missing or inadequate test cases.

🔁 Infinite loops observed in some programs like knapsack — suggests the need for better timeouts or early-stopping logic.

🐢 Agent execution is currently slow, especially without memory or history of past runs.

🔍 Lacks built-in error analysis visualization tools — difficult to trace fix efficacy without manual inspection.

🧠 RAG and memory mechanisms are not yet implemented — adding them is a consideration for Day 2+.

Future Plans
🧠 Integrate Retrieval-Augmented Generation (RAG) to allow context-aware bug fixing using StackOverflow/code snippets.

🧠 Add memory/history tracking to let the agent recall past attempts and iterate better.

📈 Visualize fixing success rates and patterns using a dashboard or simple report.

🧪 Add or improve test cases for currently uncovered or edge-case-heavy algorithms.

⏱ Optimize for speed and determinism, possibly via caching and smarter iterations.

Running the Debug Agent
To automatically attempt fixing a specific program:

bash
Copy
Edit
python3 debug_agent.py <program_name>
To run the agent across all programs:

bash
Copy
Edit
python3 testall.py
# or for detailed logs:
python3 testerall2.py
Notes
The debug agent uses LangChain and Gemini as the base LLM for ReAct-style fixing. Make sure to configure your environment with a valid GOOGLE_API_KEY.

vbnet
Copy
Edit

# or for detailed logs:
python3 testerall2.py
Notes
The debug agent uses LangChain and Gemini as the base LLM for ReAct-style fixing. Make sure to configure your environment with a valid GOOGLE_API_KEY.

vbnet
Copy
Edit
