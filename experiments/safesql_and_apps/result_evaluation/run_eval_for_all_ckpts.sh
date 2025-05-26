model_path=$1
dataset_name=$2
eval_type=$3

data_root=$4

if [ -z "$model_path" ] || [ -z "$dataset_name" ] || [ -z "$eval_type" ]; then
    echo "Usage: $0 model_path dataset_name eval_type"
    exit 1
fi

ckpts=($(ls "$model_path"))

dataset_split="test"

# echo all the parameters to make sure they are correct
echo "model_path: $model_path"
echo "dataset_name: $dataset_name"
echo "dataset_split: $dataset_split"
echo "ckpts: ${ckpts[@]}"
echo "========================================"

for ckpt in "${ckpts[@]}"; do
    if [ ! -d "$model_path/$ckpt" ]; then
        continue
    fi

    if [ "$eval_type" == "sql_eval" ]; then
        echo "Conducting SQL evaluation for checkpoint: $ckpt"
        python sql_eval.py \
            --actor_dir "$model_path/$ckpt/actor" \
            --dataset_name "$dataset_name" \
            --dataset_split "$dataset_split" \
            --data_root "$data_root"
    elif [ "$eval_type" == "leetcode_correctness" ]; then
        echo "Conducting LeetCode correctness evaluation for checkpoint: $ckpt"
        python leetcode_correctness.py \
            --actor_dir "$model_path/$ckpt/actor" \
            --dataset_name "$dataset_name" \
            --dataset_split "$dataset_split" \
            --data_root "$data_root"
    elif [ "$eval_type" == "mypy_typecheck" ]; then
        echo "Conducting MyPy type checking for checkpoint: $ckpt"
        python mypy_typecheck.py \
            --actor_dir "$model_path/$ckpt/actor" \
            --dataset_name "$dataset_name" \
            --dataset_split "$dataset_split" \
            --data_root "$data_root"
    else
        echo "Unknown eval_type: $eval_type"
        exit 1
    fi
done
