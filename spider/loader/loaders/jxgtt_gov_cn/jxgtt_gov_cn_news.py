# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader, MergeLoader


class JxgttGovCnNewsLoader(MergeLoader):

    def __init__(self):
        super(JxgttGovCnNewsLoader, self).__init__([
            JxgttGovCnNewsLoader1(),
            JxgttGovCnNewsLoader2()
        ])


class JxgttGovCnNewsLoader1(NewsLoader):

    u"""江西省国土资源厅新闻"""

    title_xpath = '//*[@class="titleNews"]'
    content_xpath = '//*[@class="newsCont"]'

    publish_time_xpath = '//*[@class="infoNews"]'
    publish_time_re = u'.*?日期：(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})'
    publish_time_format = '%Y-%m-%d %H:%M:%S'

    source_domain = 'jxgtt.gov.cn'
    source_name = u'江西省国土资源厅'


class JxgttGovCnNewsLoader2(NewsLoader):

    u"""江西省国土资源厅新闻"""

    title_xpath = '//*[@class="newstitle"]'
    content_xpath = '//*[@class="newcontent"]'

    publish_time_xpath = '//*[@class="data"]'
    publish_time_re = u'.*?日期：(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})'
    publish_time_format = '%Y-%m-%d %H:%M:%S'

    source_domain = 'jxgtt.gov.cn'
    source_name = u'江西省国土资源厅'
