from configurations.ip_validator import start_resume_ip_validator
from configurations.ip_collector import start_resume_retrieve_asn_details, ip_prefix_to_list

asn_details_grouped_by_country = start_resume_retrieve_asn_details()

for country, asn_details in asn_details_grouped_by_country.items():
    ip_addresses = []
    for asn_detail in asn_details:
        ip_prefixes = asn_detail["inetnums"]
        netname = asn_detail["netname"]
        for ip_prefix in ip_prefixes:
            ip_addresses.extend(ip_prefix_to_list(ip_prefix, netname))
    
    print(f"Total IP Addresses for {country}: {len(ip_addresses)}")
    
# ip_addresses = []
# valid_ip_addresses = start_resume_ip_validator(ip_addresses, num_of_threads=512, chunk_size=512, country_name="Mauritius")