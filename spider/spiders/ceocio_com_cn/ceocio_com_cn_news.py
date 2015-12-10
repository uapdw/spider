# -*- coding: utf-8 -*-

from spider.spiders import NewsSpider


class CeocioNewsSpider(NewsSpider):
    '''经理世界网新闻爬虫'''

    name = 'ceocio_com_cn_news'
    allowed_domains = ['ceocio.com.cn']
    start_urls = ['http://www.ceocio.com.cn/']

    target_urls = [
        'ceocio\.com\.cn/.*/\d{4}-\d{2}-\d{2}/\d+\.shtml'
    ]

    title_xpath = '//*[@class="news_title"]'
    content_xpath = '//*[@class="news_body"]'
    author_xpath = '//*[@class="news_from"]'
    author_re = u'.*?作者：\s*(\S+).*'
    publish_time_xpath = '//*[@class="news_from"]'
    publish_time_re = u'.*时间：\s*(\d{4}-\d{2}-\d{2}).*'
    publish_time_format = '%Y-%m-%d'
    source_xpath = '//*[@class="news_from"]'
    source_re = u'.*?来源：\s*(\S+).*'

    source_domain = 'ceocio.com.cn'
    source_name = u'经理世界网'
