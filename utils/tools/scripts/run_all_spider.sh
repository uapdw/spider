#!/bin/bash

for i in `cd /data0/sourcecode/spider/current && ~/.virtualenvs/spider/bin/scrapy list`
do
    cd /data0/sourcecode/spider/current && ~/.virtualenvs/spider/bin/scrapy crawl $i
done
