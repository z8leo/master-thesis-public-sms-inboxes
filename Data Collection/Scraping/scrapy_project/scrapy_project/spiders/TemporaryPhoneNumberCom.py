from .GenericSpider import GenericSpider


class TemporaryPhoneNumberCom(GenericSpider):     # Clsuter 1!
    ### Needs to be modified for each host

    name = 'temporary-phone-number.com'
    allowed_domains = ['temporary-phone-number.com']
    start_urls = ['https://temporary-phone-number.com/countrys/']
    optimal_interval = 12       # Interval to scrape in hours
    message_max_age = 2

    # Reference: https://www.w3schools.com/cssref/css_selectors.asp
    # https://docs.scrapy.org/en/latest/topics/selectors.html
    # Scrapy (parsel) implements a couple of non-standard pseudo-elements:
    # to select text nodes, use ::text
    # to select attribute values, use ::attr(name) where name is the name of the attribute that you want the value of

    COUNTRY_SELECTOR = "div.col-sm-6"       # Empty if no Country overview. To get list of countries
    COUNTRY_LINK_SELECTOR = "a ::attr(href)"      # Link to inboxes corresponding to country
    COUNTRY_NAME_SELECTOR = "a>div>span.info-box-number ::text"      # Name of country corresponding to country
    COUNTRY_NEXT_SELECTOR = "div.pagination>ul>li>a:contains('»') ::attr(href)"      # Link to next page

    INBOX_SELECTOR = "div.col-sm-6"       # To get list of inboxes to iterate over
    INBOX_NUMBER_SELECTOR = "a>div>span.info-box-number ::text"     # Number corresponding to inbox
    INBOX_LINK_SELECTOR = "a ::attr(href)"        # Link to inbox
    INBOX_NEXT_SELECTOR = "div.pagination>ul>li>a:contains('»') ::attr(href)"        # Link to next page

    MESSAGE_SELECTOR = "div.direct-chat-msg"       # To get list of messages
    MESSAGE_NUMBER_SELECTOR = "h1.btn1 ::text"        # Number displayed on inbox
    MESSAGE_SENDER_SELECTOR = "div.direct-chat-info>span.pull-right>a.direct-chat-name ::text"        # Sender / From field
    MESSAGE_BODY_SELECTOR = "div.direct-chat-text *::text"      # Message Body / Text
    MESSAGE_DATE_SELECTOR = "div.direct-chat-info>time.timeago ::text"      # Message Date
    MESSAGE_NEXT_SELECTOR = "div.pagination>ul>li>a:contains('»') ::attr(href)"      # Next page link

    ### Filters must only be defined if needed

    def message_filter(self, message):
        if message.css("div.direct-chat-text>ins").extract_first():      # Filter ads
            return True
        else:
            return False