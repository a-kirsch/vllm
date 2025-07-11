# VLLM Local Usage Documentation

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Problems](#problems)

---

## Installation

### Download Model

1. Create a **read token** on [Hugging Face](https://huggingface.co/settings/tokens) in **Access Tokens** → **Create Token**
2. Log in to your account in the terminal:

    ```bash
    huggingface-cli login
    ```

3. Download an OpenAI-compatible model locally. Specify the model, directory, and set use-symlinks to false. For example:

    ```bash
    huggingface-cli download mistralai/Mistral-7B-Instruct-v0.3 \
      --local-dir /home/beams/AKIRSCH/rareevent/vllm/Mistral-7B-Instruct-v0.3 \
      --local-dir-use-symlinks False
    ```

---

## Usage

### Launch VLLM Server

4. Create a Bash script and specify the endpoint, model, port, host, and datatype. For example:

    ```bash
    #!/bin/bash

    export CUDA_VISIBLE_DEVICES=1

    python -m vllm.entrypoints.openai.api_server \
      --model /home/beams/AKIRSCH/rareevent/vllm/Mistral-7B-Instruct-v0.3 \
      --port 8000 \
      --host 0.0.0.0 \
      --dtype auto
    ```

> This exposes an OpenAI-compatible API at:  
> `http://localhost:8000/v1/chat/completions`

---

### Connect Cline to Local Endpoint

5. In Cline, go to **Settings** → **API Configuration**.
6. Set **API Provider** to `OpenAI Compatible`.
7. Set **Base URL** to:

    ```
    http://localhost:8000/v1
    ```

8. Leave **Model ID** and **API Key** **blank** — VLLM will use the single loaded model by default.

---

### Run the Model

9. Run the VLLM server script and begin chatting in Cline using your local model.

---

## Problems

### Too Many Tokens

If you receive errors like:
ValueError: This model's maximum context length is 8192 tokens. However, you requested 13553 tokens in the messages...

Try the following:
- Use a model with a larger context window
- Restart Cline to clear chat history.
- Shorten the conversation or set `max_tokens` in advanced settings.

---