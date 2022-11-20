Activate Python Environment: \
Windows: `.venv\Scripts\activate.bat` \
MacOS: `$ source .venv/bin/activate`

Run a specific spider:\
`cd scrapy_project` \
`scrapy crawl receive-sms-free.cc -s CLOSESPIDER_PAGECOUNT=100` \

To check CSS Selectors in Chrome Dev Tools: \
`$$("div.row")`

Build requirements.txt
`pip freeze > requirements.txt`
! Remove module iocsupport, causes errors in docker container

Build Docker image: \
`docker build -t scrapebot .`

MySQL Setup: \
`CREATE TABLE scrapebot (
id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
scrape_start INT,
host VARCHAR(512),
country_page VARCHAR(512),
country_name VARCHAR(512),
inbox_page VARCHAR(512),
inbox_number VARCHAR(512),
message_page VARCHAR(512),
message_scrape_timestamp INT,
message_number VARCHAR(512),
sender VARCHAR(512),
body VARCHAR(512),
date VARCHAR(512),
timeframe_earliest INT,
timeframe_latest INT,
max_message_age INT)`

### Deployment: \
Copy cia scp to server: \
`scp -r ./05_Scraping root@167.99.130.203:/opt`

SSH: \
`ssh root@167.99.130.203` \

Move to dir: \
`cd ~/../dev/05_Scraping`

Build docker image: \
`docker build -t scrapebot .`

Run docker image: \
`docker run -d scrapebot`

View logs: \
`docker logs -m all [containerid]`

### MySQL:

SQL count messages per host: \
`SELECT host, COUNT(*) FROM scrapebot GROUP BY host`

Numbers shared by providers: \
`SELECT inbox_number, GROUP_CONCAT(DISTINCT host), COUNT(DISTINCT host)
FROM scrapebot
GROUP BY inbox_number`

Top ten senders: \
`SELECT sender, COUNT(sender)
FROM scrapebot
GROUP BY sender
ORDER BY COUNT(sender) DESC
LIMIT 100
`