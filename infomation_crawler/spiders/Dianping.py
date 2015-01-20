# -*- coding: utf-8 -*-
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider,Rule


from infomation_crawler.items import DianPing
import datetime
import pymongo
from scrapy import Spider,Request
import re


class DianpingSpider(CrawlSpider):
    name = 'Dianping'
    allowed_domains = ['dianping.com']
    urls = []
    temp = "0_%E5%A4%A7%E5%A8%98%E6%B0%B4%E9%A5%BA"
    for i in range(1,18):
         urls.append(
             'http://www.dianping.com/search/keyword/%s/' % i + temp
         )
    start_urls = urls
    conn = pymongo.Connection('localhost',27017)
    infoDB = conn.info
    tDazhongdp = infoDB.dazhongdp
    rules = [
        Rule(SgmlLinkExtractor(allow=(r'/search/keyword/\d/0_%E5%A4%A7%E5%A8%98%E6%B0%B4%E9%A5%BA/p\d'))),
        Rule(SgmlLinkExtractor(allow=(r'http://www.dianping.com/shop/\d+'),deny=r'review'),callback='parse_item'),
    ]



    def parse_item(self, response):
        re_d = re.compile(r'\d+')
        sel = Selector(response)
        i = DianPing()
        shopid = re_d.findall(response.url)
        i['shopid'] = len(shopid)>0 and shopid[0] or ''
        brief = sel.xpath('//div[@class="brief-info"]/span')[0:]
        level = sel.xpath('//div[@class="brief-info"]/span[1]/@title').extract()
        i['level'] = len(level)>0 and level[0] or ''
        comment = sel.xpath('//div[@class="brief-info"]/span[2]/text()').extract()[0]
        if u"\uff1a" in comment:
            i['comment'] = ''
            consume = sel.xpath('//div[@class="brief-info"]/span[2]/text()').extract()
            i['consume'] = len(consume)>0 and consume[0].split(u'\uff1a')[1].strip() or ''
            taste = sel.xpath('//div[@class="brief-info"]/span[3]/text()').extract()
            i['taste'] = len(taste)>0 and taste[0].split(u'\uff1a')[1].strip() or ''
            environment = sel.xpath('//div[@class="brief-info"]/span[4]/text()').extract()
            i['environment'] = len(environment)>0 and environment[0].split(u'\uff1a')[1].strip() or ''
            service = sel.xpath('//div[@class="brief-info"]/span[5]/text()').extract()
            i['service'] = len(service)>0 and service[0].split(u'\uff1a')[1].strip() or ''
        else:
            i['comment'] = len(comment)>1 and re_d.findall(comment)[0] or ''
            consume = sel.xpath('//div[@class="brief-info"]/span[3]/text()').extract()
            i['consume'] = len(consume)>0 and consume[0].split(u'\uff1a')[1].strip() or ''
            taste = sel.xpath('//div[@class="brief-info"]/span[4]/text()').extract()
            i['taste'] = len(taste)>0 and taste[0].split(u'\uff1a')[1].strip() or ''
            environment = sel.xpath('//div[@class="brief-info"]/span[5]/text()').extract()
            i['environment'] = len(environment)>0 and environment[0].split(u'\uff1a')[1].strip() or ''
            service = sel.xpath('//div[@class="brief-info"]/span[6]/text()').extract()
            i['service'] = len(service)>0 and service[0].split(u'\uff1a')[1].strip() or ''
        shopname= sel.xpath('//h1[@class="shop-name"]/text()').extract()
        i['shopname'] = len(shopname)>0 and shopname[0].strip() or ''
        city = sel.xpath('//a[@class="city J-city"]/text()').extract()
        i['city'] = len(city)>0 and city[0].strip() or ''
        area = sel.xpath('//div[@class="expand-info address"]/a/span/text()').extract()[0].strip()
        detail = sel.xpath('//div[@class="expand-info address"]/span[2]/text()').extract()[0].strip()
        address = area + " " + detail
        i['address'] = len(address)>0 and address or ''
        business = sel.xpath('//div[@class="breadcrumb"]/a[3]/text()').extract()
        i['business'] = len(business)>0 and business[0].strip() or ''
        #recommend = sel.xpath('//div[@class="shop-tab-recommend J-panel"]/p/a/@title').extract()
        #i['recommend'] = len(recommend)>0 and recommend or ''
        #rnumber = sel.xpath('//div[@class="shop-tab-recommend J-panel"]/p/a/em/text()').extract()
        #i['rnumber'] = len(rnumber)>0 and rnumber[0].strip() or ''
        return i



