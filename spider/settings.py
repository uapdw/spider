# -*- coding: utf-8 -*-

from faker import Factory


BOT_NAME = 'spider'

SPIDER_MODULES = ['spider.spiders']
NEWSPIDER_MODULE = 'spider.spiders'

fake = Factory.create()
USER_AGENT = fake.internet_explorer()

# FILES_STORE = '/data0/files/stock_reports'

ITEM_PIPELINES = {
    # 'spider.pipelines.NamedFilesPipeline': 1,
    # 'spider.pipelines.SqlalchemyPipeline': 2,
    'spider.pipelines.JSONWriterPipeline': 1,
    # 'spider.pipelines.HBaseItemPipeline': 3,
    # 'spider.pipelines.SolrItemPipeline': 2
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

# ROBOTSTXT_OBEY = True

# DEPTH_LIMIT = 3
# DEPTH_STATS_VERBOSE = True
#
# LOG_LEVEL = 'INFO'
# LOG_STDOUT = False
# LOG_FILE = '/tmp/scrapy.log'


HBASE_HOST = '172.20.19.137'
HBASE_PORT = 9090
SOLR_HOST = '172.20.13.207'
SOLR_PORT = 8983
SOLR_INDEX = 'uradar_article'
