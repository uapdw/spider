# -*- coding: utf-8 -*-

from spider.spiders import NewsSpider


class YidonghuaNewsSpider(NewsSpider):

    u"""移动信息化新闻爬虫"""

    name = 'yidonghua_com_news'
    allowed_domains = ['yidonghua.com']
    start_urls = ['http://www.yidonghua.com']

    target_urls = [
        'yidonghua\.com/post/\d+\.html'
    ]

    title_xpath = '//*[@class="title"]'
    content_xpath = '//*[@id="wrap-content"]/*[@class="content"]'
    publish_time_xpath = '//*[@class="meta_date"]'
    publish_time_re = '.*(\d{4}/\d{2}/\d{2}).*'
    publish_time_format = '%Y/%m/%d'

    source_domain = 'yidonghua.com'
    source_name = u'移动信息化'
