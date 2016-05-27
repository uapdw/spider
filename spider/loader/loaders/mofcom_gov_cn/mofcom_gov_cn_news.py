# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader, MergeLoader


class MofcomGovCnNewsLoader(MergeLoader):

    def __init__(self):
        super(MofcomGovCnNewsLoader, self).__init__([
            MofcomGovCnNewsLoader1(), MofcomGovCnNewsLoader2()
        ])


class MofcomGovCnNewsLoader1(NewsLoader):

    u"""中华人民共和国商务部新闻"""

    title_xpath = '//*[@class="artTitle"]'
    content_xpath = '//*[@class="artCon"]'
    publish_time_xpath = 'body/script/text()'
    publish_time_re = '.*?var tm = "(\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})"'
    publish_time_format = '%Y-%m-%d %H:%M:%S'
    source_xpath = 'body/script/text()'
    source_re = '.*?var source = "(\S*)"'

    source_domain = 'mofcom.gov.cn'
    source_name = u'中华人民共和国商务部'


class MofcomGovCnNewsLoader2(NewsLoader):

    u"""中华人民共和国商务部新闻"""

    title_xpath = '//*[@id="artitle"]'
    content_xpath = '//*[@class="cont"]'
    publish_time_xpath = 'body/script/text()'
    publish_time_re = '.*?var tm = "(\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})"'
    publish_time_format = '%Y-%m-%d %H:%M:%S'
    source_xpath = 'body/script/text()'
    source_re = '.*?var source = "(\S*)"'

    source_domain = 'mofcom.gov.cn'
    source_name = u'中华人民共和国商务部'
