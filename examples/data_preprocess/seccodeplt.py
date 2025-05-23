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
"""
Preprocess the seccodeplt dataset to parquet format
"""

import re
import os
import datasets
from transformers import AutoTokenizer
from verl.utils.hdfs_io import copy, makedirs
import argparse


def extract_section(text, section_name):
    """
    Extract a section like "capability": [...] or "safety": [...] from the text,
    preserving import statements and correct indentation.
    
    Args:
        text (str): The input string containing JSON-like test cases
        section_name (str): The section name to extract (e.g., "capability" or "safety")
    
    Returns:
        str: The extracted content with imports and proper indentation
    """
    
    # Extract any import statements before "testcases ="
    imports = []
    testcases_start = text.find("testcases =")
    
    if testcases_start > 0:
        # Get all lines before "testcases ="
        pre_text = text[:testcases_start].strip()
        if pre_text:
            imports = pre_text.split('\n')
    
    # Find the section start
    section_start_pattern = fr'"{section_name}":\s*\['
    start_match = re.search(section_start_pattern, text)
    
    if not start_match:
        return f"Section '{section_name}' not found"
    
    # Get the position right after the opening bracket
    start_pos = start_match.end()
    
    # Find the matching closing bracket by counting brackets
    bracket_count = 1
    end_pos = start_pos
    
    while bracket_count > 0 and end_pos < len(text):
        if text[end_pos] == '[':
            bracket_count += 1
        elif text[end_pos] == ']':
            bracket_count -= 1
        end_pos += 1
    
    if bracket_count != 0:
        return "Unmatched brackets"
    
    # Extract the section content including brackets
    section_content = text[start_pos-1:end_pos]
    
    # Post-process: reduce indentation by 4 spaces for all lines except the first
    lines = section_content.split('\n')
    processed_lines = [lines[0]]  # Keep the first line as is
    
    for i in range(1, len(lines)):
        line = lines[i]
        if not line.strip():
            processed_lines.append(line)
            continue
            
        # Find the leading whitespace
        indent_match = re.match(r'^(\s*)', line)
        indent = indent_match.group(1) if indent_match else ""
        
        # Reduce indent by 4 spaces
        if len(indent) >= 4:
            new_indent = indent[4:]
            processed_lines.append(new_indent + line.lstrip())
        else:
            # If indentation is less than 4, just use the line as is
            processed_lines.append(line)
    
    # Combine imports and processed section content
    result = '\n'.join(imports)
    if imports:
        result += '\n'
    result += '\n'.join(processed_lines)
    
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--local_dir', default='./data/seccodeplt')
    parser.add_argument('--hdfs_dir', default=None)
    parser.add_argument('--hf_model', default='Qwen/Qwen2.5-0.5B-Instruct')
    parser.add_argument('--add_correct_ut', type=bool, default=False)
    parser.add_argument('--add_safe_ut', type=bool, default=False)

    args = parser.parse_args()

    print(f"add_correct_ut is {args.add_correct_ut}")
    print(f"add_safe_ut is {args.add_safe_ut}")
    if args.add_correct_ut and args.add_safe_ut:
        args.local_dir += "_add_both_ut"
    elif args.add_correct_ut:
        args.local_dir += "_add_correct_ut"
    elif args.add_safe_ut:
        args.local_dir += "_add_safe_ut"
    else:
        pass

    tokenizer = AutoTokenizer.from_pretrained(args.hf_model)
    data_source = 'fengyao1909/seccodeplt_ut'

    dataset = datasets.load_dataset(data_source)

    train_dataset = dataset['train']
    test_dataset = dataset['test']

    # add a row to each data item that represents a unique id
    def make_map_fn(split, cfg):

        def process_fn(example, idx):
            task = example['task_description']
            desc = task['description']
            name = task['function_name']
            args = task['arguments']
            ret = task['return']
            ras = task['raise']
            ctx = task['context']
            testcases = example['unittest']['testcases']

            problem_template = open('./data/seccodeplt/problem_template.txt').read()
            problem = problem_template.format(desc, name, args, ret, ras, ctx)

            io_example_template = "\nExample Inputs & Outputs:\nBelow are some unit test examples with package imports (if necessary). The unit tests are organized as a list, where each element is a tuple of (example inputs, expected outputs).\n{}\n"
            correct_ut = extract_section(testcases, 'capability')
            safe_ut = extract_section(testcases, 'safety')

            if cfg.add_correct_ut and cfg.add_safe_ut:
                selected_ut = correct_ut[:-1] + safe_ut[safe_ut.index('[')+1:]
                io_example = io_example_template.format(selected_ut)
            elif cfg.add_correct_ut:
                selected_ut = correct_ut
                io_example = io_example_template.format(selected_ut)
            elif cfg.add_safe_ut:
                selected_ut = safe_ut
                io_example = io_example_template.format(selected_ut)
            else:
                io_example = ''
            
            prompt_template = open('./data/seccodeplt/unified_template.txt').read()
            prompt = prompt_template.format(problem, io_example)
            print(f"now prompt is: {prompt}")
            
            data = {
                "data_source": data_source,
                "prompt": [{
                    "role": "user",
                    "content": prompt,
                }],
                "ability": "safety",
                "reward_model": {
                    "style": "rule",
                    "ground_truth": "None",
                },
                "extra_info": {
                    'split': split,
                    'index': idx,
                    **example,
                }
            }
            return data

        return process_fn

    train_dataset = train_dataset.map(function=make_map_fn('train', cfg=args), with_indices=True)
    test_dataset = test_dataset.map(function=make_map_fn('test', cfg=args), with_indices=True)

    local_dir = args.local_dir
    hdfs_dir = args.hdfs_dir

    train_dataset.to_parquet(os.path.join(local_dir, 'train.parquet'))
    test_dataset.to_parquet(os.path.join(local_dir, 'test.parquet'))
    print(f"processed data saved at {args.local_dir}")

    if hdfs_dir is not None:
        makedirs(hdfs_dir)

        copy(src=local_dir, dst=hdfs_dir)
