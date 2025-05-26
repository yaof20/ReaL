import fire
import os
import re
import json
import datasets
from tqdm import tqdm
from eval_utils import mp_solve
from verl.utils.reward_score import mypy_utils

def mypy_check_dummy(code):
    try:
        result, error, exit_code = mypy_utils.mypy_check(code)
        return result, error, exit_code
    except Exception as e:
        return None, str(e), -1

def main(
    actor_dir,
    dataset_name,
    dataset_split,
    data_root=None
):
    # print the args
    print(f"actor_dir: {actor_dir}")
    print(f"dataset_name: {dataset_name}")
    print(f"dataset_split: {dataset_split}")
    print("-" * 20)

    response_dir = os.path.join(actor_dir, "outputs", dataset_name, dataset_split)
    output_dir = os.path.join(actor_dir, "mypy_typecheck_evals", dataset_name, dataset_split)
    os.makedirs(output_dir, exist_ok=True)

    response_files = os.listdir(response_dir)
    response_dict = {}
    for response_file in response_files:
        assert response_file.endswith(".json")
        response_id = response_file.split(".")[0]
        response_value = json.load(open(os.path.join(response_dir, response_file), "r"))
        response_dict[response_id] = response_value

    response_keys = sorted(response_dict.keys())
    response_values = [response_dict[key] for key in response_keys]
    
    mp_func = mypy_check_dummy
    mp_args = []
    for response_value in response_values:
        code = response_value["processed_response"]
        if code is None:
            code = ''
        else:
            code = mypy_utils.add_imports(code)
        mp_args.append((code,))
    mp_returns = mp_solve(mp_func, mp_args)
    
    pass_results = []
    error_counts = []
    
    for response_key, response_value, mp_return in tqdm(zip(response_keys, response_values, mp_returns), total=len(response_keys)):
        result, error, exit_code = mp_return
        
        if exit_code == 0:
            pass_results.append(1)
            error_counts.append(0)
        else:
            pass_results.append(0)
            
            if result is not None:
                error_cnt = mypy_utils.parse_mypy_result(result)
            else:
                error_cnt = 1
            error_counts.append(error_cnt)
        
        with open(os.path.join(output_dir, f"{response_key}.txt"), "w") as f:
            print("[PROMPT]", file=f)
            print(response_value['prompt'], file=f)
            print('='* 80, file=f)
            
            print("[RESPONSE]", file=f)
            print(response_value['response'], file=f)
            print('='* 80, file=f)
            
            print("[CODE]", file=f)
            print(response_value["processed_response"], file=f)
            print('='* 80, file=f)
            
            print(f'Exit code: [{exit_code}]', file=f)
            print(f'Error: [{error}]', file=f)
            print(f'Result: [{result}]', file=f)
            
        with open(os.path.join(output_dir, f"{response_key}.json"), "w") as f:
            json.dump({
                'prompt': response_value['prompt'],
                'response': response_value['response'],
                'processed_response': response_value["processed_response"],
                'exit_code': exit_code,
                'error': error,
                'result': result,
            }, f, indent=4)
    
    with open(os.path.join(output_dir, "eval_summary.json"), "w") as f:
        eval_summary = {
            'pass_rate': sum(pass_results) / len(pass_results),
            'avg_error_num': sum(error_counts) / len(error_counts),
            'total_num': len(pass_results),
        }
        print("Pass rate:", eval_summary['pass_rate'])
        print("Avg error num:", eval_summary['avg_error_num'])
        print("Total num:", eval_summary['total_num'])
        
        json.dump(eval_summary, f, indent=4)

    print("Done!")
    
if __name__ == "__main__":
    fire.Fire(main)
