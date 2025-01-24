def detect_anomaly(input: str) -> str:
    # Simple simulation of neural model
    if "failed login" in input.lower():
        return "Anomaly detected: Unusual login attempts"
    return "No anomaly detected"
