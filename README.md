# **TLDR Fail Testing for IP Addresses in Mauritius**

*This repository contains scripts for testing the prevalence of the TLDR Fail vulnerability in websites hosted on IP addresses within Mauritius.*

## Overview
This project was made possible due to the help of [Cyberstorm.mu](https://cyberstorm.mu/). 

Our projects analyses the readyness of Mauritius' against Quantum Computing. As many of you may know, Quantum Computing will be a game changer in the world of IT. 
This project checks if the the websites in Mauritius uses the latest version of TLS and if the TLS was correctly implemented using David Benjamin's code ([source of the tldr_fail_test.py](https://gist.github.com/dadrian/f51e7f96aa659937775232cc3576e5f8#file-tldr_fail_test-py)).

## About TLDR Fail

* Explanation of TLDR Fail: [https://tldr.fail](https://tldr.fail)

## Scripts and Functionality

**Key Scripts:**

* `tldr_fail_test.py`: Tests for the TLDR Fail vulnerability. This is David Benjamin's script. ([source link](https://gist.github.com/dadrian/f51e7f96aa659937775232cc3576e5f8))
* `test_for_port.py`: Scans IP addresses for open ports 80 and 443
* `test_vulnerability.py`: Runs `tldr_fail_test.py` on IPs with open ports and saves results
* `classify_ip_addresses.py`: Classifies vulnerable IP addresses by provider
* `test_popular_websites.py`: Tests 47 popular websites for the vulnerability using different ISPs

**Workflow:**
1. **IP Address Collection:**
   - IP ranges for Mauritius are obtained from [ip2location](https://lite.ip2location.com/mauritius-ip-address-ranges)
2. **Port Scanning:**
   - `test_for_port.py` scans IPs for open ports and saves results to CSV files
3. **Check if IP is firewalled or filtered**
   - `test_for_tls.py` checks if the IP is either **open** or **filtered**.
4. **Vulnerability Testing:**
   - `test_vulnerability.py` runs `tldr_fail_test.py` on IPs with open ports 80 and 443
   - Results are saved to text files in `./results/vulnerability_result`
5. **IP Address Classification:**
   - `classify_ip_addresses.py` classifies vulnerable IPs by provider
6. **Popular Website Testing:**
   - `test_popular_websites.py` tests 47 popular websites using different ISPs
   - Results are saved to files in `./results/classified_by_provider`


## Results

* See `./results` for detailed results, including:
    - Lists of vulnerable and non-vulnerable IP addresses
    - Vulnerability overview and percentage error
    - Classification of vulnerable IPs by provider
    - Results of popular website testing by ISP

## Usage

To run the script, we highly suggest you use linux as it requires `OpenSSL` to work properly otherwise there will be errors in it. Below is the steps required to run it properly. If you have any problem please open an issue on [GitHub issue section](https://github.com/AtishJoottun/Tldr_fail_testing/issues).

1. Clone this repository
2. Go the directory where the file `requirements.txt` is.
3. Run command `python3 pip install -r requirements.txt`. This will install the required dependencies for python.
3. Run the scripts in the following order:
   - `test_for_port.py`
   - `test_for_firewall.py`
   - `test_vulnerability.py`
   - `classify_ip_addresses.py` (optional)
   - `test_popular_websites.py` (optional)
4. View the results in the `./results` directory

## Dependencies

* Python 3
* Pandas
* openpyxl