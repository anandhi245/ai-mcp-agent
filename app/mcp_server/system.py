import random

def get_system_status():
    return {
        "cpu_usage": f"{random.randint(20,80)}%",
        "memory_usage": f"{random.randint(30,70)}%",
        "status": "Running"
    }