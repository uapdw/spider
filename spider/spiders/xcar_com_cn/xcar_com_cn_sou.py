# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from urllib import quote 

from spider.loader.loaders.xcar_com_cn.xcar_com_cn_bbs import XcarComCnBBSLoader
from spider.loader.loaders.xcar_com_cn.xcar_com_cn_news import XcarComCnNewsLoader


class XcarComCnSouSpider(CrawlSpider):
    u"""爱卡汽车搜索爬虫"""

    name = 'xcar_com_cn_sou'

    allowed_domains = [
        'info.xcar.com.cn',
        'drive.xcar.com.cn',
    ]

    start_url_pattern = 'http://search.xcar.com.cn/search.php?c=%s&k=%s'

    list_url_pattern = 'http://search.xcar.com.cn/search.php\?c=%s&k=%s.*&pn=\d+'

    categories = ['2', '5']

    keywords = [u'北汽', u'b40', u'北京汽车', u'传动效率', u'动力', u'整车', u'外观', u'内饰', u'越野']

    def __init__(self):
        self.start_urls = []
        rules = []
        for category in self.categories:
            for keyword in self.keywords:
                self.start_urls.append(self.start_url_pattern % (category, keyword))
                rules.append(
                    Rule(
                        LinkExtractor(
                            allow=(self.list_url_pattern % (category, quote(keyword.encode('utf-8')))),
                            allow_domains=self.allowed_domains
                        )
                    )
                )
        rules.append(
            Rule(
                LinkExtractor(
                    allow=('.*viewthread\.php\?.*tid=(\d+).*'),
                    allow_domains=self.allowed_domains,
                ),
                callback=self.parse_bbs
            )
        )
        rules.append(
            Rule(
                LinkExtractor(
                    allow=('.*/news_\d+_1.html'),
                    allow_domains=self.allowed_domains,
                ),
                callback=self.parse_news
            )
        )
        self._rules = tuple(rules)

    def parse_bbs(self, response):
        bl = XcarComCnBBSLoader()
        return bl.load(response)

    def parse_news(self, response):
        nl = XcarComCnNewsLoader()
        return nl.load(response)
