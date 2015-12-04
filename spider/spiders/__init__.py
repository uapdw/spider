# -*- coding: utf-8 -*-

import datetime

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.loader.processor import TakeFirst, MapCompose

from spider.loader import ItemLoader
from spider.items import UradarNewsItem
from spider.loader.processors import (text, DateProcessor, PipelineProcessor,
                                      RegexProcessor, safe_html)


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

    abstract_xpath = '//meta[@name="description"]/@content'
    keywords_xpath = '//meta[@name="keywords"]/@content'

    def __init__(self):
        self.target_url_callback = 'parse_news'
        TargetUrlsCallbackSpider.__init__(self)

        for attr in self.subclass_required_attrs:
            if not getattr(self, attr, None):
                raise ValueError(
                    "%s must have a %s" % (type(self).__name__, attr)
                )

    def parse_news(self, response):
        l = ItemLoader(item=UradarNewsItem(), response=response)

        l.default_output_processor = TakeFirst()

        l.add_value('url', response.url)

        l.add_xpath('title', self.title_xpath, MapCompose(text))

        l.add_xpath('content', self.content_xpath, MapCompose(safe_html))

        # author_re可选
        auther_re = getattr(self, 'author_re', None)
        if auther_re is None:
            l.add_xpath('author', self.author_xpath, MapCompose(text))
        else:
            l.add_xpath('author', self.author_xpath, MapCompose(text),
                        MapCompose(RegexProcessor(auther_re)))

        # publish_time_re可选
        publish_time_re = getattr(self, 'publish_time_re', None)
        if publish_time_re is None:
            l.add_xpath('publish_time', self.publish_time_xpath,
                        MapCompose(PipelineProcessor(
                                   text,
                                   DateProcessor(self.publish_time_format))))
        else:
            l.add_xpath('publish_time', self.publish_time_xpath,
                        MapCompose(PipelineProcessor(
                                   text,
                                   RegexProcessor(publish_time_re),
                                   DateProcessor(self.publish_time_format))))

        # abstract默认使用meta中description
        l.add_xpath('abstract', self.abstract_xpath, MapCompose(text))

        # keywords默认使用meta中keywords
        l.add_xpath('keywords', self.keywords_xpath, MapCompose(text))

        # source_re可选
        source_re = getattr(self, 'source_re', None)
        if source_re is None:
            l.add_xpath('source', self.source_xpath, MapCompose(text))
        else:
            l.add_xpath('source', self.source_xpath, MapCompose(text),
                        MapCompose(RegexProcessor(source_re)))

        l.add_value('source_domain', self.source_domain)
        l.add_value('source_name', self.source_name)

        l.add_value('add_time', datetime.datetime.now())

        i = l.load_item()
        return i
