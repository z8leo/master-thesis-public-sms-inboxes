from .GenericSpider import GenericSpider


class SmsReceiveFreeCom(GenericSpider):
    ### Needs to be modified for each host

    name = 'smsreceivefree.com'
    allowed_domains = ['smsreceivefree.com']
    start_urls = ['https://smsreceivefree.com/']
    optimal_interval = 12       # Interval to scrape in hours

    # Reference: https://www.w3schools.com/cssref/css_selectors.asp
    # https://docs.scrapy.org/en/latest/topics/selectors.html
    # Scrapy (parsel) implements a couple of non-standard pseudo-elements:
    # to select text nodes, use ::text
    # to select attribute values, use ::attr(name) where name is the name of the attribute that you want the value of

    COUNTRY_SELECTOR = "div.fields>ul>li"       # Empty if no Country overview. To get list of countries
    COUNTRY_LINK_SELECTOR = "a ::attr(href)"      # Link to inboxes corresponding to country
    COUNTRY_NAME_SELECTOR = "a ::text"      # Name of country corresponding to country
    COUNTRY_NEXT_SELECTOR = ""      # Link to next page

    INBOX_SELECTOR = "section.container>div.row>div.column>div.numview>div.column>"       # To get list of inboxes to iterate over
    INBOX_NUMBER_SELECTOR = "div:nth-child(3)>a ::text"     # Number corresponding to inbox
    INBOX_LINK_SELECTOR = "div:nth-child(3)>a ::attr(href)"        # Link to inbox
    INBOX_NEXT_SELECTOR = ""        # Link to next page

    MESSAGE_SELECTOR = "table.messagesTable2>tbody>tr"       # To get list of messages
    MESSAGE_NUMBER_SELECTOR = "h1.title>small>b ::text"        # Number displayed on inbox
    MESSAGE_SENDER_SELECTOR = "td:nth-child(1) ::text"        # Sender / From field
    MESSAGE_BODY_SELECTOR = "td:nth-child(2) ::text"      # Message Body / Text
    MESSAGE_DATE_SELECTOR = "td:nth-child(1)>small ::text"      # Message Date
    MESSAGE_NEXT_SELECTOR = "div.pagination>a:contains('»') ::attr(href)"      # Next page link