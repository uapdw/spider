# -*- coding: utf-8 -*-
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from group3.items import WebArticleItem
import datetime
from scrapy.http import Request
import pymongo
import re
from thrift.transport.TSocket import TSocket
from thrift.transport.TTransport import TBufferedTransport
from thrift.protocol import TBinaryProtocol
from group3.hbase import Hbase
from group3.hbase.ttypes import *
import htmlfilter
class ZongSCaiJingSpider(CrawlSpider):
	name = 'zongs_caijing'
	allowed_domains = ['caijing.com.cn']
	start_urls = ['http://industry.caijing.com.cn/industrianews/','http://finance.caijing.com.cn/fdailynews/','http://economy.caijing.com.cn/economynews/']
	
	conn = pymongo.Connection('172.20.8.3',27017)
	infoDB = conn.info
	tWebArticles = infoDB.web_articles
	rules = (
			Rule(SgmlLinkExtractor(allow=r'(industrianews|fdailynews|economynews)/\d+.shtml'),callback='parse_item01',follow=True),
			#Rule(SgmlLinkExtractor(allow=r'(dynamic_detail|news_detail|market_detail)\.php\?id=\d+'), callback='parse_item'),
  )
        def __init__(self,**kw):
          super(ZongSCaiJingSpider,self).__init__(**kw)
          self.host = "172.20.6.61"
          self.port = 9090
          self.transport = TBufferedTransport(TSocket(self.host, self.port))
          self.transport.open()
          self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
          self.client = Hbase.Client(self.protocol)
          self.today = datetime.date.today()
          self.yesterday = (datetime.date.today() - datetime.timedelta(days=1))
          self.time_range = [self.today, self.yesterday]
      
      
        def __del__(self):
          self.transport.close()
	
	def parse_item01(self, response):
		
		
		print "enter ZongSCaiJing_parse_item...."
		sel = Selector(response)
		items = []
		urllist = sel.xpath('//ul[@class="list"]/li')[0:]
		for url in urllist:
				i = WebArticleItem()
				i['url']= url.xpath('div[@class="wzbt"]/a/@href').extract()[0]
				title = url.xpath('div[@class="wzbt"]/a/text()').extract()
				i['title'] = len(title)>0 and title[0].strip() or ''
				abstract= url.xpath('div[@class="subtitle"]/text()').extract()
				i['abstract'] = len(abstract)>0 and abstract[0] or ''
				items.append(i)
		for item in items:
				yield Request(item['url'],meta={'item':item},callback=self.parse_item)
	def parse_item(self, response):
		sel = Selector(response)
		i = response.meta['item']
		try:	
				pubTime = sel.xpath('//span[@id="pubtime_baidu"]/text()').extract()[0]
				i['publishTime'] = datetime.datetime.strptime(pubTime, '%Y-%m-%d %H:%M:%S')
		except:
				pass
		if i['publishTime']:
				pass
				#if i['publishTime'].date() not in self.time_range:
        			#		return
		else:
				i['publishTime'] = datetime.datetime(1970,1,1)
		try:	
				source = sel.xpath('//span[@id="source_baidu"]/text()').extract()
				i['source'] = len(source)>0 and source[0] or ''
		except:
				pass
		if not i['source']:
				i['source'] = ''
		i['author'] = ''
		i['keyWords'] = ''
		i['newstype'] = '财经'
		
		content = sel.xpath('//div[@id="the_content"]').extract()[0]
		i['content'] = htmlfilter.filterTags(content)
		i['siteName'] = 'caijing.com.cn'
		
		i['addTime'] = datetime.datetime.now()
		return i
