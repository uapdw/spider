# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.crc_com_hk.crc_com_hk_news import(
    CrcComHkNewsLoader
)


class CrcComHkNewsSpider(LoaderMappingSpider):

    u"""华润集团新闻爬虫"""

    name = 'crc_com_hk_news'
    allowed_domains = [
        'crc.com.hk',
        'crc.com.cn'
    ]
    start_urls = ['http://www.crc.com.hk/']

    mapping = {
        'winfo.crc.com.cn/news/\S+/\S+/\d{6}/t\d{8}_\d+.htm' or
        'winfo.crc.com.cn/news/\S+/\d{6}/t\d{8}_\d+.htm':
        CrcComHkNewsLoader
    }
