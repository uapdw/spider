# -*- coding: utf-8 -*-

# import re
# import datetime

from spider.loader.loaders import NewsLoader
#
# publish_time_matcher = re.compile(
#     news.cnpc.com.cn/system/2016/05/30/001594573.shtml
#     '.*?www.ndrc.gov.cn/xwzx/xwfb/\d{6}/t(\d{8})_\d+.html'
# )

class CnpcComCnNewsLoader(NewsLoader):

    u"""中国石油新闻中心新闻"""

    title_xpath = '//*[@class="sj-title"]/h2'
    content_xpath = '//*[@class="sj-main"]'

    author_xpath = '//*[@class="ly-c fl"]'
    author_re = u'.*?作者：\s*(\S+).*'

    publish_time_xpath = '//*[@class="sj-t"]/a'
    publish_time_re = u'.*?发表日期：\s*(\d{4}-\d{2}-\d{2} \d{2}:\d{2}).*'
    publish_time_format = '%Y-%m-%d %H:%M'

    source_xpath = '//*[@class="ly-l fl"]/a'

    source_domain = 'cnpc.com.cn'
    source_name = u'中国石油新闻中心'
