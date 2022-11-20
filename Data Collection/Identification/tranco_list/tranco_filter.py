# Iterates through Tranco list. If domain has "sms" in it, it is candidate
import csv, re

csvInputFile = open("tranco_2L69.csv", "r", newline="")

csvOutputFile = open("tranco_candidates.csv", "w", newline="")
csvOutputWriter = csv.writer(csvOutputFile)

for row in csv.reader(csvInputFile):

    # Check regex sms
    if re.search("sms", row[1]):
        print(row)

        # Write to output file
        csvOutputWriter.writerow(row)

csvOutputFile.close()
print("Saved file")