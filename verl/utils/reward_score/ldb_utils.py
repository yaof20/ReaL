import os
import re
import json
import subprocess
import ast
import tempfile
import astunparse


def clean_code(code):
    code_lines = code.split('\n')
    cleaned_code_lines = []
    for line in code_lines:
        if line.startswith('assert'):
            continue
        if line.startswith('print'):
            continue
        cleaned_code_lines.append(line)
    return '\n'.join(cleaned_code_lines)


def extract_content_in_code_blocks(input: str) -> list[str]:
    # Using regular expression to find content between code blocks ```
    re_res = re.findall(r"```python(.*?)```", input, re.DOTALL)
    return [clean_code(res) for res in re_res]

def add_imports(code):
    IMPORT_HEADER = (
        "from typing import *\n"
        "import math\n"
        "from heapq import *\n"
        "import itertools\n"
        "import re\n"
        "import typing\n"
        "import heapq\n"
        "_str=str\n"
        "import re\n"    
    )
    code = code.strip()
    if IMPORT_HEADER not in code:
        code = f"{IMPORT_HEADER}\n{code}"
    return code

def eval_hidden_test(code, test_info):
    entry_point = test_info["entry_point"]
    hidden_test = test_info["hidden_test"]
    
    template = (
        "{CODE}\n"
        "\n"
        "{TEST_STR}\n"
        "check({ENTRY_POINT})"
    )
    program = template.format(
        CODE=add_imports(code),
        TEST_STR=hidden_test,
        ENTRY_POINT=entry_point
    )
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        env = os.environ.copy()
        env["TMPDIR"] = tmp_dir
        
        try:
            result = subprocess.run(
                ["python", "-c", program],  # Run the script string as a command
                input=None,
                text=True,
                capture_output=True,
                timeout=10,
                env=env,
                cwd=tmp_dir
            )
            stderr = result.stderr
            if stderr:
                return False, f"Error: {str(stderr)}"
            else:
                return True, 'All tests passed'
        except subprocess.TimeoutExpired:
            return False, "Timeout expired"
        except Exception as e:
            return False, f"Error: {str(e)}"

def get_call_str_from_test(assert_statement: str) -> str:
    ast_parsed = ast.parse(assert_statement)
    try:
        call_str = ast_parsed.body[0].test.left # type: ignore
    except:
        call_str = ast_parsed.body[0].test # type: ignore

    return astunparse.unparse(call_str).strip()

def eval_visible_test(code, test_info):
    entry_point = test_info["entry_point"]
    
    visible_tests = test_info["visible_test"]
    # sanity check
    if entry_point is not None:
        # acecode doesn't explitly specify the entry point
        visible_tests = [test for test in visible_tests if entry_point in test and 'assert False' not in test]
    
    success_tests = []
    failed_tests = []
    is_passing = True
    
    eval_template = (
        "{CODE}\n"
        "\n"
        "{TEST_STR}"
    )
    func_call_template = (
        "{CODE}\n"
        "\n"
        "print(repr({FUNC_CALL}))"
    )
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        env = os.environ.copy()
        env["TMPDIR"] = tmp_dir
        
        for i, test_str in enumerate(visible_tests):
            program = eval_template.format(
                CODE=add_imports(code),
                TEST_STR=test_str
            )
            
            try:
                result = subprocess.run(
                    ["python", "-c", program],
                    input=None,
                    text=True,
                    capture_output=True,
                    timeout=5,
                    
                    env=env,
                    cwd=tmp_dir
                )
                stderr = result.stderr
                
                if stderr:
                    func_call = get_call_str_from_test(test_str)
                    func_call_program = func_call_template.format(
                        CODE=add_imports(code),
                        FUNC_CALL=func_call
                    )
                    
                    func_call_result = subprocess.run(
                        ["python", "-c", func_call_program],
                        input=None,
                        text=True,
                        capture_output=True,
                        timeout=5,
                        
                        env=env,
                        cwd=tmp_dir
                    )
                    
                    func_call_stderr = func_call_result.stderr
                    
                    if not func_call_stderr:
                        func_call_stdout = func_call_result.stdout                
                        func_call_stdout = eval(func_call_stdout.strip())
                        
                        actual_output = func_call_stdout
                        is_passing = False
                        failed_tests.append(f"{test_str} # But Actual Execution Output: {actual_output}")
                    else:
                        is_passing = False
                        failed_tests.append(f"{test_str} # Error: {str(stderr).strip()}")
                else:
                    is_passing = True
                    success_tests.append(test_str)
                
            except subprocess.TimeoutExpired:
                is_passing = False
                failed_tests.append(f"{test_str} # Timeout expired")
            except Exception as e:
                is_passing = False
                failed_tests.append(f"{test_str} # Error: {str(e).strip()}")
            
    return is_passing, success_tests, failed_tests


def compute_score(solution_str, extra_info=None, eval_mode=True):
    assert eval_mode, "LDB should only be used in eval mode"
    extracted = extract_content_in_code_blocks(solution_str)

    if len(extracted) == 0:
        # No code block found
        return 0
    else:
        code = extracted[-1]
        # during evaluation, we only use the hidden test
        test_info = extra_info['test_info']
        is_solved, feedback = eval_hidden_test(code=code, test_info=test_info)
        return 1 if is_solved else 0

        



if __name__ == '__main__':
    # example = json.load(open('/home/ziw049/Projects_ds-serv8/verl/data/ldb-humaneval/humaneval-correctness/example.json'))
    
    # code = (
    #     f'{example["extra_info"]["starter_code"]}\n'
    #     f'{example["reward_model"]["ground_truth"]}'
    # )
    # print(code)
    
    code = \
"""
from typing import List
from typing import Union

def has_close_elements(numbers: List[float], threshold: float) -> bool:
    # Check if all numbers are list-like
    if not all(isinstance(num, (list, tuple)) for num in numbers):
        raise TypeError("All elements in the list must be either of type list or tuple.")
    
    # Get all unique numbers and sort them
    unique_numbers = sorted(set(numbers))
    
    # Check if the absolute difference between any two numbers is less than the threshold
    for i in range(len(unique_numbers) - 1):
        if abs(unique_numbers[i] - unique_numbers[i + 1]) < threshold:
            return True
    
    return False

# Test cases
assert has_close_elements([1.0, 2.0, 3.0], 0.5) == False
assert has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3) == True
print("All test cases passed!")
"""
    
    # test_info = example["extra_info"]["test_info"]
    
    # print(eval_hidden_test(code=code, test_info=test_info))
    # print(eval_visible_test(code=code, test_info=test_info))
    print(clean_code(code))
