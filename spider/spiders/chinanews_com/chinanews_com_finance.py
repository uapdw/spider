# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.chinanews_com.chinanews_com_finance import(
	ChinanewsFinanceLoader
)


class ChinanewsFinanceSpider(LoaderMappingSpider):
    
    u"""中新网财经爬虫"""

    name = 'chinanews_com_finance'
    allowed_domains = [
        'chinanews.com',
    ]
    start_urls = ['http://www.chinanews.com/']

    mapping = {
        'chinanews.com/cj/\d{4}/\d{2}-\d{2}/\d+.shtml':
        ChinanewsFinanceLoader
    }

