from .GenericSpider import GenericSpider


class ReceiveSmsCc(GenericSpider):
    name = 'receive-sms.cc'
    allowed_domains = ['receive-sms.cc']
    start_urls = ['https://receive-sms.cc/Countries/']
    optimal_interval = 1
    message_max_age = 26

    COUNTRY_SELECTOR = "div.number-boxes-item"       # Empty if no Country overview. To get list of countries
    COUNTRY_LINK_SELECTOR = "div>div>a ::attr(href)"      # Link to inboxes corresponding to country
    COUNTRY_NAME_SELECTOR = "div>div>h4 ::text"      # Name of country corresponding to country
    COUNTRY_NEXT_SELECTOR = ""      # Link to next page

    INBOX_SELECTOR = "div.number-boxes-item"       # To get list of inboxes to iterate over
    INBOX_NUMBER_SELECTOR = "div>div>h4 ::text"     # Number corresponding to inbox
    INBOX_LINK_SELECTOR = "div>div>a ::attr(href)"        # Link to inbox
    INBOX_NEXT_SELECTOR = "div.pagination>ul>li>a:contains('»') ::attr(href)"        # Link to next page

    MESSAGE_SELECTOR = "div.row.border-temps"       # To get list of messages
    MESSAGE_NUMBER_SELECTOR = "div.h3 ::text"        # Number displayed on inbox
    MESSAGE_SENDER_SELECTOR = "div:nth-child(1)>div.mobile_show>a ::text"        # Sender / From field
    MESSAGE_BODY_SELECTOR = "div:nth-child(3) *::text"      # Message Body / Text
    MESSAGE_DATE_SELECTOR = "div.mobile_hide:nth-child(2) ::text"      # Message Date
    MESSAGE_NEXT_SELECTOR = "div.pagination>ul>li>a:contains('»') ::attr(href)"      # Next page link