# -*- coding: utf-8 -*-

from spider.spiders import NewsSpider


class ZJOLComCnNewsSpider(NewsSpider):
    '''浙江在线新闻爬虫'''

    name = 'zjol_com_cn_news'
    allowed_domains = ['zjol.com.cn']
    start_urls = ['http://www.zjol.com.cn/']

    target_urls = [
        '\w+\.zjol.com.cn/\w+/\d{4}/\d{2}/\d{2}/\d+.shtml'
    ]

    title_xpath = '//div[@class="contTit" or @class="artTitle"]'
    content_xpath = '//div[@class="contTxt"]'
    author_xpath = '//span[@id="author_baidu"]'
    author_re = u'.*?作者：\s*(\S+).*'
    publish_time_xpath = '//*[@id="pubtime_baidu"]'
    publish_time_re = u'.*?(\d{4})年(\d{2})月(\d{2})日\s+(\d{2}:\d{2}:\d{2}).*'
    publish_time_format = '%Y%m%d%H:%M:%S'
    source_xpath = '//span[@id="source_baidu"]'
    source_re = u'.*?来源：\s*(\S+).*'

    source_domain = 'zjol.com.cn'
    source_name = '浙江在线'
