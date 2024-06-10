from configurations.ip_collector import ip_prefix_to_list
from utils.checkpoint import save_ip_validator_checkpoint
import json
import os


def fix_bleeding(country, asn_details):
    checkpoint = f"checkpoints/{country}/ip_validator_results.json"
    ip_addresses = []
    for asn_detail in asn_details:
        ip_prefixes = asn_detail["inetnums"]
        netname = asn_detail["netname"]
        for ip_prefix in ip_prefixes:
            ip_addresses.extend(ip_prefix_to_list(ip_prefix, netname))
    ip_addresses = set((ip['ip_address'], ip['netname']) for ip in ip_addresses)

    if not os.path.exists(checkpoint):
        return

    with open(checkpoint, "r") as f:
        data = json.load(f)
        valid_ip_addresses = set((ip['ip_address'], ip['netname']) for ip in data["valid_ip_addresses"])
        invalid_ip_addresses = set((ip['ip_address'], ip['netname']) for ip in data["invalid_ip_addresses"])

        valid_ip_addresses = valid_ip_addresses & ip_addresses
        invalid_ip_addresses = invalid_ip_addresses & ip_addresses

        valid_ip_addresses = list({'ip_address': ip[0], 'netname': ip[1]} for ip in valid_ip_addresses)
        invalid_ip_addresses = list({'ip_address': ip[0], 'netname': ip[1]} for ip in invalid_ip_addresses)

    save_ip_validator_checkpoint(valid_ip_addresses, invalid_ip_addresses, checkpoint)

    return valid_ip_addresses