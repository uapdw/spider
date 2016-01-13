# -*- coding: utf-8 -*-

from faker import Factory


BOT_NAME = 'spider'

SPIDER_MODULES = ['spider.spiders']
NEWSPIDER_MODULE = 'spider.spiders'

fake = Factory.create()
USER_AGENT = fake.internet_explorer()

ITEM_PIPELINES = {
    'spider.pipelines.JSONWriterPipeline': 1,
    # 'spider.pipelines.HBaseItemPipeline': 1,
    # 'spider.pipelines.SolrItemPipeline': 2
}

CONCURRENT_REQUESTS = 100
REACTOR_THREADPOOL_MAXSIZE = 20
LOG_LEVEL = 'INFO'
COOKIES_ENABLED = False
RETRY_ENABLED = False
DOWNLOAD_TIMEOUT = 15
REDIRECT_ENABLED = False
AJAXCRAWL_ENABLED = True

HBASE_HOST = '172.20.6.61'
HBASE_PORT = 9090
SOLR_HOST = '172.20.8.87'
SOLR_PORT = 8983
SOLR_INDEX = 'uradar_article'
