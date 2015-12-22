# -*- coding: utf-8 -*-

from spider.spiders import NewsSpider


class N100ecNewsSpider(NewsSpider):

    u"""中国电子商务研究中心新闻爬虫"""

    name = '100ec_cn_news'
    allowed_domains = ['100ec.cn']
    start_urls = ['http://www.100ec.cn']

    target_urls = [
        '100ec\.cn/detail--\d+\.html'
    ]

    title_xpath = '//*[@class="newsview"]/h2'
    content_xpath = '//*[@class="nr"]'
    publish_time_xpath = '//*[@class="public f_hong"]'
    publish_time_re = u'.*(\d{4})年(\d{2})月(\d{2})日(\d{2}:\d{2}).*'
    publish_time_re_join = '-'
    publish_time_format = '%Y-%m-%d-%H:%M'
    source_xpath = '//*[@class="public f_hong"]'
    source_re = u'.*?(\S+)\s*\d{4}年\d{2}月\d{2}日\d{2}:\d{2}.*'

    site_domain = '100ec.com'
    site_name = u'中国电子商务研究中心'
