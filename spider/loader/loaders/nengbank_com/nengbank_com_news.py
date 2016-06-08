# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader

class NengbankComNewsLoader(NewsLoader):

    u"""能源创客聚乐部新闻"""

    title_xpath = '//*[@id="breadcrumbs"]/h1'
    content_xpath = '//*[@class="single-text"]'

    author_xpath = '//*[@class="single-meta-author"]/a'

    publish_time_xpath = '//*[@class="single-meta-time"]'
    publish_time_re_join = '-'
    publish_time_format = '%Y-%m-%d'

    source_domain = 'nengbank.com'
    source_name = u'能源创客聚乐部'
