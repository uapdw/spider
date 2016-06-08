# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.cnrec_info.cnrec_info_news import(
    CnrecInfoNewsLoader
)


class CnrecInfoNewsSpider(LoaderMappingSpider):

    u"""中国可再生能源信息网新闻爬虫"""

    name = 'cnrec_info_news'
    allowed_domains = ['cnrec.info']
    start_urls = ['http://www.cnrec.info/']

    mapping = {
        '/\S+/\S+/\d{4}-\d{2}-\d{2}-\d+.html' or
        '/\S+/\d{4}-\d{2}-\d{2}-\d+.html':
        CnrecInfoNewsLoader
    }
