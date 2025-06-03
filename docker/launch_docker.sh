#!/usr/bin/env bash
# Docker container launcher script for the project
# Usage: bash ./launch_docker.sh

set -e

# Get the absolute path of the project directory
project_dir=$(realpath "$(dirname "$(pwd)")")
docker_image="fengyao1909/real:v1.0"

echo "🚀 Launching Docker container..."
echo "📦 Using Docker image: ${docker_image}"
echo "📂 Mounting project directory: ${project_dir}"

# Run the Docker container with proper configuration
docker run \
    --gpus all \
    --name real \
    --rm \
    --shm-size=10g \
    --ipc=host \
    --ulimit memlock=-1 \
    --ulimit stack=67108864 \
    -v "${project_dir}/:/workspace" \
    -e NCCL_P2P_LEVEL=NVL \
    -it "${docker_image}"