from .TSmsTemplate import TSmsTemplate


class TempSmsNet(TSmsTemplate):
    name = 'temp-sms.net'
    allowed_domains = ['temp-sms.net']
    start_urls = ['https://temp-sms.net/']
    optimal_interval = 24
    message_max_age = 200

    # Selectors inherited from tSmsTemplate
    INBOX_LINK_SELECTOR = "div.number_action>a ::attr(href)"        # Link to inbox
    INBOX_NUMBER_SELECTOR = "div.number>div.number_number>h5 ::text"     # Number corresponding to inbox

    MESSAGE_NUMBER_SELECTOR = "h3 ::text"        # Number displayed on inbox
    MESSAGE_BODY_SELECTOR = "div.msg::text"      # Message Body / Text
    MESSAGE_NEXT_SELECTOR = ""      # Next page link