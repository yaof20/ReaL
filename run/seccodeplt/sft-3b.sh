set -x
# export VLLM_ATTENTION_BACKEND=XFORMERS
export WANDB_API_KEY="YOUR_KEY_HERE"  # specify your key if you want to use wandb
CUDA_VISIBLE_DEVICES=0,1 torchrun --nnodes=1 --nproc_per_node=2 -m verl.trainer.fsdp_sft_trainer \
    data.train_files=./data/seccodeplt_sft/train.parquet \
    data.val_files=./data/seccodeplt_sft/test.parquet \
    data.prompt_key=question \
    data.response_key=answer \
    data.train_batch_size=8 \
    data.micro_batch_size_per_gpu=4 \
    data.max_length=1024 \
    data.truncation=right \
    model.partial_pretrain=Qwen/Qwen2.5-Coder-3B-Instruct \
    trainer.project_name="ReaL" \
    trainer.experiment_name="sft_3b_bs8_epoch4" \
    trainer.total_epochs=4 \
    trainer.default_local_dir='./checkpoints/sft_3b_bs8_epoch4' \
    trainer.logger=['console'] 2>&1 | tee ./log/sft_3b_bs8_epoch4.log  # use ['console','wandb'] and specify the key above if you want to log in wandb