# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader

class MohrssGovCnNewsLoader(NewsLoader):

    u"""中华人民共和国人力资源和社会保障部新闻"""

    title_xpath = '//*[@class="insMainConTitle_b"]'
    content_xpath = '//*[@class="insMainConTxt"]'

    publish_time_xpath = '//*[@class="insMainConTitle_c"]'
    publish_time_re = u'.*?发布日期：\s*(\d{4}-\d{2}-\d{2}).*'
    publish_time_format = '%Y-%m-%d'

    # source_xpath = '//*[@class="insMainConTxt_c"]'
    # source_re = u'.*?来源：\s*(\S+).*'
    source_xpath = '//*[@class="insMainConTitle_c"]/script/text()'
    source_re = u'.*?来源：\s*(\S+)\''

    source_domain = 'mohrss.gov.cn'
    source_name = u'中华人民共和国人力资源和社会保障部'
