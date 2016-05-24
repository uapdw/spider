# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.n10jqka_com_cn.n10jqka_com_cn_news import (
    N10jqkaComCnNewsLoader
)


class N10jqkaComCnNewsSpider(LoaderMappingSpider):

    u"""同花顺财经新闻爬虫"""

    name = '10jqka_com_cn_news'
    allowed_domains = ['10jqka.com.cn']
    start_urls = ['http://news.10jqka.com.cn/']

    mapping = {
        '10jqka\.com\.cn/\d{8}/c\d+\.shtml': N10jqkaComCnNewsLoader
    }
