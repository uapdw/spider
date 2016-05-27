# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader
import re,datetime


class MEPNewsLoader(NewsLoader):

    u"""国家环境保护部爬虫"""


    title_xpath = '//*[@class="title" or @class="dthh21" or @class="details_title"]'
    content_xpath = '//*[@class="Custom_UnionStyle" or @id="ContentRegion" or @class="TRS_Editor"]'

    publish_time_xpath = '//*[@id="authortime"]'

    publish_time_format = '%Y-%m-%d'


    source_domain = 'mep.gov.cn'
    source_name = u'国家环境保护部'


    def load(self, response):
        i = super(MEPNewsLoader, self).load(response)
        publish_time_re = re.compile('t(\d+)_',re.S)

        i['publish_time'] = datetime.datetime.strptime(publish_time_re.findall(response.url)[0],'%Y%m%d')
        print i