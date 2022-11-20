# Iterates through Tranco list. If domain has "sms" in it, open in browser and ask for labeling
import csv, re, webbrowser
from urllib.parse import urlparse

csvInputFile = open("combined_candidates.csv", "r", newline="")
csvInputReader = csv.reader(csvInputFile)
# Skip Header
next(csvInputReader)

csvOutputFile = open("combined_labeled.csv", "a", newline="")
csvOutputWriter = csv.writer(csvOutputFile)

chrome_path="C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))

# Start from line x downwards
lineStart = input("From which line to start?: ")
lineCount = 1

# Write header
if int(lineStart) == 0:
    csvOutputWriter.writerow(["url", "source", "searchString", "rank", "host", "isInbox", "inboxUrl", "monetization", "tos", "privacy"])

# List of hosts for deduplication
hosts = []

for row in csvInputReader:

    print("Row: {} URL: {}".format(lineCount, row[0]))

    # Extract host
    parsed = urlparse(row[0])
    if parsed.netloc.startswith('www.'):
        host = parsed.netloc[4:]
    else:
        host = parsed.netloc
    row += [host]

    # Start from line x downwards
    lineCount += 1      # Increment
    if lineCount < int(lineStart):
        # Add host to list for deduplication
        hosts += [host]
        continue    # Skip row

    # Deduplication
    if host in hosts:
        print("Duplicate")
        row += ["Duplicate", "", "", "", ""]
        csvOutputWriter.writerow(row)
        continue    # Skip row, host already labeled
    # Add host to list for deduplication
    hosts += [host]

    # Open in browser
    webbrowser.get('chrome').open(row[0], new=0, autoraise=False)

    # Is domain a public sms inbox?
    question = input('Is a public SMS inbox? [y]yes [*]no: [break]break')
    if question == "y":
        row += ["True"]
    elif question == "break":
        break
    else:
        # Label domain as NOT BEING a public sms inbox
        row += ["False", "", "", "", ""]
        # Write to output file
        csvOutputWriter.writerow(row)
        # Skip to next Row
        continue

    # Example inbox url?
    question = input("Inbox url: ")
    row += [question]

    # What monetization?
    question = input("What monetization? [g]GenericAd [t]TemporaryNumberAd [p]PremiumService [n]None ")
    if question == "g":
        question = "GenericAd"
    elif question == "t":
        question = "TemporaryNumberAd"
    elif question == "p":
        question = "PremiumService"
    elif question == "n":
        question = "None"
    row += [question]

    # Terms of service?
    question = input("TOS url? []none: ")
    if question == "":
        question = "None"
    row += [question]

    # Privacy policy?
    question = input("Privacy policy url? []none: ")
    if question == "":
        question = "None"
    row += [question]

    csvOutputWriter.writerow(row)

csvOutputFile.close()
print("Saved file")