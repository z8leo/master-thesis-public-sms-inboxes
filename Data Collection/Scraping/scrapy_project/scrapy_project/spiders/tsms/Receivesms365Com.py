from .TSmsTemplate import TSmsTemplate


class Receivesms365Com(TSmsTemplate):
    name = 'receivesms365.com'
    allowed_domains = ['receivesms365.com']
    start_urls = ['https://receivesms365.com/']
    optimal_interval = 24
    message_max_age = 200

    # Selectors inherited from tSmsTemplate
    INBOX_NUMBER_SELECTOR = "div.details>div.phone_number>h5 ::text"     # Number corresponding to inbox
    MESSAGE_NUMBER_SELECTOR = "h3 ::text"        # Number displayed on inbox
