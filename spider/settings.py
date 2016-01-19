# -*- coding: utf-8 -*-

from faker import Factory


BOT_NAME = 'spider'

SPIDER_MODULES = ['spider.spiders']
NEWSPIDER_MODULE = 'spider.spiders'

fake = Factory.create()
USER_AGENT = fake.internet_explorer()

ITEM_PIPELINES = {
    'spider.pipelines.JSONWriterPipeline': 1,
    #'spider.pipelines.HBaseItemPipeline': 1,
    #'spider.pipelines.SolrItemPipeline': 2
}

REACTOR_THREADPOOL_MAXSIZE = 20
COOKIES_ENABLED = False
# REDIRECT_ENABLED = False
AJAXCRAWL_ENABLED = True

DOWNLOAD_DELAY = 0.25
DOWNLOAD_TIMEOUT = 10
CONCURRENT_REQUESTS_PER_DOMAIN = 8
CONCURRENT_REQUESTS = 16

RETRY_ENABLED = False

ROBOTSTXT_OBEY = True




HBASE_HOST = '172.20.6.61'
HBASE_PORT = 9090
SOLR_HOST = '172.20.8.87'
SOLR_PORT = 8983
SOLR_INDEX = 'uradar_article'
