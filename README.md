# REAL: Reinforcement rEwards from Automated program anaLysis

[![arXiv](https://img.shields.io/badge/arXiv-2505.22704v1-b31b1b.svg)](https://arxiv.org/abs/2505.22704)

This repository contains the official implementation of our paper:

> **Training Language Models to Generate Quality Code with Program Analysis Feedback**  
> Feng Yao*, Zilong Wang*, Liyuan Liu, Junxia Cui, Li Zhong, Xiaohan Fu, Haohui Mai, Vish Krishnan, Jianfeng Gao, Jingbo Shang  
> (*equal contribution)  
> [[arXiv]](https://arxiv.org/abs/2505.22704)

## 🔍 Overview

The rise of **[vibe coding](https://en.wikipedia.org/wiki/Vibe_coding)**—a term coined by [Andrej Karpathy](https://x.com/karpathy/status/1886192184808149383?lang=en)—has transformed software development by enabling individuals to generate code through natural language prompts. Tools like **[Cursor](https://www.cursor.com/)**, **[Replit](https://replit.com/)**, and **[ChatGPT](https://chatgpt.com/g/g-CfL5dQPbs-code-generator)** have made this approach accessible, allowing for rapid prototyping and democratizing coding for non-programmers.

However, while vibe coding excels in speed and functionality (e.g., passing unit tests), it often lacks the robustness required for production-level code—leading to critical issues in **security** (e.g., SQL injection) and **maintainability** (e.g., missing type annotations, poor structure).

**REAL** (Reinforcement rEwards from Automated program anaLysis) bridges this gap by integrating **automated program analysis** with **unit test feedback** during training. Unlike prior work focused only on correctness, REAL provides **reference-free**, **prompt-agnostic** rewards that explicitly incentivize the generation of **secure**, **clean**, and **production-quality** code.

> ✨ REAL makes vibe coding not just fast — but **safe**, **secure**, and **reliable**.

### ✅ Key Advantages of REAL in the Vibe Coding Era

- **Hybrid Reward System**: Combines static analysis (for security and maintainability) with dynamic unit testing (for correctness) to guide LLMs toward high-quality outputs.
- **Reference-Free Supervision**: No ground-truth labels or hand-crafted rules — models learn directly from automated analysis signals.
- **Scalability**: Supports LLMs from 0.5B to 7B (e.g., Qwen2.5) and integrates seamlessly with standard RL frameworks like PPO.
- **Enhanced Safety**: Targets real-world vulnerabilities using detectors for 17+ CWEs, and enforces best practices for long-term maintainability.

<p align="center">
  <img src="assets/real_framework.png" width="700" alt="REAL Framework Diagram"/>
</p>

We evaluate REAL on three enhanced benchmarks:
- **SafeSQL**: Realistic tasks designed to catch SQL injection flaws.
- **SecCodePLT+**: Code generation tasks with rich CWE coverage.
- **APPS+**: Classic algorithmic challenges augmented with static maintainability checks.

Across all settings, REAL consistently outperforms state-of-the-art baselines—enabling LLMs to write code that’s not just functional, but **secure and reliable by design**.


## 🚀 Key Components

- **Automated Feedback**: Leverages static program analysis (for security and maintainability) and dynamic unit testing (for correctness).
- **Reference-Free Training**: Reinforcement learning with hybrid rewards — no need for case-by-case human-labeled data for safety and security requirement.
- **Robust Evaluation Benchmarks**:
  - 🧪 **SafeSQL** – realistic SQL tasks with injection vulnerabilities.
  - 🔐 **SecCodePLT+** – security benchmark enhanced with 17+ CWE detectors.
  - 🔧 **APPS+** – maintainability-focused version of the APPS dataset with static analysis checks.
- **Scalable RL Setup**: Trained with PPO on Qwen2.5 models (0.5B–7B), using the [VeRL framework](https://github.com/volcengine/verl).

---
## 🛠️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/yaof20/ReaL.git  
cd ReaL
```

### 2. Create environment

We provide a conda environment file for easy setup, or alternatively, you can use Docker for a containerized environment.

### 3. Run experiments

#### SecCodePLT+


#### SafeSQL & APPS+

##### 1. Training

Run the training script for your target dataset and model size:

```bash
# For APPS+  
bash run/apps-code/hybrid-[0.5b|3b|7b].sh

# For SafeSQL  
bash run/safesql/hybrid-[0.5b|3b|7b].sh
```

> Checkpoints will be automatically saved to:  
> `checkpoints/[proj_name]/[exp_name]`

##### 2. Evaluation

Execute the evaluation pipeline after training:

```bash
# For APPS+
bash experiments/safesql_and_apps/apps_eval_main.sh [path_to_exp_dir] [sharded|single]

# For SafeSQL
bash experiments/safesql_and_apps/safesql_eval_main.sh [path_to_exp_dir] [sharded|single]
```

- Replace <code>[path_to_exp_dir]</code> with your checkpoint directory.
- Set the mode as <code>sharded</code> or <code>single</code> depending on whether your outputs are split across GPUs.

> ✅ The evaluation pipeline handles:
> - Checkpoint formatting  
> - Response generation  
> - End-to-end quality + functionality assessment
---

## 📜 Citation

If you find this work useful, please cite:

```bibtex
@misc{yao2025real,
  title={Training Language Models to Generate Quality Code with Program Analysis Feedback},
  author={Feng Yao and Zilong Wang and Liyuan Liu and Junxia Cui and Li Zhong and Xiaohan Fu and Haohui Mai and Vish Krishnan and Jianfeng Gao and Jingbo Shang},
  year={2025},
  eprint={2505.22704},
  archivePrefix={arXiv},
  primaryClass={cs.CL}
}
```

---

## 📬 Contact

For questions or contributions, feel free to open an issue or reach out to  
📧 [zlwang@ucsd.edu](mailto:zlwang@ucsd.edu)  
📧 [fengyao@ucsd.edu](mailto:fengyao@ucsd.edu)