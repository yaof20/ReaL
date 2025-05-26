model_path=$1
dataset_name=$2
need_clean_code=$3

data_root=$4

# assert $1 and $2 are not empty
if [ -z "$model_path" ] || [ -z "$dataset_name" ]; then
    echo "Usage: $0 model_path dataset_name [need_clean_code]"
    exit 1
fi

if [ -z "$need_clean_code" ]; then
    need_clean_code="True"
fi

if [[ "$model_path" == *"Qwen2.5-Coder-3B-Instruct"* ]]; then
    base_model="Qwen/Qwen2.5-Coder-3B-Instruct"
else
    base_model="Qwen/Qwen2.5-Coder-0.5B-Instruct"
fi

dataset_split="test"

# ckpts is os.listdir(model_path), use shell to list all ckpts
ckpts=($(ls "$model_path"))

# echo all the parameters to make sure they are correct
echo "model_path: $model_path"
echo "template_name: $template_name"
echo "base_model: $base_model"
echo "dataset_name: $dataset_name"
echo "dataset_split: $dataset_split"
echo "need_clean_code: $need_clean_code"
echo "ckpts: ${ckpts[@]}"
echo "========================================"

# special case for global_step_0
echo "Generating responses for global_step_0"
ckpt="global_step_0"
mkdir -p "$model_path/$ckpt/actor"
python response_generation.py \
    --actor_dir "$model_path/$ckpt/actor" \
    --model_name "$base_model" \
    --dataset_name "$dataset_name" \
    --dataset_split "$dataset_split" \
    --need_clean_code "$need_clean_code" \
    --data_root "$data_root"

# other checkpoints
for ckpt in "${ckpts[@]}"; do
    if [ ! -d "$model_path/$ckpt" ]; then
        continue
    fi

    if [ "$ckpt" == "global_step_0" ]; then
        continue
    fi

    python response_generation.py \
        --actor_dir "$model_path/$ckpt/actor" \
        --dataset_name "$dataset_name" \
        --dataset_split "$dataset_split" \
        --need_clean_code "$need_clean_code" \
        --data_root "$data_root"
done
