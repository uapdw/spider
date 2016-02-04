# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from spider.loader.loaders import SinaComCnBBSLoader


class SinaComCnBBSSpider(CrawlSpider):
    u"""新浪论坛爬虫"""

    name = 'sina_com_cn_bbs'

    allowed_domains = ['bbs.auto.sina.com.cn']

    start_url_pattern = 'http://bbs.auto.sina.com.cn/%s/forum-%s-1.html'
    list_url_pattern = '.*bbs\.auto\.sina\.com\.cn/%s/forum-%s-\d+\.html'
    thread_url_patterns = [
        '.*bbs\.auto\.sina\.com\.cn/thread-\d+-\d+-\d+\.html'
    ]

    categories = [
        '349'
    ]

    for category in categories:
        thread_url_patterns.append(
            '.*bbs\.auto\.sina\.com\.cn/%s/thread-\d+-\d+-\d+\.html' % category
        )

    def __init__(self):
        self.start_urls = []
        rules = []
        for category in self.categories:
            self.start_urls.append(
                self.start_url_pattern % (category, category))
            rules.append(
                Rule(
                    LinkExtractor(
                        allow=(self.list_url_pattern % (category, category)),
                        allow_domains=self.allowed_domains
                    )
                )
            )
            for thread_url_pattern in self.thread_url_patterns:
                rules.append(
                    Rule(
                        LinkExtractor(
                            allow=thread_url_pattern,
                            allow_domains=self.allowed_domains
                        ),
                        callback=self.parse_thread
                    )
                )
        self._rules = tuple(rules)

    def parse_thread(self, response):
        l = SinaComCnBBSLoader()
        return l.load(response)
