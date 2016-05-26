# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader


class ZccctComNewsLoader(NewsLoader):

    u"""株洲钻石切削刀具股份有限公司新闻"""

    title_xpath = '//center/text()'
    content_xpath = '//*[@class="solution_right2_content"]'
    publish_time_xpath = '//center/p'
    publish_time_re = u'.*?发布时间：(\d{4}/\d{1,2}/\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})'
    publish_time_format = '%Y/%m/%d %H:%M:%S'

    source_domain = 'zccct.com'
    source_name = u'株洲钻石切削刀具股份有限公司'
