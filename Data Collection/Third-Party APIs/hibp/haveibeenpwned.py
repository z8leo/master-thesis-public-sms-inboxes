
from email import header
from multiprocessing.connection import wait
from urllib import response
from numpy import number
import requests
import json
import csv
from datetime import datetime
import hashlib
import time

csvInputFile = open(
    "Data/Characteristics/distinct_phone_numbers.csv", "r", newline="")
csv_reader = csv.reader(csvInputFile)
# Skip header
next(csv_reader)

# Connect to Have i been pwned api
API_KEY = ''
headers = {
    'hibp-api-key': API_KEY
}

results_hibp = []     # Results for number type

for row in csv_reader:
    # For testing, limiting API calls
    #if int(row[0]) > 10:
    #    continue
    number = row[1]
    print(f'Requesting {number}')
    try:
        res = requests.get(url=f'https://haveibeenpwned.com/api/v3/breachedaccount/{number}',
                        headers=headers)
    except:
        continue
    if(res.ok):
        res_json = res.json()
        result = {'number': number,
                'response': res_json}
        results_hibp += [result]
        print(results_hibp)
    time.sleep(2)

csvInputFile.close()

# Write number type reuslts to file
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
with open(f"Data Collection\Third-Party APIs\hibp\hibp_{timestamp}.json", "w") as i:
    json.dump(results_hibp, i)