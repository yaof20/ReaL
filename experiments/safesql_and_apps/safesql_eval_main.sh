# The overal evaluation pipleine:
# 1. Format the checkpoints (convert the original format to the huggingface format)
# 2. Generate the responses
# 3. Evaluate the responses

EXP_DIR=$1  # Path to a specific experiment directory, e.g. /.../ReaL/checkpoints/[PROJECT]/[EXP_NAME]
MODEL_SHARDED_OR_SINGLE=$2  # Whether the model is sharded or single 

DATA_ROOT="[YOUR_DATA_ROOT_PATH]"  # Replace with your actual data root path

# 1. Format the checkpoints
cd model_formatting
bash run_model_merger_for_all_ckpts.sh $EXP_DIR $MODEL_SHARDED_OR_SINGLE
cd ..

# 2. Generate the responses for all checkpoints and the corresponding base model (aka ckpt "global_step_0")
cd response_generation
bash run_response_generation_for_all_ckpts.sh $EXP_DIR "safesql" "False" $DATA_ROOT
cd ..

# 3. Evaluate the responses for all checkpoints and the corresponding base model (aka ckpt "global_step_0")
cd result_evaluation
bash run_eval_for_all_ckpts.sh $EXP_DIR "safesql" "sql_eval" $DATA_ROOT
cd ..

# Finish
echo "All done!"
