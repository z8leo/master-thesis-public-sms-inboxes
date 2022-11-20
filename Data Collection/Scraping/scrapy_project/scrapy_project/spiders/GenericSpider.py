import scrapy
import re
from urllib.parse import urlparse
from dateutil import parser
import time


# A class for every host. To reduce code, a template class is defined and methods reused by inheritance.


class GenericSpider(scrapy.Spider):

    def __init__(self, message_max_age=0):
        self.message_max_age = message_max_age  # Max message age as Unix timestamp

    ### Needs to be modified for each host

    name = 'example.com'
    allowed_domains = ['example.com']
    start_urls = ['http://example.com/']

    # Reference: https://www.w3schools.com/cssref/css_selectors.asp
    # https://docs.scrapy.org/en/latest/topics/selectors.html
    # Scrapy (parsel) implements a couple of non-standard pseudo-elements:
    # to select text nodes, use ::text
    # to select attribute values, use ::attr(name) where name is the name of the attribute that you want the value of

    COUNTRY_SELECTOR = ""  # Empty if no Country overview. To get list of countries
    COUNTRY_LINK_SELECTOR = ""  # Link to inboxes corresponding to country
    COUNTRY_NAME_SELECTOR = ""  # Name of country corresponding to country
    COUNTRY_NEXT_SELECTOR = ""  # Link to next page

    INBOX_SELECTOR = ""  # To get list of inboxes to iterate over
    INBOX_NUMBER_SELECTOR = ''  # Number corresponding to inbox
    INBOX_LINK_SELECTOR = ""  # Link to inbox
    INBOX_NEXT_SELECTOR = ""  # Link to next page

    MESSAGE_SELECTOR = ""  # To get list of messages
    MESSAGE_NUMBER_SELECTOR = ""  # Number displayed on inbox
    MESSAGE_SENDER_SELECTOR = ""  # Sender / From field
    MESSAGE_BODY_SELECTOR = ""  # Message Body / Text
    MESSAGE_DATE_SELECTOR = ""  # Message Date
    MESSAGE_NEXT_SELECTOR = ""  # Next page link

    ### Filters must only be defined if needed

    def country_filter(self, country):
        return False

    def inbox_filter(self, inbox):
        return False

    def message_filter(self, message):
        return False

    ### Function to modify body of message

    def body_parse(self, body):
        return body

    ### Parse functions normally must not be overwritten

    def parse(self, response):
        cb_kwargs = {
            "scrape_start": int(time.time()),  # Unix timestamp
            "host": self.name,
        }
        # If start page is not a country overview (No country selector defined) continue with inbox parser
        if not self.COUNTRY_SELECTOR:
            # Pass down value
            cb_kwargs = {
                **cb_kwargs,
                "country_page": "None",
                "country_name": "None"
            }
            self.logger.warning("start with inboxes")
            return self.parse_inboxes(response, **cb_kwargs)
        else:
            return self.parse_countries(response, **cb_kwargs)  # Start with Country parser

    def parse_countries(self, response, **kwargs):
        countries = response.css(self.COUNTRY_SELECTOR)
        for country in countries:
            link = self.to_absolute(country.css(self.COUNTRY_LINK_SELECTOR).extract_first(), response)
            name = country.css(self.COUNTRY_NAME_SELECTOR).extract_first()
            if self.country_filter(country):
                continue  # Skip if Filter evaluates to true
            # Values to pass down
            cb_kwargs = {
                **kwargs,
                "country_page": response.url,
                "country_name": name
            }
            # Scrape link and parse inboxes
            if link:
                yield scrapy.Request(
                    link,
                    callback=self.parse_inboxes,
                    cb_kwargs=cb_kwargs
                )
        # Scrape next page
        if self.COUNTRY_NEXT_SELECTOR:
            next_page = response.css(self.COUNTRY_NEXT_SELECTOR)
            if next_page:
                next_page_url = self.to_absolute(next_page[-1].extract(), response)
                yield scrapy.Request(
                    next_page_url,
                    callback=self.parse_countries,
                    cb_kwargs=kwargs
                )

    def parse_inboxes(self, response, **kwargs):
        inboxes = response.css(self.INBOX_SELECTOR)
        for inbox in inboxes:
            link = self.to_absolute(inbox.css(self.INBOX_LINK_SELECTOR).extract_first(), response)
            number = self.format_number(inbox.css(self.INBOX_NUMBER_SELECTOR).extract_first())
            if self.inbox_filter(inbox):
                continue  # Skip if Filter evaluates to true
            # Values to pass down
            cb_kwargs = {
                **kwargs,
                'inbox_page': response.url,
                'inbox_number': number,
            }
            # Scrape link and parse messages
            if link:
                yield scrapy.Request(
                    link,
                    callback=self.parse_messages,
                    cb_kwargs=cb_kwargs
                )
        # Scrape next page
        if self.INBOX_NEXT_SELECTOR:
            next_page = response.css(self.INBOX_NEXT_SELECTOR)
            if next_page:
                next_page_url = self.to_absolute(next_page[-1].extract(), response)
                yield scrapy.Request(
                    next_page_url,
                    callback=self.parse_inboxes,
                    cb_kwargs=kwargs
                )

    def parse_messages(self, response, **kwargs):
        messages = response.css(self.MESSAGE_SELECTOR)
        number = self.format_number("".join(response.css(self.MESSAGE_NUMBER_SELECTOR).getall()))
        scrape_timestamp = int(time.time())
        stop_next_page = False  # Stop signal to skip next pages
        for message in messages:
            sender = "".join(message.css(self.MESSAGE_SENDER_SELECTOR).getall())
            sender = sender.replace("\n", "").replace("\r", "").strip()
            body = "".join(message.css(self.MESSAGE_BODY_SELECTOR).getall())
            body = body.replace("\n", "").replace("\r", "").strip()  # Remove newline
            body = self.body_parse(body)
            date = "".join(message.css(self.MESSAGE_DATE_SELECTOR).getall())
            date = date.replace("\n", "").replace("\r", "").strip()  # Remove newline
            timeframe = self.util_timeframe(date, scrape_timestamp)
            if timeframe[1] < self.message_max_age:  # Skip if message too old
                stop_next_page = True  # Do not parse next page
                continue     # Skip current page
            if self.message_filter(message):
                continue  # Skip if Filter evaluates to true
            yield {
                **kwargs,
                'message_page': response.url,
                'message_scrape_timestamp': scrape_timestamp,
                'message_number': number,
                'sender': sender,
                'body': body,
                'date': date,
                'timeframe_earliest': timeframe[1],
                'timeframe_latest': timeframe[0],
                'max_message_age': self.message_max_age
            }
        # Scrape next page
        if self.MESSAGE_NEXT_SELECTOR and not stop_next_page:
            next_page = response.css(self.MESSAGE_NEXT_SELECTOR)
            if next_page:
                next_page_url = self.to_absolute(next_page[-1].extract(), response)
                yield scrapy.Request(
                    next_page_url,
                    callback=self.parse_messages,
                    cb_kwargs=kwargs
                )

    # Utility function. Converts relative time "x minutes ago" to earliest or latest timestamp
    # Introduces uncertainty of time. minutes: +- 60 seconds, hours +- 60*60 seconds, etc.
    # Returns (0, 0) tuple if it can not be converted
    # Returns (earliest, latest) unix timestamp tuple
    # Example: if "1 minutes ago" -> earliest = timestamp - 60 seconds ago, latest = timestamp - 119 seconds ago
    def util_timeframe(self, relative_time, timestamp):
        try:
            # Can be parsed?
            parsed = parser.parse(relative_time)
            timestamp = int(time.mktime(parsed.timetuple()))
            return (timestamp), (timestamp)
        except:
            pass
        try:
            elapsed = int(re.search(r"[0-9]{1,2}", relative_time).group())
            if re.search(r"sec", relative_time):
                uncertainty = 1
            elif re.search(r"min|分钟前", relative_time):
                uncertainty = 60
            elif re.search(r"hour| h ago|小时前", relative_time):
                uncertainty = 60 * 60
            elif re.search(r"day|天前", relative_time):
                uncertainty = 60 * 60 * 24
            elif re.search(r"week", relative_time):
                uncertainty = 60 * 60 * 24 * 7
            elif re.search(r"month", relative_time):
                uncertainty = 60 * 60 * 24 * 7 * 31
            else:
                return 0, 0
            return (timestamp - elapsed * uncertainty), (timestamp - elapsed * uncertainty) - uncertainty
        except:
            return 0, 0

    # Utility function: Formats number string to international format "... +43 1234 ..." -> "+431234"
    # Returns 0 if error
    def format_number(self, number):
        try:
            number = number.replace(" ", "").replace("(", "").replace(")", "")  # Remove whitespace
            number = re.search(r"[0-9]{1,14}", number).group()  # Extract number with regex
            number = "+" + number
            return number
        except:
            return 0

    # Utility function: Make url aboslute
    def to_absolute(self, url, response):
        if not url or url == "#":
            return None
        if bool(urlparse(url).netloc):
            return url
        else:
            return response.urljoin(url)
