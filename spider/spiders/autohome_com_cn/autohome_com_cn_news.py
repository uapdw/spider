# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from spider.loader.loaders.autohome_com_cn.autohome_com_cn_news import AutohomeNewsLoader


class AutohomeNewsSpider(CrawlSpider):
    u"""汽车之家新闻爬虫"""

    name = 'autohome_com_cn_news'

    allowed_domains = ['autohome.com.cn']

    start_url_pattern = 'http://www.autohome.com.cn/%s'

    list_url_pattern = 'http://www.autohome.com.cn/%s/[23]/'

    target_url_pattern = 'http://www.autohome.com.cn/%s/\d+/\d+.html'

    categories = ['all', 'news', 'drive', 'tech']

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
                        allow=(self.target_url_pattern % category),
                        allow_domains=self.allowed_domains
                    ),
                    callback=self.parse_target
                )
            )
        self._rules = tuple(rules)

    def parse_target(self, response):
        l = AutohomeNewsLoader()
        return l.load(response)
