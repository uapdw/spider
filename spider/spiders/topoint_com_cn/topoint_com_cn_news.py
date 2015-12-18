# -*- coding: utf-8 -*-

from spider.spiders import NewsSpider


class TopointNewsSpider(NewsSpider):

    u"""支点网新闻爬虫"""

    name = 'topoint_com_cn_news'
    allowed_domains = ['topoint.com.cn']
    start_urls = ['http://www.topoint.com.cn/']

    target_urls = [
        'http://www.topoint.com.cn/html/article/\d{4}/\d+/\d+.html'
    ]

    title_xpath = '//h1'
    content_xpath = '//div[@id="content"]'
    author_xpath = '//div[@class="other"]'
    author_re = u'.*?作者：(\S+).*'
    publish_time_xpath = '//div[@class="other"]'
    publish_time_re = u'.*?(\d{4}-\d{1,2}-\d{1,2})\s+(\d{2}:\d{2}:\d{2}).*'
    publish_time_format = '%Y-%m-%d%H:%M:%S'
    source_xpath = '//div[@class="other"]'
    source_re = u'.*?来源：(\S+).*'

    source_domain = 'topoint.com.cn'
    source_name = u'支点网'
