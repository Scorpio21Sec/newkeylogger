import socket
import struct
import os

def block_ip(ip):
    print(f"Blocking IP: {ip}")
    os.system(f"iptables -A INPUT -s {ip} -j DROP")

def monitor_traffic():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        sock.setblocking(True)  # Ensure blocking mode to avoid BlockingIOError
        while True:
            try:
                packet, addr = sock.recvfrom(65535)
                ip_header = packet[0:20]
                iph = struct.unpack('!BBHHHBBH4s4s', ip_header)
                src_ip = socket.inet_ntoa(iph[8])
                print(f"Detected connection from: {src_ip}")
                if src_ip.startswith("192.168."):
                    block_ip(src_ip)
            except BlockingIOError:
                continue  # Ignore the error and continue listening
    except KeyboardInterrupt:
        print("Firewall stopped.")
    except PermissionError:
        print("Run the script as root to capture packets.")

if __name__ == "__main__":
    monitor_traffic()
 