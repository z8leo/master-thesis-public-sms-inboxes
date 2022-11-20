#Download Python from DockerHub and use it
FROM python:3.9.10

#Set the working directory in the Docker container
WORKDIR /scraperbot

# Install dependencies:
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy source code
COPY . .

WORKDIR /scraperbot/scrapy_project

# Write rights for log file
RUN chmod -R 666 /scraperbot/scrapy_project

# Delete Logfile
RUN touch log.txt && rm log.txt

# Run the container
# Turn of output buffering with -u
CMD ["python", "-u", "main.py" ]