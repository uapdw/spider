# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader
import re,datetime


class MWRNewsLoader(NewsLoader):

    u"""国家水利部爬虫"""


    title_xpath = '//*[@id="maintabletitle" or @class="contents-title"]'
    content_xpath = '//*[@class="TRS_Editor" or @class="Zoom"]'

    publish_time_xpath = '//*[@id="authortime"]'
    
    publish_time_format = '%Y-%m-%d'
 

    source_domain = 'mwr.gov.cn'
    source_name = u'国家水利部'


    def load(self, response):
        i = super(MWRNewsLoader, self).load(response)
        publish_time_re = re.compile('t(\d+)_',re.S)

        i['publish_time'] = datetime.datetime.strptime(publish_time_re.findall(response.url)[0],'%Y%m%d')
        print i