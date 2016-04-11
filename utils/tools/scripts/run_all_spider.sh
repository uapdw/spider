#!/bin/bash

for i in `scrapy list`
do
    scrapy crawl $i
done
