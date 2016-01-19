# -*- coding: utf-8 -*-

import re
import json

from scrapy import Spider, Request
from scrapy.linkextractors import LinkExtractor

import spider.loader.loaders as loaders


class UradarUrlSpider(Spider):

    u"""UradarUrl爬虫
    爬虫内注册(url的正则表达式,Item的Loader类)，对匹配的url进行item解析，
    响应中所有的url都返回一个请求
    """

    name = 'uradar_url'

    def __init__(self, config_path=None, *args, **kwargs):
        super(UradarUrlSpider, self).__init__(*args, **kwargs)
        f = open(config_path)
        self.config = json.loads(f.read())
        f.close()

        self.start_urls = []
        self.allowed_domains = []
        self.matcher_loader_dict = {}
        for item in self.config:
            self.start_urls.extend(item['start_urls'])
            self.allowed_domains.extend(item['allowed_domains'])

            loader_name = item['loader_name']
            loader_class = getattr(loaders, loader_name, None)
            if not loader_class:
                raise ValueError('can not find %s' % loader_name)

            for target_url in item['target_urls']:
                self.matcher_loader_dict[
                    re.compile(target_url)
                ] = loader_class()

        self.link_extractor = LinkExtractor(
            allow=('.*'),
            allow_domains=self.allowed_domains
        )
        import pdb;pdb.set_trace()

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

