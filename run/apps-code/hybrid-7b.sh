export CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7

PROJECT_NAME=CodeRL
EXPERIMENT_NAME=hybrid-Qwen2.5-Coder-7B-Instruct

TRAIN_DATA=./data/apps-code/train.parquet
VAL_DATA=./data/apps-code/test.parquet
BASE_MODEL=Qwen/Qwen2.5-Coder-7B-Instruct

TRAIN_REWARD_FUNC="['mypy-typecheck','leetcode-correctness']"
TRAIN_REWARD_WEIGHT="[0.5,0.5]"

VAL_REWARD_FUNC=leetcode-correctness
VAL_REWARD_WEIGHT=1

# ---------------------------------------------------------------------------

export WANDB_API_KEY="[YOUR_WANDB_API_KEY]"
export VLLM_ATTENTION_BACKEND=XFORMERS

TIME_TAG=$(date +%Y%m%d-%H%M%S)

echo "----------------------------------------"
echo "Project: $PROJECT_NAME"
echo "Experiment: $EXPERIMENT_NAME-$TIME_TAG"
echo "Base Model: $BASE_MODEL"
echo "Train Data: $TRAIN_DATA"
echo "Validation Data: $VAL_DATA"
echo "----------------------------------------"
echo "Train Reward Model: $TRAIN_REWARD_FUNC with weights $TRAIN_REWARD_WEIGHT"
echo "Validation Reward Model: $VAL_REWARD_FUNC with weights $VAL_REWARD_WEIGHT"
echo "CUDA_VISIBLE_DEVICES: $CUDA_VISIBLE_DEVICES"
echo "----------------------------------------"

read -p "Do you want to continue? (y/n): " choice
if [[ $choice != "y" ]]; then
    echo "Exiting..."
    exit 1
fi

mkdir -p ./log/$PROJECT_NAME

# ---------------------------------------------------------------------------

PYTHONUNBUFFERED=1 python -m verl.trainer.main_ppo \
 data.train_files=$TRAIN_DATA \
 data.val_files=$VAL_DATA \
 data.train_batch_size=256 \
 data.val_batch_size=256 \
 data.max_prompt_length=1024 \
 data.max_response_length=1024 \
 actor_rollout_ref.model.path=$BASE_MODEL \
 actor_rollout_ref.model.enable_gradient_checkpointing=true \
 actor_rollout_ref.actor.optim.lr=1e-6 \
 actor_rollout_ref.actor.ppo_mini_batch_size=256 \
 actor_rollout_ref.actor.ppo_micro_batch_size_per_gpu=2 \
 actor_rollout_ref.actor.fsdp_config.param_offload=false \
 actor_rollout_ref.actor.fsdp_config.optimizer_offload=false \
 actor_rollout_ref.rollout.log_prob_micro_batch_size_per_gpu=2 \
 actor_rollout_ref.rollout.tensor_model_parallel_size=1 \
 actor_rollout_ref.rollout.gpu_memory_utilization=0.5 \
 actor_rollout_ref.ref.log_prob_micro_batch_size_per_gpu=2 \
 actor_rollout_ref.ref.fsdp_config.param_offload=false \
 critic.optim.lr=1e-5 \
 critic.model.path=$BASE_MODEL \
 critic.ppo_micro_batch_size_per_gpu=2 \
 critic.model.enable_gradient_checkpointing=false \
 critic.model.fsdp_config.param_offload=false \
 critic.model.fsdp_config.optimizer_offload=false \
 algorithm.kl_ctrl.kl_coef=0.001 \
 trainer.logger=['console','wandb'] \
 +trainer.val_before_train=true \
 trainer.default_hdfs_dir=null \
 trainer.n_gpus_per_node=8 \
 trainer.nnodes=1 \
 trainer.save_freq=100 \
 trainer.test_freq=20 \
 trainer.project_name=$PROJECT_NAME \
 trainer.experiment_name=$EXPERIMENT_NAME-$TIME_TAG \
 trainer.resume_from_path=True \
 trainer.total_epochs=10000 \
 trainer.total_training_steps=800 \
 +reward_model.train_reward.functions=$TRAIN_REWARD_FUNC \
 +reward_model.train_reward.weights=$TRAIN_REWARD_WEIGHT \
 +reward_model.val_reward.functions=$VAL_REWARD_FUNC \
 +reward_model.val_reward.weights=$VAL_REWARD_WEIGHT \
 +reward_model.num_processes=40 \
 2>&1 | tee ./log/$PROJECT_NAME/$EXPERIMENT_NAME-$TIME_TAG.log

