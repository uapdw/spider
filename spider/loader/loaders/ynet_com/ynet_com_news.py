# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader


class YnetNewsLoader(NewsLoader):

    u"""北青网新闻爬虫"""

    name = 'ynet_com_news'
    allowed_domains = ['ynet.com']
    start_urls = ['http://www.ynet.com/']

    target_urls = [
        'news\.ynet\.com/[\d\.]+/\d{4}/\d{2}/\d+\.html'
    ]

    title_xpath = '//*[@class=" BSHARE_POP"]'
    content_xpath = '//*[@id="pzoom"]'
    publish_time_xpath = '//*[@id="pubtime_baidu"]'
    publish_time_format = '%Y-%m-%d %H:%M:%S'
    source_xpath = '//*[@id="source_baidu"]'
    source_re = u'.*?来源：\s*(\S+).*'

    source_domain = 'ynet.com'
    source_name = u'北青网'
