import torch
import os
import json
import math
import pandas as pd
import argparse
from tqdm import tqdm
from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel



from verl.utils.reward_score.seccodeplt import add_imports, mypy_check, parse_mypy_result, extract_content_in_code_blocks
from verl.utils.reward_score.seccodeplt_test import unit_test
from verl.utils.reward_score.seccodeplt_detector import run_all_detectors


# Disable tokenizers parallelism warning
os.environ["TOKENIZERS_PARALLELISM"] = "false"

def get_save_name(input_name, result_name):
    """Extract a simplified name from the model path."""
    if result_name:
        input_name = result_name.replace('0_5', '0.5')

    if 'huggingface' in input_name:
        save_name = input_name.split('/')[-4]
    else:
        save_name = input_name.split('/')[-1]

    return save_name

def generate_batches(input_list, batch_size):
    """Generate batches from a list."""
    for i in range(0, len(input_list), batch_size):
        yield input_list[i:i + batch_size]

def count_test_cases(test_cases_str):
    """
    Count the number of test cases in the 'capability' sections
    of a testcases dictionary string.
    """
    import re
    
    # Helper function to extract section content
    def get_section_content(section_name):
        pattern = fr'"{section_name}"\s*:\s*\[([\s\S]*?)\]'
        match = re.search(pattern, test_cases_str)
        return match.group(1) if match else ""
    
    # Helper function to count top-level tuples in a section
    def count_tuples(content):
        count = 0
        paren_level = 0
        
        for char in content:
            if char == '(':
                if paren_level == 0:
                    # Start of a new top-level tuple
                    count += 1
                paren_level += 1
            elif char == ')':
                paren_level -= 1
        
        return count
    
    # Get content for each section
    capability_content = get_section_content('capability')
    
    # Count tuples in each section
    capability_count = count_tuples(capability_content)
    
    return {
        'ut_crct_cnt': capability_count,
    }

def calculate_overall_metrics(save_dict_list):
    """Calculate overall metrics from evaluation results."""
    overall_wrong_format = 0

    # ut
    overall_ut_runnable = 0
    overall_crct_case_pass = 0
    overall_ut_crct_pass = 0

    # scpd
    overall_scpd_runnable = 0
    overall_scpd_error_cnt = 0
    overall_scpd_pass = 0

    # mypy
    overall_mypy_runnable = 0
    overall_mypy_error_cnt = 0
    overall_mypy_pass = 0

    correct_format_cnt = 0

    for data in save_dict_list:
        # format
        overall_wrong_format += data['wrong_format']

        if not data['wrong_format']:
            correct_format_cnt += 1

            # ut
            overall_ut_runnable += data['ut_runnable']
            overall_crct_case_pass += data['ut_crct_pass']
            if data['ut_crct_pass'] == 1.0:
                overall_ut_crct_pass += 1

            # scpd
            overall_scpd_runnable += data['scpd_runnable']
            overall_scpd_error_cnt += data['scpd_error_cnt']
            if data['scpd_error_cnt'] == 0:
                overall_scpd_pass += 1

            # mypy
            overall_mypy_runnable += data['mypy_runnable']
            overall_mypy_error_cnt += data['mypy_error_cnt']
            if data['mypy_error_cnt'] == 0:
                overall_mypy_pass += 1

    total_num = len(save_dict_list)
    correct_format_cnt = max(1, correct_format_cnt)  # Avoid division by zero

    # format
    overall_wrong_format /= total_num

    # ut
    overall_ut_runnable /= total_num
    overall_crct_case_pass /= total_num
    overall_ut_crct_pass /= total_num

    # scpd
    overall_scpd_runnable /= total_num
    overall_scpd_error_cnt /= correct_format_cnt
    overall_scpd_pass /= total_num

    # mypy
    overall_mypy_runnable /= total_num
    overall_mypy_error_cnt /= correct_format_cnt
    overall_mypy_pass /= total_num

    overall_info = {
        'model_name': 0,
        'wrong_format_rate': overall_wrong_format,
        'ut_runnable_rate': overall_ut_runnable,
        'ut_crct_case_pass_rate': overall_crct_case_pass,
        'ut_crct_pass_rate': overall_ut_crct_pass,
        'scpd_runnable': overall_scpd_runnable,
        'scpd_error_cnt': overall_scpd_error_cnt,
        'scpd_pass_rate': overall_scpd_pass,
        'mypy_runnable': overall_mypy_runnable,
        'mypy_error_cnt': overall_mypy_error_cnt,
        'mypy_pass_rate': overall_mypy_pass,
    }

    for key in overall_info:
        overall_info[key] = round(overall_info[key], 4)

    return overall_info

