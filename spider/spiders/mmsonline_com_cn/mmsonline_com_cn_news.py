# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.mmsonline_com_cn.mmsonline_com_cn_news import (
    MmsonlineComCnNewsLoader
)


class MmsonlineComCnNewSpider(LoaderMappingSpider):

    u"""国际金属加工网新闻爬虫"""

    name = 'mmsonline_com_cn_news'
    allowed_domains = [
        'mmsonline.com.cn'
    ]
    start_urls = ['http://www.mmsonline.com.cn/']

    mapping = {
        'mmsonline\.com\.cn/info/\d+.shtml':
        MmsonlineComCnNewsLoader
    }
