import json

def read_ip_validator_results(country):
    with open(f"results/{country}/ip_validator_results.json", 'r') as f:
        data = json.load(f)
        valid_ip_addresses = data["valid_ip_addresses"]

    return valid_ip_addresses

def read_tls_filterer_results(country, tls_version):
    with open(f"results/{country}/tls_filterer_results.json", 'r') as f:
        data = json.load(f)
        ip_addresses = data[tls_version]

    return ip_addresses
