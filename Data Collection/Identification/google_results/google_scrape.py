from serpapi import GoogleSearch
import csv

searchStrings = ["receive sms", "receive sms free", "receive sms online", "temporary sms", "temporary sms free", "public sms inbox"]

csvOutputFile = open("google_candidates.csv", "w", newline="")
csvOutputWriter = csv.writer(csvOutputFile)
# Header
csvOutputWriter.writerow(["link", "searchString", "position"])

# Google
for searchString in searchStrings:
    search = GoogleSearch({"q": searchString, "api_key": "3d67ef44ff7ddad17f653ae17db32b30abdb3e634b1fef28a9ec5dcfc8519d2f", "num": "50"})
    result = search.get_dict()
    for links in result["organic_results"]:
        row = [links["link"], searchString, links["position"]]
        csvOutputWriter.writerow(row)

# Bing
#for searchString in searchStrings:
#    search = GoogleSearch({"q": searchString, "api_key": "3d67ef44ff7ddad17f653ae17db32b30abdb3e634b1fef28a9ec5dcfc8519d2f", "count": "50", "engine": "bing"})
#    result = search.get_dict()
#    for links in result["organic_results"]:
#        row = [links["link"], searchString, "bing", links["position"]]
#        csvOutputWriter.writerow(row)

csvOutputFile.close()
print("Saved file")