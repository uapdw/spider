# -*- coding: utf-8 -*-

from spider.spiders import NewsSpider


class SPNComNewsSpider(NewsSpider):

    u"""睿商在线新闻爬虫"""

    name = 'spn_com_cn_news'
    allowed_domains = ['spn.com.cn']
    start_urls = ['http://www.spn.com.cn/']

    target_urls = [
        'http://www.spn.com.cn/\w+/\d+/\d+.html'
    ]

    title_xpath = '//*[@class="hei20"]'
    content_xpath = '//*[@class="h14"]'
    author_xpath = '//*[@align="center" and @class="hui12"]'
    author_re = u'.*?\S+\s+\S+\s+(\S+).*'
    publish_time_xpath = '//*[@align="center" and @class="hui12"]'
    publish_time_re = u'.*(\d{4})年(\d{1,2})月(\d{1,2})日.*'
    publish_time_format = '%Y%m%d'
    source_xpath = '//*[@align="center" and @class="hui12"]'
    source_re = u'.*?\S+\s+(\S+)\s+.*'

    source_domain = 'spn.com.cn'
    source_name = u'睿商在线'
