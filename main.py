from configurations.ip_validator import start_resume_ip_validator
from configurations.ip_collector import start_resume_retrieve_asn_details

asn_details = start_resume_retrieve_asn_details()

# group by country
asn_details_by_country = {}
for asn in asn_details:
    if asn["country"] not in asn_details_by_country:
        asn_details_by_country[asn["country"]] = []
    asn_details_by_country[asn["country"]].append(asn)






# ip_addresses = []

# valid_ip_addresses = start_resume_ip_validator(ip_addresses, num_of_threads=512, chunk_size=512, country_name="Mauritius")