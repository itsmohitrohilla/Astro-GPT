# REPLICATE_API_TOKEN=r8_LUMVOg124kRA1jxaeAxgX3tfY1Bdy2w1c4O8f

import os
import os
import replicate

# Replace with a text generation model available on Replicate
# The meta/meta-llama-3.1-405b-instruct model can stream output as it's running.
for event in replicate.stream(
    "meta/meta-llama-3.1-405b-instruct",
    input={
        "top_k": 50,
        "top_p": 0.9,
        "prompt": "what is the value of pi?",
        "max_tokens": 1024,
        "min_tokens": 0,
        "temperature": 2.0,
        "system_prompt": "You are a helpful assistant.",
        "presence_penalty": 0,
        "frequency_penalty": 0
    },
):
    print(str(event), end="")