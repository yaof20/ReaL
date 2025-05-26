import os
import random
import re
import json
import subprocess
import tempfile

from .mypy_utils import compute_score as mypy_compute_score

run_template_class = (
    "from typing import *\n"
    "import collections\n"
    "import math\n"
    "import heapq\n"
    "from collections import Counter\n"
    "from math import ceil\n"
    "{CODE}\n"
    "assert Solution().{FUNCTION}({INPUT}) == {OUTPUT}, Solution().{FUNCTION}({INPUT})"
)

run_template_function = (
    "from typing import *\n"
    "import collections\n"
    "import math\n"
    "import heapq\n"
    "from collections import Counter\n"
    "from math import ceil\n"
    "{CODE}\n"
    "assert {FUNCTION}({INPUT}) == {OUTPUT}, {FUNCTION}({INPUT})"
)

run_template_dict = {
    'class': run_template_class,
    'function': run_template_function
}


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


def parse_assertion_error(error_message):
    if "AssertionError" in error_message:
        # Extract the expected value after the assert error
        match_res = re.search(r"AssertionError: (.*)", error_message)
        if match_res:
            return match_res.group(1).strip()
        return None
    else:
        # Handle other types of errors if necessary
        return None


def run_program(code, program_type, input_var, output_var, fn_name, timeout=10):
    program = run_template_dict[program_type].format(
        CODE=code,
        FUNCTION=fn_name,
        INPUT=', '.join(map(repr, input_var)),
        OUTPUT=repr(output_var)
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
                timeout=timeout,
                
                env=env,
                cwd=tmp_dir
            )
            
            # stdout = result.stdout
            stderr = result.stderr
            
            if stderr:
                actual_outputs = parse_assertion_error(stderr)
                if actual_outputs:
                    ret = 'fail', f"Expected: {output_var}, but got: {actual_outputs.strip()}"
                else:
                    ret = 'error', f"Error in execution: {stderr.strip()}"
            else:
                ret = 'pass', "Success"
                
            if random.randint(0, 1000) == 0:
                print('[DEBUG] Running the program:')
                print("=" * 50)
                print(program)
                print("-" * 50)
                print("Result:", ret)
                print("=" * 50)
                
            return ret
        
        except subprocess.TimeoutExpired:
            if random.randint(0, 1000) == 0:
                print('[DEBUG] Timeout expired while executing the program.')
                print("=" * 50)
                print(program)
                print("=" * 50)
            return 'skip', "Timeout expired"
        except Exception as e:
            print(f'[DEBUG] Encountered: "{e}" while executing the program.')
            return 'skip', str(e)
        

def compute_score(solution_str, extra_info=None, max_test_cases=5, eval_mode=False, continuous=True):
    extracted = extract_content_in_code_blocks(solution_str)

    score = None
    if len(extracted) == 0:
        # No code block found
        score = -1
    else:
        code = extracted[-1]
        
        test_info = json.loads(extra_info['test_info'])
        fn_name = test_info['fn_name']
        program_type = extra_info['program_type']
        
        res2score = {
            'pass': 1,
            'skip': 0.1,    # wierd errors or timeout (we actually don't know if it is correct)
            'fail': 0,
            'error': -0.5
        }
        
        score_list = []
        for input_var, output_var in zip(test_info['inputs'], test_info['outputs']):
            result_tag, message = run_program(code, program_type, input_var, output_var, fn_name)
            score = res2score[result_tag]
            score_list.append(score)
            
            if len(score_list) >= max_test_cases:
                break
            
        if len(score_list) == 0:
            score = 0   # shouldn't happen, but just in case
        else:
            score = sum(score_list) / len(score_list)
    
    if eval_mode:
        if score == 1:
            return 1
        else:
            return 0
    else:
        if continuous:
            return score
        else:
            # hard mode
            if score == -1:
                return -1
            if score == 1:
                return 1
            return 0


def compute_score_with_mypy_typecheck(solution_str, extra_info=None, max_test_cases=5, mypy_ratio=0.5, eval_mode=False):
    correctness_score = compute_score(solution_str, 
                                      extra_info=extra_info, 
                                      max_test_cases=max_test_cases, 
                                      eval_mode=eval_mode, 
                                      continuous=True)
    
    mypy_score = mypy_compute_score(solution_str,
                                    extra_info=extra_info, 
                                    eval_mode=eval_mode)
    
    return mypy_ratio * mypy_score + (1 - mypy_ratio) * correctness_score



if __name__ == "__main__":
    # Example usage
    solution_str = """
```python
def add(a, b):
    return a + b
```
"""
    
    extra_info = {
        'test_info': json.dumps({
            'fn_name': 'add',
            'inputs': [[1, 2], [3, 4]],
            'outputs': [3, 7]
        }),
        'program_type': 'function'
    }
    
    score = compute_score(solution_str, extra_info=extra_info)
    print(f"Computed score: {score}")