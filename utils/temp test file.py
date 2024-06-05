import ipaddress

def ip_prefix_to_list(ip_prefix):
    """
    Convert an IP prefix (CIDR notation) to a list of IP addresses.
    
    Args:
    - ip_prefix (str): IP prefix in CIDR notation (e.g., '192.0.2.0/24').
    
    Returns:
    - list: List of IP addresses within the IP prefix.
    """
    ip_list = []
    network = ipaddress.ip_network(ip_prefix)
    for ip in network:
        ip_list.append(str(ip))
    return ip_list

ip_prefix = "192.0.2.0/24"
ip_list = ip_prefix_to_list(ip_prefix)
print(ip_list)