def main():
    parser = argparse.ArgumentParser(description='Evaluate code generation models on security and correctness.')
    parser.add_argument('--model_name', type=str, default="",
                        help='Name or path of the model to evaluate')
    parser.add_argument('--result_name', type=str, default="",
                        help='Name or path of the pre-generated result to evaluate')
    parser.add_argument('--cuda_idx', type=int, default=0,
                        help='CUDA device index')
    parser.add_argument('--batch_size', type=int, default=256,
                        help='Batch size for generation')
    parser.add_argument('--max_new_tokens', type=int, default=1024,
                        help='Maximum number of new tokens to generate')
    parser.add_argument('--save_dir', type=str, default='./saved',
                        help='Directory to save results')
    parser.add_argument('--dataset_path', type=str, default='../../data/seccodeplt',
                        help='Path to the seccodeplt dataset')
    parser.add_argument('--seed', type=int, default=42,
                        help='Random seed for reproducibility')
    
    args = parser.parse_args()
    
    # Set random seed
    torch.manual_seed(args.seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(args.seed)
    
    # Get model save name and create save directory
    save_name = get_save_name(args.model_name, args.result_name)

    # Load dataset
    try:
        instruct_dataset = load_dataset(args.dataset_path)['test'].to_list()
        print(f"Loaded {len(instruct_dataset)} test examples")
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return
    
    
    if args.model_name:
        if 'lora' in args.model_name:
            tokenizer = AutoTokenizer.from_pretrained(args.model_name)

            if '0.5b' in args.model_name:
                base_model_name = "Qwen/Qwen2.5-Coder-0.5B-Instruct"
            elif '3b' in args.model_name:
                base_model_name = "Qwen/Qwen2.5-Coder-3B-Instruct"
            elif '7b' in args.model_name:
                base_model_name = "Qwen/Qwen2.5-Coder-7B-Instruct"

            base_model = AutoModelForCausalLM.from_pretrained(base_model_name, 
                                                            trust_remote_code=True, 
                                                            torch_dtype=torch.float16, 
                                                            device_map=f"cuda:{args.cuda_idx}", 
                                                            attn_implementation="flash_attention_2")
            base_model.resize_token_embeddings(len(tokenizer))
            model = PeftModel.from_pretrained(base_model, args.model_name)
            model = model.to(f"cuda:{args.cuda_idx}")  
        else:
            # Load tokenizer and model
            tokenizer = AutoTokenizer.from_pretrained(args.model_name)

            model = AutoModelForCausalLM.from_pretrained(
                args.model_name,
                torch_dtype=torch.float16,
                device_map=f"cuda:{args.cuda_idx}",
                attn_implementation="flash_attention_2"
            )
        
        model = model.eval()

    
        # Process prompts
        prompts = []
        save_dict_list = []
        
        for idx, data in enumerate(tqdm(instruct_dataset, desc="Processing prompts")):
            prompt = data['prompt']
            prompt = tokenizer.apply_chat_template(
                prompt, 
                tokenize=False,
                add_generation_prompt=True
            )
            prompts.append(prompt)
        
            tmp = {
                'id': idx,
                'CWE_ID': data['CWE_ID'],
                'prompt': prompt,
                'response': None,
                # extract code
                'wrong_format': None,
                
                # Unit test related fields
                'ut_runnable': None,
                'ut_crct_pass': None,
                'ut_crct_cnt': None,
                
                # SCPD related fields
                'scpd_runnable': None,
                'scpd_error_cnt': None,
                'scpd_error_msg': None,
                
                # MP related fields
                'mypy_runnable': None,
                'mypy_error_cnt': None,
                'mypy_error_msg': None,
                
                # Other fields
                'extracted': None,
                'install_requires': None,
                'ut_to_run': None
            }
            save_dict_list.append(tmp)
        
        # Generate responses in batches
        batches = list(generate_batches(prompts, args.batch_size))
        responses = []
        
        for batch in tqdm(batches, desc="Generating responses"):
            model_inputs = tokenizer(batch, return_tensors="pt", padding=True, truncation=True, padding_side='left').to(model.device)
        
            generated_ids = model.generate(
                **model_inputs,
                max_new_tokens=args.max_new_tokens,
                do_sample=False,
                num_beams=1,
                top_p=None,
                temperature=None,
                top_k=None,
            )
            generated_ids = [
                output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
            ]
        
            response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)
            responses.extend(response)
    
    else:
        args.model_name = args.result_name.replace('0_5', '0.5')

        saved_dataset = load_dataset(args.result_name)['train'].to_list()
        if 'promsec' in args.model_name:
            responses = ["```python" + sd['code'] + "```" for sd in saved_dataset]
        else:
            responses = [sd['response'] for sd in saved_dataset]
        
                # Process prompts
        prompts = []
        save_dict_list = []
        
        for idx, data in enumerate(tqdm(instruct_dataset, desc="Processing prompts")):
            prompt = data['prompt']
        
            tmp = {
                'id': idx,
                'CWE_ID': data['CWE_ID'],
                'prompt': prompt,
                'response': None,
                # extract code
                'wrong_format': None,
                
                # Unit test related fields
                'ut_runnable': None,
                'ut_crct_pass': None,
                'ut_crct_cnt': None,
                
                # SCPD related fields
                'scpd_runnable': None,
                'scpd_error_cnt': None,
                'scpd_error_msg': None,
                
                # MP related fields
                'mypy_runnable': None,
                'mypy_error_cnt': None,
                'mypy_error_msg': None,
                
                # Other fields
                'extracted': None,
                'install_requires': None,
                'ut_to_run': None
            }
            save_dict_list.append(tmp)



    save_path = os.path.join(args.save_dir, save_name)
    os.makedirs(save_path, exist_ok=True)
    
    print(f"Using model: {args.model_name}")
    print(f"Results will be saved to: {save_path}")

    # Process responses
    for idx, data in enumerate(tqdm(instruct_dataset, desc="Evaluating responses")):
        response = responses[idx]
        save_dict_list[idx]['response'] = response
    
        extracted = extract_content_in_code_blocks(response)
    
        wrong_format = 0
        # Check format
        if len(extracted) == 0:
            wrong_format = 1
            save_dict_list[idx]['wrong_format'] = wrong_format
            
        else:
            extracted_code = extracted[0].strip()
            extra_info = data['extra_info']
            save_dict_list[idx]['wrong_format'] = wrong_format
    
            # Unit test
            ut_runnable, ut_result, ut_to_run = unit_test(extracted_code, extra_info)
    
            save_dict_list[idx]['extracted'] = extracted_code
            save_dict_list[idx]['install_requires'] = extra_info['install_requires']
            save_dict_list[idx]['ut_to_run'] = ut_to_run
            
            if ut_runnable:
                crct_pass_cnt, crct_total_cnt = ut_result['capability']       
                ut_crct_pass = crct_pass_cnt / crct_total_cnt
    
            else:
                cnt = count_test_cases(data['unittest']['testcases'])
                crct_pass_cnt, crct_total_cnt = 0, cnt['ut_crct_cnt']
                ut_crct_pass = 0

    
            save_dict_list[idx]['ut_runnable'] = int(ut_runnable)
            save_dict_list[idx]['ut_crct_pass'] = ut_crct_pass
            save_dict_list[idx]['ut_crct_cnt'] = f"{crct_pass_cnt}/{crct_total_cnt}"

            
            # Security code pattern detection
            try:
                scpd_result = run_all_detectors(extracted_code)
                scpd_runnable = 1
            except Exception as e:
                scpd_result = []
                scpd_runnable = 0
            
            save_dict_list[idx]['scpd_runnable'] = scpd_runnable
            save_dict_list[idx]['scpd_error_cnt'] = len(scpd_result)
            save_dict_list[idx]['scpd_error_msg'] = scpd_result
    
            # mypy type checking
            code = add_imports(extracted_code)
            result, error, exit_code = mypy_check(code)
    
            if exit_code == 0:
                # Runnable and no issues
                mypy_runnable = 1
                mypy_error_cnt = 0
                mypy_error_msg = []
            elif exit_code == 1:
                # Runnable but with issues
                mypy_runnable = 1
                mypy_error_cnt = parse_mypy_result(result)
                mypy_error_msg = result
            else:
                # Not runnable
                mypy_runnable = 0
                mypy_error_cnt = 0
                mypy_error_msg = []
            
            save_dict_list[idx]['mypy_runnable'] = mypy_runnable
            save_dict_list[idx]['mypy_error_cnt'] = mypy_error_cnt
            save_dict_list[idx]['mypy_error_msg'] = mypy_error_msg
    
    # Save detailed results
    with open(f'{save_path}/{save_name}_details.json', 'w', encoding='utf-8') as f:
        json.dump(save_dict_list, f, indent=2, ensure_ascii=False)
    
    # Save as CSV as well
    df = pd.DataFrame(save_dict_list)
    df.to_csv(f'{save_path}/{save_name}_details.csv')
    
    # Calculate and save overall metrics
    overall_info = calculate_overall_metrics(save_dict_list)
    overall_info['model_name'] = save_name
    
    with open(f'{save_path}/{save_name}_overall.json', 'w', encoding='utf-8') as f:
        json.dump(overall_info, f, indent=2, ensure_ascii=False)
    
    print(f"Evaluation complete. Results saved to {save_path}")

if __name__ == "__main__":
    main()