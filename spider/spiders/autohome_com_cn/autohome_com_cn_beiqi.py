# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from spider.loader.loaders.autohome_com_cn.autohome_com_cn_beiqi import AutohomeBQLoader


class AutohomeBQSpider(CrawlSpider):
    u"""汽车之家北汽项目爬虫"""

    name = 'autohome_com_cn_beiqi'

    allowed_domains = ['autohome.com.cn']

    start_url_pattern = 'http://k.autohome.com.cn/%s/'

    list_url_pattern = '.*/%s/index_\d+.html'

    target_url_pattern = 'http://k.autohome.com.cn/spec/\d+/view_\d+_\d+.html\?.*\|%s\|.*'

    categories = ['623', '3417', '2027', '2123', '3481', '3000', '3204']

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
        l = AutohomeBQLoader()
        return l.load(response)
