# Executes spiders

import schedule
from scrapy.utils.project import get_project_settings
import time
import mysql.connector
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
import datetime
from twisted.internet import task

# List of providers to scrape
PROVIDERS = [
    'receive-smss.com',
    'receive-sms-free.cc',
    'sms24.me',
    'receivesms.co',
    '7sim.net',
    'online-sms.org',
    'receivesms.live',  # tSMS CLuster \/
    'receivesmsfast.com',
    'receivesms365.com',
    'tesms.net'
]

def scrape(provider):
    settings = get_project_settings()
    #settings['CLOSESPIDER_PAGECOUNT'] = 100     # Limit pages for testing
    runner = CrawlerRunner(settings)

    # Connect to MySQL database
    mydb = mysql.connector.connect(
        host=settings['MYSQL_HOST'],
        user=settings['MYSQL_USER'],
        password=settings['MYSQL_PASSWORD'],
        port=settings['MYSQL_PORT'],
        database=settings['MYSQL_DB']
    )
    mycursor = mydb.cursor()

    # Get last Scrape timestamp
    mycursor.execute(f"SELECT scrape_start FROM {settings['MYSQL_TABLE']} WHERE host = '{provider}' ORDER BY scrape_start DESC LIMIT 1")
    myresult = mycursor.fetchone()
    if myresult:
        last_scrape = myresult[0]
    else:
        last_scrape = 0
    # last_scrape = int(time.time()) - 60*60        # For testing

    mydb.close()        # Close DB connection

    # Schedule next run in 55 min
    reactor.callLater(60*55, scrape, provider)

    # Run spider
    try:
        print(f"{datetime.datetime.now()} Started {provider}")
        runner.crawl(provider, message_max_age=last_scrape)
    except Exception as e:
        print(f"{datetime.datetime.now()}{e}")
        pass

    return


for provider in PROVIDERS:
    scrape(provider)

reactor.run()