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
class ChmotorSpider(CrawlSpider):
	name = 'chmotor'
	allowed_domains = ['chmotor.cn']
	start_urls = ['http://www.chmotor.cn/news.php','http://www.chmotor.cn/market.php','http://www.chmotor.cn/dynamic.php']
	

	rules = (
			Rule(SgmlLinkExtractor(allow=r'(market|news|dynamic)\.php\?page=\d+'),callback='parse_item01',follow=True),
			#Rule(SgmlLinkExtractor(allow=r'(dynamic_detail|news_detail|market_detail)\.php\?id=\d+'), callback='parse_item'),
  )
        def __init__(self,**kw):
          super(ChmotorSpider,self).__init__(**kw)
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
		
		
		print "enter Chmotor_parse_item...."
		sel = Selector(response)
		items = []
		urllist = sel.xpath('//div[@class="list_content_con_details_right"]')[0:]
		for url in urllist:
				i = WebArticleItem()
				i['url']='http://www.chmotor.cn/' + url.xpath('div[@class="list_content_con_details_right_1"]/a/@href').extract()[0]
				title = url.xpath('div[@class="list_content_con_details_right_1"]/a/@title').extract()
				i['title'] = len(title)>0 and title[0].strip() or ''
				abstract= url.xpath('div[@class="list_content_con_details_right_3"]/text()').extract()
				i['abstract'] = len(abstract)>0 and abstract[0] or ''
				items.append(i)
		for item in items:
				yield Request(item['url'],meta={'item':item},callback=self.parse_item)
	def parse_item(self, response):
		sel = Selector(response)
		i = response.meta['item']
		try:	
				pubTime = sel.xpath('//div[@class="article_content_left_smalltitle"]/span[1]/text()').extract()[0]
				match = re.match(u'\d+-\d+-\d+ \d+:\d+:\d+',pubTime,re.UNICODE)
				if match:
						pubTime = match.group(0)
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
				source = sel.xpath('//div[@class="article_content_left_smalltitle"]/span[2]/text()').extract()
				i['source'] = len(source)>0 and source[0].strip().replace(u'\uff1a','@').split('@')[1] or ''
		except:
				pass
		try:	
				author = sel.xpath('//div[@class="article_content_left_smalltitle"]/span[4]/text()').extract()
				i['author'] = len(author)>0 and author[0].strip().replace(u'\uff1a','@').split('@')[1] or ''
		except:
				pass
		if not i['source']:
				i['source'] = ''
		if not i['author']:
				i['author'] = ''

		
		i['keyWords'] = ''
		i['newstype'] = '摩托'	
		content = sel.xpath('//div[@class="article_content_left_con_3"]').extract()[0]
		i['content'] = htmlfilter.filterTags(content)
		i['siteName'] = 'www.chmotor.cn'
		
		i['addTime'] = datetime.datetime.now()
		return i
