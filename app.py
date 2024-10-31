# Required for environmental variables
import os
from dotenv import load_dotenv, dotenv_values

# Required for accessing URLs
from urllib.request import urlopen
from urllib.parse import urlencode

import requests

# Data is sent & recieved as JSON
import json

# Required for scheduling
import schedule
import time

# Load environmental variables
load_dotenv()

# Check if debug output is enabled
if os.getenv("DEBUG_OUTPUT") == "1":

    debug_output = True

else:

    debug_output = False

print("[APP] Program started")

# Run job
def job():

    if debug_output: print("[DEBUG] Running job")

    # Get wanted IP address
    if os.getenv("IP_ADDRESS"):

        if debug_output: print("[DEBUG] Loading IP address from environmental variables")
        ip_address = os.getenv("IP_ADDRESS")

    else:

        # Debug output
        if debug_output: print("[DEBUG] Fetching ip.me for current IP address")

        get_ip_address_url = "https://ip.me"
        get_ip_address_request = requests.get(get_ip_address_url)
        ip_address = get_ip_address_request.content.decode("utf-8").strip()

    # Debug output for IP address
    if debug_output: print(f"[DEBUG] Desired IP address: {ip_address}")
    
    # Test that the API works
    if debug_output: print("[DEBUG] Testing API key...")

    test_api_url = "https://api.porkbun.com/api/json/v3/ping"
    auth_api_data = { "secretapikey": os.getenv("PORKBUN_SECRET_KEY"), "apikey": os.getenv("PORKBUN_API_KEY")}

    test_api_request = requests.post(test_api_url, json=auth_api_data)
    test_api_response = test_api_request.json()

    if test_api_response["status"] == "ERROR":

        raise Exception(test_api_response["message"])

    if debug_output: print("[DEBUG] API key successfully checked")

    # Get the domains from the domains.json file
    try:
        with open("config/domains.json", "r") as file:

            if debug_output: print("[DEBUG] Fetching domains from domain.json")

            data = json.load(file)

            if debug_output: print(f"[DEBUG] Fetched {len(data)} domains")
    
    except:

        raise Exception("No domains.json found!")

    # Go through each domain in the file
    for domain in data:
        current_domain = data[domain]

        if debug_output: print(f"[DEBUG] Current domain: {domain}")
        
        # Go through each entry for each domain
        for entry in current_domain:

            if debug_output: print(f"[DEBUG] * Currently trying the subdomain {entry['subdomain']}'s {entry['type']} record")

            # Get current domain info
            current_domain_get_url = f"https://api.porkbun.com/api/json/v3/dns/retrieveByNameType/{domain}/{entry['type']}/{entry['subdomain']}"
            
            current_domain_get_request = requests.post(current_domain_get_url, json=auth_api_data)
            current_domain_get_response = current_domain_get_request.json()
            
            # Check if domain ecists
            if current_domain_get_response['status'] != "SUCCESS" or current_domain_get_response["records"] == []:

                raise Exception("URL does not exist!")

            # Go through all the records in the response
            for record in current_domain_get_response["records"]:

                # Check that record doesn't have the required IP address already
                if record["type"] == entry["type"] and record["content"] != ip_address:

                    if debug_output: print(f"[DEBUG] * Updating {entry['subdomain']}.{domain}'s {entry['type']} record to {ip_address}")
                    
                    # Set IP address of subdomain
                    new_domain_get_url = f"https://api.porkbun.com/api/json/v3/dns/editByNameType/{domain}/{record['type']}/{entry['subdomain']}"
                    new_domain_data = { "content": ip_address }
                    new_domain_data.update(auth_api_data)

                    new_domain_get_request = requests.post(new_domain_get_url, json=new_domain_data)
                    new_domain_get_response = new_domain_get_request.json()

                    if debug_output: print("[DEBUG] * IP address updated successfully")
                
                else:

                    # Skip if IP address is already set
                    if debug_output: print("[DEBUG] * IP address matches, skipping")

        print(f"[APP] Updated {domain}'s records successfully")

# Schedule job
schedule.every().hour.do(job)

# Run schedule
while True:
    schedule.run_pending()
    time.sleep(1)