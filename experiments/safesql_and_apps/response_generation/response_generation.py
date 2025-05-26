import fire
import os
import re
import json
import datasets

from tqdm import tqdm
from transformers import AutoTokenizer
from vllm import LLM, SamplingParams


def get_prompt(example, tokenizer):
    prompt = example['prompt']
    formatted_prompt = tokenizer.apply_chat_template(prompt, tokenize=False, add_generation_prompt=True)
    return formatted_prompt


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


def extract_code(response, need_clean_code=True):
    res = re.findall(r"```python(.*?)```", response, re.DOTALL)
    if len(res) == 0:
        return None
    else:
        if need_clean_code:
            return clean_code(res[-1].strip())
        else:
            return res[-1].strip()
    

def main(
    actor_dir,
    dataset_name,
    dataset_split,
    model_name=None,
    sft_model_path=None,
    data_root=None,
    need_clean_code=True,
):
    # print the args
    if model_name:
        model_path = model_name
    elif sft_model_path:
        model_path = sft_model_path
    else:
        model_path = os.path.join(actor_dir, "huggingface")
    output_dir = os.path.join(actor_dir, "outputs", dataset_name, dataset_split)
    os.makedirs(output_dir, exist_ok=True)
    
    print(f'model path: {model_path}')
    print(f'output_dir: {output_dir}')
    print(f'dataset_name: {dataset_name}')
    print(f'dataset_split: {dataset_split}')
    print(f"data_root: {data_root}")
    print(f"need_clean_code: {need_clean_code}")
    print('-' * 20)
    
    dataset_path = os.path.join(data_root, dataset_name, f'{dataset_split}.parquet')
    dataset = datasets.load_dataset('parquet', data_files=dataset_path, split='train')
    
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    llm = LLM(model=model_path, gpu_memory_utilization=0.6)
    sampling_params = SamplingParams(
        best_of=1,
        top_p=1.0,
        top_k=-1,
        min_p=0.0,
        temperature=0,
        max_tokens=1024,
        n=1,
    )
    
    prompts = []
    for data in tqdm(dataset):
        prompt = get_prompt(data, tokenizer)
        prompts.append(prompt)
        
    vllm_outputs = llm.generate(prompts=prompts, sampling_params=sampling_params)
    responses = [output.outputs[0].text for output in vllm_outputs]

    # postprocess the responses
    # postproc_fn = postproc_map[postproc_type]
    processed_responses = []
    for response in responses:
        processed_response = extract_code(response, need_clean_code=need_clean_code)
        processed_responses.append(processed_response)
        
    # save the processed responses
    
    extraction_error_count = 0
    
    def _proc_item_id(item_id):
        item_id = str(item_id)
        item_id = item_id.replace('/', '_')
        return item_id    
    
    assert len(dataset) == len(prompts) == len(responses) == len(processed_responses)
    for example, prompt, response, processed_response in tqdm(zip(dataset, prompts, responses, processed_responses), 
                                                              total=len(dataset),
                                                              desc="Saving examples"):
        item_id = _proc_item_id(example["extra_info"]["problem_id"])
        item = {}
        item['id'] = item_id
        item['prompt'] = prompt
        item['response'] = response
        item['processed_response'] = processed_response
        
        if not processed_response:
            extraction_error_count += 1
        
        json.dump(item, open(os.path.join(output_dir, f'{item_id}.json'), 'w'), indent=4)
        
    print(f"Processed {len(dataset)} examples, {extraction_error_count} of them have extraction errors.")
    print(f"Saved to {output_dir}.")

if __name__ == "__main__":
    fire.Fire(main)
