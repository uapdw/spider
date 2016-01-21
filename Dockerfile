FROM ubuntu:14.04
MAINTAINER liufeng

RUN apt-get update
RUN apt-get install -y python python-pip python-dev libxml2-dev libxslt-dev libffi-dev libssl-dev

ADD . /spider

RUN pip install --upgrade pip
RUN pip install -r /spider/requirements.txt

WORKDIR /spider

CMD scrapy crawl uradar_url -a config_path=/spider/uradar_url_config.json
