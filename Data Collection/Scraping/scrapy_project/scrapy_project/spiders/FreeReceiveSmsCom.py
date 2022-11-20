from .GenericSpider import GenericSpider


class FreeReceiveSmsCom(GenericSpider):
    name = 'freereceivesms.com'
    allowed_domains = ['freereceivesms.com']
    start_urls = ['https://www.freereceivesms.com/countrys/']
    optimal_interval = 1
    message_max_age = 26

    COUNTRY_SELECTOR = "div.number-boxes-item"       # Empty if no Country overview. To get list of countries
    COUNTRY_LINK_SELECTOR = "div>div>a ::attr(href)"      # Link to inboxes corresponding to country
    COUNTRY_NAME_SELECTOR = "div>div>h5 ::text"      # Name of country corresponding to country
    COUNTRY_NEXT_SELECTOR = ""      # Link to next page

    INBOX_SELECTOR = "div.number-boxes-item.col-sm-6"       # To get list of inboxes to iterate over
    INBOX_NUMBER_SELECTOR = "div>h4 ::text"     # Number corresponding to inbox
    INBOX_LINK_SELECTOR = "div>div>a ::attr(href)"        # Link to inbox
    INBOX_NEXT_SELECTOR = "nav>ul.pagination>li.page-item.disabled+li.page-item>a ::attr(href)"        # Link to next page

    MESSAGE_SELECTOR = "div.row.border-bottom"       # To get list of messages
    MESSAGE_NUMBER_SELECTOR = "div.h3 ::text"        # Number displayed on inbox
    MESSAGE_SENDER_SELECTOR = "div:nth-child(1)>span:nth-child(1) ::text"        # Sender / From field
    MESSAGE_BODY_SELECTOR = "div:nth-child(3)>div *::text"      # Message Body / Text
    MESSAGE_DATE_SELECTOR = "div:nth-child(1)>span:nth-child(2) ::text"      # Message Date
    MESSAGE_NEXT_SELECTOR = "nav>ul.pagination>li.page-item.disabled+li.page-item>a ::attr(href)"      # Next page link

    def inbox_filter(self, message):
        if message.css("img.online ::attr(src)").extract_first() == "/images/offline.png":      # Filter Offline numbers
            return True
        else:
            return False