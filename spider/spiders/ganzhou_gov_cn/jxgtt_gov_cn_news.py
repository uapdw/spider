# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import JXGttNewsLoader


class JXGttNewsSpider(LoaderMappingSpider):
    '''江西省国土资源厅爬虫'''

    name = 'jxgtt_gov_cn_news' 
    allowed_domains = [ 'jxgtt.gov.cn', ]
    start_urls = ['http://www.jxgtt.gov.cn/']

    mapping = {
        'News.shtml\?p5=\d+&col=\d+': JXGttNewsLoader
    }