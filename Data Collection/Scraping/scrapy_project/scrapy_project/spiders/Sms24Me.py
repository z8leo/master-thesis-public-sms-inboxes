from .GenericSpider import GenericSpider


class Sms24Me(GenericSpider):     # Clsuter 1!
    ### Needs to be modified for each host

    name = 'sms24.me'
    allowed_domains = ['sms24.me']
    start_urls = ['https://sms24.me/en/numbers/']
    optimal_interval = 12       # Interval to scrape in hours

    # Reference: https://www.w3schools.com/cssref/css_selectors.asp
    # https://docs.scrapy.org/en/latest/topics/selectors.html
    # Scrapy (parsel) implements a couple of non-standard pseudo-elements:
    # to select text nodes, use ::text
    # to select attribute values, use ::attr(name) where name is the name of the attribute that you want the value of

    COUNTRY_SELECTOR = ""       # Empty if no Country overview. To get list of countries
    COUNTRY_LINK_SELECTOR = ""      # Link to inboxes corresponding to country
    COUNTRY_NAME_SELECTOR = ""      # Name of country corresponding to country
    COUNTRY_NEXT_SELECTOR = ""      # Link to next page

    INBOX_SELECTOR = "div.row>div.col-sm-12"       # To get list of inboxes to iterate over
    INBOX_NUMBER_SELECTOR = "a>div ::text"     # Number corresponding to inbox
    INBOX_LINK_SELECTOR = "a ::attr(href)"        # Link to inbox
    INBOX_NEXT_SELECTOR = "ul.pagination>li.active+li.page-item>a::attr(href), ul.pagination>li:nth-child(2)>a ::attr(href)"        # Link to next page

    MESSAGE_SELECTOR = "div.row>div.pb-3"       # To get list of messages
    MESSAGE_NUMBER_SELECTOR = "h1.text-secondary *::text"        # Number displayed on inbox
    MESSAGE_SENDER_SELECTOR = "div.callout>div>span>a ::text"        # Sender / From field
    MESSAGE_BODY_SELECTOR = "div.callout>span ::text"      # Message Body / Text
    MESSAGE_DATE_SELECTOR = "div.text-center ::attr(data-created)"      # Message Date
    MESSAGE_NEXT_SELECTOR = "ul.pagination>li.active+li.page-item>a::attr(href), ul.pagination>li:nth-child(2)>a::attr(href)"      # Next page link

