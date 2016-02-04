# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from spider.loader.loaders import IFengNewsLoader


class IFengComAutoNewsSpider(CrawlSpider):
    """凤凰汽车新闻爬虫"""

    name = 'ifeng_com_auto_news'
    allowed_domains = ['auto.ifeng.com']
    start_urls = [
        'http://auto.ifeng.com/hangye/',
        'http://auto.ifeng.com/zyy/',
        'http://auto.ifeng.com/shijia/zhuanjia/',
    ]

    rules = (
        Rule(
            LinkExtractor(
                allow=('auto\.ifeng\.com/\w+/\d{8}/\d+\.shtml'),
                allow_domains=allowed_domains,
                restrict_xpaths=('//div[@class="siwtch-content"]')
            ),
            callback='parse_news'
        ),
        Rule(
            LinkExtractor(
                allow=('.*'),
                allow_domains=allowed_domains,
                restrict_xpaths=('//div[@class="v2c-page"]')
            )
        ),
    )

    def parse_news(self, response):
        l = IFengNewsLoader()
        return l.load(response)
