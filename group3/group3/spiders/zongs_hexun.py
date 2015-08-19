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
import json
class ZongSHeXunSpider(CrawlSpider):
	name = 'zongs_hexun'
	allowed_domains = ['hexun.com']
	urls = []
	for i in range(100):
		url = 'http://open.tool.hexun.com/MongodbNewsService/newsListPageByJson.jsp?id=100018985&s=30&cp=' + str(i+1) + '&priority=0&callback=hx_json181438311181332'
		url01 = 'http://open.tool.hexun.com/MongodbNewsService/newsListPageByJson.jsp?id=100018983&s=30&cp=' + str(i+1) + '&priority=0&callback=hx_json41438311459711'
		url02 = 'http://open.tool.hexun.com/MongodbNewsService/newsListPageByJson.jsp?id=108511065&s=30&cp=' + str(i+1) + '&priority=0&callback=hx_json31438311570574'
		urls.append(url)
		urls.append(url01)
		urls.append(url02)
	start_urls = urls 
	
	conn = pymongo.Connection('172.20.8.3',27017)
	infoDB = conn.info
	tWebArticles = infoDB.web_articles
        def __init__(self):
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
	
	def parse(self, response):
		items = []
		match = re.match('hx_json\d+\( (.*) \)',response.body)
		_match = json.loads(match.group(1).decode('gbk').encode('utf8'))	
		for key in range(len(_match['result'])-1):
				i = WebArticleItem()
				url = _match['result'][key]['entityurl']
				i['url'] = url
				#print i['url']
				items.append(i)
		for item in items:
				yield Request(item['url'],meta={'item':item},callback=self.parse_item)
	def parse_item(self, response):
		sel = Selector(response)
		i = response.meta['item']
		try:	
				pubTime = sel.xpath('//span[@id="pubtime_baidu"]/text()').extract()[0]
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
				source = sel.xpath('//span[@id="source_baidu"]/a/@href').extract()
				i['source'] = len(source)>0 and source[0] or ''
		except:
				pass
		try:	
				title = sel.xpath('//h1/text()').extract()
				i['title'] = len(title)>0 and title[0] or ''
		except:
				pass
		try:	
				author = sel.xpath('//span[@id="author_baidu"]/font/text()').extract()
				i['author'] = len(author)>0 and author[0] or ''
		except:
				pass
		if not i['source']:
				i['source'] = ''
		if not i['author']:
				i['author'] = ''

		
		i['keyWords'] = ''
		i['abstract'] = ''
		i['newstype'] = '财经'
		
		content = sel.xpath('//div[@id="artibody"]').extract()[0]
		i['content'] = htmlfilter.filterTags(content)
		i['siteName'] = 'news.hexun.com'
		
		i['addTime'] = datetime.datetime.now()
		return i
		
