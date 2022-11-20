from numpy import number
import requests
import json
import csv
from datetime import datetime

# Read list of phone numbers
jsonInputFile = open("Data Collection/Third-Party APIs/phone_reputation/number_set_20220929_103358.json", "r", newline="")
json_reader = json.load(jsonInputFile)

results = []
for index, row in enumerate(json_reader):
    # For testing, limiting API calls
    if index > 0:    
        continue        
    number = row
    print(f'Requesting {number}')
    url = "https://trustcheckr-digital-identity-api.p.rapidapi.com/api/trustcheck/v1.3"

    querystring = {"name":"John Doe","email":"leonhard.zacharias@student.uibk.ac.at","phone":str(number)}

    headers = {
	    "X-RapidAPI-Key": "",
	    "X-RapidAPI-Host": ""
    }

    res = requests.request("GET", url, headers=headers, params=querystring)
    results += [res.json()]

jsonInputFile.close()

# Write reuslts to file
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
with open(f"Data Collection/Third-Party APIs/phone_reputation/trustchekr_results_{timestamp}.json", "w") as i :
    json.dump(results, i)