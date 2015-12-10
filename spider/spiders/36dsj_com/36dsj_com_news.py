# -*- coding: utf-8 -*-

from spider.spiders import NewsSpider


class N36dsjNewsSpider(NewsSpider):

    u"""36dsj新闻爬虫"""

    name = '36dsj_com_news'
    allowed_domains = ['36dsj.com']
    start_urls = ['http://www.36dsj.com/']

    target_urls = [
        '36dsj\.com/archives/\d+'
    ]

    title_xpath = '//*[@class="article-title"]'
    content_xpath = '//*[@class="article-content"]'
    author_xpath = '//*[@class="article-meta"]/li[1]'
    # author_re = u'.*?作者：\s*(\S+).*'
    publish_time_xpath = '//*[@class="article-meta"]/li[2]'
    publish_time_format = '%Y-%m-%d %H:%M:%S'
    source_xpath = '//*[@class="article-meta"]/li[3]'

    source_domain = '36dsj.com'
    source_name = u'36大数据'
