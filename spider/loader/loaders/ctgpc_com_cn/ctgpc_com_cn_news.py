# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader

class CtgpcComCnNewsLoader(NewsLoader):

    u"""中国长江三峡集团公司新闻"""

    title_xpath = '//*[@class="xwxx"]/div[1]'
    content_xpath = '//*[@class="xwxx"]/div[2]'

    publish_time_xpath = '//*[@class="xwxx"]/div[4]'
    publish_time_re = u'.*?发布日期：\s*(\d{4}-\d{2}-\d{2}).*'
    publish_time_format = '%Y-%m-%d'

    source_xpath = '//*[@class="xwxx"]/div[3]'
    source_re = u'.*?信息来源：\s*(\S+).*'

    source_domain = 'ctgpc.com.cn'
    source_name = u'中国长江三峡集团公司'
