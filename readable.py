import json
import re

# ANSI escape sequence remover
def remove_ansi_codes(text):
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)

# Format debug log text into Markdown
def format_debug_to_markdown(data):
    markdown_output = []

    for key, value in data.items():
        markdown_output.append(f"# Debug Info: `{key}`\n")
        if "debug_agent" in value:
            raw_text = value["debug_agent"]
            cleaned = remove_ansi_codes(raw_text)

            # No need to decode again — JSON decoding already handled \n, \u, etc.
            sections = cleaned.split('\n--------------------------------------------------\n')
            for section in sections:
                markdown_output.append("```\n" + section.strip() + "\n```\n")

    return "\n".join(markdown_output)


# ---- Main Execution ----
input_file = "log3.json"   # Your input filename
output_file = "debug_output.md" # Your output filename

# Read from file
with open(input_file, "r", encoding="utf-8") as f:
    json_content = f.read()

# Convert to Markdown
try:
    data = json.loads(json_content)
    markdown = format_debug_to_markdown(data)

    # Write to Markdown file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(markdown)

    print(f"✅ Converted debug info saved to: {output_file}")
except json.JSONDecodeError as e:
    print("❌ JSON Decode Error:", e)
