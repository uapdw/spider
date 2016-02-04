# -*- coding: utf-8 -*-

import json

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request

from spider.loader.loaders import IFengNewsLoader


class IFengComAutoZimeitiSpider(CrawlSpider):
    """凤凰汽车新闻爬虫"""

    name = 'ifeng_com_auto_zimeiti'
    allowed_domains = ['we.auto.ifeng.com']

    def __init__(self):
        self.start_urls = []
        rules = []
        for i in range(1, 7):
            self.start_urls.append('http://we.auto.ifeng.com/api/index_article.php?p=%s&pc=100&type=0&callback=tmpcallback' % i)

        rules.append(
            Rule(
                LinkExtractor(
                    allow=('we\.auto\.ifeng\.com/article/\d+\.html'),
                    allow_domains=self.allowed_domains,
                    restrict_xpaths=('//div[@class="list"]')
                ),
                callback='parse_news'
            )
        )

        rules.append(
            Rule(
                LinkExtractor(
                    allow=('we\.auto\.ifeng\.com/api/index_article\.php.*?'),
                    allow_domains=self.allowed_domains
                ),
                callback='parse_api'
            )
        )

        self._rules = tuple(rules)

    def parse_news(self, response):
        l = IFengNewsLoader()
        return l.load(response)

    def parse(self, response):
        string = response.body
        jsonData = json.loads(string[12:-2])
        for data in jsonData:
            yield Request(data['url'], callback=self.parse_news)
