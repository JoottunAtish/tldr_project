from configurations.ip_validator import start_resume_ip_validator
from configurations.ip_collector import start_resume_retrieve_asn_details, ip_prefix_to_list

asn_details_grouped_by_country = start_resume_retrieve_asn_details()

list_of_country = [
    "Cameroon",
    "Comoros",
    "Malawi",
    "Côte d'Ivoire",
    "Zambia",
    "Botswana",
    "Sudan",
    "Ethiopia",
    "Gambia",
    "Burkina Faso",
    "Namibia",
    "Réunion",
    "South Sudan",
    "Congo, The Democratic Republic of the",
    "Uganda",
    "Madagascar",
    "Sierra Leone",
    "Libya",
    "Benin"
]

for country, asn_details in asn_details_grouped_by_country.items():
    
    if country in list_of_country:
        ip_addresses = []
        for asn_detail in asn_details:
            ip_prefixes = asn_detail["inetnums"]
            netname = asn_detail["netname"]
            for ip_prefix in ip_prefixes:
                ip_addresses.extend(ip_prefix_to_list(ip_prefix, netname))
        print(f"Processing {country}, {len(ip_addresses)} IP Addresses")
        start_resume_ip_validator(ip_addresses, num_of_threads=512, chunk_size=512, country_name=country) 

