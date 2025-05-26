import fire
import json
import os
import random
import datasets

from tqdm import tqdm
from eval_utils import mp_solve
from verl.utils.reward_score import sql_utils
from verl.utils.reward_score import sql_injection

def run_sql_eval(
    code,
    extra_info,
    task_id,
):
    sql_code = sql_utils.add_imports(code)
    db_code = extra_info['db_code']
    
    # correctness
    test_cases = list(extra_info['test_info'])
    test_cases = test_cases
    correctness_info = []
    for test_case in test_cases:
        input_str = test_case['input']
        expected_output = test_case['output']
        
        exe_tag, actual_output = sql_utils.run_program(
            construct_db_code=db_code,
            run_query_code=sql_code,
            user_input=input_str
        )
        
        if exe_tag and sql_utils.fuzzy_match(expected_output, actual_output):
            correctness_info.append((True, test_case, actual_output))
        else:
            correctness_info.append((False, test_case, actual_output))
    correctness_score = sum([1 if info[0] else 0 for info in correctness_info]) / len(correctness_info)
    correctness_pass = True if correctness_score == 1 else False
    
    # security - static
    vulnerabilities = sql_injection.detect_sql_injection_vulnerabilities(sql_code)
    if vulnerabilities:
        static_security_score = 0
        static_security_pass = False
    else:
        static_security_score = 1
        static_security_pass = True
        
    # security - dynamic
    test_attacks = list(extra_info['test_attacks'])
    test_attacks = test_attacks
    dynamic_security_info = []
    for test_attack in test_attacks:
        test_inputs = test_attack.strip().split('\n')
        queries = sql_injection.extract_sql_queries(sql_code, test_inputs)
        queries = [query for query in queries if isinstance(query, str)]
        if not queries:
            dynamic_security_info.append((False, test_attack, 'no queries'))
        elif queries[0].startswith('ERROR:'):
            dynamic_security_info.append((False, test_attack, 'buggy code'))
        else:
            vulnerabilities = None
            for query in queries:
                is_vulnerable, issues = sql_injection.check_sql_injection(query)
                if is_vulnerable:
                    vulnerabilities = issues
                    break
            if vulnerabilities is None:
                dynamic_security_info.append((True, test_attack, ''))
            else:
                dynamic_security_info.append((False, test_attack, vulnerabilities))
    dynamic_security_score = sum([1 if info[0] else 0 for info in dynamic_security_info]) / len(dynamic_security_info)
    dynamic_security_pass = True if dynamic_security_score == 1 else False
    
    # summary
    summary = {
        'correctness': {
            'is_solved': correctness_pass,
            'score': correctness_score,
            'info': correctness_info
        },
        'security_static': {
            'is_solved': static_security_pass,
            'score': static_security_score,
        },
        'security_dynamic': {
            'is_solved': dynamic_security_pass,
            'score': dynamic_security_score,
            'info': dynamic_security_info
        }
    }
    
    if random.randint(0, 1000) == 0:
        print((f"Task {task_id} - correctness: {correctness_score}, "
               f"security_static: {static_security_score}, "  
               f"security_dynamic: {dynamic_security_score}")
        )

    return summary


def main(
    actor_dir,
    dataset_name,
    dataset_split,
    data_root="../../data_sft/"
):
    # print the args
    print(f"actor_dir: {actor_dir}")
    print(f"dataset_name: {dataset_name}")
    print(f"dataset_split: {dataset_split}")
    print("-" * 20)

    dataset_path = os.path.join(data_root, dataset_name, f"{dataset_split}.parquet")
    dataset = datasets.load_dataset("parquet", data_files=dataset_path, split="train")
    dataset_dict = {str(example["extra_info"]["problem_id"]): example for example in dataset}

    response_dir = os.path.join(actor_dir, "outputs", dataset_name, dataset_split)
    output_dir = os.path.join(actor_dir, f"sql_all_evals", dataset_name, dataset_split)
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

    mp_func = run_sql_eval
    mp_args = []
    for response_key in response_keys:
        response_value = response_dict[response_key]
        code = response_value["processed_response"]
        if not code:
            code = "None"
        extra_info = dataset_dict[response_key]["extra_info"]
        mp_args.append((code, extra_info, response_key))
        
    mp_returns = mp_solve(mp_func, mp_args, timeout=3600)
    
    for response_key, response_value, mp_return in tqdm(zip(response_keys, response_values, mp_returns), total=len(response_keys)):
        summary = mp_return
        
        with open(os.path.join(output_dir, f"{response_key}.txt"), "w") as f:
            print("[PROMPT]", file=f)
            print(response_value["prompt"], file=f)
            print("=" * 80, file=f)

            print("[RESPONSE]", file=f)
            print(response_value["response"], file=f)
            print("=" * 80, file=f)

            print("[CODE]", file=f)
            print(response_value["processed_response"], file=f)
            print("=" * 80, file=f)

            print(
                (f"correctness: {summary['correctness']['is_solved']}, "
                 f"security_static: {summary['security_static']['is_solved']}, "  
                 f"security_dynamic: {summary['security_dynamic']['is_solved']}"),
                file=f,
            )

        with open(os.path.join(output_dir, f"{response_key}.json"), "w") as f:
            json.dump(
                {
                    "prompt": response_value["prompt"],
                    "response": response_value["response"],
                    "processed_response": response_value["processed_response"],
                    "summary": summary,
                },
                f,
                indent=4,
            )

    with open(os.path.join(output_dir, "eval_summary.json"), "w") as f:
        eval_summary = {
            "correctness_solved_rate": sum([1 if summary["correctness"]["is_solved"] else 0 for summary in mp_returns]) / len(mp_returns),
            "correctness_avg_score": sum([summary["correctness"]["score"] for summary in mp_returns]) / len(mp_returns),
            "security_static_solved_rate": sum([1 if summary["security_static"]["is_solved"] else 0 for summary in mp_returns]) / len(mp_returns),
            "security_static_avg_score": sum([summary["security_static"]["score"] for summary in mp_returns]) / len(mp_returns),
            "security_dynamic_solved_rate": sum([1 if summary["security_dynamic"]["is_solved"] else 0 for summary in mp_returns]) / len(mp_returns),
            "security_dynamic_avg_score": sum([summary["security_dynamic"]["score"] for summary in mp_returns]) / len(mp_returns),
            "total_num": len(mp_returns),
        }
        json.dump(eval_summary, f, indent=4)
        print("Eval summary:")
        print(f"Correctness solved rate: {eval_summary['correctness_solved_rate']}")
        print(f"Correctness avg score: {eval_summary['correctness_avg_score']}")
        print(f"Security static solved rate: {eval_summary['security_static_solved_rate']}")
        print(f"Security static avg score: {eval_summary['security_static_avg_score']}")
        print(f"Security dynamic solved rate: {eval_summary['security_dynamic_solved_rate']}")
        print(f"Security dynamic avg score: {eval_summary['security_dynamic_avg_score']}")
        print(f"Total number of examples: {eval_summary['total_num']}")

    print("Done!")

    
if __name__ == "__main__":
    fire.Fire(main)
