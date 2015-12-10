# -*- coding: utf-8 -*-

from spider.spiders import NewsSpider


class DataTsciComCnNewsSpider(NewsSpider):

    u"""深度数据新闻爬虫"""

    name = 'data_tsci_com_cn_news'
    allowed_domains = ['data.tsci.com.cn']
    start_urls = ['http://data.tsci.com.cn/']

    target_urls = [
        'data\.tsci\.com\.cn/News/HTM/\d{8}/\d+.htm',
        'data\.tsci\.com\.cn/News/NewsShow\.aspx\?NewsId=\d+'
    ]

    title_xpath = '//*[@class="NewsTit"]'
    content_xpath = '//*[@class="NewsCon"]'
    publish_time_xpath = '//*[@class="NewsSouce"]'
    publish_time_re = u'.*(\d{4}/\d{2}/\d{2} \d{2}:\d{2}).*'
    publish_time_format = '%Y/%m/%d %H:%M'
    source_xpath = '//*[@class="NewsSouce"]'
    source_re = u'.*?来源：\s*(\S+).*'

    source_domain = 'data.tsci.com.cn'
    source_name = u'深度数据'
