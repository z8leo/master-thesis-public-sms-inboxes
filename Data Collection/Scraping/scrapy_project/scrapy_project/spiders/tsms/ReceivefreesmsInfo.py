from .TSmsTemplate import TSmsTemplate


class ReceivefreesmsInfo(TSmsTemplate):
    name = 'receivefreesms.info'
    allowed_domains = ['receivefreesms.info']
    start_urls = ['https://receivefreesms.info/']
    optimal_interval = 24
    message_max_age = 200

    # Selectors inherited from tSmsTemplate
    INBOX_NUMBER_SELECTOR = "div.details>div.phone_number>h5 ::text"     # Number corresponding to inbox
    MESSAGE_NUMBER_SELECTOR = "h3 ::text"        # Number displayed on inbox
