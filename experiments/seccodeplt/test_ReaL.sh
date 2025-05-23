# =========================== ReaL ============================
full_path="fengyao1909/ReaL_scp_0.5b"
python eval.py --model_name "$full_path" --cuda_idx 0 --batch_size 64

full_path="fengyao1909/ReaL_scp_3b"
python eval.py --model_name "$full_path" --cuda_idx 0 --batch_size 64

full_path="fengyao1909/ReaL_scp_7b"
python eval.py --model_name "$full_path" --cuda_idx 0 --batch_size 64

