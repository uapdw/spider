# -*- coding: utf-8 -*-

from spider.spiders import NewsSpider


class GmwNewsSpider(NewsSpider):

    u"""光明网新闻爬虫"""

    name = 'gmw_cn_news'
    allowed_domains = ['gmw.cn']
    start_urls = ['http://gmw.cn/']

    target_urls = [
        'gmw\.cn/\d{4}-\d{2}/\d{2}/content_\d+\.htm'
    ]

    title_xpath = '//*[@id="articleTitle" or @class="picContentHeading"]'
    content_xpath = '//*[@id="contentMain" or @id="ArticleContent"]'
    author_xpath = '//*[@id="contentLiability"]'
    author_re = u'.*?责任编辑:\s*(\S+)\].*'
    publish_time_xpath = '//*[@id="pubTime"]'
    publish_time_format = '%Y-%m-%d %H:%M'
    source_xpath = '//*[@id="source"]'
    source_re = u'.*?来源：\s*(\S+).*'

    source_domain = 'gmw.cn'
    source_name = u'光明网'
