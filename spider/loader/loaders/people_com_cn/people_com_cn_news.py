# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader


class PeopleComCnNewsLoader(NewsLoader):

    u"""人民网新闻爬虫"""

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
    source_name = u'人民网'


class N1PeopleComCnNewsLoader(NewsLoader):

    u"""中国共产党新闻网新闻爬虫"""

    title_xpath = '//*[contains(@class, "text_c")]/h1'
    content_xpath = '//*[@class="text_show"]'
    publish_time_xpath = '//*[contains(@class, "text_c")]/h5'
    publish_time_re = u'.*?(\d{4})年(\d{2})月(\d{2})日(\d{2}:\d{2})\s+来源：\S+'
    publish_time_re_join = '-'
    publish_time_format = '%Y-%m-%d-%H:%M'
    source_xpath = '//*[contains(@class, "text_c")]/h5'
    source_re = u'.*?\d{4}年\d{2}月\d{2}日\d{2}:\d{2}\s+来源：(\S+)'

    source_domain = 'people.com.cn'
    source_name = u'人民网'
