import nmap3
import concurrent.futures
import threading
import os
import json
from utils.result import save_ip_validator_results
from utils.checkpoint import save_ip_validator_checkpoint
from utils.fix_bleeding import fix_bleeding


def start_resume_ip_validator(ip_addresses, num_of_threads, country_name, asn_details):
    chunk_size = num_of_threads
    """
    Makes use of a checkpoint system to keep tracks of already processed data
    in case of an issue such as a power-cut. 

    #### :Parameters
        ip_address: String

        num_of_threads: Integer
            Number of instances to create

        chunk_size: Integer
            Number of maximum data each instances can have

        country_name: String
    """
    chunk_size = num_of_threads

    checkpoint = f"checkpoints/{country_name}/ip_validator_results.json"
    if not os.path.exists(checkpoint):
        process(ip_addresses, num_of_threads, chunk_size, checkpoint)
    else:
        with open(checkpoint, 'rb') as f:
            cp = json.loads(f)
            cp_valid_ip_addresses = cp["valid_ip_addresses"]
            cp_invalid_ip_addresses = cp["invalid_ip_addresses"]
           
            _remaining_ip_addresses = list(set((ip['ip_address'], ip['netname']) for ip in ip_addresses) - set((ip['ip_address'], ip['netname']) for ip in cp_valid_ip_addresses) - set((ip['ip_address'], ip['netname']) for ip in cp_invalid_ip_addresses))
            remaining_ip_addresses = [{'ip_address': ip[0], 'netname': ip[1]} for ip in _remaining_ip_addresses]
            
            _remaining_ip_addresses = None
            
            process(remaining_ip_addresses, num_of_threads, chunk_size, checkpoint, cp_valid_ip_addresses, cp_invalid_ip_addresses)
            
            cp = None
            cp_valid_ip_addresses = None
            cp_invalid_ip_addresses = None
            remaining_ip_addresses = None
            
    valid_ip_addresses = fix_bleeding(country_name, asn_details)
    save_ip_validator_results(len(ip_addresses), valid_ip_addresses, f"results/{country_name}/ip_validator_results.json")
    return valid_ip_addresses

def process(ip_addresses, num_of_threads, chunk_size, checkpoint, valid_ip_addresses=[], invalid_ip_addresses=[], country_name = None):
    number_of_ip_addresses = len(ip_addresses)
    progress_lock = threading.Lock()
    valid_ip_addresses_lock = threading.Lock()
    invalid_ip_addresses_lock = threading.Lock()
    progress_denominator = len(valid_ip_addresses) + len(invalid_ip_addresses) + number_of_ip_addresses
    progress = [len(valid_ip_addresses) + len(invalid_ip_addresses)]

    for i in range(0, number_of_ip_addresses, chunk_size):
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_of_threads) as executor:
            futures = {executor.submit(validate_ip_address, ip['ip_address'], progress_denominator, progress_lock, progress, country_name=country_name): ip for ip in ip_addresses[i:i+chunk_size]}
            
            for future in concurrent.futures.as_completed(futures):
                ip = futures[future]
                try:
                    if future.result():
                        # print(f"{ip} is valid\n")
                        with valid_ip_addresses_lock:
                            valid_ip_addresses.append(ip)
                    else:
                        # print(f"{ip} is invalid\n")
                        with invalid_ip_addresses_lock:
                            invalid_ip_addresses.append(ip)
                except Exception as e:
                    # print(f"{ip} is invalid: {e}\n")
                    with invalid_ip_addresses_lock:
                        invalid_ip_addresses.append(ip)
        
        save_ip_validator_checkpoint(valid_ip_addresses, invalid_ip_addresses, checkpoint)
    save_ip_validator_checkpoint(valid_ip_addresses, invalid_ip_addresses, checkpoint)

def validate_ip_address(ip, number_of_ip_addresses, progress_lock, progress, country_name=None):
    nmap = nmap3.Nmap()
    

    try:
        result_dict = nmap.scan_top_ports(ip, args="-p 443 -Pn")

        isPortID443 = result_dict[ip]["ports"][0]["portid"] == "443"
        isStateOpen = result_dict[ip]["ports"][0]["state"] == "open"
        isStateUp = result_dict[ip]["state"]["state"] == "up"

        valid = isPortID443 and isStateOpen and isStateUp
        with open ('ValidIPs.json','w') as ValidFile:
            json.dump(ip,ValidFile)
           
    
    except Exception as e:
        valid = False

    with progress_lock:
        os.system('clear')
        progress[0] += 1
        print(f"Checkpoint at Checkpoints/{country_name}/ip_validator_results.json\nTotal IP address: \t{number_of_ip_addresses}\nIP Addresses Scanned: \t{progress[0]}\n{progress_bar(progress[0], number_of_ip_addresses, 100)}")
        
    return valid

def progress_bar(current, total, bar_length=100):
    fraction = current / total
    arrow = int(fraction * bar_length - 1) * '#'
    padding = int(bar_length - len(arrow)) * ' '

    return (f'Progress: [{arrow}{padding}] {fraction * 100:.2f}% {'\n' if current == total else '\r'}')