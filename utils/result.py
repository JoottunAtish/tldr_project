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
    
    print(f"Results saved to {output_file}")

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
    
    print(f"Results saved to {output_file}")

def save_tls_filterer_results(num_of_ip_addresses, tls_1_3, tls_1_2, old_tls, output_file):
    if not os.path.exists(os.path.dirname(output_file)):
        os.makedirs(os.path.dirname(output_file))
    result = {
        "total_ip_addresses_checked": num_of_ip_addresses,
        "total_tls_1_3": len(tls_1_3),
        "total_tls_1_2": len(tls_1_2),
        "total_old_tls": len(old_tls),
        "tls_1_3": tls_1_3,
        "tls_1_2": tls_1_2,
        "old_tls": old_tls
    }

    with open(output_file, 'w') as f:
        json.dump(result, f)
    
    print(f"Results saved to {output_file}")