# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class LoaderMappingSpider(CrawlSpider):

    mapping = None

    def __init__(self):
        if not getattr(self, 'mapping', None):
            raise ValueError(
                "%s must have a mapping" % type(self).__name__
            )
        self.__generate_rules()
        super(LoaderMappingSpider, self).__init__()

    def __generate_rules(self):
        '''生成scrapy.contrib.spiders.CrawlSpider中的rules
        '''
        rule_list = []
        for url, loader in self.mapping.iteritems():
            rule = Rule(
                LinkExtractor(allow=(url),
                              allow_domains=self.allowed_domains),
                callback=lambda response: loader().load(response),
                follow=False)
            rule_list.append(rule)
        rule_list.append(
            Rule(
                LinkExtractor(allow=('.*'), allow_domains=self.allowed_domains)
            )
        )
        self.rules = tuple(rule_list)
