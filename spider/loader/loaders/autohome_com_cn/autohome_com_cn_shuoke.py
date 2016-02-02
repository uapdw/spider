# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader


class AutohomeShuoKeLoader(NewsLoader):
    u"""汽车之家说客爬虫"""

    title_xpath = '//h1/span'
    content_xpath = '//div[@class="article-context "]'
    author_xpath = '//div[@class="article-title-sub"]'
    author_re = u'.*?作者：\s*(\S+).*'
    publish_time_xpath = '//span[@class="date-time"]'
    publish_time_re = u'.*?(\d{4})-(\d{2})-(\d{2})\s+(\d{2}:\d{2}).*'
    publish_time_format = '%Y%m%d%H:%M'
    source_xpath = '//div[@class="article-title-sub"]'
    source_re = u'.*?作者：\s*(\S+).*'

    site_domain = 'autohome.com.cn'
    site_name = u'汽车之家'
