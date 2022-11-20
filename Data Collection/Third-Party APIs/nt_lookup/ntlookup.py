from email import header
from urllib import response
from numpy import number
import requests
import json
import csv
from datetime import datetime
import hashlib

csvInputFile = open(
    "Data/Characteristics/distinct_phone_numbers.csv", "r", newline="")
csv_reader = csv.reader(csvInputFile)
# Skip header
next(csv_reader)

# Connect to hlr-lookups.com API
API_KEY = 'b90ab41ecec9:A8eP-2!q2-7jAe-J7Wr-B@aA-7*4V'    # Key:Secret
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

results_nt = []     # Results for number type

for row in csv_reader:
    # For testing, limiting API calls
    #if int(row[0]) > 3:
    #    continue
    number = row[1]
    print(f'Requesting {number}')
    data = {
        "number": number,
        "msisdn": number
    }
    res = requests.post(url='https://www.hlr-lookups.com/api/v2/nt-lookup',
                        headers=headers, json=data)
    res_json = res.json()
    results_nt += [res_json]
    print(res_json)

csvInputFile.close()

# Write number type reuslts to file
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
with open(f"Data Collection\Third-Party APIs\hlr_llokups_nt_{timestamp}.json", "w") as i:
    json.dump(results_nt, i)
