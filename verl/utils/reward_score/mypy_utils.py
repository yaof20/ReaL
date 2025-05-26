import tempfile
import mypy.api
import re


def extract_content_in_code_blocks(input: str) -> list[str]:
    # Using regular expression to find content between code blocks ```
    return re.findall(r"```python(.*?)```", input, re.DOTALL)

def add_imports(code):
    IMPORT_HEADER = (
        "from typing import *\n"
    )
    code = code.strip()
    if IMPORT_HEADER not in code:
        code = f"{IMPORT_HEADER}\n{code}"
    return code


def mypy_check(code):
    with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as temp_file:
        temp_file.write(code)
        temp_file_name = temp_file.name

    result, error, exit_code = mypy.api.run([temp_file_name, "--no-color-output", "--strict",])
    
    return result, error, exit_code


def parse_mypy_result(result):
    # Parse the mypy result to extract the number of errors
    lines = result.strip().splitlines()
    last_line = lines[-1]
    # Example: "Found 2 errors in 1 file (checked 1 source file)"
    match = re.search(r'Found (\d+) error', last_line)
    if match:
        error_count = int(match.group(1))
    else:
        error_count = 1
    error_count = max(1, error_count)   # in case of parsing error
    return error_count


def compute_score(solution_str, extra_info=None, eval_mode=False):
    extracted = extract_content_in_code_blocks(solution_str)

    score = None
    if len(extracted) == 0:
        # No code block found
        score = -1
    else:
        code = extracted[-1]
        code = add_imports(code)
        result, error, exit_code = mypy_check(code)
        
        if exit_code == 0:
            # Runnable and no issues
            score = 1
        elif exit_code == 1:
            # Runnable but with issues
            error_count = parse_mypy_result(result)
            score = max(0, 1 - error_count * 0.5)
        else:
            # Not runnable
            score = -0.5
    
    if not eval_mode:
        return score
    else:
        return 1 if score == 1 else 0

if __name__ == "__main__":
    # Example usage
    solution = """
```python
def add(a: int, b):
    return a + b + "123"
```
"""
    extracted = extract_content_in_code_blocks(solution)

    if len(extracted) == 0:
        # No code block found
        print(-1)
    else:
        code = extracted[-1]
        print(code)
        result, error, exit_code = mypy_check(code)
        
        print(f'result: {result}')
        print(f'error: {error}')
        print(f'exit_code: {exit_code}')
        
        if exit_code == 0:
            # Runnable and no issues
            print(1)
        elif exit_code == 1:
            # Runnable but with issues
            error_count = parse_mypy_result(result)
            print(f'error_count: {error_count}')
            print(max(0, 1 - error_count * 0.5))
        else:
            # Not runnable
            print(-0.5)