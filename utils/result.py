import json
import os

def save_afrinic_asn_results(afrinic_asn_list, output_file):
    if not os.path.exists(os.path.dirname(output_file)):
        os.makedirs(os.path.dirname(output_file))
    result = {
        "afrinic_asn": afrinic_asn_list
    }

    with open(output_file, 'w') as f:
        json.dump(result, f)
    
    print(f"Results saved to {output_file}.")

def save_ip_validator_results(num_of_ip_addresses, valid_ip_addresses, output_file):
    if not os.path.exists(os.path.dirname(output_file)):
        os.makedirs(os.path.dirname(output_file))
    result = {
        "total_ip_addresses_checked": num_of_ip_addresses,
        "valid_ip_addresses_count": len(valid_ip_addresses),
        "valid_ip_addresses": valid_ip_addresses
    }

    with open(output_file, 'w') as f:
        json.dump(result, f)
    
    print(f"Results saved to {output_file}.")
    

def save_tldr_results(num_of_ip_addresses, list_ip, list_encoding, output_file):
    if not os.path.exists(os.path.dirname(output_file)):
        os.makedirs(os.path.dirname(output_file))
    
    results = {
        "total_ip_checked": num_of_ip_addresses,
        "ip_addresses": list_ip,
        "binary_encoding": list_encoding
    }
    
    with open(output_file, 'w') as f:
        json.dump(results, f)
    
    print(f"Results saved to {output_file}.")