# -*- coding: utf-8 -*-

import re
import datetime

from spider.loader.loaders import NewsLoader

publish_time_matcher = re.compile(
    '.*?\S+.mof.gov.cn/\S+/\S+/\d{6}/t(\d{8})_\d+.htm'
)


class MofGovCnNewsLoader(NewsLoader):

    u"""中华人民共和国财政部新闻"""

    title_xpath = '//*[@class="font_biao1"]'
    content_xpath = '//*[@class="TRS_Editor"]'

    publish_time_xpath = '//*[@class="TRS_Editor"]'
    publish_time_re = u'.*(\d{4})年(\d{1,2})月(\d{2})日.*'
    publish_time_re_join = '-'
    publish_time_format = '%Y-%m-%d'

    source_xpath = '//*[@class="TRS_Editor"]'
    source_re = u'.*?来源：\s*(\S+).*'

    source_domain = 'mof.gov.cn'
    source_name = u'中华人民共和国财政部'

    def load(self, response):
        i = super(MofGovCnNewsLoader, self).load(response)

        if 'publish_time' not in i or not i['publish_time']:
            match = publish_time_matcher.match(response.url)
            if match:
                i['publish_time'] = datetime.datetime.strptime(
                    match.group(1),
                    '%Y%m%d'
                )

        return i

