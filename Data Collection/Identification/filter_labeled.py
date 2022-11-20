# Reduces dataset to only providers. Enriches dataset with tranco rank.
import csv

csvInputFile = open("combined_labeled.csv", "r", newline="")
csvInputReader = csv.reader(csvInputFile)
# Skip Header
next(csvInputReader)

csvOutputFile = open("providers.csv", "w", newline="")
csvOutputWriter = csv.writer(csvOutputFile)

# Write header
csvOutputWriter.writerow(["url", "source", "searchString", "rank", "host", "isInbox", "inboxUrl", "monetization", "tos", "privacy", "trancoRank"])

for row in csvInputReader:

    print(row)

    # Skip if duplicate or not inbox
    if row[5] != "True":
        continue

    # Tranco file
    csvTrancoInputFile = open("tranco_list/tranco_2L69.csv", "r", newline="")
    csvTrancoInputReader = csv.reader(csvTrancoInputFile)
    # Get tranco rank
    found = False
    for trancoRow in csvTrancoInputReader:
        if row[4] == trancoRow[1]:
            row += [trancoRow[0]]       #Add Tranco rank
            found = True
    if not found:
        row += [""]
    csvTrancoInputFile.close()

    csvOutputWriter.writerow(row)


csvOutputFile.close()
print("Saved file")