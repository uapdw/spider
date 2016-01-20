# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader


class ENorthNewsLoader(NewsLoader):
    '''北方网新闻爬虫'''

    name = 'enorth_com_cn_news'
    allowed_domains = ['enorth.com.cn']
    start_urls = ['http://www.enorth.com.cn/']

    target_urls = [
        '\w+\.enorth.com.cn/\w+/\d{4}/\d{2}/\d{2}/|w+.shtml'
    ]

    title_xpath = '//*[@class="title heiti zi24 yanse1"]'
    content_xpath = '//*[@class="zi14 hanggao24"]'
    author_xpath = '//*[@id="author_baidu"]'
    author_re = u'.*?作者：(\S+).*'
    publish_time_xpath = '//*[@id="pubtime_baidu"]'
    publish_time_re = u'.*?(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}:\d{2}).*'
    publish_time_format = '%Y-%m-%d%H:%M:%S'
    source_xpath = '//*[@id="source_baidu"]'
    source_re = u'.*?来源：\s*(\S+).*'

    source_domain = 'enorth.com.cn'
    source_name = '北方网'
