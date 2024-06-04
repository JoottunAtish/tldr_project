from utils.run_command import run_command
from utils.result import save_afrinic_asn_results
from utils.checkpoint import save_afrinic_asn_checkpoint
import json
import sys
import os

def start_resume_retrieve_asn_details():
    checkpoint = f"checkpoints/asn.json"
    afrinic_asn_16_range = [(36864, 37887)]
    afrinic_asn_32_range = [(327680, 328703), (328704, 329727)]
    afrinic_asn_range = afrinic_asn_16_range + afrinic_asn_32_range
    afrinic_asn_list = ['AS' + str(asn) for asn_range in afrinic_asn_range for asn in range(asn_range[0], asn_range[1] + 1)][:10]
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
    return asn_details

def process_asn(remaining_asns=[], processed_asns=[], processed_list=[]):
    progress_denominator = len(remaining_asns) + len(processed_list)
    progress = len(processed_list)
    # obtained from https://www.iana.org/assignments/as-numbers/as-numbers.xhtml
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
                    country, netname = extract_country_netname(out)
                    print(country, netname)

                    dict = {
                        "asn": asn,
                        "netname": netname,
                        "country": country,
                        "inetnums": routes
                    }
                    processed_asns.append(dict)
        save_afrinic_asn_checkpoint(processed_asns, processed_list, "checkpoints/asn.json")
        processed_list.append(asn)
        progress += 1
        print(f"{progress / progress_denominator * 100:.2f}% complete")
        if i == 1500:
           print("Query limit reached. Try again after 24 hours.")
           sys.exit(0)

    return processed_asns

def parse_afrinic_whois(whois_output):
  routes = []
  for line in whois_output.splitlines():
    if line.startswith("route:"):
      routes.append(line.split()[1])
  return routes

def extract_country_netname(data):
  country = None
  netname = None

  for line in data.splitlines():
    if ':' in line:
      key, value = line.strip().split(":", maxsplit=1)
      if key.lower() == "country":
        country = value.strip()
      elif key.lower() == "netname":
        netname = value.strip()
    else:
      pass
  if country and netname:
    return country, netname
  else:
    return None, None