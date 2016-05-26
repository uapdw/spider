# -*- coding: utf-8 -*-

import re
import datetime

from spider.loader.loaders import NewsLoader


publish_time_matcher = re.compile(
    '.*?chongyi\.gov\.cn/.*?/\d{6}/t(\d+)_\d+\.html'
)


class ChongyiGovCnNewsLoader(NewsLoader):

    u"""崇义县人民政府新闻"""

    title_xpath = '//*[@class="div_wztitle"]'
    content_xpath = '//*[@id="MainTxt"]'
    publish_time_xpath = '//*[@id="MainTxt"]'
    publish_time_re = u'.*(\d{4})年(\d{1,2})月(\d{1,2})日'
    publish_time_re_join = '-'
    publish_time_format = '%Y-%m-%d'

    source_domain = 'chongyi.gov.cn'
    source_name = u'崇义县人民政府'

    def load(self, response):
        i = super(ChongyiGovCnNewsLoader, self).load(response)

        if 'publish_time' not in i or not i['publish_time']:
            match = publish_time_matcher.match(response.url)
            if match:
                i['publish_time'] = datetime.datetime.strptime(
                    match.group(1),
                    '%Y%m%d'
                )

        return i
