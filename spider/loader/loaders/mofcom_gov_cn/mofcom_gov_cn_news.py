# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader

class MofcomGovCnNewsLoader(NewsLoader):

    u"""中华人民共和国商务部新闻"""

    title_xpath = '//*[@class="artTitle"]'
    content_xpath = '//*[@class="artCon"]'

    publish_time_xpath = '//*[@class="artInfo"]/script/tm'
    publish_time_re = u'.*(\d{4}-\d{2}-\d{2}  \d{2}:\d{2}).*'
    publish_time_format = '%Y-%m-%d %H:%M'

    source_xpath = '//*[@class="artInfo"]/script/a'

    source_domain = 'mofcom.gov.cn'
    source_name = u'中华人民共和国商务部'
