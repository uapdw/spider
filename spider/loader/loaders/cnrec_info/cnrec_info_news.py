# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader

class CnrecInfoNewsLoader(NewsLoader):

    u"""中国可再生能源信息网新闻"""

    title_xpath = '//*[@class="article_content"]/h1'
    content_xpath = '//*[@class="article_content_list"]'

    publish_time_xpath = '//*[@class="article_info"]'
    publish_time_re = u'.*(\d{4}-\d{2}-\d{2}).*'
    publish_time_format = '%Y-%m-%d'

    source_xpath = '//*[@class="article_info"]'
    source_re = u'.*?来源：\s*(\S+).*'

    source_domain = 'cnrec.info'
    source_name = u'中国可再生能源信息网'
