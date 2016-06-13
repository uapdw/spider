# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.xyz_cn.xyz_cn_news import(
    XyzCnNewsLoader
)


class XyzCnNewsSpider(LoaderMappingSpider):

    u"""大庆油田社保中心网站新闻爬虫"""

    name = 'xyz_cn_news'
    allowed_domains = ['xyz.cn']
    start_urls = ['http://www.xyz.cn/toptag/daqingyoutianshebaowangzhan-163930.html']

    mapping = {
        '/study/\S+-news-\d+.html':
        XyzCnNewsLoader
    }
