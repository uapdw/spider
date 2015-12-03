# -*- coding: utf-8 -*-

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

from spider.items import UradarNewsItem
from spider.extractors import (
    ItemExtractor, XPathExtractor, text
)


class TargetUrlSpider(CrawlSpider):
    '''目标链接爬虫
    url_callback_mapping中设置，目标链接正则:这类链接的callback函数
    爬虫从start_urls开始抓取，遍历在allowed_domains以内的链接
    直到链接匹配目标链接正则表达式，请求目标链接，调用对应的callback函数
    '''

    url_callback_mapping = None

    def __init__(self):
        if not getattr(self, 'url_callback_mapping', None):
            raise ValueError(
                "%s must have a url_callback_mapping" % type(self).__name__
            )
        if not getattr(self, 'allowed_domains', None):
            raise ValueError(
                "%s must have a nonempty allowed_domains" % type(self).__name__
            )
        self.__generate_rules()

        super(TargetUrlSpider, self).__init__()

    def __generate_rules(self):
        '''生成scrapy.contrib.spiders.CrawlSpider中的rules
        '''
        rule_list = []
        for url, callback in self.url_callback_mapping.iteritems():
            rule = Rule(
                LinkExtractor(allow=(url),
                              allow_domains=self.allowed_domains),
                callback=callback,
                follow=False)
            rule_list.append(rule)
        rule_list.append(
            Rule(
                LinkExtractor(allow=('.*'), allow_domains=self.allowed_domains)
            )
        )
        self.rules = tuple(rule_list)


class NewsExtractor(ItemExtractor):
    '''新闻extractor
    需要子类有title_xpath字段
    '''

    item_class = UradarNewsItem

    def __init__(self):
        if not getattr(self, 'title_xpath', None):
            raise ValueError(
                "%s must have a title_xpath" % type(self).__name__
            )
        self.__generate_field_extractors_mapping()

    def __generate_field_extractors_mapping(self):
        self.field_extractors_mapping = {
            'url': [lambda response: response.url, text],
            'title': [XPathExtractor(self.title_xpath), text]
        }


class SimpleNewsSpider(TargetUrlSpider, NewsExtractor):

    def __init__(self):
        if not getattr(self, 'target_urls', None):
            raise ValueError(
                "%s must have a target_urls" % type(self).__name__
            )

        self.url_callback_mapping = {
            url: 'parse_news' for url in self.target_urls
        }

        TargetUrlSpider.__init__(self)
        NewsExtractor.__init__(self)

    def parse_news(self, response):
        extract = self
        i = extract(response)
        return i
