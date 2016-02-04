# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request

from spider.loader.loaders import IFengNewsLoader


class IFengComAutoSouSpider(CrawlSpider):
    """凤凰汽车新闻搜索"""

    name = 'ifeng_com_auto_sou'
    allowed_domains = ['data.auto.ifeng.com', 'auto.ifeng.com']
    start_url_patten = 'http://data.auto.ifeng.com/search/search.do?startPage=%s&keywords=%s&qid=0'
    keywords = [u'北汽', u'b40', u'北京汽车', u'传动效率', u'动力', u'整车', u'外观', u'内饰', u'越野']

    def __init__(self):
        self.start_urls = []
        rules = []
        for keyword in self.keywords:
            for i in range(1, 3):
                self.start_urls.append(self.start_url_patten % (i, keyword))

        '''
        rules.append(
            Rule(
                LinkExtractor(
                    allow=('auto\.ifeng\.com/\w+/\d{8}/\d+\.shtml'),
                    allow_domains=self.allowed_domains
                ),
                callback='parse_news'
            )
        )

        rules.append(
            Rule(
                LinkExtractor(
                    #allow=('data\.auto\.ifeng\.com/search/link\?url.*?auto\.ifeng\.com/\w+/\d{8}/\d+\.shtml'),
                    allow=('data\.auto\.ifeng\.com/search/link\?url.*?'),
                    allow_domains=self.allowed_domains,
                    restrict_xpaths=('//div[@class="sear-market"]')
                )
            )
        )
        '''

        self._rules = tuple(rules)

    def parse_news(self, response):
        l = IFengNewsLoader()
        return l.load(response)

    def parse(self, response):
        urls = response.xpath('//h3[@class="t"]//a/@href').extract()
        for url in urls:
            url = url.replace('/search/link?url=', '')
            yield Request(url, callback=self.parse_news)
