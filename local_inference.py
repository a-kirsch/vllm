#Use available GPU for inference
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "1"


from vllm import LLM, SamplingParams
from prometheus_client import Gauge, Counter, Histogram, start_http_server
import time

# Start Prometheus metrics server on port 8000
start_http_server(8000)

# Prometheus metrics
# Counters
INFERENCE_COUNT = Counter(
    "inference_requests_total",
    "Total number of inference requests",
    ["model"]  # label by model name
)

# Histograms
INFERENCE_LATENCY = Histogram(
    "inference_latency_seconds",
    "Inference latency in seconds"
)

TOTAL_TOKENS = Histogram(
    "inference_total_tokens",
    "Total input + output tokens per request"
)

# Gauges (for current values)
TOKENS_INPUT = Gauge(
    "inference_input_tokens",
    "Number of input tokens per prompt"
)

TOKENS_OUTPUT = Gauge(
    "inference_output_tokens",
    "Number of output tokens per response"
)


# Choose your model, currently using Llama-2-13B-GPTQ
# model = "facebook/opt-125m"
# model = "tiiuae/falcon-rw-1b"
model = "/home/beams/AKIRSCH/rareevent/vllm/Llama-2-13B-GPTQ"

'''
Parameters for sampling
temperature determines the randomness of the output
top_p controls the diversity of the output
max_tokens limits the length of the generated response
'''
sampling_params = SamplingParams(temperature = 0.1, top_p = 0.95, max_tokens= 200)
llm = LLM(model = model)

print("Chat session started. Type 'exit' to quit.")

# Chat loop
while True:
    user_input = input("You: ")
    if user_input.lower() in {"exit", "quit"}:
        print("Exiting chat.")
        break

    # Track inference count with model label
    INFERENCE_COUNT.labels(model=model).inc()

    # Token counting (approximate, based on words)
    prompt_tokens = len(user_input.split())
    TOKENS_INPUT.set(prompt_tokens)

    # Measure latency
    start_time = time.time()
    responses = llm.generate([user_input], sampling_params)
    latency = time.time() - start_time
    INFERENCE_LATENCY.observe(latency)

    for response in responses:
        output_text = response.outputs[0].text.strip()
        print("Chat Bot:", output_text)

        # Approximate output token count
        output_tokens = len(output_text.split())
        TOKENS_OUTPUT.set(output_tokens)

        # Histogram of total tokens (prompt + output)
        TOTAL_TOKENS.observe(prompt_tokens + output_tokens)