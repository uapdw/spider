# -*- coding: utf-8 -*-

import datetime
import re

from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.spiders import CrawlSpider

from spider.items import PM25ChinaItem


class PM25ChinaSpider(CrawlSpider):

    name = 'pm25china_net_pm25'
    allowed_domain = ['pm25china.net']
    start_urls = ["http://www.pm25china.net"]

    def parse(self, response):
        sel = Selector(response)
        urllist = sel.xpath('//div[@class="warp"]/a/@href').extract()
        for url in urllist:
            requesturl = 'http://www.pm25china.net' + url
            yield Request(requesturl, callback=self.parse_item)

    def parse_item(self, response):
        sel = Selector(response)

        trlist = sel.xpath('//table[@id="xiang1"]/tr')
        items = []
        for tr in trlist:
            td = tr.xpath('td')
            item = PM25ChinaItem()
            item['areacode'] = response.url.split('/')[-2] + 'shi'
            item['areaname'] = sel.xpath('//span[@class="tqnav_11"]/text()').extract()[0]
            script = sel.xpath('//div[@class="left614"]//script[@type="text/javascript"]').extract()
            item['index_value'] = len(script) > 0 and re.findall(r'jin_value \= "\d+"',script[0])[0].split('"')[1] or ''
            item['publishtime'] = sel.xpath('//h1/span/text()').extract()[0].split(u'\uff1a')[1]
            item['monitor_code'] = td[0].xpath('a/@href').extract()[0].split('_')[1].replace('/','')
            item['monitor_name'] = td[0].xpath('a/text()').extract()[0]
            item['monitor_aqi'] = td[1].xpath('text()').extract()[0]
            #jiangkongdian_pm25 = td[2].xpath('img/@alt').extract()[0].split(u'\uff1a')[1]
            item['monitor_pm25'] = td[3].xpath('text()').extract()[0]
            item['monitor_pm10'] = td[4].xpath('text()').extract()[0]
            item['monitor_key'] = len(td[5].xpath('text()')) > 0 and td[5].xpath('text()').extract()[0] or ''
            item['crawltime'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
            items.append(item)
        return items
