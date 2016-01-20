# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader


class CnsoftNewsLoader(NewsLoader):

    u"""中国软件资讯网新闻爬虫"""

    name = 'cnsoftnews_com_news'
    allowed_domains = ['cnsoftnews.com']
    start_urls = ['http://www.cnsoftnews.com/']

    target_urls = [
        'http://www.cnsoftnews.com/\w+/\d+/\d+.html'
    ]

    title_xpath = '//h1'
    content_xpath = '//*[@class="content_info"]'
    author_xpath = '//*[@class="article"]/b'
    author_re = u'.*?作者：(\S+).*'
    publish_time_xpath = '//*[@class="article"]/b'
    publish_time_re = u'.*?(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}:\d{2}).*'
    publish_time_format = '%Y-%m-%d%H:%M:%S'
    source_xpath = '//*[@class="article"]/b'
    source_re = u'.*?来源：(\S+).*'

    source_domain = 'cnsoftnews.com'
    source_name = u'中国软件资讯网'
