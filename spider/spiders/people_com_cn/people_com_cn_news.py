# -*- coding: utf-8 -*-

from spider.spiders import NewsSpider


class PeopleComCnNewsSpider(NewsSpider):
    '''新浪新闻爬虫'''

    name = 'people_com_cn_news'
    allowed_domains = ['people.com.cn']
    start_urls = ['http://www.people.com.cn/']

    target_urls = [
        'people\.com\.cn/n/\d{4}/\d{4}/c\d+-\d+.html'
    ]

    title_xpath = '//*[@id="p_title"]'
    content_xpath = '//*[@id="p_content"]'
    author_xpath = '//*[@class="author"]'
    publish_time_xpath = '//*[@id="p_publishtime"]'
    publish_time_re = u'.*?(\d{4})年(\d{2})月(\d{2})日\s*(\d{2}:\d{2}).*'
    publish_time_format = '%Y%m%d%H:%M'
    source_xpath = '//*[@id="p_origin"]'
    source_re = u'.*?来源\s*(\S+).*'

    source_domain = 'people.com.cn'
    source_name = '人民网'
