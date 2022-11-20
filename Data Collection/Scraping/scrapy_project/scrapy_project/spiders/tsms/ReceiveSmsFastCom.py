from .TSmsTemplate import TSmsTemplate


class ReceiveSmsFastCom(TSmsTemplate):
    name = 'receivesmsfast.com'
    allowed_domains = ['receivesmsfast.com']
    start_urls = ['https://receivesmsfast.com/']
    optimal_interval = 24
    message_max_age = 26

    # Selectors inherited from tSmsTemplate