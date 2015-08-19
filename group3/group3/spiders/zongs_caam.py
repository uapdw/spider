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
class ZongSCaamSpider(CrawlSpider):
	name = 'zongs_caam'
	allowed_domains = ['caam.org.cn']
	start_urls = ['http://www.caam.org.cn/newslist/a18-1.html','http://www.caam.org.cn/newslist/a23-1.html','http://www.caam.org.cn/newslist/a2-1.html','http://www.caam.org.cn/newslist/a1-1.html','http://www.caam.org.cn/newslist/a9-1.html']
	
	conn = pymongo.Connection('172.20.8.3',27017)
	infoDB = conn.info
	tWebArticles = infoDB.web_articles
	rules = (
			Rule(SgmlLinkExtractor(allow=r'a(18|23|2|1|9)-\d+.html'),callback='parse_item01',follow=True),
			#Rule(SgmlLinkExtractor(allow=r'(dynamic_detail|news_detail|market_detail)\.php\?id=\d+'), callback='parse_item'),
  )
        def __init__(self,**kw):
          super(ZongSCaamSpider,self).__init__(**kw)
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
		
		print "enter ZongSCaamSpider_parse_item...."
		sel = Selector(response)
		items = []
		urllist = sel.xpath('//div[@class="xwzxlist xwzxlist_noline"]/ul/li')[0:]
		for url in urllist:
				i = WebArticleItem()
				i['url']= 'http://www.caam.org.cn' + url.xpath('a/@href').extract()[0]
				title = url.xpath('a/text()').extract()
				i['title'] = len(title)>0 and title[0].strip() or ''
				i['abstract'] = ''
				items.append(i)
		for item in items:
				yield Request(item['url'],meta={'item':item},callback=self.parse_item)
	def parse_item(self, response):
		sel = Selector(response)
		i = response.meta['item']	
		try:
				pubTime = sel.xpath('//div[@class="timecont"]/ul/li[1]/text()').extract()[0]
				match = re.match(u'(\d+)年(\d+)月(\d+)日 (\d+):(\d+)',pubTime,re.UNICODE)
		
				if match:
						pubTime = match.group(1) + '-' + match.group(2) + '-' + match.group(3) + ' ' + match.group(4) + ':' + match.group(5)
						i['publishTime'] = datetime.datetime.strptime(pubTime, '%Y-%m-%d %H:%M')
				else:
						i['publishTime'] = datetime.datetime(1970,1,1)
		except:
				i['publishTime'] = datetime.datetime(1970,1,1)
		if i['publishTime']:
				pass
				#if i['publishTime'].date() not in self.time_range:
        			#		return
		else:
				i['publishTime'] = datetime.datetime(1970,1,1)
		try:	
				source = sel.xpath('//div[@class="timecont"]/ul/li[2]/text()').extract()
				i['source'] = len(source)>0 and source[0].strip().replace(u'\uff1a','@').split('@')[1] or ''
		except:
				pass
		if not i['source']:
				i['source'] = ''
		i['author'] = ''
		i['keyWords'] = ''
		i['newstype'] = '政策'
		
		content = sel.xpath('//div[@class="newstext"]/p').extract()[0]
		i['content'] = htmlfilter.filterTags(content)
		i['siteName'] = 'www.caam.org.cn'
		
		i['addTime'] = datetime.datetime.now()
		return i
		
