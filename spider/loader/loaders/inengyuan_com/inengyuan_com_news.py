# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader

class InengyuanComNewsLoader(NewsLoader):

    u"""能源经济网新闻"""

    title_xpath = '//*[@class="rel_detail"]/h1'
    content_xpath = '//*[@class="ns_detail"]'

    author_xpath = '//*[@class="rel_detail"]/h2'
    author_re = u'.*?作者：\s*(\S+).*'

    publish_time_xpath = '//*[@class="rel_detail"]/h2'
    publish_time_re = u'.*?发布时间：\s*(\d{4}-\d{2}-\d{2}).*'
    publish_time_format = '%Y-%m-%d'

    source_xpath = '//*[@class="rel_detail"]/h2'
    source_re = u'.*?来源：\s*(\S+).*'

    source_domain = 'inengyuan.com'
    source_name = u'能源经济网'
