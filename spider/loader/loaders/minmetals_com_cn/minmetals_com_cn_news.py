# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader


class MinmetalsComCnNewsLoader(NewsLoader):

    u"""中国五矿集团公司新闻"""

    title_xpath = '//*[@class="xl_title"]'
    content_xpath = '//*[@class="xl_cont"]'
    publish_time_xpath = '//*[@class="xl_time"]'
    publish_time_format = '%Y-%m-%d'
    source_xpath = '//*[@class="xl_ly"]'
    source_re = u'.*?文章来源：\s*(\S+)'

    source_domain = 'minmetals.com.cn'
    source_name = u'中国五矿集团公司'
