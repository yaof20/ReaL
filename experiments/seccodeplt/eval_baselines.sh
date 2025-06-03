# =========================== Baseline - SFT ============================
full_path="fengyao1909/scp_sft_0.5b"
python eval.py --model_name "$full_path" --cuda_idx 0 --batch_size 64

full_path="fengyao1909/scp_sft_3b"
python eval.py --model_name "$full_path" --cuda_idx 0 --batch_size 64

full_path="fengyao1909/scp_sft_7b"
python eval.py --model_name "$full_path" --cuda_idx 0 --batch_size 64


# =========================== Baseline - PromSec =========================
full_path="autoprogrammer/promsec-fixed-codes-0_5b"
python eval.py --result_name "$full_path" --cuda_idx 0 --batch_size 64

full_path="autoprogrammer/promsec-fixed-codes-3b"
python eval.py --result_name "$full_path" --cuda_idx 0 --batch_size 64

full_path="autoprogrammer/promsec-fixed-codes-7b"
python eval.py --result_name "$full_path" --cuda_idx 0 --batch_size 64


# =========================== Baseline - CodeGuard+ ======================
full_path="autoprogrammer/Qwen2.5-Coder-0.5B-Instruct-codeguardplus"
python eval.py --result_name "$full_path" --cuda_idx 0 --batch_size 64

full_path="autoprogrammer/Qwen2.5-Coder-3B-Instruct-codeguardplus"
python eval.py --result_name "$full_path" --cuda_idx 0 --batch_size 64

full_path="autoprogrammer/Qwen2.5-Coder-7B-Instruct-codeguardplus"
python eval.py --result_name "$full_path" --cuda_idx 0 --batch_size 64


# =========================== Baseline - SVEN ============================
full_path="autoprogrammer/qwen-0.5b-sven-lora"
python eval.py --model_name "$full_path" --cuda_idx 0 --batch_size 64

full_path="autoprogrammer/qwen-3b-sven-lora"
python eval.py --model_name "$full_path" --cuda_idx 0 --batch_size 64

full_path="autoprogrammer/qwen-7b-sven-lora"
python eval.py --model_name "$full_path" --cuda_idx 0 --batch_size 64


# =========================== Baseline - SafeCoder =======================
full_path="autoprogrammer/qwen-0.5b-safecoder-lora"
python eval.py --model_name "$full_path" --cuda_idx 0 --batch_size 64

full_path="autoprogrammer/qwen-3b-safecoder-lora"
python eval.py --model_name "$full_path" --cuda_idx 0 --batch_size 64

full_path="autoprogrammer/qwen-7b-safecoder-lora"
python eval.py --model_name "$full_path" --cuda_idx 0 --batch_size 64