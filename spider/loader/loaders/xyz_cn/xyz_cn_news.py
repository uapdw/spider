# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader

class XyzCnNewsLoader(NewsLoader):

    u"""大庆油田社保中心网站新闻"""

    title_xpath = '//*[@class="tit-news-detail"]'
    content_xpath = '//*[@id="coreText"]'

    publish_time_xpath = '//*[@class="f12 gray9 fn-left"]'
    publish_time_re = u'.*?发布日期：\s*(\d{4}).(\d{2}).(\d{2}).*'
    publish_time_re_join = '-'
    publish_time_format = '%Y-%m-%d'
    
    source_domain = 'xyz.cn'
    source_name = u'大庆油田社保中心网站'
