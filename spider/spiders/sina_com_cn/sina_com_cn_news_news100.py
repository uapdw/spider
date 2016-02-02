# -*- coding: utf-8 -*-

import json

from scrapy.http import Request
from scrapy import Spider

from spider.loader.loaders import SinaNewsLoader

__author__ = 'liufeng'


class SinaComCnNews100NewsSpider(Spider):

    name = 'sina_com_cn_news_100news'
    allowed_domain = ['auto.sina.com.cn']
    api_url_pre = 'http://news.auto.sina.com.cn/m/label/get_label_info.php?label=%E8%AF%84%E8%AE%BA%2C%E4%BA%A7%E4%B8%9A%2C%E5%8D%A1%E8%BD%A6%2C%E5%AE%A2%E8%BD%A6%2C%E4%BC%81%E4%B8%9A%2C%E8%B4%A2%E7%BB%8F%2C%E5%8F%AC%E5%9B%9E%2C%E8%90%A5%E9%94%80%2C%E8%AE%BF%E8%B0%88'
    api_url_pattern = '&length=%s&page=%s'

    page_size = 100

    def start_requests(self):
        return [Request(
            self.api_url_pre + self.api_url_pattern % (self.page_size, 1)
        )]

    def parse(self, response):
        data = json.loads(response.body)

        for d in data['data']:
            url = d['share_url']
            yield Request(url, callback=self.parse_news)

    def parse_news(self, response):
        l = SinaNewsLoader()
        return l.load(response)
