from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request
from infomation_crawler.items import IndustryReportItem
import datetime
import pymongo
import time
from thrift.transport.TSocket import TSocket
from thrift.transport.TTransport import TBufferedTransport
from thrift.protocol import TBinaryProtocol
from infomation_crawler.hbase import Hbase
from infomation_crawler.hbase.ttypes import *

class IDCSpider(CrawlSpider):
	name = 'idc'
	allowed_domains = ['idc.com.cn']
	
	def __init__(self, crawl=None, *args, **kwargs):
		super(IDCSpider, self).__init__(*args, **kwargs)
		if(cmp(crawl, 'all')==0):
			urls = []
			time = time.strftime('%Y',time.localtime(time.time()))
			for i in range(6):
				url = 'http://idc.com.cn/about/index.jsp?page=' + str(i+1) + '&thisy=2015'
				urls.append(url)
			self.start_urls = urls
		else:
			self.start_urls = ['http://idc.com.cn/about/index.jsp?page=1&thisy=2015']
		self.host = "172.20.6.61"
		self.port = 9090
		self.transport = TBufferedTransport(TSocket(self.host, self.port))
		self.transport.open()
		self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
		self.client = Hbase.Client(self.protocol)
     
	def __del__(self):
		self.transport.close()
	conn = pymongo.Connection('172.20.8.3',27017)
	infoDB = conn.info
	tIndustryReport = infoDB.IndustryReport
	
	def parse_item(self, response):
		sel = Selector(response)
		i = response.meta['item']
		
		content = sel.xpath('//td[@class="bodybk"]').extract()
		i['content'] = len(content)>0 and content[0] or ''
		
		i['siteName'] = 'idc'
		i['addTime'] = datetime.datetime.now()
		
		return i
	
	def parse(self, response):
		print "enter idc_parse_item...."
		sel = Selector(response)
		items = []
		reportContents = sel.xpath('//td[@class="bodybk"]/p')[0:]
		for report in reportContents:
			i = IndustryReportItem()
			url = report.xpath('a/@href').extract()
			if len(url) > 0 and url[0].find('http://')==-1:
				i['url'] = 'http://idc.com.cn'+url[0]
			else:
				continue
			title = report.xpath('text()').extract()
			i['title'] = len(title)>0 and title[0].strip() or ''
			
			i['author'] = ''
			i['abstract'] = ''
			i['keyWords'] = ''
			
			pubTime = report.xpath('b/text()').extract()
			i['publishTime'] = len(pubTime)>0 and pubTime[0].strip() or str(datetime.date.today())
			
			source = report.xpath('text()').extract()
			i['source'] = len(source)>1 and source[1].replace('|','').split(':')[1].strip() or ''
			
			items.append(i)
			
		for item in items:
			yield Request(item['url'],meta={'item':item},callback=self.parse_item)
