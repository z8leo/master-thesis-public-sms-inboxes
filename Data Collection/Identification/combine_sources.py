# Combines data sources
import csv

csvOutputFile = open("combined_candidates.csv", "w", newline="")
csvOutputWriter = csv.writer(csvOutputFile)

# Write Header
csvOutputWriter.writerow(["url", "source", "searchString", "rank"])

# Tranco List
csvInputFile = open("tranco_list/tranco_candidates.csv", "r", newline="")
for row in csv.reader(csvInputFile):
    csvOutputWriter.writerow(["http://" + row[1], "tranco", "", row[0]])
csvInputFile.close()

# Google Results
csvInputFile = open("google_results/google_candidates.csv", "r", newline="")
csvReader = csv.reader(csvInputFile)
next(csvReader)     # Skip first line, the header
for row in csvReader:
    csvOutputWriter.writerow([row[0], "google", row[1], row[2]])
csvInputFile.close()

# Bing Results
csvInputFile = open("bing_results/bing_candidates.csv", "r", newline="")
csvReader = csv.reader(csvInputFile)
next(csvReader)     # Skip first line, the header
for row in csvReader:
    csvOutputWriter.writerow([row[0], "bing", row[1], row[2]])
csvInputFile.close()

# Reaves Paper
csvInputFile = open("reaves_paper/reaves_candidates.csv", "r", newline="")
for row in csv.reader(csvInputFile):
    csvOutputWriter.writerow(["http://" + row[0], "reaves", "", ""])
csvInputFile.close()

# Cheng Paper
csvInputFile = open("cheng_paper/cheng_candidates.csv", "r", newline="")
for row in csv.reader(csvInputFile):
    csvOutputWriter.writerow(["http://" + row[0], "cheng", "", ""])
csvInputFile.close()

csvOutputFile.close()
print("Saved file")