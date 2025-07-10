#!/bin/bash

# Optional: choose a specific GPU
export CUDA_VISIBLE_DEVICES=1

# Verify the chat template
echo "Starting VLLM with chat template: /home/beams/AKIRSCH/rareevent/vllm/chat-template.jinja"


# Start the OpenAI-compatible VLLM server
python -m vllm.entrypoints.openai.api_server \
  --model /home/beams/AKIRSCH/rareevent/vllm/Llama-2-13B-GPTQ \
  --port 8000 \
  --dtype auto \
  --host 0.0.0.0 \
  --chat-template /home/beams/AKIRSCH/rareevent/vllm/chat-template.jinja
#   --metrics-port 8001