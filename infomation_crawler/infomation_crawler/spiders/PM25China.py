# -*- coding: utf-8 -*-
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider,Rule
from infomation_crawler.items import PM25ChinaItem
from scrapy.http import Request
from thrift.transport.TSocket import TSocket
from thrift.transport.TTransport import TBufferedTransport
from thrift.protocol import TBinaryProtocol
from infomation_crawler.hbase import Hbase
from infomation_crawler.hbase.ttypes import *
import datetime
import pymongo
import re
class PM25ChinaSpider(CrawlSpider):
	name = 'PM25China'
	allowed_domain = ['pm25china.net']
	start_urls=["http://www.pm25china.net"]

	host = "172.20.8.69"
	port = 9090
	transport = TBufferedTransport(TSocket(host, port))
	transport.open()
	protocol = TBinaryProtocol.TBinaryProtocol(transport)
	client = Hbase.Client(protocol)
	def __del__(self):
		transport.close()
	'''
	rules = [
			Rule(SgmlLinkExtractor(allow=(r''),restrict_xpaths=('//div[@id="plist"]')),callback='parse_item'),
			]
	'''
	def parse(self, response):
		sel = Selector(response)
		urllist = sel.xpath('//div[@class="warp"]/a/@href').extract()
		for url in urllist:
			requesturl = 'http://www.pm25china.net' + url
			yield Request(requesturl,callback=self.parse_item)
	def parse_item(self, response):
	 sel = Selector(response)
	 #try:
	 trlist = sel.xpath('//table[@id="xiang1"]/tr')
	 items=[]
	 for tr in trlist:
		 td = tr.xpath('td')
		 item= PM25ChinaItem()
		 item['areacode'] = response.url.split('/')[-2] + 'shi'
		 item['areaname'] = sel.xpath('//span[@class="tqnav_11"]/text()').extract()[0]
		 script = sel.xpath('//div[@class="left614"]//script[@type="text/javascript"]').extract()
		 item['index_value'] = len(script)>0 and re.findall(r'jin_value \= "\d+"',script[0])[0].split('"')[1] or ''
		 item['publishtime'] = sel.xpath('//h1/span/text()').extract()[0].split(u'\uff1a')[1]
		 item['jiankongdian_code'] = td[0].xpath('a/@href').extract()[0].split('_')[1].replace('/','')
		 item['jiankongdian_name'] = td[0].xpath('a/text()').extract()[0]
		 item['jiangkongdian_aqi'] = td[1].xpath('text()').extract()[0]
		 #jiangkongdian_pm25 = td[2].xpath('img/@alt').extract()[0].split(u'\uff1a')[1]
		 item['jiangkongdian_pm25'] = td[3].xpath('text()').extract()[0]
		 item['jiangkongdian_pm10'] = td[4].xpath('text()').extract()[0]
		 item['jiangkongdian_key'] = len(td[5].xpath('text()'))>0 and td[5].xpath('text()').extract()[0] or ''
		 item['crawltime'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
		 items.append(item)
	 return items
