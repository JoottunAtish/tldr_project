import socket
import ssl
import os
import json
import concurrent.futures
import threading
from utils.result import save_tls_filterer_results
from utils.checkpoint import save_tls_filterer_checkpoint
from utils.fix_bleeding import fix_bleeding_tls_filterer

def start_resume_tls_filterer(ip_addresses, num_of_threads, country_name, asn_details):
    chunk_size = num_of_threads


    checkpoint = f"checkpoints/{country_name}/tls_filterer_results.json"
    if not os.path.exists(checkpoint):
        process(ip_addresses, num_of_threads, chunk_size, checkpoint, country_name=country_name)
    else:
        with open(checkpoint, 'rb') as f:
            cp = json.load(f)
            cp_tls_1_3 = cp["tls_1_3"]
            cp_tls_1_2 = cp["tls_1_2"]
            cp_old_tls = cp["old_tls"]
            
            _remaining_ip_addresses = list(set((ip['ip_address'], ip['netname']) for ip in ip_addresses) - set((ip['ip_address'], ip['netname']) for ip in cp_tls_1_3) - set((ip['ip_address'], ip['netname']) for ip in cp_tls_1_2) - set((ip['ip_address'], ip['netname']) for ip in cp_old_tls))
            remaining_ip_addresses = [{'ip_address': ip[0], 'netname': ip[1]} for ip in _remaining_ip_addresses]
            
            _remaining_ip_addresses = None
            
            process(remaining_ip_addresses, num_of_threads, chunk_size, checkpoint, cp_tls_1_3, cp_tls_1_2, cp_old_tls, country_name=country_name)
            
            cp = None
            cp_tls_1_3 = None
            cp_tls_1_2 = None
            cp_old_tls = None
            remaining_ip_addresses = None
            
    tlsv1_3, tlsv1_2, tlsvOld = fix_bleeding_tls_filterer(country_name, asn_details)
    save_tls_filterer_results(len(ip_addresses), tlsv1_3, tlsv1_2, tlsvOld, f"results/{country_name}/tls_filterer_results.json")
    return tlsv1_3, tlsv1_2, tlsvOld

def process(ip_addresses, num_of_threads, chunk_size, checkpoint, tls_1_3=[], tls_1_2=[], old_tls=[], country_name = None):
    number_of_ip_addresses = len(ip_addresses)
    progress_lock = threading.Lock()
    tls_1_3_lock = threading.Lock()
    tls_1_2_lock = threading.Lock()
    old_tls_lock = threading.Lock()
    progress_denominator = len(tls_1_3) + len(tls_1_2) + len(old_tls) + number_of_ip_addresses
    progress = [len(tls_1_3) + len(tls_1_2) + len(old_tls)]

    for i in range(0, number_of_ip_addresses, chunk_size):
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_of_threads) as executor:
            futures = {executor.submit(tls_version_check, ip['ip_address'], progress_denominator, 443, progress_lock, progress, country_name=country_name): ip for ip in ip_addresses[i:i+chunk_size]}
            
            for future in concurrent.futures.as_completed(futures):
                ip = futures[future]
                try:
                    ipversion = future.result()
                    if ipversion == "TLSv1.3":
                        with tls_1_3_lock:
                            tls_1_3.append(ip)
                    elif ipversion == "TLSv1.2":
                        with tls_1_2_lock:
                            tls_1_2.append(ip)
                    else:
                        with old_tls_lock:
                            old_tls.append(ip)
                except Exception as e:
                    with old_tls_lock:
                        old_tls.append(ip)
        
        save_tls_filterer_checkpoint(tls_1_3, tls_1_2, old_tls, checkpoint)



def tls_version_check(ip_address, number_of_ip_addresses, port, progress_lock, progress, country_name=None):
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    with socket.create_connection(address=(ip_address, port), timeout=30) as sock:
        with context.wrap_socket(sock, server_hostname=ip_address) as ssock:
            with progress_lock:
                os.system("clear")
                progress[0] += 1
                print(f"Checkpoint at Checkpoints/{country_name}/tls_filterer_results.json\nTotal IP address: \t{number_of_ip_addresses}\nIP Addresses Scanned: \t{progress[0]}\n{progress_bar(progress[0], number_of_ip_addresses, 100)}")
            return ssock.version()
        
def progress_bar(current, total, bar_length=100):
    fraction = current / total

    arrow = int(fraction * bar_length - 1) * '#'
    padding = int(bar_length - len(arrow)) * ' '

    return (f'Progress: [{arrow}{padding}] {fraction * 100:.2f}% ') + ('\n' if current == total else '\r')