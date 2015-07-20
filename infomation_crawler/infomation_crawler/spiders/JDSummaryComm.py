# -*- coding: utf-8 -*-
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.http import Request
from infomation_crawler.items import JDSummaryCommItem
import datetime
import pymongo
import re
from thrift.transport.TSocket import TSocket
from thrift.transport.TTransport import TBufferedTransport
from thrift.protocol import TBinaryProtocol
from infomation_crawler.hbase import Hbase
from infomation_crawler.hbase.ttypes import *

class JDSummaryCommSpider(CrawlSpider):
	name = 'JDSummaryComm'
	allowed_domain = ['jd.com']
	start_urls=["http://list.jd.com/list.html?cat=737,794,878"]

	rules = [
			Rule(SgmlLinkExtractor(allow=("/list.html\?cat=737%2C794%2C878&page=\d+&JL=6_0_0"))),
			Rule(SgmlLinkExtractor(allow=(r'http://item.jd.com/\d+.html\#comments-list'),restrict_xpaths=('//div[@id="plist"]')),callback='parse_item'),
			]
	'''
	rules = [
	Rule(SgmlLinkExtractor(allow=(r'http://item.jd.com/\d+.html\#comments-list'),restrict_xpaths=('//div[@id="plist"]')),callback='parse_item'),
	Rule(SgmlLinkExtractor(allow=("/list.html\?cat=737%2C794%2C878&page=\d+&JL=6_0_0"), restrict_xpaths=("//a[@class='next']"))),
	]
	'''

	def __init__(self,**kw):
		super(JDSummaryCommSpider,self).__init__(**kw)
		self.host = "172.20.6.61"
		self.port = 9090
		self.transport = TBufferedTransport(TSocket(self.host, self.port))
		self.transport.open()
		self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
		self.client = Hbase.Client(self.protocol)

	def __del__(self):
		self.transport.close()

	def parse_item(self, response):
		item= JDSummaryCommItem()
		sel = Selector(response)
		priceid = response.url.decode('utf8').split('/')[-1].split('.')[0]
		commurl = 'http://club.jd.com/review/'+ priceid +'-3-1-0.html'
		item['pt_name'] = 'jd'
		danpin_name = sel.xpath('//div[@class="breadcrumb"]/span[2]/a[2]/text()').extract()
		item['danpin_name'] = len(danpin_name)>0 and danpin_name[0] or ''
		pt_sp_address = response.url
		item['pt_sp_address'] = pt_sp_address
		yield Request(commurl,meta={'item':item},callback=self.parseCommpage)

	def parseCommpage(self, response):
		sel = Selector(response)
		i = response.meta['item']
		com_count = sel.xpath('//ul[@class="tab"]/li[1]/a/em/text()').extract()
		i['com_count'] = len(com_count)>0 and com_count[0].replace('(','').replace(')','') or ''
		positive_com_count = sel.xpath('//ul[@class="tab"]/li[2]/a/em/text()').extract()
		i['positive_com_count'] = len(positive_com_count)>0 and positive_com_count[0].replace('(','').replace(')','') or ''
		moderate_com_count = sel.xpath('//ul[@class="tab"]/li[3]/a/em/text()').extract()
		i['moderate_com_count'] = len(moderate_com_count)>0 and moderate_com_count[0].replace('(','').replace(')','') or ''
		negative_com_count = sel.xpath('//ul[@class="tab"]/li[4]/a/em/text()').extract()
		i['negative_com_count'] = len(negative_com_count)>0 and negative_com_count[0].replace('(','').replace(')','') or ''
		photo_com_count = sel.xpath('//ul[@class="tab"]/li[2]/a/em/text()').extract()
		i['photo_com_count'] = len(photo_com_count)>0 and photo_com_count[0].replace('(','').replace(')','') or ''
		impressionlist = sel.xpath('//dd[@class="p-bfc"]/q/span/text()').extract()
		impression = len(impressionlist)>0 and impressionlist[0].strip() or ''
		for key in range(len(impressionlist)-1):
			impression = impression + ',' + impressionlist[key+1].strip()
		i['impression'] = impression
		return i
