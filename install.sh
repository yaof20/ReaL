pip install -e .

pip install torch==2.4.0 torchvision==0.19.0 torchaudio==2.4.0 --index-url https://download.pytorch.org/whl/cu124
pip install --no-cache-dir \
    accelerate \
    codetiming \
    datasets \
    dill \
    hydra-core \
    numpy \
    pybind11 \
    tensordict \
    "transformers<=4.46.0"\
    mypy \
    astunparse \
    sqlparse \
    fire
    
pip install --no-cache-dir vllm==0.6.3
pip install --no-cache-dir --no-build-isolation flash-attn==2.7.0.post2
pip install wandb==0.18.7 py-spy
pip install peft==0.14.0
