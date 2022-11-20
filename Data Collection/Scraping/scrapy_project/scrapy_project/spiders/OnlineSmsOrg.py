from .GenericSpider import GenericSpider


class ReceiveSmsOnlineInfo(GenericSpider):     # Clsuter 1!
    ### Needs to be modified for each host

    name = 'online-sms.org'
    allowed_domains = ['online-sms.org']
    start_urls = ['https://online-sms.org/']

    # Reference: https://www.w3schools.com/cssref/css_selectors.asp
    # https://docs.scrapy.org/en/latest/topics/selectors.html
    # Scrapy (parsel) implements a couple of non-standard pseudo-elements:
    # to select text nodes, use ::text
    # to select attribute values, use ::attr(name) where name is the name of the attribute that you want the value of

    COUNTRY_SELECTOR = ""       # Empty if no Country overview. To get list of countries
    COUNTRY_LINK_SELECTOR = ""      # Link to inboxes corresponding to country
    COUNTRY_NAME_SELECTOR = ""      # Name of country corresponding to country
    COUNTRY_NEXT_SELECTOR = ""      # Link to next page

    INBOX_SELECTOR = "div.col-sm-12"       # To get list of inboxes to iterate over
    INBOX_NUMBER_SELECTOR = "div.ngroup>div>a ::text"     # Number corresponding to inbox
    INBOX_LINK_SELECTOR = "div.ngroup>div>a ::attr(href)"        # Link to inbox
    INBOX_NEXT_SELECTOR = ""        # Link to next page

    MESSAGE_SELECTOR = "table>tbody>tr"       # To get list of messages
    MESSAGE_NUMBER_SELECTOR = "h1 ::text"        # Number displayed on inbox
    MESSAGE_SENDER_SELECTOR = "td:nth-child(1) ::text"        # Sender / From field
    MESSAGE_BODY_SELECTOR = "td:nth-child(2) ::text"      # Message Body / Text
    MESSAGE_DATE_SELECTOR = "td:nth-child(3) ::text"      # Message Date
    MESSAGE_NEXT_SELECTOR = "ul.pagination>li>a:contains('»') ::attr(href)"      # Next page link

    ### Filters must only be defined if needed

