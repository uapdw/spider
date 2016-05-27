# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader


class GZJxgttNewsLoader(NewsLoader):

    u"""赣州市国土资源局爬虫"""


    title_xpath = '//*[@class="newstitle"]'
    content_xpath = '//*[@class="newsnr news"]'

    publish_time_xpath = '//*[@width="24%"]'
    publish_time_re = u'.*?日期：\s*(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*'
    
    publish_time_format = '%Y-%m-%d %H:%M:%S'
    source_xpath = '//*[@width="37%"]'
    source_re = u'.*?稿源：\s*(\S+).*'

    source_domain = 'gz.jxgtt.gov.cn'
    source_name = u'赣州市国土资源局'