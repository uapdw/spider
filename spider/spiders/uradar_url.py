# -*- coding: utf-8 -*-

import re

from scrapy import Spider, Request
from scrapy.linkextractors import LinkExtractor

from spider.loader.loaders import N100ecNewsLoader, WWW163NewsLoader


class UradarUrlSpider(Spider):

    u"""UradarUrl爬虫
    爬虫内注册(url的正则表达式,Item的Loader类)，对匹配的url进行item解析，
    响应中所有的url都返回一个请求
    """

    name = 'urader_url'

    allowed_domains = ['100ec.cn', '163.com']

    start_urls = ['http://www.100ec.cn', 'http://www.163.com/']

    matcher_loader_dict = {
        re.compile('100ec\.cn/detail--\d+\.html'): N100ecNewsLoader(),
        re.compile('\S+\.163.com/\d{2}/\d{4}/\d+/\S+.html'): WWW163NewsLoader()
    }

    link_extractor = LinkExtractor(
        allow=('.*'),
        allow_domains=allowed_domains
    )

    def parse(self, response):

        ret_list = []

        # 加载item
        for matcher, loader in self.matcher_loader_dict.iteritems():
            if matcher.search(response.url):
                i = loader.load(response)
                if i:
                    ret_list.append(i)

        # 添加链接
        links = [
            link.url for link in self.link_extractor.extract_links(response)
        ]
        ret_list.extend([Request(link) for link in links])

        return ret_list

