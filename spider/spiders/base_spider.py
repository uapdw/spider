# -*- coding: utf-8 -*-

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

from spider.items import UradarNewsItem
from spider.extractors import (
    ItemExtractor, XPathExtractor, text,
    safe_html, RegexExtractor, DateExtractor,
    now, FixValueExtractor
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

    def __init__(self):
        for attr in self.subclass_required_attrs:
            if not getattr(self, attr, None):
                raise ValueError(
                    "%s must have a %s" % (type(self).__name__, attr)
                )
        self.__generate_field_extractors_mapping()

    def __generate_field_extractors_mapping(self):
        self.field_extractors_mapping = {}
        m = self.field_extractors_mapping
        m['url'] = [lambda response: response.url, text]
        m['title'] = [XPathExtractor(self.title_xpath), text]
        m['content'] = [XPathExtractor(self.content_xpath), safe_html]
        if hasattr(self, 'author_re'):
            m['author'] = [XPathExtractor(self.author_xpath),
                           text,
                           RegexExtractor(self.author_re)]
        else:
            m['author'] = [XPathExtractor(self.author_xpath),
                           text]
        if hasattr(self, 'publish_time_re'):
            m['publish_time'] = [XPathExtractor(self.publish_time_xpath),
                                 text,
                                 RegexExtractor(self.publish_time_re),
                                 DateExtractor(self.publish_time_format)]
        else:
            m['publish_time'] = [XPathExtractor(self.publish_time_xpath),
                                 text,
                                 DateExtractor(self.publish_time_format)]
        if not hasattr(self, 'abstract_xpath'):
            m['abstract'] = [self.__generate_default_abstract_extractor()]
        else:
            if hasattr(self, 'abstract_re'):
                m['abstract'] = [XPathExtractor(self.abstract_xpath),
                                 text,
                                 RegexExtractor(self.abstract_re)]
            else:
                m['abstract'] = [XPathExtractor(self.abstract_xpath),
                                 text]
        if not hasattr(self, 'keywords_xpath'):
            m['keywords'] = [self.__generate_default_keywords_extractor()]
        else:
            if hasattr(self, 'keywords_re'):
                m['keywords'] = [XPathExtractor(self.keywords_xpath),
                                 text,
                                 RegexExtractor(self.keywords_re)]
            else:
                m['keywords'] = [XPathExtractor(self.keywords_xpath),
                                 text]
        if hasattr(self, 'source_re'):
            m['source'] = [XPathExtractor(self.source_xpath),
                           text,
                           RegexExtractor(self.source_re)]
        else:
            m['source'] = [XPathExtractor(self.source_xpath),
                           text]
        m['source_domain'] = [FixValueExtractor(self.source_domain)]
        m['source_name'] = [FixValueExtractor(self.source_name)]
        m['add_time'] = [now]

    def __generate_default_abstract_extractor(self):
        '''默认摘要'''
        return XPathExtractor('//meta[@name="description"]/@content')

    def __generate_default_keywords_extractor(self):
        '''默认关键字'''
        return XPathExtractor('//meta[@name="keywords"]/@content')


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
