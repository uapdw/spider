# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader


class ZdnetNewsLoader(NewsLoader):

    u"""至顶网新闻爬虫"""

    name = 'zdnet_com_cn_news'
    allowed_domains = ['zdnet.com.cn']
    start_urls = ['http://www.zdnet.com.cn']

    target_urls = [
        'zdnet\.com\.cn/.*/\d{4}/\d{4}/\d+\.shtml'
    ]

    title_xpath = '//*[@class="foucs_title" or @class="root_h1"]'
    content_xpath = '//*[@class="qu_ocn"]'
    author_xpath = '//*[@class="qu_zuo"]'
    author_re = u'.*?作者：\s*(\S+).*'
    publish_time_xpath = '//*[@class="qu_zuo"]'
    publish_time_re = u'.*(\d{4})年(\d{2})月(\d{2})日.*'
    publish_time_re_join = '-'
    publish_time_format = '%Y-%m-%d'
    source_xpath = '//*[@class="qu_zuo"]'
    source_re = u'.*?来源：\s*(\S+).*'

    source_domain = 'zdnet.com.cn'
    source_name = u'至顶网'
