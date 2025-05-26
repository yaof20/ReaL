# Copyright 2024 Bytedance Ltd. and/or its affiliates
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from verl import DataProto
from verl.utils.reward_score import _default_compute_score
import torch
import multiprocessing
import time
import datetime
import signal


def handler(signum, frame):
    raise TimeoutError("Function timed out!")


class NaiveRewardManager:
    """The reward manager.
    """

    def __init__(self, tokenizer, num_examine, compute_score=None, config=None, 
                 reward_setting=None, eval_mode=False, num_processes=16) -> None:
        self.tokenizer = tokenizer
        self.num_examine = num_examine  # the number of batches of decoded responses to print to the console
        self.compute_score = compute_score or _default_compute_score
        self.config = config
        
        self.reward_setting = reward_setting
        self.eval_mode = eval_mode  # whether to use the reward selector for evaluation
        self.num_processes = num_processes  # number of processes for multiprocessing


    def compute_score_with_timeout(self, *args):
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(600)
        score = 0
        try:
            data_source, sequences_str, ground_truth, extra_info = args
            score = self.compute_score(
                data_source=data_source,
                solution_str=sequences_str,
                ground_truth=ground_truth,
                extra_info=extra_info,
                reward_setting=self.reward_setting,
                eval_mode=self.eval_mode,
            )
        finally:
            signal.alarm(0)
        return score

    def __call__(self, data: DataProto):
        if self.reward_setting is None:
            return self.call_for_seccodeplt(data)
        else:
            return self.call_for_safecode_apps(data)


    def call_for_seccodeplt(self, data: DataProto):
        """We will expand this function gradually based on the available datasets"""

        # If there is rm score, we directly return rm score. Otherwise, we compute via rm_score_fn
        if 'rm_scores' in data.batch.keys():
            return data.batch['rm_scores']

        reward_tensor = torch.zeros_like(data.batch['responses'], dtype=torch.float32)
        reward_tensor_ut = torch.zeros_like(data.batch['responses'], dtype=torch.float32)
        reward_tensor_mypy = torch.zeros_like(data.batch['responses'], dtype=torch.float32)
        reward_tensor_scpd = torch.zeros_like(data.batch['responses'], dtype=torch.float32)

        already_print_data_sources = {}

        for i in range(len(data)):
            data_item = data[i]  # DataProtoItem

            prompt_ids = data_item.batch['prompts']

            prompt_length = prompt_ids.shape[-1]

            valid_prompt_length = data_item.batch['attention_mask'][:prompt_length].sum()
            valid_prompt_ids = prompt_ids[-valid_prompt_length:]

            response_ids = data_item.batch['responses']
            valid_response_length = data_item.batch['attention_mask'][prompt_length:].sum()
            valid_response_ids = response_ids[:valid_response_length]

            # decode
            sequences = torch.cat((valid_prompt_ids, valid_response_ids))
            sequences_str = self.tokenizer.decode(sequences)

            ground_truth = data_item.non_tensor_batch['reward_model']['ground_truth']

            data_source = data_item.non_tensor_batch['data_source']

            extra_info = data_item.non_tensor_batch.get('extra_info', None)

            score = self.compute_score(
                data_source=data_source,
                solution_str=sequences_str,
                ground_truth=ground_truth,
                extra_info=extra_info,
                config=self.config,
                eval_mode=self.eval_mode,
            )

            if isinstance(score, list):
                score, ut_score, mypy_score, scpd_score = score  # for seccodeplt
            else:
                ut_score = 0.0
                mypy_score = 0.0
                scpd_score = 0.0

            reward_tensor[i, valid_response_length - 1] = score
            reward_tensor_ut[i, valid_response_length - 1] = ut_score
            reward_tensor_mypy[i, valid_response_length - 1] = mypy_score
            reward_tensor_scpd[i, valid_response_length - 1] = scpd_score

            if data_source not in already_print_data_sources:
                already_print_data_sources[data_source] = 0

            if already_print_data_sources[data_source] < self.num_examine:
                already_print_data_sources[data_source] += 1
                print(sequences_str)

        return reward_tensor, reward_tensor_ut, reward_tensor_mypy, reward_tensor_scpd



    def call_for_safecode_apps(self, data: DataProto):
        """We will expand this function gradually based on the available datasets"""

        # If there is rm score, we directly return rm score. Otherwise, we compute via rm_score_fn
        if "rm_scores" in data.batch.keys():
            return data.batch["rm_scores"]

        reward_tensor = torch.zeros_like(data.batch["responses"], dtype=torch.float32)
        
        reward_tensor_placeholder = torch.zeros_like(data.batch['responses'], dtype=torch.float32)

        already_print_data_sources = {}

        compute_score_args = []

        for i in range(len(data)):
            data_item = data[i]  # DataProtoItem

            prompt_ids = data_item.batch["prompts"]

            prompt_length = prompt_ids.shape[-1]

            valid_prompt_length = data_item.batch["attention_mask"][
                :prompt_length
            ].sum()
            valid_prompt_ids = prompt_ids[-valid_prompt_length:]

            response_ids = data_item.batch["responses"]
            valid_response_length = data_item.batch["attention_mask"][
                prompt_length:
            ].sum()
            valid_response_ids = response_ids[:valid_response_length]

            # decode
            # sequences = torch.cat((valid_prompt_ids, valid_response_ids))
            # sequences_str = self.tokenizer.decode(sequences)
            # NOTE: otherwise we can always get some code snippets from the prompt
            sequences_str = self.tokenizer.decode(valid_response_ids)

            ground_truth = data_item.non_tensor_batch["reward_model"]["ground_truth"]

            data_source = data_item.non_tensor_batch["data_source"]

            extra_info = data_item.non_tensor_batch.get("extra_info", None)

            compute_score_args.append(
                [data_source, sequences_str, ground_truth, extra_info]
            )

        # batched scoring with multiprocessing
        num_processes = self.num_processes
        start_time = time.time()
        formatted_start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(
            f"[DEBUG] Using {num_processes} processes for scoring {len(compute_score_args)} samples (start time: {formatted_start_time})"
        )

        with multiprocessing.Pool(processes=num_processes) as pool:

            mp_task = pool.starmap_async(
                self.compute_score_with_timeout, compute_score_args
            )

            try:
                scores = mp_task.get(timeout=2400)
            except multiprocessing.TimeoutError as e:
                print("Global timeout reached! Terminating all processes...")
                pool.terminate()
                for p in pool._pool:
                    p.terminate()
                scores = [0.0 for _ in range(len(compute_score_args))]
            except Exception as e:
                print(
                    f"Unexpected error in batched reward computing. Setting all as 0.: {e}"
                )
                pool.terminate()
                scores = [0.0 for _ in range(len(compute_score_args))]
            finally:
                pool.close()
                pool.join()

            # scores = mp_task.get(timeout=2400)
            # pool.terminate()
            # pool.close()
            # pool.join()

        end_time = time.time()
        used_time = round(end_time - start_time)
        formatted_used_time = str(datetime.timedelta(seconds=used_time))
        print(
            f"[DEBUG] Finished scoring {len(scores)} samples (average score: {round(sum(scores) / len(scores), 4)}, eclapsed time: {formatted_used_time})"
        )

        for i, (
            score,
            (data_source, sequences_str, ground_truth, extra_info),
        ) in enumerate(zip(scores, compute_score_args)):
            # score = self.compute_score(
            #     data_source=data_source,
            #     solution_str=sequences_str,
            #     ground_truth=ground_truth,
            #     extra_info=extra_info,
            # )
            reward_tensor[i, valid_response_length - 1] = score

            if data_source not in already_print_data_sources:
                already_print_data_sources[data_source] = 0

            if already_print_data_sources[data_source] < self.num_examine:
                already_print_data_sources[data_source] += 1
                print(sequences_str)

        return reward_tensor, reward_tensor_placeholder, reward_tensor_placeholder, reward_tensor_placeholder