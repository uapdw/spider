# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader
import re,datetime


class MOFNewsLoader(NewsLoader):

    u"""国家财政部爬虫"""


    title_xpath = '//*[@class="font_biao1"]'
    content_xpath = '//*[@class="TRS_Editor" or @class="Custom_UnionStyle"]'
    publish_time_xpath = '//*[@class="TRS_Editor"]'

    publish_time_format = '%Y-%m-%d'
    source_xpath = '//*[@class="TRS_Editor"]'
    source_re = u'.*?来源：\s*(\S+).*'

    source_domain = 'mof.gov.cn'
    source_name = u'国家财政部'


    def load(self, response):
        i = super(MOFNewsLoader, self).load(response)
        publish_time_re = re.compile('t(\d+)_',re.S)

        i['publish_time'] = datetime.datetime.strptime(publish_time_re.findall(response.url)[0],'%Y%m%d')
        print i
