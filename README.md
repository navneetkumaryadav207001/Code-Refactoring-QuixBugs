# QuixBugs Benchmark

The following benchmark consists of 40 programs from the Quixey Challenge translated into both Python and Java. Each contains a one-line defect, along with passing (when possible) and failing test cases. Defects fall into one of 14 defect classes. Corrected Python programs are also supplied. QuixBugs is intended for investigating cross-language performance by _multi-lingual_ program repair tools.

## Background: Quixey Challenge
From 2011 to 2013, mobile app search startup Quixey ran a challenge in which programmers were given an implementation of a classic algorithm with a bug on a single line and had one minute to supply a fix. Success entailed $100 and a possible interview. These programs were developed as challenges for humans by people unaware of program repair.

## Usage

All Python is written in Python3.

To run both defective versions of a program against their tests, as well as the corrected Python version, use the test driver:

<h1>🛠️ Debug Agent for QuixBugs</h1>
  <p>We are building a <strong>LangChain + Gemini-based autonomous debugging agent</strong> to automatically fix buggy algorithms in the 
    <a href="https://github.com/jkoppel/QuixBugs">QuixBugs</a> benchmark.
  </p>

  <hr>

  <h2>✅ Progress So Far</h2>

  <h3>Code Updates</h3>
  <ul>
    <li>Fixed bugs in <code>tester.py</code> to make test results consistent and accurate.</li>
    <li>Built <code>debug_agent.py</code>:
      <ul>
        <li>Uses LangChain ReAct framework.</li>
        <li>Connected to Gemini via Google Generative AI API.</li>
        <li>Tools:
          <ul>
            <li>FileReader</li>
            <li>FileWriter</li>
            <li>Executor</li>
            <li>Tester</li>
            <li>PythonDocs</li>
            <li>DuckDuckGoSearch</li>
            <li>(Optional) ErrorAnalyzer</li>
          </ul>
        </li>
      </ul>
    </li>
    <li>Built <code>testall.py</code> to run the agent on all QuixBugs problems.</li>
    <li>Built <code>testerall2.py</code> for batch testing with better logging.</li>
  </ul>

  <hr>

  <h2>🐞 Observations (Day 1)</h2>
  <ul>
    <li>Agent fails for graph problems like <code>bfs</code>, <code>dfs</code> — likely due to missing test cases.</li>
    <li>Infinite loops in some problems like <code>knapsack</code> — no safe exit or timeout.</li>
    <li>Agent is slow due to multiple model calls and tool use.</li>
    <li>No memory module or RAG system yet — limits long-term reasoning.</li>
    <li><code>ErrorAnalyzer</code> tool is unused in current agent loop.</li>
    <li>No confidence estimation or automated retry logic.</li>
  </ul>

  <hr>

  <h2>🐞 Observations (Day 2)</h2>
  <ul>
    <li>Graph based algorithms are working.</li>
    <li>Everything is almost working just need Some refactoring(hehe)</li>
  </ul>
