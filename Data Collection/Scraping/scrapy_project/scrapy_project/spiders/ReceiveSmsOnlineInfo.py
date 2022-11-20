from .GenericSpider import GenericSpider


class ReceiveSmsOnlineInfo(GenericSpider):     # Clsuter 1!
    ### Needs to be modified for each host

    name = 'receive-sms-online.info'
    allowed_domains = ['receive-sms-online.info']
    start_urls = ['http://receive-sms-online.info/']
    optimal_interval = 4       # Interval to scrape in hours
    message_max_age = 26

    # Reference: https://www.w3schools.com/cssref/css_selectors.asp
    # https://docs.scrapy.org/en/latest/topics/selectors.html
    # Scrapy (parsel) implements a couple of non-standard pseudo-elements:
    # to select text nodes, use ::text
    # to select attribute values, use ::attr(name) where name is the name of the attribute that you want the value of

    COUNTRY_SELECTOR = ""       # Empty if no Country overview. To get list of countries
    COUNTRY_LINK_SELECTOR = ""      # Link to inboxes corresponding to country
    COUNTRY_NAME_SELECTOR = ""      # Name of country corresponding to country
    COUNTRY_NEXT_SELECTOR = ""      # Link to next page

    INBOX_SELECTOR = "div.Row>div.Cell"       # To get list of inboxes to iterate over
    INBOX_NUMBER_SELECTOR = "div>a ::text"     # Number corresponding to inbox
    INBOX_LINK_SELECTOR = "div>a ::attr(href)"        # Link to inbox
    INBOX_NEXT_SELECTOR = ""        # Link to next page

    MESSAGE_SELECTOR = "table#msgs>tr"       # To get list of messages
    MESSAGE_NUMBER_SELECTOR = "h4>strong>b ::text"        # Number displayed on inbox
    MESSAGE_SENDER_SELECTOR = "td:nth-child(1) ::text"        # Sender / From field
    MESSAGE_BODY_SELECTOR = "td:nth-child(2)>div ::text"      # Message Body / Text
    MESSAGE_DATE_SELECTOR = "td:nth-child(3) ::text"      # Message Date
    MESSAGE_NEXT_SELECTOR = ""      # Next page link

    ### Filters must only be defined if needed

    def message_filter(self, message):
        if message.css("th").extract_first():      # Filter ads
            return True
        elif message.css("tr:nth-child(1) ::text").extract_first() == "From":      # Filter Header
            return True
        else:
            return False