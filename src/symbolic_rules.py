def apply_rules(log_entry: str, anomaly_result: str) -> str:
    # Apply symbolic rules
    if "192.168" in log_entry and "anomaly detected" in anomaly_result.lower():
        return "Rule matched: Suspicious IP activity"
    elif "port scan" in log_entry:
        return "Rule matched: Potential scanning activity"
    return "No rule matched"