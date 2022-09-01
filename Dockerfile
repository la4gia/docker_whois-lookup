FROM ubuntu:latest

MAINTAINER your_name

# SET WORKING DIRECTORY
WORKDIR /usr/src/app

# COPY PROJECT FILES TO CONTAINER
COPY . .

# INSTALL PYTHON (plus requirements) & CRON
RUN apt update && apt upgrade -y
RUN apt install python3 -y
RUN apt install python3-pip -y
RUN apt install cron -y
RUN pip install -r requirements.txt

# ADD CRONTAB FILE TO CRON DIRECTORY
ADD crontab /etc/cron.d/python-cron

# GRANT EXECUTION RIGHTS TO SHELL SCRIPT
RUN chmod +x script.sh

# GIVE EXECUTION RIGHTS TO CRONJOB
RUN chmod 0644 /etc/cron.d/python-cron

# CREATE LOG FILE TO BE ABLE TO RUN TAIL
# USED TO KEEP DOCKER CONTAINER RUNNING
RUN touch /var/log/cron.log

# Run the command on container startup
CMD cron && tail -f /var/log/cron.log
