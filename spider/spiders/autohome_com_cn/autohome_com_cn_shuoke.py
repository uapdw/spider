# -*- coding: utf-8 -*-

from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from spider.loader.loaders.autohome_com_cn.autohome_com_cn_shuoke import AutohomeShuoKeLoader


class AutohomeShuokeSpider(CrawlSpider):
    u"""汽车之家说客爬虫"""

    name = 'autohome_com_cn_shuoke'

    allowed_domains = ['shuoke.autohome.com.cn']

    start_urls = ['http://shuoke.autohome.com.cn']

    rules = (
        Rule(
            LinkExtractor(
                allow=('http://shuoke.autohome.com.cn/article/\d+(-\d+)?.html'),
                allow_domains=allowed_domains,
            ),
            callback='parse_target'
        ),
    )

    def parse_target(self, response):
        l = AutohomeShuoKeLoader()
        return l.load(response)
