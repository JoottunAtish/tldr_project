from configurations.ip_validator import start_resume_ip_validator
from configurations.ip_collector import start_resume_retrieve_asn_details, get_ip_addresses
from configurations.tls_filterer import tls_version_check
import json


asn_details_grouped_by_country = start_resume_retrieve_asn_details()

list_of_country = [
    "Tunisia"
]

for country, asn_details in asn_details_grouped_by_country.items():
    if country in list_of_country:
        ip_addresses = get_ip_addresses(asn_details=asn_details)
        print(f"Processing {country}, {len(ip_addresses)} IP Addresses")

        start_resume_ip_validator(ip_addresses, num_of_threads=512, country_name=country)    


        


#reading from validate_ip_address the .json file created

f=open('ValidIPs.json')

data = json.load(f)
f.close()

for ips in ["8.8.8.8","157.240.192.24"]:
    ipLists= ips
    validportnum= "443"

    try:
        ipversion=tls_version_check(ips,validportnum)  
        print(ipversion)
        
        with open(f"ipaddresses_with_{ipversion}.json","a") as jsonfile:
            json.dump(ips,jsonfile)        
    except (RuntimeError):  
        with open("/IPAddress_with_oldertls.json",'w') as jsonfile:
            json.dump(ips,jsonfile)
            print ("success 3")
