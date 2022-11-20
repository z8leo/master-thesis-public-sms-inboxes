from .GenericSpider import GenericSpider


class ReceiveSmsFreeCc(GenericSpider):     # Clsuter 1!
    ### Needs to be modified for each host

    name = 'receive-sms-free.cc'
    allowed_domains = ['receive-sms-free.cc']
    start_urls = ['https://receive-sms-free.cc/regions/']
    optimal_interval = 12       # Interval to scrape in hours

    # Reference: https://www.w3schools.com/cssref/css_selectors.asp
    # https://docs.scrapy.org/en/latest/topics/selectors.html
    # Scrapy (parsel) implements a couple of non-standard pseudo-elements:
    # to select text nodes, use ::text
    # to select attribute values, use ::attr(name) where name is the name of the attribute that you want the value of

    COUNTRY_SELECTOR = "div.index-case>ul.clearfix>li.wow"       # Empty if no Country overview. To get list of countries
    COUNTRY_LINK_SELECTOR = "a ::attr(href)"      # Link to inboxes corresponding to country
    COUNTRY_NAME_SELECTOR = "a>h2>span ::text"      # Name of country corresponding to country
    COUNTRY_NEXT_SELECTOR = "ul.pagination>li>a:contains('»') ::attr(href)"      # Link to next page

    INBOX_SELECTOR = "div.index-case>ul.clearfix>li.wow"       # To get list of inboxes to iterate over
    INBOX_NUMBER_SELECTOR = "a>h2>span ::text"     # Number corresponding to inbox
    INBOX_LINK_SELECTOR = "a ::attr(href)"        # Link to inbox
    INBOX_NEXT_SELECTOR = "ul.pagination>li>a:contains('»') ::attr(href)"        # Link to next page

    MESSAGE_SELECTOR = "div.casetext>div.row"       # To get list of messages
    MESSAGE_NUMBER_SELECTOR = "div.name>h1 ::text"        # Number displayed on inbox
    MESSAGE_SENDER_SELECTOR = "div:nth-child(1)>div.mobile_hide ::text"        # Sender / From field
    MESSAGE_BODY_SELECTOR = "div:nth-child(3) *::text"      # Message Body / Text
    MESSAGE_DATE_SELECTOR = "div.mobile_hide:nth-child(2) ::text"      # Message Date
    MESSAGE_NEXT_SELECTOR = "ul.pagination>li>a:contains('»') ::attr(href)"      # Next page link

    ### Filters must only be defined if needed

    def message_filter(self, message):
        if message.css("div>ins").extract_first():      # Filter ads
            return True
        elif message.css("div.mobile_hide:nth-child(1):contains('From')").extract_first():      # Filter Header
            return True
        else:
            return False