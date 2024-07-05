from configurations.ip_validator import start_resume_ip_validator
from configurations.ip_collector import start_resume_retrieve_asn_details, ip_prefix_to_list
from configurations.tls_filterer import start_resume_tls_filterer
from utils.read_results import read_ip_validator_results, read_tls_filterer_results
from configurations.tldr_anomaly_detector import resume_tldr_process
import json



asn_details_grouped_by_country = start_resume_retrieve_asn_details()

list_of_country = [
    # "Algeria",
    # "Benin",
    # "Burundi",
    # "Central African Republic",
    # "Mauritius",
    # "Mozambique",
    # "Niger",
    # "Rwanda",
    # "Djibouti",
    # "Eritrea",
    # "Angola",
    # "Equatorial Guinea",
    # "Senegal",
    # "Liberia",
    # "Somali",
    # "Guinea",
    # "Chad",
    # "Congo"
    
    # Poshan
    
    "Botswana",
    "Burkina Faso",
    "Cameroon",
    "Comoros",
    "Côte d'Ivoire",
    "Eswatini",
    "Ethiopia",
    
    "Gambia",
    "Ghana",
    "Kenya",
    "Lesotho",
    "Libya",
    "Madagascar",
    "Malawi",
    
    # # Atish
    
    # "Mali",
    # "Namibia",
    # "Nigeria",
    # "Réunion",
    # "Seychelles",
    # "Sierra Leone",
    # "Somalia",
    
    # Kevin
    
    "South Sudan",
    "Sudan",
    "Tanzania, United Republic of",
    "Uganda",
    "Zambia",
    "Zimbabwe",
    "Congo, The Democratic Republic of the",
    
    #"Gabon"
    "Cabo Verde",
    "Sao Tome and Principe",
    "Indonesia",
    "Togo"
    
    # DONT TOUCH THIS ONE
    # "Egypt"
]

for country, asn_details in asn_details_grouped_by_country.items():
    if country in list_of_country:
        ip_addresses = []
        for asn_detail in asn_details:
            ip_prefixes = asn_detail["inetnums"]
            netname = asn_detail["netname"]
            for ip_prefix in ip_prefixes:
                ip_addresses.extend(ip_prefix_to_list(ip_prefix, netname))
        ip_addresses = list({'ip_address': _ip[0], 'netname': _ip[1]} for _ip in set((ip['ip_address'], ip['netname']) for ip in ip_addresses))
        
            
        print(f"Processing {country}, {len(ip_addresses)} IP Addresses")

        start_resume_ip_validator(ip_addresses, num_of_threads=512, country_name=country, asn_details=asn_details)
        valid_ip_addresses = read_ip_validator_results(country)
        
        start_resume_tls_filterer(valid_ip_addresses, num_of_threads=512, country_name=country, asn_details=asn_details)
        
        tlsv1_2 = read_tls_filterer_results(country, "tls_1_2")
        tlsv1_3 = read_tls_filterer_results(country, "tls_1_3")

        # # scanning for TLS1.3
        resume_tldr_process(ip_address=tlsv1_3, num_of_threads=512, chunk_size=512, countryname=country, asndetails=asn_details, version="v1.3")
        
        # # # scanning for TLS1.2
        resume_tldr_process(ip_address=tlsv1_2, num_of_threads=512, chunk_size=512, countryname=country, asndetails=asn_details, version="v1.2")

print("Process finished!")
