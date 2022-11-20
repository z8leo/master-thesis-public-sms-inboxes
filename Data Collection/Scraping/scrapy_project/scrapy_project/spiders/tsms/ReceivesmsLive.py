from .TSmsTemplate import TSmsTemplate


class ReceivesmsLive(TSmsTemplate):
    name = 'receivesms.live'
    allowed_domains = ['receivesms.live']
    start_urls = ['https://receivesms.live/']
    optimal_interval = 24
    message_max_age = 200

    # Selectors inherited from tSmsTemplate