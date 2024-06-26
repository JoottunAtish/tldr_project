import concurrent.futures, os, json
from configurations.tldr_fail_test import tldr_dectector
from utils.checkpoint import save_tldr_checkpoint
from utils.result import save_tldr_results
from utils.fix_bleeding import fix_bleeding_tldr_anomaly
import threading


def tldr_process(ip_addresses, num_of_threads, chunk_size, countryname, version,  Processed_ip_addresses = {}, asndetails = None):
    """
    This function make use of parallel computing to speed up the process which calls 
    the tldr_detector function.

    #### :Parameters
        ip_address: string

        num_of_threads: integer
            Number of instances to create

        chunck_size: integer
            The number of IPs of each instance

        Processed_ip_address : list
            By default, the list is empty.
    """
    num_processed_ip = sum(len(Processed_ip_addresses[key]) for key in Processed_ip_addresses)
    progress = [num_processed_ip]
    progress_lock = threading.Lock()
    number_of_ip_addresses = len(ip_addresses) + num_processed_ip
    checkpoint = f"checkpoints/{countryname}/tldr_process_{version}_results.json"
    processed_ip_addresses_lock = threading.Lock()
    
    for i in range(0, number_of_ip_addresses, chunk_size):
        with concurrent.futures.ThreadPoolExecutor(num_of_threads) as executor:
            futures = {executor.submit(tldr_dectector, ip["ip_address"], timeout=30, netname=ip["netname"]): ip for ip in ip_addresses[i:i+chunk_size]}
            for future in concurrent.futures.as_completed(futures):                
                try:
                    dict, binary_encoding = future.result()
                    with processed_ip_addresses_lock:
                        Processed_ip_addresses[binary_encoding].append(dict)
                except Exception as e:
                    print(e)
                    dict, binary_encoding = future.result()
                    with processed_ip_addresses_lock:
                        Processed_ip_addresses[binary_encoding].append(dict)
                with progress_lock:
                    progress[0] += 1
                
                os.system('clear')
                print(f"Checkpoint at Checkpoints/{countryname}/tldr_process_{version}_results.json\nTotal IP address: \t{number_of_ip_addresses}\nIP Addresses Scanned: \t{progress[0]}\n{progress_bar(progress[0], number_of_ip_addresses, 100)}")
        
        # list_ip = [list(ip.values())[0] for ip in Processed_ip_addresses]
        # list_encoding = [list(binary.keys())[0] for binary in Processed_ip_addresses]
             
        save_tldr_checkpoint(Processed_ip_addresses, checkpoint)
    save_tldr_checkpoint(Processed_ip_addresses, checkpoint)
    fix_bleeding_tldr_anomaly(asndetails, checkpoint)
    save_tldr_results(number_of_ip_addresses, Processed_ip_addresses, f"results/{countryname}/tldr_process_{version}_results.json")
    

def resume_tldr_process(ip_address, num_of_threads, chunk_size, countryname, asndetails, version):
    checkpoint = f"checkpoints/{countryname}/tldr_process_{version}_results.json"
    dict = {
        "0000": [],
        "0001": [],
        "0010": [],
        "0011": [],
        "0100": [],
        "0101": [],
        "0110": [],
        "0111": [],
        "1000": [],
        "1001": [],
        "1010": [],
        "1011": [],
        "1100": [],
        "1101": [],
        "1110": [],
        "1111": []
    }
    
    if not os.path.exists(checkpoint):
        tldr_process(ip_address, num_of_threads,version=version, chunk_size=chunk_size, countryname=countryname, Processed_ip_addresses=dict, asndetails=asndetails)
    else:
        with open(checkpoint, "rb") as f:
            cp= json.load(f)
            cp_ip_addresses_encoding = cp["ip_addresses_encoding"]
            cp_ip_addresses_without_key = set((ip["ip_address"], ip["netname"]) for key in cp_ip_addresses_encoding for ip in cp_ip_addresses_encoding[key])
            
            _remaining_ip_addresses = list(set((ip['ip_address'], ip['netname']) for ip in ip_address) - cp_ip_addresses_without_key)
            remaining_ip_addresses = [{'ip_address': ip[0], 'netname': ip[1]} for ip in _remaining_ip_addresses]
                        
            tldr_process(remaining_ip_addresses, num_of_threads, chunk_size, countryname,version, cp_ip_addresses_encoding, asndetails)


def progress_bar(current, total, bar_length=100):
    fraction = current / total

    arrow = int(fraction * bar_length - 1) * '#'
    padding = int(bar_length - len(arrow)) * ' '

    return (f'Progress: [{arrow}{padding}] {fraction * 100:.2f}% ') + ('\n' if current == total else '\r')


# # Given test data
# ip = ['8.8.8.8', '192.168.100.1', '164.234.65.57', '197.64.102.55']

# # example of output
# stuff = [{'1111': '8.8.8.8'}, {'0000': '192.168.100.1'}, {'0000': '164.234.65.57'}, {'0000': '197.64.102.55'}]

# # get the Ip address
# ip_address = [list(d.values())[0] for d in stuff]

# # Get the Binary encoding
# ip_address = [list(d.keys())[0] for d in stuff]
