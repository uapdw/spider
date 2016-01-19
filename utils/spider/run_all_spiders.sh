#!/bin/sh

nohup scrapy list|xargs -P 5 -n 1 scrapy crawl > ../current.log 2>&1 &
