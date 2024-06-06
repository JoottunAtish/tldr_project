import concurrent.futures
from tldr_fail_test import tldr_dectector


def process(ip_addresses, num_of_threads, chunk_size, Processed_ip_addresses = []):
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

    number_of_ip_addresses = len(ip_addresses)

    for i in range(0, number_of_ip_addresses, chunk_size):
        with concurrent.futures.ThreadPoolExecutor(num_of_threads) as executor:
            futures = {executor.submit(tldr_dectector, ip): ip for ip in ip_addresses[i:i+chunk_size]}
            
            for future in concurrent.futures.as_completed(futures):
                BinaryEncoding = futures[future]
                try:
                    if future.result():
                        Processed_ip_addresses.append(BinaryEncoding)
                    else:
                        Processed_ip_addresses.append(BinaryEncoding)
                except Exception as e:
                    print(e)
                    Processed_ip_addresses.append(BinaryEncoding)

    return Processed_ip_addresses

