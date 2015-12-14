# -*- coding: utf-8 -*-

from spider.spiders import NewsSpider


class HexunNewsSpider(NewsSpider):

    u"""和讯新闻爬虫"""

    name = 'hexun_com_news'
    allowed_domains = ['hexun.com']
    start_urls = ['http://www.hexun.com/']

    target_urls = [
        'hexun\.com/\d{4}-\d{2}-\d{2}/\d+\.html'
    ]

    title_xpath = '//*[@id="artibodyTitle"]/h1'
    content_xpath = '//*[@id="artibody"]'
    author_xpath = '//*[@id="arctTailMark"]/following::*'
    author_re = u'.*?（责任编辑：\s*(\S+)\s*.*）.*'
    publish_time_xpath = '//*[@id="pubtime_baidu"]'
    publish_time_format = '%Y-%m-%d %H:%M:%S'
    source_xpath = '//*[@id="source_baidu"]'
    source_re = u'.*?来源：\s*(\S+).*'

    source_domain = 'hexun.com'
    source_name = u'和讯网'
