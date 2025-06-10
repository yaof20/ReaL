#!/bin/bash

# Define experiment parameters
# Model list
MODELS=(
  "Qwen/Qwen2.5-Coder-7B-Instruct"
)

# Dataset list
DATASETS=(
 "sql7b"
)

# GPU device ID list
GPU_IDS=(2)

# OpenAI model list
OPENAI_MODELS=(
  "gpt-3.5-turbo" 
)

# OpenAI API key (default uses environment variable)
OPENAI_KEY=""

# Number of iterations
ITER_NUM=20

# Create log directory
LOG_DIR="experiment_logs"
mkdir -p $LOG_DIR

# Display experiment configuration
echo "==== Experiment Configuration ===="
echo "Model(s): ${MODELS[@]}"
echo "Dataset(s): ${DATASETS[@]}"
echo "GPU IDs: ${GPU_IDS[@]}"
echo "OpenAI Model(s): ${OPENAI_MODELS[@]}"
echo "Iterations: $ITER_NUM"
echo "Log directory: $LOG_DIR"
echo "==================="

# Loop over all experiment combinations
experiment_count=0
total_experiments=0

# First, calculate total number of experiments
for model in "${MODELS[@]}"; do
  # Extract model size (0.5B or 7B)
  if [[ $model == *"0.5B"* ]]; then
    model_size="0.5b"
  elif [[ $model == *"7B"* ]]; then
    model_size="7b"
  else
    echo "Could not determine size of model $model; skipping"
    continue
  fi
  
  # Count matching datasets
  matched_datasets=0
  for dataset in "${DATASETS[@]}"; do
    if [[ $dataset == *"$model_size"* ]]; then
      matched_datasets=$((matched_datasets + 1))
    fi
  done
  
  # Accumulate to total experiments count
  total_experiments=$((total_experiments + matched_datasets * ${#OPENAI_MODELS[@]}))
done

echo "Total experiments to run: $total_experiments"

# Start running experiments
for model in "${MODELS[@]}"; do
  # Extract model name for output directory
  model_name=$(echo $model | sed 's/.*\///')
  
  # Extract model size (0.5B or 7B)
  if [[ $model == *"0.5B"* ]]; then
    model_size="0.5b"
    echo "Model $model size is 0.5B; matching 0.5b datasets"
  elif [[ $model == *"7B"* ]]; then
    model_size="7b"
    echo "Model $model size is 7B; matching 7b datasets"
  else
    echo "Could not determine size of model $model; skipping"
    continue
  fi
  
  # Select an available GPU
  gpu_id=${GPU_IDS[0]}
  
  for dataset in "${DATASETS[@]}"; do
    # Verify dataset size matches model size
    if [[ $dataset != *"$model_size"* ]]; then
      echo "Dataset $dataset does not match model size $model_size; skipping"
      continue
    fi
    
    echo "Model $model will run on dataset $dataset"
    
    for openai_model in "${OPENAI_MODELS[@]}"; do
      experiment_count=$((experiment_count + 1))
      
      # Create unique output directory name
      output_dir="Results_${model_name}_${dataset}_${openai_model}"
      output_dir=$(echo $output_dir | sed 's/\./-/g' | sed 's/\//-/g')
      
      # Create unique log file name
      log_file="${LOG_DIR}/${output_dir}.log"
      
      echo "==== Starting experiment ${experiment_count}/${total_experiments} ===="
      echo "Model: $model"
      echo "Dataset: $dataset"
      echo "OpenAI Model: $openai_model"
      echo "GPU ID: $gpu_id"
      echo "Output directory: $output_dir"
      echo "Log file: $log_file"
      
      # Run Python script
      echo "Running experiment..."
      python3 -u demo_real.py \
        --model "$model" \
        --data_path "$dataset" \
        --output_dir "$output_dir" \
        --gpu_id $gpu_id \
        --iter_num $ITER_NUM \
        --openai_key "$OPENAI_KEY" \
        --openai_model "$openai_model" > "$log_file" 2>&1
      
      echo "Experiment completed; log saved to: $log_file"
      echo "======================="
    done
  done
done

echo "All experiments completed!"
echo "Results are saved in respective output directories"
echo "Logs are saved in: $LOG_DIR"
