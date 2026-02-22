import ipaddress

def check_private_ip(ip):
  try:
      ip_obj = ipaddress.ip_address(ip)
      return ip_obj.is_private
  except ValueError:   
        return False
    
ip = "172.16.212.198"
print(f"IS {ip} a private IP? {check_private_ip(ip)}")
    
    #source code --> 2.py