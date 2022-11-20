from .GenericSpider import GenericSpider


class ReceivesmsCo(GenericSpider):
    name = 'receivesms.co'
    allowed_domains = ['receivesms.co']
    start_urls = ['https://www.receivesms.co/available-countries/']
    optimal_interval = 1
    message_max_age = 1

    COUNTRY_SELECTOR = "table>tbody>tr"       # Empty if no Country overview. To get list of countries
    COUNTRY_LINK_SELECTOR = "td.table_link>a ::attr(href)"      # Link to inboxes corresponding to country
    COUNTRY_NAME_SELECTOR = "td.table_link>a ::text"      # Name of country corresponding to country
    COUNTRY_NEXT_SELECTOR = ""      # Link to next page

    INBOX_SELECTOR = "table>tbody>tr"       # To get list of inboxes to iterate over
    INBOX_NUMBER_SELECTOR = "td:nth-child(3)>a ::text"     # Number corresponding to inbox
    INBOX_LINK_SELECTOR = "td:nth-child(5)>a ::attr(href)"        # Link to inbox
    INBOX_NEXT_SELECTOR = ""        # Link to next page

    MESSAGE_SELECTOR = "div.table-hover"       # To get list of messages
    MESSAGE_NUMBER_SELECTOR = "div.h3 ::text"        # Number displayed on inbox
    MESSAGE_SENDER_SELECTOR = "div:nth-child(1)>div:nth-child(1)>a ::text"        # Sender / From field
    MESSAGE_BODY_SELECTOR = "div:nth-child(3) *::text"      # Message Body / Text
    MESSAGE_DATE_SELECTOR = "div.mobile_hide:nth-child(2) ::text"      # Message Date
    MESSAGE_NEXT_SELECTOR = ""      # Next page link