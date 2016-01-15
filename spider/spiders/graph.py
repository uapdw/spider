# -*- coding: utf-8 -*-

from scrapy import Spider, Request
from scrapy.linkextractors import LinkExtractor
from scrapy.item import Item, Field


class LinkItem(Item):
    url = Field()
    links = Field()


class GraphSpider(Spider):
    '''抓取域名中的链接'''

    name = "graph_spider"

    def __init__(self, domain=None, *args, **kwargs):
        super(GraphSpider, self).__init__(*args, **kwargs)
        self.start_urls = [
            'http://%s' % domain
        ]
        self.allowed_domains = [domain]
        self.link_extractor = LinkExtractor(
            allow=('.*'),
            allow_domains=self.allowed_domains
        )

    def parse(self, response):

        ret_list = []

        url = response.url
        links = [
            link.url for link in self.link_extractor.extract_links(response)
        ]

        i = LinkItem()
        i['url'] = url
        i['links'] = links
        ret_list.append(i)

        ret_list.extend([Request(link) for link in links])

        return ret_list
