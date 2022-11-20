from email import header
from urllib import response
from numpy import number
import requests
import json
import csv
from datetime import datetime
import hashlib
import time

# API is rate limit to 1000 requests / hour !

jsonInputFile = open(
    "Data Collection\Third-Party APIs\hlr_llokups_nt_20220920_115342.json", "r", newline="")
json_data = json.load(jsonInputFile)

# Connect to hlr-lookups.com API
API_KEY = ''    # Key:Secret
API_HASH = hashlib.sha256(API_KEY.encode('utf-8')).hexdigest()
headers = {
    'X-Basic': API_HASH
}

# Check authentication
response = requests.get(
    url='https://www.hlr-lookups.com/api/v2/auth-test', headers=headers)
print(response.text)
if response.status_code != 200:
    raise Exception('Authentication failed!')

# Count how many HLR lookups
counter = 0
for entry in json_data:
    if entry['qualifies_for_hlr_lookup'] == True:
        counter += 1
print('HLR lookups to perform: %d' % counter)

# Perform HLR lookups
results_hlr = []    # Results for HLR Lokup
counter = 0
for entry in json_data:
    counter = counter+1

    # For testing, limiting API calls
    if int(counter) > 1011:
        continue


    # Sleep for rate limit
    time.sleep(1)

    number = entry['number']
    print(f'Requesting {number}, Counter {counter}')
    data = {
        "number": number,
        "msisdn": number
    }

    # Perform HLR lookup
    if entry['qualifies_for_hlr_lookup'] == True:
        res = requests.post(url='https://www.hlr-lookups.com/api/v2/hlr-lookup',
                        headers=headers, json=data)
        res_json = res.json()
        results_hlr += [res_json]
        print(res_json)

print(counter)

jsonInputFile.close()

# Write hlr lookup results to file
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
with open(f"Data Collection\Third-Party APIs\hlr_llokups_hlr_{timestamp}.json", "w") as i:
    json.dump(results_hlr, i)
