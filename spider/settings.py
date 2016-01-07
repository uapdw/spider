# -*- coding: utf-8 -*-

from faker import Factory


BOT_NAME = 'spider'

SPIDER_MODULES = ['spider.spiders']
NEWSPIDER_MODULE = 'spider.spiders'

fake = Factory.create()
USER_AGENT = fake.internet_explorer()

ITEM_PIPELINES = {
    #'spider.pipelines.JSONWriterPipeline': 1
    'spider.pipelines.HBaseItemPipeline': 1
}

DOWNLOAD_DELAY = 1
CONCURRENT_REQUESTS_PER_DOMAIN = 8
CONCURRENT_REQUESTS = 16
DOWNLOAD_TIMEOUT = 10

HBASE_HOST = '172.20.3.107'
HBASE_PORT = 9090
