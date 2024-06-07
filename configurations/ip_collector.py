from utils.run_command import run_command
from utils.result import save_afrinic_asn_results
from utils.checkpoint import save_afrinic_asn_checkpoint
import pandas as pd
import ipaddress
import json
import os
import pycountry

def start_resume_retrieve_asn_details():
    checkpoint = f"checkpoints/asn.json"
    afrinic_asn_list = ['AS' + str(asn) for asn in extract_asns()]
    if not os.path.exists(checkpoint):
        asn_details = process_asn(afrinic_asn_list)
    else:
        with open(checkpoint, 'r') as f:
            cp = json.load(f)
            processed_asns = cp["processed_asn"]
            processed_list = cp["processed_list"]
            remaining_asns = list(set(afrinic_asn_list) - set(processed_list))
            asn_details = process_asn(remaining_asns, processed_asns, processed_list)
    save_afrinic_asn_results(asn_details, f"results/afrinic_asn.json")
    return group_by_country(asn_details)

def process_asn(remaining_asns=[], processed_asns=[], processed_list=[]):
    progress_denominator = len(remaining_asns) + len(processed_list)
    progress = len(processed_list)
    for i, asn in enumerate(remaining_asns):
        print(f"Processing ASN {asn}")
        out, err = run_command(['whois', '-h', 'whois.afrinic.net', '-i', 'origin', asn])
        if err:
            print(err)
        else:
            routes = parse_afrinic_whois(out)
            if len(routes) > 0:
                out, err = run_command(['whois', '-h', 'whois.afrinic.net', '-r', '-T', 'inetnum', routes[0]])        
                if err:
                    print(err)
                else:
                    country_code, country_name, netname = extract_country_netname(out)
                    print(country_code, netname)

                    dict = {
                        "asn": asn,
                        "netname": netname,
                        "country_code": country_code,
                        "country": country_name,
                        "inetnums": list(set(routes))
                    }
                    processed_asns.append(dict)
        processed_list.append(asn)
        save_afrinic_asn_checkpoint(processed_asns, processed_list, "checkpoints/asn.json")
        progress += 1
        print(f"{progress / progress_denominator * 100:.2f}% complete")
        # if i == 1500:
        #    print("Query limit reached. Try again after 24 hours.")
        #    sys.exit(0)

    return processed_asns

def extract_asns():
    asns = pd.read_csv('data/afrinic_asndata.csv')
    return asns['asnum'].values.tolist()

def parse_afrinic_whois(whois_output):
  routes = []
  for line in whois_output.splitlines():
    if line.startswith("route:"):
      routes.append(line.split()[1])
  return routes

def extract_country_netname(data):
  country_code = None
  netname = None

  for line in data.splitlines():
    if ':' in line:
      key, value = line.strip().split(":", maxsplit=1)
      if key.lower() == "country":
        country_code = value.strip()
      elif key.lower() == "netname":
        netname = value.strip()
    else:
      pass
  if country_code and netname:
    try:
        country = pycountry.countries.get(alpha_2=country_code)
        country_name = country.name if country else None
    except KeyError:
        country_name = None
    return country_code, country_name, netname
  else:
    return None, None, None
  
def group_by_country(asn_details):
    asn_details_by_country = {}
    for asn in asn_details:
        if asn["country"] not in asn_details_by_country:
            asn_details_by_country[asn["country"]] = []
        asn_details_by_country[asn["country"]].append(asn)
    return asn_details_by_country

def ip_prefix_to_list(ip_prefix, netname):
    return [{"ip_address": str(ip), "netname": netname} for ip in ipaddress.ip_network(ip_prefix)]