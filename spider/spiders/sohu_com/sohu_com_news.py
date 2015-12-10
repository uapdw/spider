# -*- coding: utf-8 -*-

from spider.spiders import NewsSpider


class SohuNewsSpider(NewsSpider):

    u"""搜狐新闻爬虫"""

    name = 'sohu_com_news'
    allowed_domains = ['sohu.com']
    start_urls = ['http://www.sohu.com/']

    target_urls = [
        '.*?sohu.com/\d{8}/n\d+.shtml'
    ]

    title_xpath = '//h1[@itemprop="headline"]'
    content_xpath = '//div[@itemprop="articleBody"]'
    author_xpath = '//*[@id="author_baidu"]'
    author_re = u'.*?作者：\s*(\S+).*'
    publish_time_xpath = '//*[@class="time"]'
    publish_time_format = '%Y-%m-%d %H:%M:%S'
    source_xpath = '//*[@id="source_baidu"]'
    source_re = u'.*?来源：\s*(\S+).*'

    source_domain = 'sohu.com'
    source_name = u'搜狐'
