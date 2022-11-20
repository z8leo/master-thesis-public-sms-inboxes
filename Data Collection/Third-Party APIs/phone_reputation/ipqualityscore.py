from numpy import number
import requests
import json
import csv
from datetime import datetime

# Read list of phone numbers
jsonInputFile = open("Data Collection/Third-Party APIs/phone_reputation/number_set_20220929_103358.json", "r", newline="")
json_reader = json.load(jsonInputFile)

results = []
for row in json_reader:
    # For testing, limiting API calls
    #if int(row[0]) > 2:    
    #    continue        
    number = row
    print(f'Requesting {number}')
    res = requests.get(f'https://ipqualityscore.com/api/json/phone/8RH5aWz6rqFQKyOmZrsNHNcC1EnSa0wQ/{number}')
    results += [res.json()]
    #results += [{'a': 'b'}]
jsonInputFile.close()

# Write reuslts to file
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
with open(f"Data Collection\Third-Party APIs\phone_reputation/ipqualityscore_results_{timestamp}.json", "w") as i :
    json.dump(results, i)