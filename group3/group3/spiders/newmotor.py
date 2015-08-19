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
class NewmotorSpider(CrawlSpider):
	name = 'newmotor'
	allowed_domains = ['newmotor.com.cn']
	start_urls = ['http://www.newmotor.com.cn/html/cjdt_1164.html','http://www.newmotor.com.cn/html/zsss_1224.html','http://www.newmotor.com.cn/html/mtzh_1171.html']
	
	conn = pymongo.Connection('172.20.8.3',27017)
	infoDB = conn.info
	tWebArticles = infoDB.web_articles
	rules = (
			Rule(SgmlLinkExtractor(allow=r'(cjdt_1164|zsss_1224|mtzh_1171)_\d+\.html'),callback='parse_item01',follow=True),
			#Rule(SgmlLinkExtractor(allow=r'(dynamic_detail|news_detail|market_detail)\.php\?id=\d+'), callback='parse_item'),
  )
        def __init__(self,**kw):
          super(NewmotorSpider,self).__init__(**kw)
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
		print "enter newmotor_parse_item...."
		sel = Selector(response)
		items = []
		urllist = sel.xpath('//ul[@class="ly_tj_content"]/li')[0:]
		for url in urllist:
				i = WebArticleItem()
				i['url']=url.xpath('div[@class="itcMain"]/a/@href').extract()[0]
				title = url.xpath('div[@class="itcMain"]/a/@title').extract()
				i['title'] = len(title)>0 and title[0].strip() or ''
				abstract= url.xpath('div[@class="itcMain"]/p/text()').extract()
				i['abstract'] = len(abstract)>0 and abstract[0].replace(u'\xa0',' ').strip().replace('\n','').replace('\t','') or ''		
				items.append(i)
		for item in items:
				yield Request(item['url'],meta={'item':item},callback=self.parse_item)
	def parse_item(self, response):
		sel = Selector(response)
		i = response.meta['item']
		try:	
				pubTime = sel.xpath('//div[@class="t0601sviewurl"]/span[1]/text()').extract()[0]
				match = re.match(u'时间：(\d+-\d+-\d+ \d+:\d+:\d+)',pubTime,re.UNICODE)
				if match:
						pubTime = match.group(1)
				if pubTime:
						i['publishTime'] = datetime.datetime.strptime(pubTime, '%Y-%m-%d %H:%M:%S')
				else:
						i['publishTime'] = datetime.datetime(1970,1,1)
				
		except:
				pass
		
		if i['publishTime']:
				pass
				#if i['publishTime'].date() not in self.time_range:
        			#		return
		else:
				i['publishTime'] = datetime.datetime(1970,1,1)
		try:	
				source = sel.xpath('//div[@class="t0601sviewurl"]/span[2]/text()').extract()
				i['source'] = len(source)>0 and source[0].strip().replace(u'\uff1a','@').split('@')[1] or ''
		except:
				pass
		try:	
				author = sel.xpath('//div[@class="t0601sviewurl"]/span[3]/text()').extract()
				i['author'] = len(author)>0 and author[0].strip().replace(u'\uff1a','@').split('@')[1] or ''
		except:
				pass
		if not i['source']:
				i['source'] = ''
		if not i['author']:
				i['author'] = ''

		
		i['keyWords'] = ''
		i['newstype'] = '摩托'	
		content = sel.xpath('//div[@id="MyContent"]').extract()[0]
		i['content'] = htmlfilter.filterTags(content)
		i['siteName'] = 'newmotor'
		
		i['addTime'] = datetime.datetime.now()
		return i
		
