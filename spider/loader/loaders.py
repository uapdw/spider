# -*- coding: utf-8 -*-

import datetime

from scrapy.loader.processors import TakeFirst, MapCompose, Join

from spider.loader import ItemLoader
from spider.loader.processors import (SafeHtml, text, DateProcessor,
                                      RegexProcessor, PipelineProcessor)
from spider.items import UradarNewsItem, UradarBlogItem


class NewsLoader(object):
    '''新闻爬虫'''

    subclass_required_attrs = [
        'content_xpath',
        'publish_time_xpath',
        'publish_time_format'
    ]

    title_xpath = '//title'
    abstract_xpath = '//meta[@name="description"]/@content'
    keywords_xpath = '//meta[@name="keywords"]/@content'

    def __init__(self):
        for attr in self.subclass_required_attrs:
            if not getattr(self, attr, None):
                raise ValueError(
                    "%s must have a %s" % (type(self).__name__, attr)
                )

        if not getattr(self, 'site_domain', None) and \
                not getattr(self, 'source_domain', None):
            raise ValueError(
                "%s must have a site_domain" % (type(self).__name__, attr)
            )

        if not getattr(self, 'site_name', None) and \
                not getattr(self, 'source_name', None):
            raise ValueError(
                "%s must have a site_name" % (type(self).__name__, attr)
            )

    def load(self, response):
        l = ItemLoader(item=UradarNewsItem(), response=response)

        l.default_output_processor = TakeFirst()

        l.add_value('url', response.url)

        l.add_xpath('title', self.title_xpath, MapCompose(text))

        l.add_xpath('content', self.content_xpath,
                    MapCompose(SafeHtml(response.url)), Join('\n'))

        # author可选
        auther_xpath = getattr(self, 'author_xpath', None)
        if auther_xpath is not None:
            auther_re = getattr(self, 'author_re', None)
            if auther_re is None:
                l.add_xpath('author', self.author_xpath, MapCompose(text))
            else:
                l.add_xpath('author', self.author_xpath, MapCompose(text),
                            MapCompose(RegexProcessor(auther_re)))

        # publish_time_re可选

        processor_list = [text]

        publish_time_re = getattr(self, 'publish_time_re', None)
        if publish_time_re is not None:
            processor_list.append(
                RegexProcessor(
                    publish_time_re,
                    join_str=getattr(self, 'publish_time_re_join', u'')
                )
            )

        publish_time_filter = getattr(self, 'publish_time_filter', None)
        if publish_time_filter is not None:
            processor_list.append(
                publish_time_filter
            )

        processor_list.append(DateProcessor(self.publish_time_format))

        l.add_xpath('publish_time', self.publish_time_xpath,
                    MapCompose(
                        PipelineProcessor(
                            *processor_list
                        )
                    ))

        # abstract默认使用meta中description
        l.add_xpath('abstract', self.abstract_xpath, MapCompose(text))

        # keywords默认使用meta中keywords
        l.add_xpath('keywords', self.keywords_xpath, MapCompose(text))

        # source可选
        source_xpath = getattr(self, 'source_xpath', None)
        if source_xpath:
            source_re = getattr(self, 'source_re', None)
            if source_re is None:
                l.add_xpath('source', self.source_xpath, MapCompose(text))
            else:
                l.add_xpath('source', self.source_xpath, MapCompose(text),
                            MapCompose(RegexProcessor(source_re)))

        l.add_value('site_domain', getattr(self, 'site_domain', None))
        l.add_value('site_name', getattr(self, 'site_name', None))

        # 兼容原有爬虫
        l.add_value('site_domain', getattr(self, 'source_domain', None))
        l.add_value('site_name', getattr(self, 'source_name', None))

        l.add_value('add_time', datetime.datetime.now())

        i = l.load_item()
        return i


class BlogLoader(object):
    '''新闻爬虫'''

    subclass_required_attrs = [
        'title_xpath',
        'content_xpath',
        'author_xpath',
        'publish_time_xpath',
        'publish_time_format'
    ]

    abstract_xpath = '//meta[@name="description"]/@content'
    keywords_xpath = '//meta[@name="keywords"]/@content'

    def __init__(self):
        for attr in self.subclass_required_attrs:
            if not getattr(self, attr, None):
                raise ValueError(
                    "%s must have a %s" % (type(self).__name__, attr)
                )

        if not getattr(self, 'site_domain', None) and \
                not getattr(self, 'source_domain', None):
            raise ValueError(
                "%s must have a site_domain" % (type(self).__name__, attr)
            )

        if not getattr(self, 'site_name', None) and \
                not getattr(self, 'source_name', None):
            raise ValueError(
                "%s must have a site_name" % (type(self).__name__, attr)
            )

    def load(self, response):
        l = ItemLoader(item=UradarBlogItem(), response=response)

        l.default_output_processor = TakeFirst()

        l.add_value('url', response.url)

        l.add_xpath('title', self.title_xpath, MapCompose(text))

        l.add_xpath('content', self.content_xpath,
                    MapCompose(SafeHtml(response.url)))

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
        if getattr(self, 'source_xpath', None) is not None:
            source_re = getattr(self, 'source_re', None)
            if source_re is None:
                l.add_xpath('source', self.source_xpath, MapCompose(text))
            else:
                l.add_xpath('source', self.source_xpath, MapCompose(text),
                            MapCompose(RegexProcessor(source_re)))

        l.add_value('site_domain', getattr(self, 'site_domain', None))
        l.add_value('site_name', getattr(self, 'site_name', None))

        # 兼容原有爬虫
        l.add_value('site_domain', getattr(self, 'source_domain', None))
        l.add_value('site_name', getattr(self, 'source_name', None))

        l.add_value('add_time', datetime.datetime.now())

        i = l.load_item()
        return i


class N100ecNewsLoader(NewsLoader):

    u"""中国电子商务研究中心新闻爬虫"""

    title_xpath = '//*[@class="newsview"]/h2'
    content_xpath = '//*[@class="nr"]'
    publish_time_xpath = '//*[@class="public f_hong"]'
    publish_time_re = u'.*(\d{4})年(\d{2})月(\d{2})日(\d{2}:\d{2}).*'
    publish_time_re_join = '-'
    publish_time_format = '%Y-%m-%d-%H:%M'
    source_xpath = '//*[@class="public f_hong"]'
    source_re = u'.*?(\S+)\s*\d{4}年\d{2}月\d{2}日\d{2}:\d{2}.*'

    site_domain = '100ec.com'
    site_name = u'中国电子商务研究中心'


class WWW163NewsLoader(NewsLoader):

    u"""网易新闻爬虫"""

    title_xpath = '//h1[@id="h1title"]'
    content_xpath = '//div[@class="end-text"]'
    author_xpath = '//*[contains(@class, "ep-source")]/*[@class="left"]'
    author_re = u'.*?作者：\s*(\S+).*'
    publish_time_xpath = '//*[contains(@class, "ep-time-soure")]'
    publish_time_re = u'.*?(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*'
    publish_time_format = '%Y-%m-%d %H:%M:%S'
    source_xpath = '//*[contains(@class, "ep-source")]/*[@class="left"]'
    source_re = u'.*?来源：\s*(\S+).*'

    source_domain = '163.com'
    source_name = u'网易'
