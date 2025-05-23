# Copyright 2024 Bytedance Ltd. and/or its affiliates
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re
import asyncio
from CodeShield.insecure_code_detector import insecure_code_detector
from CodeShield.insecure_code_detector.languages import Language

def extract_content_in_code_blocks(input: str) -> list[str]:
    # Using regular expression to find content between code blocks ```
    return re.findall(r"```(.*?)```", input, re.DOTALL)

lang_dict = {
    'c': Language.C,
    'cpp': Language.CPP,
    'csharp': Language.CSHARP,
    'javascript': Language.JAVASCRIPT,
    'java': Language.JAVA,
    'rust': Language.RUST,
    'php': Language.PHP,
    'python': Language.PYTHON
}



def compute_score(solution_str, extra_info=None):
    """The scoring function for GoReasoner.

    Reference: Trung, Luong, et al. "Reft: Reasoning with reinforced fine-tuning." Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers). 2024.

    Args:
        solution_str: the solution text
        ground_truth: the ground truth
        method: the method to extract the solution, choices are 'strict' and 'flexible'
        format_score: the score for the format
        score: the score for the correct answer
    """
    extracted = extract_content_in_code_blocks(solution_str)

    if len(extracted) == 0:
        return -1
    else:
        code = extracted[0]
        lang = lang_dict[extra_info['language']]
        result = asyncio.run(insecure_code_detector.analyze(lang, code, code_before=None))
        if len(result) == 0:
            return 1.0
        else:
            return 1 - len(result) * 0.2