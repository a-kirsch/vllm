from vllm import LLM, SamplingParams
from prometheus_client import Counter, Histogram, start_http_server
import time

# Start Prometheus metrics server on port 8000
start_http_server(8000)

# Prometheus metrics
INFERENCE_COUNT = Counter("inference_requests_total", "Total number of inference requests")
INFERENCE_LATENCY = Histogram("inference_latency_seconds", "Inference latency in seconds")


# Choose your model, currently using facebook/opt-125m
model = "facebook/opt-125m"

'''
Parameters for sampling
temperature determines the randomness of the output
top_p controls the diversity of the output
max_tokens limits the length of the generated response
'''
sampling_params = SamplingParams(temperature = 0.4, top_p = 0.95, max_tokens= 100)
llm = LLM(model = model)

print("Chat session started. Type 'exit' to quit.")

# Chat loop
while True:
    user_input = input("You: ")
    if user_input.lower() in {"exit", "quit"}:
        print("Exiting chat.")
        break

    INFERENCE_COUNT.inc()
    start_time = time.time()

    responses = llm.generate([user_input], sampling_params)

    latency = time.time() - start_time
    INFERENCE_LATENCY.observe(latency)

    for response in responses:
        print("Chat Bot:", response.outputs[0].text.strip())