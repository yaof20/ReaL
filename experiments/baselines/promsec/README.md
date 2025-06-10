# PromSec: Prompt Optimization for Secure Generation of Functional Source Code with Large Language Models (LLMs)

## Setup (Added by ReaL)

- Follow the setup guide of the official promsec repo as below.

- Prepare the code you want to process in promsec with `.py` format. 
(Examples provided in /sql0.5b, /sql3b and /sql7b)

## Usage (Added by ReaL)

Here is an example command to run promsec.

```
bash demo_real.sh
```
where, `demo_real.py` is modified from `Demo_PromSec_PoC_Oct_2024_public.ipynb` in the repo of promsec.

## Overview

This repository contains a demo implementation code for the paper:

*M. Nazzal, I. Khalil, A. Khreishah, and N.H. Phan, "PromSec: Prompt Optimization for Secure Generation of Functional Source Code with Large Language Models (LLMs)," Accepted for presentation at the 31st ACM Conference on Computer and Communications Security (CCS 2024), Salt Lake City, UT, USA, Oct. 2024.*

PromSec is a novel approach that ustilizes graph-based Generative Adversarial Networks (gGANs) and Large Language Models (LLMs) to generate secure and functional source code.

## Key Features

- Implementation of a graph-based Generative Adversarial Network (gGAN)
- Integration with OpenAI's GPT model for code generation
- Control Flow Graph (CFG) generation and analysis
- Vulnerability assessment using Bandit
- Iterative code improvement process

## Requirements

- Python 3.x
- PyTorch
- PyTorch Geometric
- NetworkX
- Matplotlib
- OpenAI API
- Bandit

## Setup

1. Clone this repository
2. Install the required packages

## Key Components

- `Generator` and `Discriminator` classes for the gGAN
- CFG generation functions
- Code vulnerability scanning using Bandit
- Iterative code improvement process
- Visualization of results

## Results

The code generates various plots and statistics, including:
- CWE counts per code base
- CWE ID histograms
- Iteration count for code cleansing
- Remaining CWEs after iterations

Results are saved in a designated folder with timestamp.

## Citation

If you use this code in your research, please cite our paper:
@inproceedings{nazzal2024promsec, title={PromSec: Prompt Optimization for Secure Generation of Functional Source Code with Large Language Models (LLMs)}, author={Nazzal, Mahmoud and Khalil, Issa and Khreishah, Abdallah and Phan, Nguyen H}, booktitle={Proceedings of the 31st ACM Conference on Computer and Communications Security (CCS)}, year={2024}, address={Salt Lake City, UT, USA} }

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

MIT License

Copyright (c) 2024 Mahmoud Nazzal

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Contact

For any questions or issues, please contact Mahmoud Nazzal at mn69@njit.edu.

