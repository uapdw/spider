# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.ghkj_com.ghkj_com_news import(
    GhkjComNewsLoader
)


class GhkjComNewsSpider(LoaderMappingSpider):

    u"""北京国华科技集团有限公司新闻爬虫"""

    name = 'ghkj_com_news'
    allowed_domains = ['ghkj.com']
    start_urls = ['http://www.ghkj.com/']

    mapping = {
        'newsview.aspx\?NewsID=\d+\&NewsCateId=\d+':
        GhkjComNewsLoader
    }
