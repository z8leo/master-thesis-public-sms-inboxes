import re
import requests

def format_number( number):
    try:
        number = number.replace(" ", "")  # Remove whitespace
        number = re.search(r"[0-9]{1,14}", number).group()  # Extract number with regex
        number = "+" + number
        return number
    except:
        return 0

def to_absolute(url, response):
    if not url:
        return None
    if bool(urlparse(url).netloc):
        return url
    else:
        return response.urljoin(url)
print(format_number("+34 604385313  dd"))


print(requests.get("https://tesms.net/").text)