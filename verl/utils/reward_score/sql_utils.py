import subprocess
import tempfile
import shutil
import random
import os
import re
from typing import Tuple

from verl.utils.reward_score.sql_injection import compute_score_security_dynamic, compute_score_security_static


def detect_input_prompts(code: str) -> list[str]:
    """
    Detect all input prompts in a Python code string.
    
    Args:
        code (str): Python code string to analyze
        
    Returns:
        list[str]: List of input prompts found in the code
    """
    prompts = []
    
    # Find all input() calls with any string content
    input_pattern = r'(?<![a-zA-Z0-9_])input\(([\'"])(.*?)(?<!\\)\1\)'
    matches = re.finditer(input_pattern, code)
    
    for match in matches:
        prompts.append(match.group(2))
        
    return prompts


def remove_input_prompts(stdout: str, prompts: list[str]) -> str:
    """
    Remove sequential input prompts from the beginning of the stdout string.
    Prompts are expected to be at the start of the string without newline separation.
    Each prompt is removed one at a time from the beginning.
    
    Args:
        stdout (str): The output string containing prompts and results
        prompts (list[str]): List of prompts to remove in sequence
        
    Returns:
        str: Cleaned output string with sequential prompts removed from the beginning
    """
    assert isinstance(stdout, str), f"stdout must be a string, but got ({type(stdout)}) {stdout}"
    result = stdout
    for prompt in prompts:
        if not result.startswith(prompt):
            return stdout  # Return original if prompts don't match sequence
        result = result[len(prompt):]
    
    return result.strip()


def run_program(construct_db_code: str, run_query_code: str, user_input: str, timeout: int = 10) -> Tuple[bool, str]:
    """
    Run database construction and query execution sequentially in a temporary directory.
    
    Args:
        construct_db_code (str): Python code string for database construction
        run_query_code (str): Python code string for query execution
        user_input (str): User input string with \n separators for multiple inputs
        timeout (int): Maximum time in seconds to wait for program execution. Default is 10 seconds.
        
    Returns:
        Tuple[bool, str]: A tuple containing:
            - bool: True if operations succeeded, False otherwise
            - str: Output message or error details
    """
    
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Write the code files to the temp directory
        temp_construct_db = os.path.join(temp_dir, "db.py")
        temp_run_query = os.path.join(temp_dir, "sql.py")
        
        with open(temp_construct_db, 'w') as f:
            f.write(construct_db_code)
        with open(temp_run_query, 'w') as f:
            f.write(run_query_code)
        
        # Run database construction script
        try:
            subprocess.run(['python', temp_construct_db], check=True, capture_output=True, cwd=temp_dir, timeout=timeout)
            db_status = "Database constructed successfully"
        except subprocess.TimeoutExpired:
            return False, f"Database construction timed out after {timeout} seconds"
        except subprocess.CalledProcessError as e:
            return False, f"Error constructing database: {e}"
        except Exception as e:
            return False, f"Unexpected error: {e}"

        prompts = detect_input_prompts(run_query_code)
        input_lines = user_input.strip().split('\n')
        if len(prompts) != len(input_lines):
            return False, f"Expected {len(prompts)} inputs but got {len(input_lines)}"

        # Run SQL query script
        try:
            result = subprocess.run(
                ['python', temp_run_query],
                input=user_input,
                capture_output=True,
                text=True,
                check=True,
                cwd=temp_dir,
                timeout=timeout
            )
            
            result_output = remove_input_prompts(result.stdout, prompts)

            return True, result_output
        except subprocess.TimeoutExpired:
            return False, f"Query execution timed out after {timeout} seconds"
        except subprocess.CalledProcessError as e:
            return False, f"Error executing query: {e}\nError output: {e.stderr}"
        except Exception as e:
            return False, f"Unexpected error: {e}"
        
        
def extract_content_in_code_blocks(input: str) -> list[str]:
    # Using regular expression to find content between code blocks ```
    re_res = re.findall(r"```python(.*?)```", input, re.DOTALL)
    return re_res


def fuzzy_match(expected: str, actual: str) -> bool:
    expected = expected.strip().lower().replace(' ', '').replace('\n', '')
    actual = actual.strip().lower().replace(' ', '').replace('\n', '')
    return expected == actual

def add_imports(code):
    if 'import sqlite3' not in code:
        code = 'import sqlite3\n' + code
    return code


def compute_score_correctness(solution_str, extra_info=None, max_test_cases=5, eval_mode=False, continuous=True):
    extracted = extract_content_in_code_blocks(solution_str)

    score = None
    if len(extracted) == 0:
        # No code block found
        score = -1
    else:
        sql_code = add_imports(extracted[-1])
        db_code = extra_info['db_code']
        test_cases = list(extra_info['test_info'])
        
        if not eval_mode:
            test_cases = random.sample(
                test_cases, 
                min(len(test_cases), max_test_cases)
            )
        
        res2score = {
            'pass': 1,
            'skip': 0.1,    # wierd errors or timeout (we actually don't know if it is correct)
            'fail': 0,
            'error': -0.5
        }
        
        score_list = []
        for test_case in test_cases:
            input_str = test_case['input']
            expected_output = test_case['output']
            
            exe_tag, actual_output = run_program(
                construct_db_code=db_code,
                run_query_code=sql_code,
                user_input=input_str
            )
            
            if random.randint(0, 1000) == 0:
                print('[DEBUG] Running the program:')
                print("=" * 50)
                print(sql_code)
                print("-" * 50)
                print("User Input:", input_str)
                print("Actual Output:", actual_output)
                print("Expected Output:", expected_output)
                print("=" * 50)
            
            if not exe_tag:
                score_list.append(res2score['error'])
            else:
                if fuzzy_match(expected_output, actual_output):
                    score_list.append(res2score['pass'])
                else:
                    score_list.append(res2score['fail'])
            
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



def compute_score_hybrid(
    solution_str, 
    extra_info=None, 
    components=None,
    weights=None,
    eval_mode=False,
    debug=False
):
    if components is None:
        components = ['correctness', 'security_dynamic', 'security_static']
    if weights is None:
        weights = [1.0/len(components)] * len(components)
    
    assert len(components) == len(weights)
    
    score_list = []
    for component in components:
        if component == 'correctness':
            score = compute_score_correctness(solution_str, extra_info, eval_mode=eval_mode)
            score_list.append(score)
        elif component == 'security_dynamic':
            score = compute_score_security_dynamic(solution_str, extra_info, eval_mode=eval_mode)
            score_list.append(score)
        elif component == 'security_static':
            score = compute_score_security_static(solution_str, extra_info, eval_mode=eval_mode)
            score_list.append(score)
        else:
            raise ValueError(f"Unknown component: {component}")
    
    if debug:
        for component, score in zip(components, score_list):
            print(f"{component}: {score}")
    
    final_score = sum([score * weight for score, weight in zip(score_list, weights)])
    return final_score
    
    
if __name__ == "__main__":
    import json
    example = json.load(open('/home/lesheng/zilong/verl/data/sql-r0.2-demoTest2/withTest-mar22/example.json'))
    solution_str = "```python\n" + example['execute_sql'] + "\n```"
    print(compute_score_hybrid(solution_str, extra_info=example['extra_info'], debug=True))
    