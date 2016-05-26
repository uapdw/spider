# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader


class ChinataxGovCnNewsLoader(NewsLoader):

    u"""国家税务总局新闻"""

    title_xpath = '//*[@class="sv_texth1"]'
    content_xpath = '//*[@class="sv_texth3"]'

    publish_time_xpath = '//*[@class="sv_texth2"]'
    publish_time_re = u'.*?发布日期：\s*(\d{4})年(\d{2})月(\d{2})日.*'
    publish_time_re_join = '-'
    publish_time_format = '%Y-%m-%d'

    source_xpath = '//*[@class="sv_texth2"]'
    source_re = u'.*?来源：\s*(\S+).*'

    source_domain = 'chinatax.gov.cn'
    source_name = u'国家税务总局'
