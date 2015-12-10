#!/bin/sh

scrapy list|xargs -P 5 -n 1 scrapy crawl
