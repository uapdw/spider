# -*- coding: utf-8 -*-

from spider.spiders import NewsSpider


class TechwebNewsSpider(NewsSpider):
    '''TechWeb新闻爬虫'''

    name = 'techweb_com_cn_news'
    allowed_domains = ['techweb.com.cn']
    start_urls = ['http://www.techweb.com.cn/']

    target_urls = [
        'www\.techweb\.com\.cn/\S+/\d{4}-\d{2}-\d{2}/\d+\.shtml'
    ]

    title_xpath = '//*[@class="title"]'
    content_xpath = '//*[@class="content_txt"]'
    author_xpath = '//*[@class="author"]'
    author_re = u'.*?作者:\s*(\S+).*'
    publish_time_xpath = '//*[@class="date"]'
    publish_time_format = '%Y.%m.%d %H:%M:%S'
    source_xpath = '//*[@class="where"]'
    source_re = u'.*?来源:\s*(\S+).*'

    source_domain = 'techweb.com.cn'
    source_name = 'TechWeb'
