from numpy import number
import requests
import json
import csv
from datetime import datetime
import random

# Read list of phone numbers
csvInputFile = open("Data/Characteristics/distinct_phone_numbers.csv", "r", newline="")
csv_reader = csv.reader(csvInputFile)
# Skip header
# next(csv_reader)

# Get a random sample
sample = random.sample(list(csv_reader), 40)

# Result array
results = []

for i, x in enumerate(sample):
    #Pick random phone number
    print(f'Choosen row \n {x[1]}')
    results += [x[1]]

csvInputFile.close()

# Write reuslts to file
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
with open(f"Data Collection\Third-Party APIs\phone_reputation/number_set_{timestamp}.json", "w") as i :
    json.dump(results, i)