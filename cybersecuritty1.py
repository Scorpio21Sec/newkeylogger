import time
import random
import os
import sys

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def moving_cybersecurity_tools():
    tools = ["Firewall", "Antivirus", "SIEM", "IDS", "VPN", "Malware Scanner", "PenTesting"]
    positions = [random.randint(0, 20) for _ in tools]
    directions = [1] * len(tools)
    
    try:
        while True:
            clear_console()
            for i, tool in enumerate(tools):
                print(" " * positions[i] + tool)
                
                # Move tool
                if directions[i] == 1:
                    positions[i] += 1
                    if positions[i] >= 30:
                        directions[i] = -1
                else:
                    positions[i] -= 1
                    if positions[i] <= 0:
                        directions[i] = 1
            
            time.sleep(0.2)
    except KeyboardInterrupt:
        print("\nAnimation stopped.")
        StopAsyncIteration

if __name__ == "__main__":
    moving_cybersecurity_tools()
