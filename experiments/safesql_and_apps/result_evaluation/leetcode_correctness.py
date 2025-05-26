import fire
import os
import re
import json
import datasets
import random
from tqdm import tqdm
from eval_utils import mp_solve
from verl.utils.reward_score import leetcode_utils


def run_leetcode_tests(code, test_info, fn_name, program_type, task_id):
    score_list = []
    success_tests = []
    failed_tests = []

    for input_var, output_var in zip(test_info["inputs"], test_info["outputs"]):
        result_tag, message = leetcode_utils.run_program(
            code, program_type, input_var, output_var, fn_name
        )
        if result_tag == "pass":
            score_list.append(1)
            success_tests.append((input_var, output_var, message))
        else:
            score_list.append(0)
            failed_tests.append((input_var, output_var, message))

    if len(score_list) == 0:
        score = 0
    else:
        score = sum(score_list) / len(score_list)

    if random.randint(0, 100) == 0:
        print(
            f"Task {task_id} - is_solved: {score == 1}, score: {score} ({sum(score_list)}/{len(score_list)})"
        )

    summary = {
        "is_solved": score == 1,
        "score": score,
        "success_tests": success_tests,
        "failed_tests": failed_tests,
    }

    return summary


def main(actor_dir, dataset_name, dataset_split, data_root):
    assert os.path.exists(data_root), f"Data root {data_root} does not exist"

    # print the args
    print(f"actor_dir: {actor_dir}")
    print(f"dataset_name: {dataset_name}")
    print(f"dataset_split: {dataset_split}")
    print("-" * 20)

    dataset_path = os.path.join(data_root, dataset_name, f"{dataset_split}.parquet")
    dataset = datasets.load_dataset("parquet", data_files=dataset_path, split="train")
    dataset_dict = {str(example["extra_info"]["problem_id"]): example for example in dataset}

    response_dir = os.path.join(actor_dir, "outputs", dataset_name, dataset_split)
    output_dir = os.path.join(
        actor_dir, "leetcode_correctness_evals", dataset_name, dataset_split
    )
    os.makedirs(output_dir, exist_ok=True)

    response_files = os.listdir(response_dir)
    response_dict = {}
    for response_file in response_files:
        response_id = response_file.split(".")[0]
        response_value = json.load(open(os.path.join(response_dir, response_file), "r"))
        response_dict[response_id] = response_value

    response_keys = sorted(response_dict.keys())
    response_values = [response_dict[key] for key in response_keys]

    mp_func = run_leetcode_tests
    my_args = []
    for response_key in response_keys:
        
        response_value = response_dict[response_key]
        code = response_value["processed_response"]
        if not code:
            code = "None"
            
        test_info = json.loads(dataset_dict[response_key]["extra_info"]["test_info"])
        fn_name = test_info["fn_name"]
        program_type = dataset_dict[response_key]["extra_info"]["program_type"]
        
        my_args.append((code, test_info, fn_name, program_type, response_key))

    mp_returns = mp_solve(mp_func, my_args, timeout=3600)

    solved_results = []
    scores = []

    for response_key, response_value, mp_return in tqdm(
        zip(response_keys, response_values, mp_returns), total=len(response_keys)
    ):
        summary = mp_return

        is_solved = summary["is_solved"]
        score = summary["score"]
        success_tests = summary["success_tests"]
        failed_tests = summary["failed_tests"]

        solved_results.append(1 if is_solved else 0)
        scores.append(score)

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

            print(f"is_solved: {is_solved}", file=f)
            print(
                f"score: {len(success_tests)}/{len(success_tests)+len(failed_tests)}={score}",
                file=f,
            )

        with open(os.path.join(output_dir, f"{response_key}.json"), "w") as f:
            json.dump(
                {
                    "prompt": response_value["prompt"],
                    "response": response_value["response"],
                    "processed_response": response_value["processed_response"],
                    "is_solved": is_solved,
                    "score": score,
                    "success_tests": success_tests,
                    "failed_tests": failed_tests,
                },
                f,
                indent=4,
            )

    with open(os.path.join(output_dir, "eval_summary.json"), "w") as f:
        eval_summary = {
            "solved_rate": (
                sum(solved_results) / len(solved_results)
                if len(solved_results) > 0
                else -1
            ),
            "avg_score": sum(scores) / len(scores) if len(scores) > 0 else -1,
            "total_num": len(solved_results),
        }
        json.dump(eval_summary, f, indent=4)
        print("Eval summary:")
        print(f"Solved rate: {eval_summary['solved_rate']}")
        print(f"Avg score: {eval_summary['avg_score']}")
        print(f"Total num: {eval_summary['total_num']}")

    print("Done!")


if __name__ == "__main__":
    fire.Fire(main)
