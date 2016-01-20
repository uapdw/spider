# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader


class ChinaNewsLoader(NewsLoader):
    '''中华网新闻爬虫'''

    name = 'china_com_news'
    allowed_domains = ['china.com']
    start_urls = ['http://www.china.com/index.html']

    target_urls = [
        '\w+\.china.com/\w+/\w*/\d+/\d{8}/\d{8}_all.html'
    ]

    title_xpath = '//h1[@id="chan_newsTitle"]'
    content_xpath = '//div[@id="chan_newsDetail"]'
    author_xpath = '//div[@class="editor"]'
    author_re = u'.*?\(责任编辑：(\S+)\).*'
    publish_time_xpath = '//div[@id="chan_newsInfo"]'
    publish_time_re = u'.*?(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}:\d{2}).*'
    publish_time_format = '%Y-%m-%d%H:%M:%S'
    source_xpath = '//div[@id="chan_newsInfo"]'
    source_re = u'.*?\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}\s*(\S+)\s*参与评论.*'

    source_domain = 'china.com'
    source_name = '中华网'
