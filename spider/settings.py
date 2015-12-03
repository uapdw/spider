# -*- coding: utf-8 -*-

from faker import Factory


BOT_NAME = 'spider'

SPIDER_MODULES = ['spider.spiders']
NEWSPIDER_MODULE = 'spider.spiders'

fake = Factory.create()
USER_AGENT = fake.internet_explorer()

ITEM_PIPELINES = {
    'spider.pipelines.JSONWriterPipeline': 1
}

HBASE_HOST = '172.20.6.61'
HBASE_PORT = 9090
