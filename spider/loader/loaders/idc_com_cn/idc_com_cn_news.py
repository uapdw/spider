# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader


class IdcNewsLoader(NewsLoader):

    u"""idc新闻爬虫"""

    name = 'idc_com_cn_news'
    allowed_domains = ['idc.com.cn']
    start_urls = ['http://www.idc.com.cn/']

    target_urls = [
        'idc\.com\.cn/about/press\.jsp\?id=\S+'
    ]

    title_xpath = '//*[@class="bodybkbd"]'
    content_xpath = '//*[@class="bodybk"]'
    publish_time_xpath = '//*[@class="bodybk"]'
    publish_time_re = u'.*日期：\s*(\d{4}-\d{2}-\d{2}).*'
    publish_time_format = '%Y-%m-%d'
    source_xpath = '//*[@class="bodybk"]'
    source_re = u'.*信息来源：\s*(\S+).*'

    source_domain = 'idc.com.cn'
    source_name = 'IDC'
