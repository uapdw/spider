# -*- coding: utf-8 -*-

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

from spider.items import UradarNewsItem
from spider.extractors import (text, safe_html, DateExtractor,
                               now, ItemExtractor, XPathTypeRegexExtractor)


class TargetUrlCallbackMappingSpider(CrawlSpider):
    '''目标链接回调映射爬虫
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

        super(TargetUrlCallbackMappingSpider, self).__init__()

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


class TargetUrlsCallbackSpider(TargetUrlCallbackMappingSpider):
    '''目标链接回调爬虫
    url_callback_mapping中设置，目标链接正则:这类链接的callback函数
    爬虫从start_urls开始抓取，遍历在allowed_domains以内的链接
    直到链接匹配目标链接正则表达式，请求目标链接，调用对应的callback函数
    '''

    target_urls = None
    target_url_callback = None

    def __init__(self):
        if not getattr(self, 'target_urls', None):
            raise ValueError(
                "%s must have a target_urls" % type(self).__name__
            )
        if not getattr(self, 'target_url_callback', None):
            raise ValueError(
                "%s must have a nonempty target_url_callback" %
                type(self).__name__
            )

        self.url_callback_mapping = {
            url: self.target_url_callback for url in self.target_urls
        }

        super(TargetUrlsCallbackSpider, self).__init__()


class NewsSpider(TargetUrlsCallbackSpider):
    '''新闻爬虫'''

    item_class = UradarNewsItem

    subclass_required_attrs = [
        'title_xpath',
        'content_xpath',
        'author_xpath',
        'publish_time_xpath',
        'publish_time_format',
        'source_xpath',
        'source_domain',
        'source_name'
    ]

    default_abstract_xpath = '//meta[@name="description"]/@content'
    default_keywords_xpath = '//meta[@name="keywords"]/@content'

    def __init__(self):
        self.target_url_callback = 'parse_news'
        TargetUrlsCallbackSpider.__init__(self)

        for attr in self.subclass_required_attrs:
            if not getattr(self, attr, None):
                raise ValueError(
                    "%s must have a %s" % (type(self).__name__, attr)
                )

        self.extract = ItemExtractor(
            self.item_class,
            self.__generate_field_extractors_mapping()
        )

    def parse_news(self, response):
        i = self.extract(response)
        return i

    def __generate_field_extractors_mapping(self):
        m = {}

        m['url'] = lambda response: response.url

        m['title'] = XPathTypeRegexExtractor(self.title_xpath, text)

        m['content'] = XPathTypeRegexExtractor(self.content_xpath, safe_html)

        m['author'] = XPathTypeRegexExtractor(self.author_xpath, text,
                                              getattr(self, 'author_re', None))

        m['publish_time'] = XPathTypeRegexExtractor(
            self.publish_time_xpath,
            text,
            getattr(self, 'publish_time_re', None),
            [DateExtractor(self.publish_time_format)])

        if not hasattr(self, 'abstract_xpath'):
            m['abstract'] = XPathTypeRegexExtractor(
                self.default_abstract_xpath
            )
        else:
            m['abstract'] = XPathTypeRegexExtractor(
                self.abstract_xpath, text,
                getattr(self, 'abstract_re', None))

        if not hasattr(self, 'keywords_xpath'):
            m['keywords'] = XPathTypeRegexExtractor(
                self.default_keywords_xpath
            )
        else:
            m['keywords'] = XPathTypeRegexExtractor(
                self.keywords_xpath, text,
                getattr(self, 'keywords_re', None))

        m['source'] = XPathTypeRegexExtractor(
            self.source_xpath, text,
            getattr(self, 'source_re', None))

        m['source_domain'] = self.source_domain
        m['source_name'] = self.source_name

        m['add_time'] = [now]

        return m
