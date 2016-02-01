# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from spider.loader.loaders import AutohomeComCnBBSLoader


class AutohomeComCnBBSSpider(CrawlSpider):
    u"""汽车之家论坛爬虫"""

    name = 'autohome_com_cn_news'

    allowed_domains = ['club.autohome.com.cn']

    start_url_pattern = 'http://club.autohome.com.cn/bbs/forum-%s-1.html'
    list_url_pattern = 'club\.autohome\.com\.cn/bbs/forum-%s-\d+.html'
    thread_url_pattern = 'club\.autohome\.com\.cn/bbs/thread-%s-\d+-\d+.html'

    categories = [
        'a-100002',
        'c-4019',
        'c-3284',
        'c-3361',
        'c-3426',
        'c-3874',
        'c-3661',
        'c-3997',
        'c-3714',
        'c-3557',
        'c-3794',
        'c-2791',
        'c-3427',
        'c-2787',
        'c-3673',
        'c-3839',
        'c-3795',
        'c-3417',
        'c-3928',
        'c-2482',
        'c-3231',
        'c-3191',
        'c-3916',
        'c-3428',
        'c-4009',
        'c-3712',
        'c-2943',
        'c-4016',
        'c-4017',
        'c-3533',
        'c-3884',
        'c-3537',
        'c-3630',
        'c-4018',
        'c-4015',
        'c-3810',
        'c-965',
        'c-3035',
        'c-2126',
        'c-622',
        'c-966',
        'c-2960',
        'c-2915',
        'c-3221',
        'c-852',
        'c-2959'
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
                        allow=(self.thread_url_pattern % category),
                        allow_domains=self.allowed_domains
                    ),
                    callback=self.parse_thread
                )
            )
        self._rules = tuple(rules)

    def parse_thread(self, response):
        ml = AutohomeComCnBBSLoader()
        return ml.load(response)
