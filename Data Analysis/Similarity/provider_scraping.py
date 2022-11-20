# Scrapes html for the given inbox link. saves it as csv.
import csv, requests, cloudscraper
from time import sleep

csvInputFile = open("providers.csv", "r", newline="")
csvInputReader = csv.reader(csvInputFile)
# Skip Header
next(csvInputReader)

csvOutputFile = open("inbox_html.csv", "w", newline="", encoding="utf-8")
csvOutputWriter = csv.writer(csvOutputFile)

# Write header
csvOutputWriter.writerow(["host", "inboxUrl", "html"])

providers = []
scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance

for row in csvInputReader:
    # List of providers
    providers += [(row[4], row[6])]

# providers = providers[:5]   # Slice provider list for testing

while len(providers) > 0:   # loop until all requests are succesful
    for index, (host, url) in enumerate(providers):
        print(index, host)
        # Get html
        try:
            html = scraper.get(url).text
        except:
            print("Error: %s" % host)
            continue # If unsuccesfull, skip row. Gets repeated because of while loop
        # Save to csv
        csvOutputWriter.writerow([host, url, html])
        # Remove provider from provider list
        providers.pop(index)
        print(providers)
        # Wait 5 secs to distribute requests
        sleep(5)

csvOutputFile.close()
print("Saved file")


