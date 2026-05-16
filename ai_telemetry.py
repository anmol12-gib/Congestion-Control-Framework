import time
import random
import plotext as plt

queue_data = []
latency_data = []

print("==================================================")
print("  INITIALIZING LIVE 6G TELEMETRY DASHBOARD")
print("==================================================")
time.sleep(2)

try:
    for i in range(1, 1000):
        # Simulated extraction from the 6G Token Bucket Filter
        queue_size = random.uniform(10.0, 32.0)
        latency = random.uniform(20.0, 45.0)
        
        queue_data.append(queue_size)
        latency_data.append(latency)
        
        if len(queue_data) > 30:
            queue_data.pop(0)
            latency_data.pop(0)
            
        # The AI Trigger Logic
        if queue_size > 28.0 and latency > 40.0:
            action = "[[ THROTTLE_SOURCE ACTIVE ]]"
        else:
            action = "MAINTAIN_FLOW"

        plt.clc() 
        plt.subplots(2, 1) 
        
        plt.subplot(1, 1)
        plt.plot(queue_data, marker="dot")
        plt.title(f"Live Queue Size (KB) | Status: {action}")
        plt.ylim(0, 35)
        
        plt.subplot(2, 1)
        plt.plot(latency_data, marker="dot")
        plt.title("Live Latency (ms)")
        plt.ylim(0, 50)
        
        plt.show()
        time.sleep(1)
            
except KeyboardInterrupt:
    print("\n[*] Live Dashboard safely terminated.")