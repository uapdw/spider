# -*- coding: utf-8 -*-

import time
import datetime

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request

from spider.items import UradarNewsItem


class GartnerSpider(CrawlSpider):
    name = 'gartner_com_news'
    allowed_domains = ['gartner.com']
    SCROLLCOUNT = 0
    SCROLLFREE = 0
    SCROLLPREMIUM = 0

    def __init__(self, crawl=None, *args, **kwargs):
        super(GartnerSpider, self).__init__(*args, **kwargs)
        self.start_urls = [
            'http://www.gartner.com/search/site/freecontent/simple',
            'http://www.gartner.com/search/site/premiumresearch/sort?sortType=\
            date&sortDir=desc'
        ]

        if(cmp(crawl, 'all') == 0):
            GartnerSpider.SCROLLCOUNT = 5

    def parse_item(self, response):
        sel = Selector(response)
        i = response.meta['item']

        content = sel.xpath('//div[@id="doc-body"]').extract()
        i['content'] = len(content) > 0 and content[0] or ''

        i['source_domain'] = 'gartner.com'
        i['source_name'] = 'gartner'
        i['add_time'] = datetime.datetime.now()

        return i

    def parse(self, response):
        sel = Selector(response)
        items = []
        reportContents = sel.xpath(
            '//table[@class="table searchResults"]/tbody/tr')[0:]
        for report in reportContents:
            i = UradarNewsItem()

            i['url'] = report.xpath('td/div/h3/a/@href').extract()[0]

            title = report.xpath('td/div/h3/a/text()').extract()
            i['title'] = len(title) > 0 and title[0].strip() or ''

            authorList = report.xpath(
                'td/div/p[@class="results-analyst"]/a/text()').extract()
            authors = len(authorList) > 0 and authorList[0].strip() or ''
            for aut in range(len(authorList) - 1):
                authors = authors + ', ' + authorList[aut + 1].strip()
            i['author'] = authors

            abstract = report.xpath(
                'td/div/p[@class="arial result-summary"]/text()'
            ).extract()

            if len(abstract) > 0:
                i['abstract'] = abstract[0]

            pubTime = report.xpath('td/div/h4/text()').extract()
            if len(pubTime) > 0:
                t = time.strptime(pubTime[0].strip(), "%d %B %Y")
                y, m, d = t[0:3]
                i['publish_time'] = datetime.date(y, m, d)

            items.append(i)

        for item in items:
            yield Request(
                item['url'],
                meta={'item': item},
                callback=self.parse_item
            )

        if self.SCROLLFREE < self.SCROLLCOUNT \
                and 'freecontent' in response.url:
            self.SCROLLFREE += 1
            urlFree = 'http://www.gartner.com/search/site/freecontent/scrollResults\
                ?&scrollRequestSuccessCount=' + (self.SCROLLFREE)
            yield Request(urlFree, callback=self.parse)

        if self.SCROLLPREMIUM < self.SCROLLCOUNT \
                and 'premiumresearch' in response.url:
            self.SCROLLPREMIUM += 1
            urlPremium = 'http://www.gartner.com/search/site/premiumresearch/\
                scrollResults?&scrollRequestSuccessCount=' + \
                str(self.SCROLLPREMIUM)
            yield Request(urlPremium, callback=self.parse)
