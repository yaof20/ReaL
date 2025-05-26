exp_dir=$1
model_sharded_or_single=$2

if [ -z ${exp_dir} ]; then
    echo "exp_dir is empty!"
    exit 1
fi

if [ ! -d ${exp_dir} ]; then
    echo "exp_dir ${exp_dir} not exists!"
    exit 1
fi

ckpt_dirs=$(ls -d ${exp_dir}/*)
for ckpt_dir in ${ckpt_dirs}
do
    if [ ! -d ${ckpt_dir} ]; then
        echo "${ckpt_dir} is not a dir, skip..."
        continue
    fi
    
    # Skip if the checkpoint is global_step_0
    if [[ $(basename ${ckpt_dir}) == "global_step_0" ]]; then
        echo "Skipping global_step_0 checkpoint..."
        continue
    fi
    
    actor_dir=${ckpt_dir}/actor
    echo "Merging ${actor_dir}..."
    
    if [ -f ${actor_dir}/huggingface/model.safetensors ]; then
        echo "Skip ${actor_dir}, already merged..."
        continue
    fi
    if [ -f ${actor_dir}/huggingface/model.safetensors.index.json ]; then
        echo "Skip ${actor_dir}, already merged..."
        continue
    fi

    if [ ${model_sharded_or_single} == "sharded" ]; then
        echo "Merging with sharded model..."
        python model_merger.py --local_dir ${actor_dir}
    else
        echo "Merging with single model..."
        python single_model_merger.py --local_dir ${actor_dir}
    fi
done

