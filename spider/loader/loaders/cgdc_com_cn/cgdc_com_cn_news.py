# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader

class CgdcComCnNewsLoader(NewsLoader):

    u"""中国国电集团公司新闻"""

    title_xpath = '//*[@class="biaoti1"]/h1'
    content_xpath = '//*[@class="wenzi"]'

    publish_time_xpath = '//*[@class="con"]/div[2]/span'
    publish_time_re = u'.*?发布日期：\s*(\d{2})/(\d{2})/(\d{2}).*'
    publish_time_re_join = '-'
    publish_time_format = '%y-%m-%d'

    source_xpath = '//*[@class="con"]/div[2]/span/a'

    source_domain = 'cgdc.com.cn'
    source_name = u'中国国电集团公司'
