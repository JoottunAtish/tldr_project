import nmap3
import concurrent.futures
import threading
import json
import os
from utils.result import save_ip_validator_results
from utils.checkpoint import save_ip_validator_checkpoint

def start_resume_ip_validator(ip_addresses, num_of_threads, chunk_size, country_name):
    checkpoint = f"checkpoints/{country_name}/ip_validator_results.json"
    if not os.path.exists(checkpoint):
        valid_ip_addresses = process(ip_addresses, num_of_threads, chunk_size, checkpoint)
    else:
        with open(checkpoint, 'r') as f:
            cp = json.load(f)
            cp_valid_ip_addresses = cp["valid_ip_addresses"]
            cp_invalid_ip_addresses = cp["invalid_ip_addresses"]
            
            remaining_ip_addresses = list(set(ip_addresses) - set(cp_valid_ip_addresses) - set(cp_invalid_ip_addresses))
            valid_ip_addresses = process(remaining_ip_addresses, num_of_threads, chunk_size, checkpoint, cp_valid_ip_addresses, cp_invalid_ip_addresses)
            cp = None
            cp_valid_ip_addresses = None
            cp_invalid_ip_addresses = None
            remaining_ip_addresses = None
    save_ip_validator_results(len(ip_addresses), valid_ip_addresses, f"results/{country_name}/ip_validator_results.json")
    return valid_ip_addresses

def process(ip_addresses, num_of_threads, chunk_size, checkpoint, valid_ip_addresses = [], invalid_ip_addresses = []):
    number_of_ip_addresses = len(ip_addresses)
    progress_lock = threading.Lock()
    progress_denominator = len(valid_ip_addresses) + len(invalid_ip_addresses) + number_of_ip_addresses
    progress = [len(valid_ip_addresses) + len(invalid_ip_addresses)]

    for i in range(0, number_of_ip_addresses, chunk_size):
        with concurrent.futures.ThreadPoolExecutor(num_of_threads) as executor:
            futures = {executor.submit(validate_ip_address, ip, progress_denominator, progress_lock, progress): ip for ip in ip_addresses[i:i+chunk_size]}
            
            for future in concurrent.futures.as_completed(futures):
                ip = futures[future]
                try:
                    if future.result():
                        print(f"{ip} is valid\n")
                        valid_ip_addresses.append(ip)
                    else:
                        print(f"{ip} is invalid\n")
                        invalid_ip_addresses.append(ip)
                except Exception as e:
                    print(f"{ip} is invalid: {e}\n")
                    invalid_ip_addresses.append(ip)
        
        save_ip_validator_checkpoint(valid_ip_addresses, invalid_ip_addresses, checkpoint)

    return valid_ip_addresses
    

def validate_ip_address(ip, number_of_ip_addresses, progress_lock, progress):
    nmap = nmap3.Nmap()
    try:
        result_dict = nmap.scan_top_ports(ip, args="-p 443 -Pn")

        isPortID443 = result_dict[ip]["ports"][0]["portid"] == "443"
        isStateOpen = result_dict[ip]["ports"][0]["state"] == "open"
        isStateUp = result_dict[ip]["state"]["state"] == "up"

        valid = isPortID443 and isStateOpen and isStateUp
        result_dict = None
    except Exception as e:
        valid = False
    
    nmap = None

    with progress_lock:
        progress[0] += 1
        print(f"{progress[0]/number_of_ip_addresses * 100:.2f}% complete")

    return valid