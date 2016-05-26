# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader


class JxstcGovCnNewsLoader(NewsLoader):

    u"""江西省科学技术厅新闻"""

    title_xpath = u'//*[@face="楷体_GB2312"]/strong'
    content_xpath = '//*[@id="fontzoom"]'

    publish_time_xpath = u'//*[@face="楷体_GB2312"]/..'
    publish_time_re = u'.*?发表日期：(\d{4})年(\d{1,2})月(\d{1,2})日'
    publish_time_re_join = u'-'
    publish_time_format = '%Y-%m-%d'

    source_domain = 'jxstc.gov.cn'
    source_name = u'江西省科学技术厅'
