# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.ctgpc_com_cn.ctgpc_com_cn_news import(
    CtgpcComCnNewsLoader
)


class CtgpcComCnNewsSpider(LoaderMappingSpider):

    u"""中国长江三峡集团公司新闻爬虫"""

    name = 'ctgpc_com_cn_news'
    allowed_domains = ['ctgpc.com.cn']
    start_urls = ['http://www.ctgpc.com.cn/']

    mapping = {
        './xwzx/news.php\?mnewsid=\d+':
        CtgpcComCnNewsLoader
    }
