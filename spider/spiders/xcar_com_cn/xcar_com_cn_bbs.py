# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from spider.loader.loaders import XcarComCnBBSLoader


class XcarComCnBBSSpider(CrawlSpider):
    u"""爱卡汽车论坛爬虫"""

    name = 'xcar_com_cn_news'

    allowed_domains = ['xcar.com.cn']

    start_url_pattern = 'http://www.xcar.com.cn/bbs/forumdisplay.php?fid=%s'
    list_url_pattern = '.*forumdisplay\.php\?fid=%s&orderby=dateline&page=\d+'
    thread_url_pattern = '.*viewthread\.php\?tid=\d+'

    categories = [
        '10113'
    ]

    def __init__(self):
        self.start_urls = []
        rules = []

        for category in self.categories:
            self.start_urls.append(self.start_url_pattern % category)
            rules.append(
                Rule(
                    LinkExtractor(
                        allow=(self.list_url_pattern % category),
                        allow_domains=self.allowed_domains
                    )
                )
            )
            rules.append(
                Rule(
                    LinkExtractor(
                        allow=self.thread_url_pattern,
                        allow_domains=self.allowed_domains
                    ),
                    callback=self.parse_thread
                )
            )
        self._rules = tuple(rules)

    def parse_thread(self, response):
        l = XcarComCnBBSLoader()
        return l.load(response)
