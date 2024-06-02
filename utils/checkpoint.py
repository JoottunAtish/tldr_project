import json
import os

def save_ip_validator_checkpoint(valid_ip_addresses, invalid_ip_addresses, output_file):
    if not os.path.exists(os.path.dirname(output_file)):
        os.makedirs(os.path.dirname(output_file))
    result = {
        "valid_ip_addresses": valid_ip_addresses,
        "invalid_ip_addresses": invalid_ip_addresses
    }

    with open(output_file, 'w') as f:
        json.dump(result, f)
    
    print(f"Checkpoint saved to {output_file}")