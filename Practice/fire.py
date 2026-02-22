# firewall.py

import math
from scapy.all import sniff, IP, TCP, UDP
import datetime

# ====== 1. Rule set: IPs/Ports to block ======
BLOCKED_IPS = ["192.168.1.10"]
BLOCKED_PORTS = [22, 23, 445]
BLOCKED_PROTOCOLS = ["TCP", "UDP"]

# ====== 2. Logging function ======
def log_packet(pkt, reason):
    log_entry = f"[{datetime.datetime.now()}] BLOCKED: {reason} - {pkt.summary()}\n"
    with open("firewall_log.txt", "a") as f:
        f.write(log_entry)
    print(log_entry.strip())

# ====== 3. Packet filtering logic ======
def packet_callback(pkt):
    if IP in pkt:
        src_ip = pkt[IP].src
        proto = pkt.proto

        if src_ip in BLOCKED_IPS:
            log_packet(pkt, f"Blocked IP {src_ip}")
            return

        if TCP in pkt:
            sport = pkt[TCP].sport
            if sport in BLOCKED_PORTS:
                log_packet(pkt, f"Blocked TCP port {sport}")
                return

        if UDP in pkt:
            dport = pkt[UDP].dport
            if dport in BLOCKED_PORTS:
                log_packet(pkt, f"Blocked UDP port {dport}")
                return

# ====== 4. Start sniffing ======
print("[*] Firewall is running. Monitoring traffic...")
sniff(prn=packet_callback, store=0)
# Note: This code is for educational purposes only. Use responsibly and ethically.