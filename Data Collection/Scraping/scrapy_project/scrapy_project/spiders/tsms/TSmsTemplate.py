from ..GenericSpider import GenericSpider


class TSmsTemplate(GenericSpider):
    name = 'tsms'

    COUNTRY_SELECTOR = ""       # Empty if no Country overview. To get list of countries
    COUNTRY_LINK_SELECTOR = ""      # Link to inboxes corresponding to country
    COUNTRY_NAME_SELECTOR = ""      # Name of country corresponding to country
    COUNTRY_NEXT_SELECTOR = ""      # Link to next page

    INBOX_SELECTOR = "div.number"       # To get list of inboxes to iterate over
    INBOX_NUMBER_SELECTOR = "div.details>div.phone_number>h4 ::text"     # Number corresponding to inbox
    INBOX_LINK_SELECTOR = "div.action>a ::attr(href)"        # Link to inbox
    INBOX_NEXT_SELECTOR = "ul.pagination>li.page-item>a:contains('›') ::attr(href)"        # Link to next page

    MESSAGE_SELECTOR = "div.message_details"       # To get list of messages
    MESSAGE_NUMBER_SELECTOR = "h2 ::text"        # Number displayed on inbox
    MESSAGE_SENDER_SELECTOR = "div.sender::text"        # Sender / From field
    MESSAGE_BODY_SELECTOR = "div.msg>span *::text"      # Message Body / Text
    MESSAGE_DATE_SELECTOR = "div.time::text"      # Message Date
    MESSAGE_NEXT_SELECTOR = "ul.pagination>li.page-item>a:contains('›') ::attr(href)"      # Next page link