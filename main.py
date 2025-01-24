import asyncio
from src.neural_model import detect_anomaly
from src.symbolic_rules import apply_rules
from src.response_generator import generate_response

# Simulated log entry
log_entry = "Failed login attempt detected from IP 192.168.1.100"

# Neural anomaly detection
anomaly_result = detect_anomaly(log_entry)
print(f"Anomaly Detection Result: {anomaly_result}")

# Apply symbolic rules
rule_result = apply_rules(log_entry, anomaly_result)
print(f"Rule Checking Result: {rule_result}")

# Generate a response using Semantic Kernel
response = asyncio.run(generate_response(anomaly_result, rule_result))
print(f"Generated Response:\n{response}")
