# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader

class CrcComHkNewsLoader(NewsLoader):

    u"""华润集团新闻"""

    title_xpath = '//*[@class="newsContent"]/div[1]/h1'
    content_xpath = '//*[@class="Custom_UnionStyle"]'

    publish_time_xpath = '//*[@class="info"]'
    publish_time_re = u'.*?发稿时间：\s*(\d{4}-\d{2}-\d{2}).*'
    publish_time_format = '%Y-%m-%d'

    source_xpath = '//*[@class="info"]'
    source_re = u'.*?来源：\s*(\S+).*'

    source_domain = 'crc.com.hk'
    source_name = u'华润集团'
