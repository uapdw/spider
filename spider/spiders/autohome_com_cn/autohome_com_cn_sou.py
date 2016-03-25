# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from urllib import quote

from spider.loader.loaders.autohome_com_cn.autohome_com_cn_bbs import AutohomeComCnBBSLoader
from spider.loader.loaders.autohome_com_cn.autohome_com_cn_news import AutohomeNewsLoader


class AutohomeSouSpider(CrawlSpider):
    u"""汽车之家搜索爬虫"""

    name = 'autohome_com_cn_sou'

    allowed_domains = [
        'www.autohome.com.cn',
        'zhidao.autohome.com.cn',
        'club.autohome.com.cn'
    ]

    start_url_pattern = 'http://sou.autohome.com.cn/%s?q=%s'

    list_url_pattern = 'http://sou.autohome.com.cn/%s\?q=%s.*&page=[2]&.*'

#     categories = ['zonghe', 'luntan', 'wenzhang', 'zhidao']
    categories = ['luntan']

    keywords = [u'北汽', u'b40', u'北京汽车', u'传动效率', u'动力', u'整车', u'外观', u'内饰', u'越野']

    def __init__(self):
        self.start_urls = []
        rules = []
        for category in self.categories:
            for keyword in self.keywords:
                self.start_urls.append(self.start_url_pattern % (category, quote(keyword.encode('gbk'))))
                rules.append(
                    Rule(
                        LinkExtractor(
                            allow=(self.list_url_pattern % (category, quote(keyword.encode('gbk')))),
                            allow_domains=self.allowed_domains
                        )
                    )
                )
        rules.append(
            Rule(
                LinkExtractor(
                    allow=('http://club.autohome.com.cn/bbs/thread-\w+-\d+-\d+-1.html'),
                    allow_domains=self.allowed_domains,
                ),
                callback=self.parse_bbs
            )
        )
        rules.append(
            Rule(
                LinkExtractor(
                    allow=('http://zhidao.autohome.com.cn/question/\d+.html'),
                    allow_domains=self.allowed_domains,
                ),
                callback=self.parse_bbs
            )
        )
        rules.append(
            Rule(
                LinkExtractor(
                    allow=('http://www.autohome.com.cn/\w+/\d+/\d+(-\d+)?\.html'),
                    allow_domains=self.allowed_domains,
                ),
                callback=self.parse_news
            )
        )
        self._rules = tuple(rules)

    def parse_bbs(self, response):
        bl = AutohomeComCnBBSLoader()
        return bl.load(response)

    def parse_news(self, response):
        nl = AutohomeNewsLoader()
        return nl.load(response)
