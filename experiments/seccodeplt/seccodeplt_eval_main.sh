# =========================== ReaL ============================
# You will first have to use `scripts/merge.sh` to merge your checkpoint
full_path="PATH_TO_YOUR_MODEL_CHECKPOINT"
python eval.py --model_name "$full_path" --cuda_idx 0 --batch_size 64