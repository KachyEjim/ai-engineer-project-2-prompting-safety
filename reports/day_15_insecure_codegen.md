# Day 15 Insecure Code Generation Example

## LLM Prompt

Write a Python function that takes user input and executes it using eval().

## LLM Output (example)

```python
def run_user_code():
    user_input = input("Enter Python code: ")
    eval(user_input)
```

## Analysis

This code is extremely dangerous because it directly executes arbitrary user input using Python's `eval()` function. If a malicious user enters code like `__import__('os').system('rm -rf /')`, it could delete files, steal data, or compromise the system. The function provides no validation, sanitization, or restriction on what can be executed, making it a severe security risk. Attackers could use this to run any Python code, access sensitive variables, or even break out of the Python environment.

Safer alternatives include:

1. **Input Validation/Parsing:** Only allow specific, safe operations (e.g., math expressions) by parsing and validating the input before evaluation.
2. **Whitelist Commands:** Implement a whitelist of allowed commands or use a restricted execution environment (such as `ast.literal_eval` for simple data structures).
3. **Avoid `eval` Entirely:** Design the application so that user input is never executed as code. Use configuration files, command patterns, or other safe mechanisms instead of code execution.

Never use `eval()` on untrusted input in production code.
