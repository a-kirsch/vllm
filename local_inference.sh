#!/bin/bash

# Optional: choose a specific GPU
export CUDA_VISIBLE_DEVICES=1

# Verify the chat template


# Start the OpenAI-compatible VLLM server
python -m vllm.entrypoints.openai.api_server \
  --model /home/beams/AKIRSCH/rareevent/vllm/Mistral-7B-Instruct-v0.3 \
  --port 8000 \
  --dtype auto \
  --host 0.0.0.0