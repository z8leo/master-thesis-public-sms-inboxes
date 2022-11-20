from .GenericSpider import GenericSpider


class ReceiveSmssCom(GenericSpider):
    name = 'receive-smss.com'
    allowed_domains = ['receive-smss.com']
    start_urls = ['http://receive-smss.com/']
    optimal_interval = 1

    COUNTRY_SELECTOR = ""       # Empty if no Country overview. To get list of countries
    COUNTRY_LINK_SELECTOR = ""      # Link to inboxes corresponding to country

    INBOX_SELECTOR = ".number-boxes-item"       # To get list of inboxes to iterate over
    INBOX_NUMBER_SELECTOR = '.number-boxes-itemm-number ::text'     # Number corresponding to inbox
    INBOX_LINK_SELECTOR = '.number-boxes-item-button ::attr(href)'        # Link to inbox

    MESSAGE_SELECTOR = "table>tbody>tr"       # To get list of messages
    MESSAGE_NUMBER_SELECTOR = "div.tooltip>a ::text"        # Number displayed on inbox
    MESSAGE_SENDER_SELECTOR = "td:nth-child(1) *::text"        # Sender / From field
    MESSAGE_BODY_SELECTOR = "td:nth-child(2) *::text"      # Message Body / Text
    MESSAGE_DATE_SELECTOR = "td:nth-child(3) *::text"      # Message Date
    MESSAGE_NEXT_SELECTOR = ""      # Next page link

    # Filter inboxes that are premium or registration needed
    def inbox_filter(self, inbox):
        if inbox.css(".number-boxes-item-button ::text").extract_first() in ["Premium", "Registered Users"]:
            return True
        else:
            return False