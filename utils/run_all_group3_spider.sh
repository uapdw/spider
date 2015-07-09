#!/bin/sh

cd /data0/sourcecode/information_crawler/group3/

for spider in `scrapy list`
do
  echo $spider
done