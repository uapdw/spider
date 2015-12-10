# -*- coding: utf-8 -*-

from spider.spiders import NewsSpider


class ZolNewsSpider(NewsSpider):

    u"""中关村在线新闻爬虫"""

    name = 'zol_com_cn_news'
    allowed_domains = ['zol.com.cn']
    start_urls = ['http://www.zol.com.cn/']

    target_urls = [
        'zol\.com\.cn/\d+/\d+\.html'
    ]

    title_xpath = '//*[contains(@class, "article-header") or \
                  @class="article-tit"]/h1'
    content_xpath = '//*[@id="article-content"]'
    author_xpath = '//*[@class="editor"]'
    publish_time_xpath = '//*[@id="pubtime_baidu"]'
    publish_time_format = '%Y-%m-%d %H:%M:%S'
    source_xpath = '//*[@id="source_baidu"]'
    source_re = u'.*?\[\s*(.*)\s*\].*'

    source_domain = 'zol.com.cn'
    source_name = u'中关村在线'
